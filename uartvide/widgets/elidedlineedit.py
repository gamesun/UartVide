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

import sys, os
from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from qfluentwidgets.components.widgets.menu import LineEditMenu

if os.name == 'nt':
    CODE_FONT = "Consolas"
    UI_FONT = "Segoe UI"
elif os.name == 'posix':
    CODE_FONT = "Monospace"
    UI_FONT = "Ubuntu"

class ElidedLineEdit(QLineEdit):
    def __init__(self, parent = None, text=''):
        super(ElidedLineEdit, self).__init__(text, parent)
        self.content = text
        self.textEdited.connect(self.onTextEdited)
        self.installEventFilter(self)

        self.setStyleSheet('QLineEdit {border: none;font-size:9pt;font-family:%(Code_Font)s;}' % dict(Code_Font = CODE_FONT))

    def contextMenuEvent(self, e):
        menu = LineEditMenu(self)
        menu.exec(e.globalPos())

    def setText(self, text, elided = True):
        self.content = text
        if elided:
            fm = QFontMetrics(self.font())
            et = fm.elidedText(self.content, Qt.ElideRight, self.width() - 4)
            if et != self.content:
                self.setToolTip(self.content)
            super(ElidedLineEdit, self).setText(et)
        else:
            super(ElidedLineEdit, self).setText(text)

    def text(self):
        return self.content

    def eventFilter(self, obj, event):
        if event.type() == QEvent.FocusIn:
            self.setText(self.content, False)
        elif event.type() == QEvent.FocusOut or event.type() == QEvent.Resize or event.type() == QEvent.Create:
            self.setText(self.content, True)

        return super(ElidedLineEdit, self).eventFilter(obj, event)

    def onTextEdited(self, text):
        self.content = text
