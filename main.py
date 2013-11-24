#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# Copyright (c) 2013, gamesun
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#
#     * Redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above
# copyright notice, this list of conditions and the following disclaimer
# in the documentation and/or other materials provided with the
# distribution.
#     * Neither the name of gamesun nor the names of its contributors
# may be used to endorse or promote products derived from this software
# without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY GAMESUN "AS IS" AND ANY EXPRESS OR
# IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL GAMESUN BE LIABLE FOR ANY DIRECT,
# INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
# HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
# STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING
# IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#

import sys, os
import wx
import GUI as ui
import threading
import re
import serial
# import time
from wx.lib.wordwrap import wordwrap
import itertools
import icon32
import pkg_resources
import zipfile
from cStringIO import StringIO
import webbrowser
import appInfo
import glob
import subprocess
import ConfigParser

MAINMENU  = 0
SUBMENU   = 1
MENUITEM  = 2
CHECKITEM = 3
SEPARATOR = 4
RADIOITEM = 5

ASCII           = 0
HEX_LOWERCASE   = 1
HEX_UPPERCASE   = 2


THREAD_TIMEOUT = 0.5
SERIAL_WRITE_TIMEOUT = 0.5
SASHPOSITION = 180


if sys.platform == 'win32':
    DIRECTORY_SEPARATER = '\\'
elif sys.platform.startswith('linux'):
    DIRECTORY_SEPARATER = '/'


SERIALRXCNT = wx.NewEventType()                         # Create an own event type
EVT_SERIALRXCNT = wx.PyEventBinder(SERIALRXCNT, 0)      # bind to serial data receive events
class SerialRxCntEvent(wx.PyCommandEvent):
    eventType = SERIALRXCNT
    def __init__(self, windowID):
        wx.PyCommandEvent.__init__(self, self.eventType, windowID)

    def Clone(self):
        self.__class__(self.GetId())
 
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

        import _winreg as winreg
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


MENU_ID_LOCAL_ECHO = wx.NewId()

MENU_ID_RX_ASCII = wx.NewId()
MENU_ID_RX_HEX_L = wx.NewId()
MENU_ID_RX_HEX_U = wx.NewId()

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
    (CHECKITEM, MENU_ID_LOCAL_ECHO, '&Local echo','echo what you typed', 'self.OnLocalEcho'      ),
    (SUBMENU, '&Rx view as', (
        (RADIOITEM, MENU_ID_RX_ASCII, '&Ascii', '', 'self.OnRxAsciiMode' ),
        (RADIOITEM, MENU_ID_RX_HEX_L, '&hex(lowercase)',   '', 'self.OnRxHexModeLowercase'   ),
        (RADIOITEM, MENU_ID_RX_HEX_U, '&HEX(UPPERCASE)',   '', 'self.OnRxHexModeUppercase'   ),
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
        self.frame.SplitterWindow.SetSashPosition(SASHPOSITION, True)
        
#         self.frame.cmbPort.AppendItems(('COM1', 'COM2', 'COM3', 'COM4', 'COM5', 'COM6', 'COM7', 'COM8'))

        self.OnEnumPorts()

        # Make a menu
        self.menuBar = wx.MenuBar()
        self.MakeMenu(self.menuBar, MenuDefs)
        self.frame.SetMenuBar(self.menuBar)
        
        # initial variables
        self.rxmode = ASCII
        self.txmode = ASCII
        self.localEcho = False
        self.rxCount = 0
        self.txCount = 0
        
        self.config = ConfigParser.RawConfigParser()
        self.LoadSettings()
        
        
        # bind events
        self.frame.btnHideBar.Bind(wx.EVT_BUTTON, self.OnHideSettingBar)
        self.frame.btnOpen.Bind(wx.EVT_BUTTON, self.OnBtnOpen)
        self.frame.btnEnumPorts.Bind(wx.EVT_BUTTON, self.OnEnumPorts)
        self.frame.btnClear.Bind(wx.EVT_BUTTON, self.OnClear)
        
#         self.frame.Bind(wx.EVT_WINDOW_DESTROY, self.Cleanup)
        self.frame.Bind(wx.EVT_CLOSE, self.Cleanup)

        self.Bind(EVT_SERIALRXCNT, self.OnSerialRxCnt)
        self.Bind(EVT_SERIALEXCEPT, self.OnSerialExcept)
        self.frame.txtctlMain.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)
        self.frame.txtctlMain.Bind(wx.EVT_CHAR, self.OnSerialWrite)
        self.frame.txtctlMain.Bind(wx.EVT_TEXT_PASTE, self.OnPaste)
        self.frame.txtctlMain.Bind(wx.EVT_TEXT_URL, self.OnURL)

        self.SetTopWindow(self.frame)
        self.frame.SetTitle( appInfo.title )
        self.frame.Show()
        
        self.evtPortOpen = threading.Event()
#         self.rxQueue = Queue.Queue()
#         self.txQueue = Queue.Queue()
        
        return True
    
    
    def LoadSettings(self):
        self.config.read('setting.ini')
        
        if self.config.has_section('serial'):
            self.frame.cmbPort.SetStringSelection(self.config.get('serial', 'port'))
            self.frame.cmbBaudRate.SetStringSelection(self.config.get('serial', 'baudrate'))
            self.frame.choiceDataBits.SetStringSelection(self.config.get('serial', 'databits'))
            self.frame.choiceParity.SetStringSelection(self.config.get('serial', 'parity'))
            self.frame.choiceStopBits.SetStringSelection(self.config.get('serial', 'stopbits'))
            
            if self.config.get('serial', 'rtscts') == 'on':
                self.frame.chkboxrtscts.SetValue(True)
            else:
                self.frame.chkboxrtscts.SetValue(False)
            
            if self.config.get('serial', 'xonxoff') == 'on':
                self.frame.chkboxxonxoff.SetValue(True)
            else:
                self.frame.chkboxxonxoff.SetValue(False)
            
        
        if self.config.has_section('display'):
            {'ASCII':  self.OnRxAsciiMode,
             'hex':    self.OnRxHexModeLowercase,
             'HEX':    self.OnRxHexModeUppercase,
             }[self.config.get('display', 'rx_view_as')]()
            
            self.menuBar.Check({ASCII:           MENU_ID_RX_ASCII,
                                HEX_LOWERCASE:   MENU_ID_RX_HEX_L,
                                HEX_UPPERCASE:   MENU_ID_RX_HEX_U,
                                }.get(self.rxmode),
                               True)

            if self.config.get('display', 'local_echo') == 'on':
                self.menuBar.Check(MENU_ID_LOCAL_ECHO, True)
                self.localEcho = True
                self.frame.statusbar.SetStatusText('Local echo:On', 4)
            else:
                self.menuBar.Check(MENU_ID_LOCAL_ECHO, False)
                self.localEcho = False
                self.frame.statusbar.SetStatusText('Local echo:Off', 4)
            
#             MENU_ID_LOCAL_ECHO
    
    def SaveSettings(self):
        if not self.config.has_section('serial'):
            self.config.add_section('serial')
        
        self.config.set('serial', 'port',       str(self.frame.cmbPort.GetStringSelection()))
        self.config.set('serial', 'baudrate',   str(self.frame.cmbBaudRate.GetStringSelection()))
        self.config.set('serial', 'databits',   str(self.frame.choiceDataBits.GetStringSelection()))
        self.config.set('serial', 'parity',     str(self.frame.choiceParity.GetStringSelection()))
        self.config.set('serial', 'stopbits',   str(self.frame.choiceStopBits.GetStringSelection()))
        self.config.set('serial', 'rtscts',
                        self.frame.chkboxrtscts.IsChecked() and 'on' or 'off' )
        self.config.set('serial', 'xonxoff',
                        self.frame.chkboxxonxoff.IsChecked() and 'on' or 'off' )
        
        
        if not self.config.has_section('display'):
            self.config.add_section('display')
        
        self.config.set('display', 'rx_view_as', 
                        {ASCII:        'ASCII',
                         HEX_LOWERCASE:'hex',
                         HEX_UPPERCASE:'HEX',
                         }.get(self.rxmode)
                        )
        
        self.config.set('display', 'local_echo', self.localEcho and 'on' or 'off')
        
        with open('setting.ini', 'w') as configfile:
            self.config.write(configfile)
    
    def OnURL(self, evt):
        if evt.MouseEvent.LeftUp():
            s = evt.GetURLStart()
            e = evt.GetURLEnd()
            strURL = self.frame.txtctlMain.GetRange(s, e)
            webbrowser.open(strURL)
            return
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
            
            f = open(path, 'w')
            
            f.write(self.frame.txtctlMain.GetValue())
            
            f.close()
            
        dlg.Destroy()
            
    def GetPort(self):
        if sys.platform == 'win32':
            r = regex_matchPort.search(self.frame.cmbPort.GetStringSelection())
            if r:
                return int(r.group('port')) - 1
            return
        elif sys.platform.startswith('linux'):
            return self.frame.cmbPort.GetStringSelection()

    def GetBaudRate(self):
        return int(self.frame.cmbBaudRate.GetValue())

    def GetDataBits(self):
        s = self.frame.choiceDataBits.GetStringSelection()
        if s == '5': 
            return serial.FIVEBITS
        elif s == '6': 
            return serial.SIXBITS
        elif s == '7': 
            return serial.SEVENBITS
        elif s == '8': 
            return serial.EIGHTBITS
    
    def GetParity(self):
        s = self.frame.choiceParity.GetStringSelection()
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
        s = self.frame.choiceStopBits.GetStringSelection()
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
        self.frame.cmbPort.Clear()
        for p in EnumerateSerialPorts():
            self.frame.cmbPort.AppendItems((p,))
        self.frame.cmbPort.Select(0)
        
    def OnBtnOpen(self, evt = None):
        if serialport.isOpen():
            self.OnClosePort(evt)
        else:
            self.OnOpenPort(evt)
        
    def OnOpenPort(self, evt = None):
        if serialport.isOpen():
            return
        
        serialport.port     = self.GetPort()
        serialport.baudrate = self.GetBaudRate()
        serialport.bytesize = self.GetDataBits()
        serialport.stopbits = self.GetStopBits()
        serialport.parity   = self.GetParity()
        serialport.rtscts   = self.frame.chkboxrtscts.IsChecked()
        serialport.xonxoff  = self.frame.chkboxxonxoff.IsChecked()
        serialport.timeout  = THREAD_TIMEOUT
        serialport.writeTimeout = SERIAL_WRITE_TIMEOUT
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
            self.frame.btnOpen.SetLabel('Close')
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

                if self.rxmode == HEX_LOWERCASE:
                    self.rxCount += len(text)
                    text = ''.join('%02x ' % ord(t) for t in text)
                    self.frame.txtctlMain.AppendText(text)
                elif self.rxmode == HEX_UPPERCASE:
                    self.rxCount += len(text)
                    text = ''.join('%02X ' % ord(t) for t in text)
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
                        self.frame.txtctlMain.AppendText(text)
                    self.rxCount += len(text)

                """Using event to display is slow when the data is too big."""
#                 evt = SerialRxEvent(self.frame.GetId(), text)
#                 self.frame.GetEventHandler().AddPendingEvent(evt)
                
#                 self.frame.statusbar.SetStatusText('Rx:%d' % self.rxCount, 1)
                """ Under Linux, to update statusbar in threads will cause 
                assert or X windows error or some other strange errors.
                Using event to update statusbar can avoid those errors."""
                evt = SerialRxCntEvent(self.frame.GetId())
                self.frame.GetEventHandler().AddPendingEvent(evt)                

        print 'exit thread'
        
    def OnSerialRxCnt(self, evt = None):
        self.frame.statusbar.SetStatusText('Rx:%d' % self.rxCount, 1)
        
        
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
                try:
                    serialport.write(chr(keycode))
                except serial.SerialException, e:
                    evt = SerialExceptEvent(self.frame.GetId(), e)
                    self.frame.GetEventHandler().AddPendingEvent(evt)
                else:
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
                    try:
                        serialport.write(chr(keycode))
                    except serial.SerialException, e:
                        evt = SerialExceptEvent(self.frame.GetId(), e)
                        self.frame.GetEventHandler().AddPendingEvent(evt)
                    else:
                        self.txCount += 1
                        self.frame.statusbar.SetStatusText('Tx:%d' % self.txCount, 2)
            else:
                evt.Skip()
            
    def OnPaste(self ,evt = None):
        data = wx.TextDataObject()
        wx.TheClipboard.GetData(data)

        if serialport.isOpen():
            try:
                serialport.write( data.GetText() )
            except serial.SerialException, e:
                evt = SerialExceptEvent(self.frame.GetId(), e)
                self.frame.GetEventHandler().AddPendingEvent(evt)
            else:
                self.txCount += len( data.GetText() )
                self.frame.statusbar.SetStatusText('Tx:%d' % self.txCount, 2)
                    
        if self.localEcho:
            evt.Skip()
    
    def OnSerialExcept(self, evt):
        e = evt.param
        dlg = wx.MessageDialog(None, str(e), "Serial Port Error", wx.OK | wx.ICON_ERROR)
        dlg.ShowModal()
        dlg.Destroy()

        self.StopThread()
        serialport.close()
        self.frame.SetTitle(appInfo.title)
        self.frame.btnOpen.SetBackgroundColour(wx.NullColour)
        self.frame.btnOpen.SetLabel('Open')
        self.frame.btnOpen.Refresh()

    def OnHideSettingBar(self, evt = None):
        self.frame.SplitterWindow.SetSashPosition(1, True)
        
    def OnShowSettingBar(self, evt = None):
        self.frame.SplitterWindow.SetSashPosition(SASHPOSITION, True)
    
    def OnShowStatusBar(self, evt = None):
        pass
    
    def OnRxAsciiMode(self, evt = None):
        self.rxmode = ASCII
        self.frame.statusbar.SetStatusText('Rx:Ascii', 3)
    
    def OnRxHexModeLowercase(self, evt = None):
        self.rxmode = HEX_LOWERCASE
        self.frame.statusbar.SetStatusText('Rx:hex', 3)
        
    def OnRxHexModeUppercase(self, evt =None):
        self.rxmode = HEX_UPPERCASE
        self.frame.statusbar.SetStatusText('Rx:HEX', 3)

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
            '\nMyTerm is a RS232 serial port communication utility that can '
            'display the received data either in hexadecimal or ASCII format, '
            'allowing you to configure the connection parameters.'
            '\n\nIts other features including detecting the valid serial '
            'ports, echoing the sending data in local or not.',
            335, wx.ClientDC(self.frame))
        info.WebSite = (appInfo.url, "Home Page")
        info.Developers = [ appInfo.author ]
        info.License = wordwrap(appInfo.copyright, 500, wx.ClientDC(self.frame))

        info.Icon = icon32.geticon32Icon()

        # Then we call wx.AboutBox giving it that info object
        wx.AboutBox(info)
    
    def OnExitApp(self, evt = None):
        self.frame.Close(True)      # send EVT_CLOSE
    
    def Cleanup(self, evt = None):
        self.SaveSettings()
        
        self.frame.Destroy()
        self.OnClosePort()
#         for t in threading.enumerate():
#             print t.getName()
        if hasattr(self, 'thread'):
            if self.thread is not None:
                assert not self.thread.is_alive(), "the thread should be dead but isn't!"
#             self.threadCommunicate.terminate()

        
if __name__ == '__main__':
    app = MyApp(0)
    app.MainLoop()
