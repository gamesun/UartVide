#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
#
#############################################################################
##
## Copyright (c) 2013-2025, gamesun
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


# PySide2
from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from qfluentwidgets import *

class UVToggleButton(TransparentToggleToolButton):
    # rightClicked = Signal()
    
    def __init__(self, parent=None, icon=None):
        super(UVToggleButton, self).__init__(parent)
        
        self.setFixedSize(QSize(24, 24))
        self.setStyleSheet("""
            UVToggleButton { background-color: transparent; border:none; border-radius: 6px; }
            UVToggleButton:hover { background-color:#51c0d1; }
            UVToggleButton:pressed { background-color:#b8e5f1; }
            UVToggleButton:checked { background-color: #51c0d1; }
        """)
        self.setIcon(icon)
        self.setIconSize(QtCore.QSize(20, 20))
        self.setToolTip("Timestamp")
        self.setCursor(Qt.PointingHandCursor)

    # def mousePressEvent(self, event):
    #     if event.button() == Qt.RightButton:
    #         self.rightClicked.emit()
    #     super(UVToggleButton, self).mousePressEvent(event)

