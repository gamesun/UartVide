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
from qframelesswindow import *


class AboutDialog(FramelessDialog):

    def __init__(self, parent=None, title='', content=''):
        super(AboutDialog, self).__init__(parent)

        self.setStyleSheet('''
            QWidget { background-color: white; outline: none; border: none; }
            QDialog { border: 1px solid rgba(0, 0, 0, 0.1); }
        ''')

        self.lblTitleIcon = QLabel(self)
        self.lblTitleIcon.setFixedSize(QSize(20, 20))
        self.lblTitleIcon.setPixmap(QIcon(":/uartvide-icon/uartvide.ico").pixmap(20, 20))

        self.lblTitle = QLabel(self)
        self.lblTitle.setText(title)
        # self.lblTitle.setStyleSheet('QLabel {font-weight: Bold;}')

        self.hBxLyt_tb = QHBoxLayout()
        self.hBxLyt_tb.setObjectName('hBxLyt_tb')
        self.hBxLyt_tb.setSpacing(4)
        self.hBxLyt_tb.setContentsMargins(3, 0, 0, 0)
        self.hBxLyt_tb.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)

        self.hBxLyt_tb.addWidget(self.lblTitleIcon)
        self.hBxLyt_tb.addWidget(self.lblTitle)

        self.titleBar.hBoxLayout.insertLayout(0, self.hBxLyt_tb, 0)

        self.titleBar.hBoxLayout.setContentsMargins(4, 0, 0, 0)

        self.lblIcon = QLabel(self)
        self.lblIcon.setFixedSize(QSize(64, 64))
        self.lblIcon.setPixmap(QIcon(":/uartvide-icon/uartvide.ico").pixmap(64, 64))

        self.lblContent = QLabel(self)
        # self.lblContent.setWordWrap(True)
        self.lblContent.setText(content)

        self.hBxLyt = QHBoxLayout(self)
        self.hBxLyt.setSpacing(12)
        self.hBxLyt.setContentsMargins(10, 50, 10, 10)
        self.hBxLyt.setAlignment(Qt.AlignTop | Qt.AlignLeft)

        self.hBxLyt.addWidget(self.lblIcon)
        self.hBxLyt.addWidget(self.lblContent)

        self.setFixedSize(QSize(460, 200))