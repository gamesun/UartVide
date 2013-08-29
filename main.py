# -*- coding:utf-8 -*-

import sys, os
import wx
import GUI as ui
import threading
import re
import serial
import time
from wx.lib.wordwrap import wordwrap
import _winreg as winreg
import itertools
import icon32
import pkg_resources
import zipfile
from cStringIO import StringIO
import webbrowser
import appInfo
import glob

MAINMENU  = 0
SUBMENU   = 1
MENUITEM  = 2
CHECKITEM = 3
SEPARATOR = 4
RADIOITEM = 5

ASCII = 0
HEX   = 1

THREAD_TIMEOUT = 0.5


SERIALRX = wx.NewEventType()                    # Create an own event type
EVT_SERIALRX = wx.PyEventBinder(SERIALRX, 0)    # bind to serial data receive events
class SerialRxEvent(wx.PyCommandEvent):
    eventType = SERIALRX
    def __init__(self, windowID, data):
        wx.PyCommandEvent.__init__(self, self.eventType, windowID)
        self.data = data

    def Clone(self):
        self.__class__(self.GetId(), self.data)
        

SERIALEXCEPT = wx.NewEventType()
EVT_SERIALEXCEPT = wx.PyEventBinder(SERIALEXCEPT, 0)
class SerialExceptEvent(wx.PyCommandEvent):
    eventType = SERIALEXCEPT
    def __init__(self, windowID, param):
        wx.PyCommandEvent.__init__(self, self.eventType ,windowID)
        self.param = param
    
    def Clone(self):
        self.__class__(self.GetId(), self.param)

regex_matchTTY = re.compile('/tty/(?P<tty>\w+)')
def EnumerateSerialPorts(): 
    if sys.platform == 'win32':
        """ Uses the Win32 registry to return an 
            iterator of serial (COM) ports 
            existing on this computer.
        """
        pathDevi = r'HARDWARE\DEVICEMAP'
        try:
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, pathDevi)
        except WindowsError:
            # failed in reading registry.
            # return COM1 ~ COM16
            for i in range(1, 17):
                yield "COM" + str(i)
            return

        pathCOMM = r'HARDWARE\DEVICEMAP\SERIALCOMM'
        try:
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, pathCOMM)
        except WindowsError:
            # when getting none serial port, 
            # SERIALCOMM is not exist in "HARDWARE\DEVICEMAP\".
            # return nothing.
            return
        
        for i in itertools.count():
            try:
                val = winreg.EnumValue(key, i)
                yield str(val[1])
            except EnvironmentError:
                break
    elif sys.platform.startswith('linux'):
        for t in glob.glob('/sys/class/tty/*/device/driver'):
            r = regex_matchTTY.search(t)
            if r:
                yield '/dev/%s' % r.group('tty') 

        
            
MenuDefs = (
MAINMENU,
('&File', (
    (MENUITEM,  wx.NewId(), '&Save',              'Save to a file' ,    'self.OnSave'      ),
    (SEPARATOR,),
    (MENUITEM,  wx.NewId(), '&Exit MyTerm',       'Exit MyTerm',        'self.OnExitApp'   ),
)),
('&Port', (
    (MENUITEM,  wx.NewId(), '&Open',              'Open the Port' ,     'self.OnOpenPort'  ),
    (MENUITEM,  wx.NewId(), '&Close',             'Close the Port',     'self.OnClosePort' ),
)),
('&Display', (
    (MENUITEM,  wx.NewId(), '&Show Setting Bar',  'Show Setting Bar',    'self.OnShowSettingBar' ),
    (CHECKITEM, wx.NewId(), '&Always on top',     'always on most top',  'self.OnAlwayOnTop'     ),
    (CHECKITEM, wx.NewId(), '&Local echo',        'echo what you typed', 'self.OnLocalEcho'      ),
    (SUBMENU, '&Rx view as', (
        (RADIOITEM, wx.NewId(), '&Ascii', '', 'self.OnRxAsciiMode' ),
        (RADIOITEM, wx.NewId(), '&Hex',   '', 'self.OnRxHexMode'   ),
    )),
#     (SUBMENU, 'Tx view as', (
#         (RADIOITEM, wx.NewId(), 'ASCII', '', 'self.OnTxAsciiMode' ),
#         (RADIOITEM, wx.NewId(), 'HEX',   '', 'self.OnTxHexMode'   ),
#     )),
#     (CHECKITEM, wx.NewId(), 'S&tatus Bar',        'Show Status Bar',    'self.OnShowStatusBar'  ),
)),
('&Help', (
    (MENUITEM,  wx.NewId(), '&About',             'About  MyTerm',      'self.OnAbout' ),
))
)

regex_matchPort = re.compile('COM(?P<port>\d+)')
regex_matchCmdList = re.compile(
    '\|\s+(?P<index>\d)\s+\|\s+(?P<time>\d+|-)\s+\|\s+(?P<count>\d+|-)\s+\|\s+(?P<setvolt>\d+|-)\s+\|\s+(?P<realvolt>[0-9.]+|-)\s+\|')


serialport = serial.Serial()

class MyApp(wx.App):
    def OnInit(self):
        self.frame = ui.MyFrame(None, wx.ID_ANY, "")

        my_data = pkg_resources.resource_string(__name__,"library.zip")
        filezip = StringIO(my_data)
        zf = zipfile.ZipFile(filezip)
        data = zf.read("media/icon16.ico")
#         self.frame.SetIcon(icon16.geticon16Icon())
        
        icon = wx.EmptyIcon()
        icon.CopyFromBitmap(wx.ImageFromStream(StringIO(data), wx.BITMAP_TYPE_ICO).ConvertToBitmap())
        self.frame.SetIcon(icon)
        
#         self.frame.SetIcon(wx.Icon("media\icon16.ico", wx.BITMAP_TYPE_ICO, 16, 16))
        
        self.frame.SplitterWindow.SetSashSize(0)
        self.frame.SplitterWindow.SetSashPosition(160, True)
        
#         self.frame.choicePort.AppendItems(('COM1', 'COM2', 'COM3', 'COM4', 'COM5', 'COM6', 'COM7', 'COM8'))

        self.OnEnumPorts()
        self.frame.choicePort.Select(0)
        self.frame.cmbBaudRate.Select(6)

        # initial variables
        
        self.rxmode = ASCII
        self.txmode = ASCII
        self.localEcho = False
        self.rxCount = 0
        self.txCount = 0
        
        # Make a menu
        menuBar = wx.MenuBar()
        self.MakeMenu(menuBar, MenuDefs)
        self.frame.SetMenuBar(menuBar)
        
        # bind events
        self.frame.btnHideBar.Bind(wx.EVT_BUTTON, self.OnHideSettingBar)
        self.frame.btnOpen.Bind(wx.EVT_BUTTON, self.OnBtnOpen)
        self.frame.btnEnumPorts.Bind(wx.EVT_BUTTON, self.OnEnumPorts)
        self.frame.btnClear.Bind(wx.EVT_BUTTON, self.OnClear)
        
#         self.frame.Bind(wx.EVT_WINDOW_DESTROY, self.Cleanup)
        self.frame.Bind(wx.EVT_CLOSE, self.Cleanup)

        self.Bind(EVT_SERIALEXCEPT, self.OnSerialExcept)
        self.Bind(EVT_SERIALRX, self.OnSerialRx)
        self.frame.txtctlMain.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)
        self.frame.txtctlMain.Bind(wx.EVT_CHAR, self.OnSerialWrite)
        self.frame.txtctlMain.Bind(wx.EVT_TEXT_PASTE, self.OnPaste)
        self.frame.txtctlMain.Bind(wx.EVT_TEXT_URL, self.OnURL)
        
        self.frame.btnGetInfo.Bind(wx.EVT_BUTTON, self.OnBtnGetInfo)
        self.frame.btnSetInfo.Bind(wx.EVT_BUTTON, self.OnBtnSetInfo)
        self.frame.btnSave.Bind(wx.EVT_BUTTON, self.OnBtnSave)
        
        self.SetTopWindow(self.frame)
        self.frame.SetTitle( appInfo.title )
        self.frame.Show()
        
        self.evtPortOpen = threading.Event()
        self.evtSerialCmdBuffComplete = threading.Event()
        self.IsWaitingSerialReplyForAnalysis = False
        self.SerialReplyForAnalysisBuff = ''
        
        return True
        
        
    def OnBtnGetInfo(self, evt = None):
        if serialport.isOpen():
            serialport.write('\n')
            serialport.write('list\n')
            self.IsWaitingSerialReplyForAnalysis = True
            t = threading.Thread(target = self.ThreadAnalysis)
            t.start()
    
    def ThreadAnalysis(self):
        """ 
        the string to analysis looks like as follow:
        
        |No.| Time  | Count | Set Volt | Real Volt |
        |   | (ms)  |       |   (mV)   |   (mV)    |
        |---+-------+-------+----------+-----------|
        | 1 | 12345 |   -   | 111      | 1111.111  |
        | 2 |   -   | 22    | 222      | 2222.222  |
        | 3 |   -   | 33    | 333      | 3333.333  |
        | 4 |   -   | 44    | 444      | 4444.444  |
        | 5 |   -   | 55    | 555      | 5555.555  |
        | 6 |   -   |   -   | 666      | 6666.666  |
        
        """
        if self.evtSerialCmdBuffComplete.wait(1.0):
            self.evtSerialCmdBuffComplete.clear()
            for l in self.SerialReplyForAnalysisBuff.splitlines():
                r = regex_matchCmdList.search(l)
                if r:
                    i = int(r.group('index'))
                    if 1 <= i <= 1: 
                        self.SetT(i, int(r.group('time')))
                    if 2 <= i <= 5:
                        self.SetC(i, int(r.group('count')))
                    if 1 <= i <= 6:
                        self.SetV(i, int(r.group('setvolt')))
                        self.SetRV(i, r.group('realvolt'))
            self.SerialReplyForAnalysisBuff = ''
        else:
            print 'wait list timeout.'
            
    def OnBtnSetInfo(self, evt = None):
        if serialport.isOpen():
            data = (((1, self.GetT(1)),),
                    ((2, self.GetC(2)), (3, self.GetC(3)), (4, self.GetC(4)), (5, self.GetC(5)),),
                    ((1, self.GetV(1)), (2, self.GetV(2)), (3, self.GetV(3)), (4, self.GetV(4)), (5, self.GetV(5)), (6, self.GetV(6)),),)
            t = threading.Thread(target = ThreadSetInfo, args = (data,))
            t.start()
    
    def OnBtnSave(self, evt = None):
        if serialport.isOpen():
            serialport.write('\n')
            serialport.write('save\n')

    def GetT(self, index):
        if 1 <= index <= 1:
            return eval('self.frame.spin_ctrl_T' + ('%s' % index) + '.GetValue()')

    def GetC(self, index):
        if 2 <= index <= 5:
            return eval('self.frame.spin_ctrl_C' + ('%s' % index) + '.GetValue()')
        
    def GetV(self, index):
        if 1 <= index <= 6:
            return eval('self.frame.spin_ctrl_V' + ('%s' % index) + '.GetValue()')
        
    def SetT(self, index, value):
        if 1 <= index <= 1:
            eval('self.frame.spin_ctrl_T' + ('%s' % index) + '.SetValue(value)')
        
    def SetC(self, index, value):
        if 2 <= index <= 5:
            eval('self.frame.spin_ctrl_C' + ('%s' % index) + '.SetValue(value)')
            
    def SetV(self, index, value):
        if 1 <= index <= 6:
            eval('self.frame.spin_ctrl_V' + ('%s' % index) + '.SetValue(value)')
    
    def SetRV(self, index, label):
        if 1 <= index <= 6:
            eval('self.frame.label_RV' + ('%s' % index) + '.SetLabel("  %s" % label)')
            
    def OnURL(self, evt = None):
        if evt.MouseEvent.LeftUp():
            webbrowser.open(evt.GetEventObject().GetValue())
        evt.Skip()
        
    def OnClear(self, evt = None):
        self.frame.txtctlMain.Clear()
        self.rxCount = 0
        self.txCount = 0
        self.frame.statusbar.SetStatusText('Rx:%d' % self.rxCount, 1)
        self.frame.statusbar.SetStatusText('Tx:%d' % self.txCount, 2)
        
    def OnSave(self, evt = None):
        dlg = wx.FileDialog(self.frame,
                            message="Save file as ...",
                            defaultDir = os.getcwd(),
                            wildcard = "Text Files|*.txt",
                            style = wx.SAVE | wx.CHANGE_DIR)

        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            print "You selected %s\n" % path,
            
            # read file
            f = open(path, 'w')
            
            f.write(self.frame.txtctlMain.GetValue())
            
            f.close()
            
        dlg.Destroy()
            
    def GetPort(self):
        r = regex_matchPort.search(self.frame.choicePort.GetLabelText())
        if r:
            return int(r.group('port')) - 1
        return

    def GetBaudRate(self):
        return int(self.frame.cmbBaudRate.GetValue())

    def GetDataBits(self):
        s = self.frame.choiceDataBits.GetLabelText()
        if s == '5': 
            return serial.FIVEBITS
        elif s == '6': 
            return serial.SIXBITS
        elif s == '7': 
            return serial.SEVENBITS
        elif s == '8': 
            return serial.EIGHTBITS
    
    def GetParity(self):
        s = self.frame.choiceParity.GetLabelText()
        if s == 'None': 
            return serial.PARITY_NONE
        elif s == 'Even': 
            return serial.PARITY_EVEN
        elif s == 'Odd': 
            return serial.PARITY_ODD
        elif s == 'Mark': 
            return serial.PARITY_MARK
        elif s == 'Space': 
            return serial.PARITY_SPACE
        
    def GetStopBits(self):
        s = self.frame.choiceStopBits.GetLabelText()
        if s == '1': 
            return serial.STOPBITS_ONE
        elif s == '1.5': 
            return serial.STOPBITS_ONE_POINT_FIVE
        elif s == '2': 
            return serial.STOPBITS_TWO
            
    def MakeMenu(self, menuBar, args, menu = None):
        if args[0] == MENUITEM:
            menu.Append(args[1], args[2], args[3])
            eval('self.frame.Bind(wx.EVT_MENU,' + args[4] + ', id = args[1])')
        elif args[0] == CHECKITEM:
            menu.AppendCheckItem(args[1], args[2], args[3])
            eval('self.frame.Bind(wx.EVT_MENU,' + args[4] + ', id = args[1])')
        elif args[0] == SEPARATOR:
            menu.AppendSeparator()
        elif args[0] == RADIOITEM:
            menu.AppendRadioItem(args[1], args[2], args[3])
            eval('self.frame.Bind(wx.EVT_MENU,' + args[4] + ', id = args[1])')
        elif args[0] == SUBMENU:
            submenu = wx.Menu() 
            for i in args[2:][0]:
                self.MakeMenu(menuBar, i, submenu)
            menu.AppendSubMenu(submenu, args[1])
        elif args[0] == MAINMENU:
            for a in args[1:]:
                m = wx.Menu()
                for i in a[1]:
                    self.MakeMenu(menuBar, i, m)
                menuBar.Append(m, a[0])

    def OnEnumPorts(self, evt = None):
        self.frame.choicePort.Clear()
        for p in EnumerateSerialPorts():
            self.frame.choicePort.AppendItems((p,))
        
    def OnBtnOpen(self, evt = None):
        if serialport.isOpen():
            self.OnClosePort(evt)
        else:
            self.OnOpenPort(evt)
        
    def OnOpenPort(self, evt = None):
        serialport.port     = self.GetPort()
        serialport.baudrate = self.GetBaudRate()
        serialport.bytesize = self.GetDataBits()
        serialport.stopbits = self.GetStopBits()
        serialport.parity   = self.GetParity()
        serialport.rtscts   = self.frame.chkboxrtscts.IsChecked()
        serialport.xonxoff  = self.frame.chkboxxonxoff.IsChecked()
        serialport.timeout  = THREAD_TIMEOUT
        try:
            serialport.open()
        except serial.SerialException, e:
            dlg = wx.MessageDialog(None, str(e), "Serial Port Error", wx.OK | wx.ICON_ERROR)
            dlg.ShowModal()
            dlg.Destroy()
        else:
            self.StartThread()
            self.frame.SetTitle("%s on %s [%s, %s%s%s%s%s]" % (
                appInfo.title,
                serialport.portstr,
                serialport.baudrate,
                serialport.bytesize,
                serialport.parity,
                serialport.stopbits,
                serialport.rtscts and ' RTS/CTS' or '',
                serialport.xonxoff and ' Xon/Xoff' or '',
                )
            )
            self.frame.btnOpen.SetBackgroundColour((0,0xff,0x7f))
            self.frame.btnOpen.SetLabel('Opened')
            self.frame.btnOpen.Refresh()
            
    
    def OnClosePort(self, evt = None):
        if serialport.isOpen():
            self.StopThread()
            serialport.close()
            self.frame.SetTitle(appInfo.title)
            self.frame.btnOpen.SetBackgroundColour(wx.NullColour)
            self.frame.btnOpen.SetLabel('Open')
            self.frame.btnOpen.Refresh()
    
    def StartThread(self):
        """Start the receiver thread"""
        self.thread = threading.Thread(target = self.UartCommThread)
#         self.thread.setDaemon(1)
        self.evtPortOpen.set()
        self.thread.start()

    def StopThread(self):
        """Stop the receiver thread, wait util it's finished."""
        if self.thread is not None:
            self.evtPortOpen.clear()        #clear alive event for thread
            self.thread.join()              #wait until thread has finished
            self.thread = None
    
    def UartCommThread(self):
        """ sub process for receive data from uart port """
        while self.evtPortOpen.is_set():
#             print 'running'
            try:
                text = serialport.read(1)      # block for THREAD_TIMEOUT = 0.5s
            except serial.serialutil.SerialException:
                evt = SerialExceptEvent(self.frame.GetId(), -1)
                self.frame.GetEventHandler().AddPendingEvent(evt)
                print 'thread exit for except'
                return -1

            if text:
#                 print ord(text),
                n = serialport.inWaiting()
                if n:
                    text = text + serialport.read(n)

                if self.rxmode == HEX:
                    text = ''.join(str(ord(t)) + ' ' for t in text)     # text = ''.join([(c >= ' ') and c or '<%d>' % ord(c)  for c in text])
                    self.frame.txtctlMain.AppendText(text)
                else:
                    text = text.replace('\n', '')
                    if -1 != text.find(chr(wx.WXK_BACK)):
                        for t in text:
                            if t == chr(wx.WXK_BACK):   #0x08
                                self.frame.txtctlMain.Remove(self.frame.txtctlMain.GetLastPosition() - 1,
                                                             self.frame.txtctlMain.GetLastPosition() )
                            else:
                                self.frame.txtctlMain.AppendText(t)
                    else:
                        if self.IsWaitingSerialReplyForAnalysis:
                            self.SerialReplyForAnalysisBuff += text
                            if '\r\r' in self.SerialReplyForAnalysisBuff:
                                evt = SerialRxEvent(self.frame.GetId(), self.SerialReplyForAnalysisBuff)
                                self.frame.GetEventHandler().AddPendingEvent(evt)
                                self.IsWaitingSerialReplyForAnalysis = False
                                self.evtSerialCmdBuffComplete.set()
                        else:
                            self.frame.txtctlMain.AppendText(text)
                """Using event to display is slow when the data is too big."""
#                 evt = SerialRxEvent(self.frame.GetId(), text)
#                 self.frame.GetEventHandler().AddPendingEvent(evt)
                self.rxCount += len(text)
                self.frame.statusbar.SetStatusText('Rx:%d' % self.rxCount, 1)
        print 'exit thread'
        
    def OnSerialRx(self, evt):
        """Handle input from the serial port."""
        text = evt.data
        if self.rxmode == HEX:
            text = ''.join(str(ord(t)) + ' ' for t in text)     # text = ''.join([(c >= ' ') and c or '<%d>' % ord(c)  for c in text])
        self.frame.txtctlMain.AppendText(text)

        
    def OnSerialWrite(self, evt = None):
        keycode = evt.GetKeyCode()
#         controlDown = evt.CmdDown()
#         altDown = evt.AltDown()
#         shiftDown = evt.ShiftDown()
 
        print keycode,
#         if keycode == wx.WXK_SPACE:
#             print "you pressed the spacebar!"
#         elif controlDown and altDown:
#             print keycode
        if self.localEcho:
            evt.Skip()
            
        if serialport.isOpen():
            if keycode < 256:
                serialport.write(chr(keycode))
                self.txCount += 1
                self.frame.statusbar.SetStatusText('Tx:%d' % self.txCount, 2)
            else:
                print "Extra Key:", keycode
        
    def OnKeyDown(self ,evt = None):
        if self.localEcho:
            evt.Skip()
        else:
            keycode = evt.GetKeyCode()
            if wx.WXK_RETURN == keycode or wx.WXK_BACK == keycode:
                print keycode,
                if serialport.isOpen():
                    serialport.write(chr(keycode))
                    self.txCount += 1
                    self.frame.statusbar.SetStatusText('Tx:%d' % self.txCount, 2)
            else:
                evt.Skip()
            
    def OnPaste(self ,evt = None):
        data = wx.TextDataObject()
        wx.TheClipboard.GetData(data)

        if serialport.isOpen():
            serialport.write( data.GetText() )
            self.txCount += len( data.GetText() )
            self.frame.statusbar.SetStatusText('Tx:%d' % self.txCount, 2)
                    
        if self.localEcho:
            evt.Skip()
    
    def OnSerialExcept(self, evt):
        param = evt.param
        if param == -1:
            self.StopThread()
            serialport.close()
            self.frame.SetTitle(appInfo.title)
            self.frame.btnOpen.SetBackgroundColour(wx.NullColour)
            self.frame.btnOpen.SetLabel('Open')
            self.frame.btnOpen.Refresh()
        else:
            print 'OnSerialExcept() invalid parameter:%d' % param
        
    def OnHideSettingBar(self, evt = None):
        self.frame.SplitterWindow.SetSashPosition(1, True)
        
    def OnShowSettingBar(self, evt = None):
        self.frame.SplitterWindow.SetSashPosition(160, True)
    
    def OnShowStatusBar(self, evt = None):
        pass
    
    def OnRxAsciiMode(self, evt = None):
        self.rxmode = ASCII
        self.frame.statusbar.SetStatusText('Rx:Ascii', 3)
    
    def OnRxHexMode(self, evt = None):
        self.rxmode = HEX
        self.frame.statusbar.SetStatusText('Rx:Hex', 3)
        
    def OnTxAsciiMode(self, evt = None):
        self.txmode = ASCII
        self.frame.statusbar.SetStatusText('Tx:Ascii', 4)
    
    def OnTxHexMode(self, evt = None):
        self.txmode = HEX
        self.frame.statusbar.SetStatusText('Tx:Hex', 4)

    def OnAlwayOnTop(self, evt = None):
        if evt.Selection == 1:
            style = self.frame.GetWindowStyle()
            # stay on top
            self.frame.SetWindowStyle( style | wx.STAY_ON_TOP )
        elif evt.Selection == 0:
            style = self.frame.GetWindowStyle()
            # normal behavior again
            self.frame.SetWindowStyle( style & ~wx.STAY_ON_TOP )
    
    def OnLocalEcho(self, evt = None):
        if evt.Selection == 1:
            self.localEcho = True
            self.frame.statusbar.SetStatusText('Local echo:On', 4)
        elif evt.Selection == 0:
            self.localEcho = False
            self.frame.statusbar.SetStatusText('Local echo:Off', 4)
        
    def OnAbout(self, evt = None):
        # First we create and fill the info object
        info = wx.AboutDialogInfo()
        info.Name = appInfo.title
        info.Version = appInfo.version
        info.Copyright = appInfo.copyright
        info.Description = wordwrap(
            '\nMyTerm for FCVS offer a great solution for communication with the "Frequency-Controlled Voltage Source".\n\n'
            '"MyTerm for FCVS" development is based on MyTerm, the "MyTerm" offer a great solution for RS232 serial port communication.\n\n'
            'Press button "GetInfo" to display all parameters setting in FCVS.\n'
            'Press button "SetInfo" to transmit all parameters to FCVS.\n'
            'Press button "Save" to let FCVS save all parameters into its EEPROM.\n',
            550, wx.ClientDC(self.frame))
        info.WebSite = (appInfo.url, ("%s Home Page" % appInfo.title))
        info.Developers = [ "sun.yt" ]
        info.License = wordwrap("(C) 2013 Programmers and Coders Everywhere", 500, wx.ClientDC(self.frame))

        info.Icon = icon32.geticon32Icon()

        # Then we call wx.AboutBox giving it that info object
        wx.AboutBox(info)
    
    def OnExitApp(self, evt = None):
        self.frame.Close(True)      # send EVT_CLOSE
        print 'exit'
    
    def Cleanup(self, evt = None):
        self.frame.Destroy()
        self.OnClosePort()
#         for t in threading.enumerate():
#             print t.getName()
        if hasattr(self, 'thread'):
            if self.thread is not None:
                assert not self.thread.is_alive(), "the thread should be dead but isn't!"
#             self.threadCommunicate.terminate()


def ThreadSetInfo(data):
    serialport.write('\n')
    for d in data[0]:
        time.sleep(0.15)
        serialport.write('settime %d %s\n' % (d[0], d[1]))
            
    for d in data[1]:
        time.sleep(0.15)
        serialport.write('setcnt %d %s\n' % (d[0], d[1]))
        
    for d in data[2]:
        time.sleep(0.15)
        serialport.write('setvol %d %s\n' % (d[0], d[1]))
           
if __name__ == '__main__':
    app = MyApp(0)
    app.MainLoop()
