#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
#
#############################################################################
##
## Copyright (c) 2013-2023, gamesun
## All right reserved.
##
## This file is part of UartVide(MyTerm).
##
## UartVide(MyTerm) is free software: you can redistribute it and/or
## modify it under the terms of the GNU General Public License as
## published by the Free Software Foundation, either version 3 of the
## License, or (at your option) any later version.
##
## UartVide(MyTerm) is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License along
## with UartVide(MyTerm).  If not, see <http://www.gnu.org/licenses/>.
##
#############################################################################


from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from qfluentwidgets import *
from qfluentwidgets.components.widgets.menu import TextEditMenu

class UVTextEdit(QTextEdit):
    
    def __init__(self, *args, **kwargs):
        super(UVTextEdit, self).__init__(*args, **kwargs)
        self.scrollDelegate = SmoothScrollDelegate(self, True)
        self.setStyleSheet('''
            TextEdit {
                background-color:white;
                color:%(TextColor)s;
                border-top: none;
                border-bottom: none;
                border-left: 2px solid %(BackgroundColor)s;
                border-right: 2px solid %(BackgroundColor)s;
            }
            TextEdit::focus {}
        '''% dict(
            BackgroundColor =  '#99d9ea',
            TextColor =        '#202020',
            ScrollBar_Handle = '#61b9e1',
            ScrollBar_Line =   '#7ecfe4',
            TableView_Corner = '#8ae6d2',
            TableView_Header = '#8ae6d2',
            TableView_Border = '#eeeeee',
        ))

    def contextMenuEvent(self, e):
        menu = TextEditMenu(self)
        menu.exec(e.globalPos())
