# -*- coding:utf-8 -*-

#import sys,os
import wx
import GUI as ui
# import multiprocessing
import threading, Queue
# import UartProcess
import re
import serial
import time
from wx.lib.wordwrap import wordwrap
import _winreg as winreg
import itertools

SUBMENU   = 0
MENUITEM  = 1
CHECKITEM = 2
SEPARATOR = 3
RADIOITEM = 4

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

def EnumerateSerialPorts():
    """ Uses the Win32 registry to return an 
        iterator of serial (COM) ports 
        existing on this computer.
    """
    path = r'HARDWARE\DEVICEMAP\SERIALCOMM'
    try:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, path)
    except WindowsError:
        raise IterationError
    
    for i in itertools.count():
        try:
            val = winreg.EnumValue(key, i)
            yield str(val[1])
        except EnvironmentError:
            break
            
MenuDefs = (
('&Operation', (
    (MENUITEM,  wx.NewId(), '&Open Port',         'Open the Port' ,     'self.OnOpenPort'  ),
    (MENUITEM,  wx.NewId(), '&Close Port',        'Close the Port',     'self.OnClosePort' ),
    (SEPARATOR,),
    (MENUITEM,  wx.NewId(), '&Exit MyTerm',       'Exit this tool',     'self.OnExitApp'   ),
)),
('&Display', (
    (MENUITEM,  wx.NewId(), 'Show S&etting Bar',  'Show Setting Bar',    'self.OnShowSettingBar' ),
    (CHECKITEM, wx.NewId(), 'Always on top',      'always on most top',  'self.OnAlwayOnTop'     ),
    (CHECKITEM, wx.NewId(), 'Local echo',         'echo what you typed', 'self.OnLocalEcho'  ),
    (SUBMENU, 'Rx view as', (
        (RADIOITEM, wx.NewId(), 'ASCII', '', 'self.OnRxAsciiMode' ),
        (RADIOITEM, wx.NewId(), 'HEX',   '', 'self.OnRxHexMode'   ),
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


class MyApp(wx.App):
    def OnInit(self):
        self.frame = ui.MyFrame(None, wx.ID_ANY, "")
        
        self.frame.SplitterWindow.SetSashSize(0)
        self.frame.SplitterWindow.SetSashPosition(160, True)
        
#         self.frame.choicePort.AppendItems(('COM1', 'COM2', 'COM3', 'COM4', 'COM5', 'COM6', 'COM7', 'COM8'))

        self.OnEnumPorts()
        self.frame.choicePort.Select(0)

        # initial variables
        self.serialport = serial.Serial()
        self.rxmode = ASCII
        self.txmode = ASCII
        self.localEcho = False
        self.rxCount = 0
        self.txCount = 0
        
        # Make a menu
        menuBar = wx.MenuBar()
        for m in MenuDefs:
            menu = wx.Menu()
            for k in m[1]:
                self.MakeMenu(menu, k)
            menuBar.Append(menu, m[0])

        self.frame.SetMenuBar(menuBar)
        
        # bind events
        self.frame.btnHideBar.Bind(wx.EVT_BUTTON, self.OnHideSettingBar)
        self.frame.btnOpen.Bind(wx.EVT_BUTTON, self.OnBtnOpen)
        self.frame.btnEnumPorts.Bind(wx.EVT_BUTTON, self.OnEnumPorts)
        
#         self.frame.Bind(wx.EVT_WINDOW_DESTROY, self.Cleanup)
        self.frame.Bind(wx.EVT_CLOSE, self.Cleanup)

        self.Bind(EVT_SERIALRX, self.OnSerialRead)
        self.Bind(EVT_SERIALEXCEPT, self.OnSerialExcept)
        self.frame.txtctlMain.Bind(wx.EVT_CHAR, self.OnSerialWrite)
        
        self.SetTopWindow(self.frame)
        self.frame.Show()
        
        
        self.evtPortOpen = threading.Event()
        self.rxQueue = Queue.Queue()
        self.txQueue = Queue.Queue()
        
        return True

    def GetPort(self):
        r = regex_matchPort.search(self.frame.choicePort.GetLabelText())
        if r:
            return int(r.group('port')) - 1
        return

    def GetBaudRate(self):
        return int(self.frame.cmbBaudRate.GetLabelText())

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
            
    def MakeMenu(self, menu, args = ()):
#         print args
        if args[0] == 1:
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
                self.MakeMenu(submenu, i)
            menu.AppendSubMenu(submenu, args[1])

    def OnEnumPorts(self, evt = None):
        self.frame.choicePort.Clear()
        for p in EnumerateSerialPorts():
            self.frame.choicePort.AppendItems((p,))
        
    def OnBtnOpen(self, evt = None):
        if self.serialport.isOpen():
            self.OnClosePort(evt)
        else:
            self.OnOpenPort(evt)
        
    def OnOpenPort(self, evt = None):
        self.serialport.port     = self.GetPort()
        self.serialport.baudrate = self.GetBaudRate()
        self.serialport.bytesize = self.GetDataBits()
        self.serialport.stopbits = self.GetStopBits()
        self.serialport.parity   = self.GetParity()
        self.serialport.rtscts   = self.frame.chkboxrtscts.IsChecked()
        self.serialport.xonxoff  = self.frame.chkboxxonxoff.IsChecked()
        self.serialport.timeout  = THREAD_TIMEOUT
        try:
            self.serialport.open()
        except serial.SerialException, e:
            dlg = wx.MessageDialog(None, str(e), "Serial Port Error", wx.OK | wx.ICON_ERROR)
            dlg.ShowModal()
            dlg.Destroy()
        else:
            self.StartThread()
            self.frame.SetTitle("MyTerm on %s [%s, %s%s%s%s%s]" % (
                self.serialport.portstr,
                self.serialport.baudrate,
                self.serialport.bytesize,
                self.serialport.parity,
                self.serialport.stopbits,
                self.serialport.rtscts and ' RTS/CTS' or '',
                self.serialport.xonxoff and ' Xon/Xoff' or '',
                )
            )
            self.frame.btnOpen.SetBackgroundColour((0,0xff,0x7f))
            self.frame.btnOpen.SetLabel('Opened')
            self.frame.btnOpen.Refresh()
            
    
    def OnClosePort(self, evt = None):
        if self.serialport.isOpen():
            self.StopThread()
            self.serialport.close()
            self.frame.SetTitle('MyTerm')
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
                text = self.serialport.read(1)
            except serial.serialutil.SerialException:
                evt = SerialExceptEvent(self.frame.GetId(), -1)
                self.frame.GetEventHandler().AddPendingEvent(evt)
                print 'thread exit for except'
                return -1

            if text:
#                 print ord(text),
                n = self.serialport.inWaiting()
                if n:
                    text = text + self.serialport.read(n)

                if self.rxmode == HEX:
                    text = ''.join(str(ord(t)) + ' ' for t in text)     # text = ''.join([(c >= ' ') and c or '<%d>' % ord(c)  for c in text])
                self.frame.txtctlMain.AppendText(text)
                
                """Using event to display is slow when the data is too big."""
#                 evt = SerialRxEvent(self.frame.GetId(), text)
#                 self.frame.GetEventHandler().AddPendingEvent(evt)
                self.rxCount += len(text)
                self.frame.statusbar.SetStatusText('Rx:%d' % self.rxCount, 1)
        print 'exit thread'
    
    def OnSerialRead(self, evt):
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
            
        if self.serialport.isOpen():
            if keycode < 256:
                self.serialport.write(chr(keycode))
                self.txCount += 1
                self.frame.statusbar.SetStatusText('Tx:%d' % self.txCount, 2)
            else:
                print "Extra Key:", keycode
        
    def OnSerialExcept(self, evt):
        param = evt.param
        if param == -1:
            self.StopThread()
            self.serialport.close()
            self.frame.SetTitle('MyTerm')
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
        self.frame.statusbar.SetStatusText('Rx:ASCII', 3)
    
    def OnRxHexMode(self, evt = None):
        self.rxmode = HEX
        self.frame.statusbar.SetStatusText('Rx:HEX', 3)
        
    def OnTxAsciiMode(self, evt = None):
        self.txmode = ASCII
        self.frame.statusbar.SetStatusText('Tx:ASCII', 4)
    
    def OnTxHexMode(self, evt = None):
        self.txmode = HEX
        self.frame.statusbar.SetStatusText('Tx:HEX', 4)

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
        elif evt.Selection == 0:
            self.localEcho = False
        
    def OnAbout(self, evt = None):
        AboutPanel(self.frame).OnShow()
        
    
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

class AboutPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, -1)

    def OnShow(self):
        # First we create and fill the info object
        info = wx.AboutDialogInfo()
        info.Name = "MyTerm"
        info.Version = "1.0"
        info.Copyright = "(C) 2013 Programmers and Coders Everywhere"
        info.Description = wordwrap(
            '\nMyTerm offer a great solution for RS232 serial port communication.'
            '\n\nIts other features including detecting the valid serial ports, '
            'receiving data from serial ports and viewing it in ASCII text or hexadecimal formats, '
            'echoing the sending data in local or not.',
            350, wx.ClientDC(self))
        info.WebSite = ("https://github.com/gamesun/MyTerm", "MyTerm Home Page")
        info.Developers = [ "sun.yt" ]
        info.License = wordwrap("Copywrong All Lefts Unreserved.", 500, wx.ClientDC(self))

        # Then we call wx.AboutBox giving it that info object
        wx.AboutBox(info)
        
if __name__ == '__main__':
    app = MyApp(0)
    app.MainLoop()
