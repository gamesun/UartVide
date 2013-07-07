# -*- coding:utf-8 -*-

#import sys,os
import wx
import GUI as ui
import multiprocessing
import UartProcess

SUBMENU   = 0
MENUITEM  = 1
CHECKITEM = 2
SEPARATOR = 3
RADIOITEM = 4

MenuDefs = (
('&Operation', (
    (MENUITEM,  wx.NewId(), '&Open Port',         'Open the Port' ,     'self.OnOpenPort'  ),
    (MENUITEM,  wx.NewId(), '&Close Port',        'Close the Port',     'self.OnClosePort' ),
    (SEPARATOR,),
    (MENUITEM,  wx.NewId(), '&Exit MyTerm',       'Exit this tool',     'self.OnExitApp'   ),
)),
('&Option', (
    (CHECKITEM, wx.NewId(), 'Local echo',         "echo what you typed", 'self.OnShowStatusBar'  ),
    (MENUITEM,  wx.NewId(), 'Show S&etting Bar',  'Show Setting Bar',    'self.OnShowSettingBar' ),
    (SUBMENU, 'Rx display mode', (
        (RADIOITEM, wx.NewId(), 'Ascii mode', '', 'self.OnRxAsciiMode' ),
        (RADIOITEM, wx.NewId(), 'Hex mode',   '', 'self.OnRxHexMode'   ),
    )),
    (SUBMENU, 'Tx display mode', (
        (RADIOITEM, wx.NewId(), 'Ascii mode', '', 'self.OnTxAsciiMode' ),
        (RADIOITEM, wx.NewId(), 'Hex mode',   '', 'self.OnTxHexMode'   ),
    )),
#     (CHECKITEM, wx.NewId(), 'S&tatus Bar',        'Show Status Bar',    'self.OnShowStatusBar'  ),
)),
('&Help', (
    (MENUITEM,  wx.NewId(), '&About',             'About  MyTerm',      'self.OnAbout' ),
))
)


class MyApp(wx.App):
    def OnInit(self):
        self.frame = ui.MyFrame(None, wx.ID_ANY, "")
        
        self.frame.SplitterWindow.SetSashSize(0)
        self.frame.chiocePort.AppendItems(('COM1', 'COM2', 'COM3', 'COM4', 'COM5', 'COM6', 'COM7', 'COM8'))
        
        # initial variables
        self.port = -1
        self.baud = 0
        
        # Make a menu
        menuBar = wx.MenuBar()
        for m in MenuDefs:
            menu = wx.Menu()
            for k in m[1]:
                self.MakeMenu(menu, k)
            menuBar.Append(menu, m[0])

        self.frame.SetMenuBar(menuBar)
        
        self.frame.btnHideBar.Bind(wx.EVT_BUTTON, self.OnHideBar)
        self.frame.Bind(wx.EVT_WINDOW_DESTROY, self.Cleanup)
 
        self.SetTopWindow(self.frame)
        self.frame.Show()
        
        self.processCommunicate = multiprocessing.Process(name = 'Uart_Communicate',
                                    target = UartProcess.UartCommunicate, 
                                    args = (None, None))
        
#         self.processCommunicate.start()
        
        return True

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
            

    def OnHideBar(self, evt = None):
        self.frame.SplitterWindow.SetSashPosition(1, True)

    def OnOpenPort(self, evt = None):
        
        pass
    
    def OnClosePort(self, evt = None):
        pass
    
    def OnShowSettingBar(self, evt = None):
        self.frame.SplitterWindow.SetSashPosition(160, True)
    
    def OnShowStatusBar(self, evt = None):
        pass
    
    def OnRxAsciiMode(self, evt = None):
        
        pass
    
    def OnRxHexMode(self, evt = None):
        
        pass
        
    def OnTxAsciiMode(self, evt = None):
        
        pass
    
    def OnTxHexMode(self, evt = None):
        
        pass
    def OnAbout(self, evt = None):
        pass
    
    def OnExitApp(self, evt = None):
        self.frame.Close(True)
    
    def Cleanup(self, evt = None):
        if self.processCommunicate.is_alive():
            self.processCommunicate.terminate()


if __name__ == '__main__':
    app = MyApp(0)
    app.MainLoop()
