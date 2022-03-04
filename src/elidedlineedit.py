#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
#
#############################################################################
##
## Copyright (c) 2013-2022, gamesun
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


class ElidedLineEdit(QLineEdit):
    def __init__(self, text, parent = None):
        super(ElidedLineEdit, self).__init__(text, parent)
        self.content = text
        self.textEdited.connect(self.onTextEdited)
        self.installEventFilter(self)

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
