# -*- coding:utf-8 -*-

#import sys,os
import wx
import GUI as ui

MENUITEM  = 1
CHECKITEM = 2
SEPARATOR = 3

MenuDefs = (
('&Operation', (
    (MENUITEM,  wx.NewId(), '&Open Port',         'Open the Port' ,     'self.OnOpenPort'  ),
    (MENUITEM,  wx.NewId(), '&Close Port',        'Close the Port',     'self.OnClosePort' ),
    (SEPARATOR,),
    (MENUITEM,  wx.NewId(), '&Exit MyTerm',       'Exit this tool',     'self.OnExitApp'   ),
)),
('&Display', (
    (MENUITEM,  wx.NewId(), 'Show S&etting Bar',  'Show Setting Bar',   'self.OnShowSettingBar' ),
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
        
        self.frame.btnHideBar.Bind(wx.EVT_BUTTON, self.OnHideBar)
        
        # Make a menu
        menuBar = wx.MenuBar()

#         # 1st menu from left
#         m1 = wx.Menu()
#         m1.Append(wx.ID_OPEN,    "&Open Port", "Open the Port")
#         m1.Append(wx.ID_CLOSE,   "&Close Port", "Close the Port")
#         m1.AppendSeparator()
#         m1.Append(wx.ID_EXIT,    "&Exit MyTerm", "Exit this tool")
#         m1.Enable(wx.ID_CLOSE, False)
#         menuBar.Append(m1, "&Operation")
#          
#         m2 = wx.Menu()
#         m2.Append(wx.ID_ANY, )
        
        for m in MenuDefs:
            menu = wx.Menu()
            for k in m[1]:
                if k[0] == 1:
                    menu.Append(k[1], k[2], k[3])
                    eval('self.frame.Bind(wx.EVT_MENU,' + k[4] + ', id = k[1])')
                elif k[0] == CHECKITEM:
                    menu.AppendCheckItem(k[1], k[2], k[3])
                    eval('self.frame.Bind(wx.EVT_MENU,' + k[4] + ', id = k[1])')
                elif k[0] == SEPARATOR:
                    menu.AppendSeparator()
            menuBar.Append(menu, m[0])

        self.frame.SetMenuBar(menuBar)
 
        self.SetTopWindow(self.frame)
        self.frame.Show()
        
        return True

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
    
    def OnAbout(self, evt = None):
        pass
    
    def OnExitApp(self, evt = None):
        self.frame.Close(True)



if __name__ == '__main__':
    app = MyApp(0)
    app.MainLoop()
