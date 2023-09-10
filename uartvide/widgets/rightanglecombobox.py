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
from qfluentwidgets.common.icon import FluentIcon as FIF

class RightAngleComboBox(ComboBox):
    listShowEntered = Signal()
    currentTextChanged = Signal(str)
    
    def __init__(self, *args, **kwargs):
        super(RightAngleComboBox, self).__init__(*args, **kwargs)
        self.setStyleSheet('''
            ComboBox {
                padding: 2px 22px 3px 4px;
                color: black;
                background-color: rgba(255, 255, 255, 0.7);
                text-align: left;
            }

            ComboBox:hover {
                background-color: rgba(249, 249, 249, 0.5);
            }

            ComboBox:pressed {
                background-color: rgba(249, 249, 249, 0.3);
                color: rgba(0, 0, 0, 0.63);
            }

            ComboBox:disabled {
                
                background: rgba(145, 255, 0, 1);
            }

            ComboBoxMenu>MenuActionListWidget {
                border: 1px solid rgba(0, 0, 0, 0.1);
                background-color: rgb(249, 249, 249);
                outline: none;
                font-size:10pt;
            }

            ComboBoxMenu>MenuActionListWidget::item {
                margin-top: 0px;
                padding-left: 0px;
                padding-right: 0px;
                border: none;
                color: black;
                font-size:10pt;
            }

            ComboBoxMenu>MenuActionListWidget::item:disabled {
                padding-left: 0px;
                padding-right: 0px;
                border: none;
                color: black;
            }

            ComboBoxMenu>MenuActionListWidget::item:hover {
                background-color: rgba(0, 0, 0, 9);
            }

            ComboBoxMenu>MenuActionListWidget::item:selected {
                background-color: rgba(0, 0, 0, 7);
                color: black;
            }

            ComboBoxMenu>MenuActionListWidget::item:selected:active {
                background-color: rgba(0, 0, 0, 0.06);
                color: rgba(0, 0, 0, 0.7);
            }
            
            LineEdit {
                color: black;
                font-size:10pt;
                background-color: rgba(255, 255, 255, 0.7);
                border: none;
                padding: 0px 0px 2px 0px;
            }

            LineEdit:hover {
                background-color: rgba(249, 249, 249, 0.5);
            }

            LineEdit:focus {
                background-color: white;
            }

            LineEdit:disabled {
                color: rgba(0, 0, 0, 150);
                background-color: rgba(249, 249, 249, 0.3);
            }

            #lineEditButton {
                background-color: transparent;
                margin: 0;
            }

            #lineEditButton:hover {
                background-color: rgba(0, 0, 0, 9);
            }

            #lineEditButton:pressed {
                background-color: rgba(0, 0, 0, 6);
            }

        ''')

    def setText(self, text):
        super().setText(text)
        self.currentTextChanged.emit(text)

    def mousePressEvent(self, event):
        self.listShowEntered.emit()
        super(RightAngleComboBox, self).mousePressEvent(event)

    def setCurrentText(self, text):
        self.setText(text)

    def currentText(self):
        return self.text()
    
    def findText(self, text, flags:Qt.MatchFlags=Qt.MatchExactly):
        for index, item in enumerate(self.items):
            if flags == Qt.MatchContains:
                if text in item.text:
                    return index
            elif flags == Qt.MatchExactly:
                if text == item.text:
                    return index
        return -1

    def paintEvent(self, e):
        QPushButton.paintEvent(self, e)
        painter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing)
        if self.isHover:
            painter.setOpacity(0.8)
        elif self.isPressed:
            painter.setOpacity(0.7)

        rect = QRectF(self.width()-16, self.height()/2-5+self.arrowAni.y, 10, 10)
        FIF.ARROW_DOWN.render(painter, rect)

