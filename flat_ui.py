#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
#
#############################################################################
##
## Copyright (c) 2013-2018, gamesun
## All right reserved.
##
## This file is part of MyTerm.
##
## MyTerm is free software: you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation, either version 3 of the License, or
## (at your option) any later version.
##
## MyTerm is distributed in the hope that it will be useful, but
## WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with MyTerm.  If not, see <http://www.gnu.org/licenses/>.
##
#############################################################################

from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import QMenuBar, QPushButton, QPainter, QColor, QPen, QBrush
from PyQt4.QtCore import Qt, QRect

class FMenuBar(QMenuBar):
    """flat MenuBar"""
    def __init__(self, *args, **kwargs):
        super(FMenuBar, self).__init__(*args, **kwargs)
        self._dragPos = self.pos()
        self._isDragging = False
    
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._isDragging = True
            self._dragPos = event.globalPos() - self.parent().pos()
        super(FMenuBar, self).mousePressEvent(event)
        
    def mouseMoveEvent(self, event):
        if event.buttons() and Qt.LeftButton and self._isDragging and not self.isMaximized():
            self.parent().move(event.globalPos() - self._dragPos)
        super(FMenuBar, self).mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        self._isDragging = False
        super(FMenuBar, self).mouseReleaseEvent(event)

    def isMaximized(self):
        return ((self.parent().windowState() == Qt.WindowMaximized))
