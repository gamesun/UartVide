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


# PySide2
from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from qfluentwidgets import *
from qframelesswindow import *

theSolitaryRenameDailog = None

class RenameDailog(FramelessDialog):

    def __init__(self, *args, **kwargs):
        super(RenameDailog, self).__init__(*args, **kwargs)

        self.titleBar.closeBtn.hide()

        self.setAttribute(Qt.WA_DeleteOnClose)
        self.destroyed.connect(self.close)

        self.newname = None

        self.__edt = LineEdit()
        
        vLayout = QVBoxLayout(self)
        vLayout.addWidget(self.__edt)

        btnOK = PushButton('OK')
        btnOK.setFixedSize(QSize(70, 28))
        btnOK.clicked.connect(self.onOK)
        
        btnCancel = PushButton('Cancel')
        btnCancel.setFixedSize(QSize(70, 28))
        btnCancel.clicked.connect(self.onCancel)

        spacer_1 = QSpacerItem(10, 10, QSizePolicy.Expanding, QSizePolicy.Minimum)
        spacer_2 = QSpacerItem(10, 10, QSizePolicy.Expanding, QSizePolicy.Minimum)
        spacer_3 = QSpacerItem(10, 10, QSizePolicy.Expanding, QSizePolicy.Minimum)
        
        hLayout = QHBoxLayout()
        hLayout.addItem(spacer_1)
        hLayout.addWidget(btnOK)
        hLayout.addItem(spacer_2)
        hLayout.addWidget(btnCancel)
        hLayout.addItem(spacer_3)

        vLayout.addLayout(hLayout)

        self.setStyleSheet('QWidget { background-color: white; outline: none; border: 1px solid rgba(0, 0, 0, 0.1); }')
        self.setFixedSize(QSize(250, 100))

    def onOK(self):
        self.newname = self.__edt.text()
        self.close()

    def onCancel(self):
        self.close()

    @staticmethod
    def getNewName(oldname, pos):
        global theSolitaryRenameDailog
        theSolitaryRenameDailog = RenameDailog()
        theSolitaryRenameDailog.__renamedailog(oldname, pos)
        return theSolitaryRenameDailog.newname
    
    def __renamedailog(self, oldname, pos):
        self.move(pos.x(), pos.y())
        self.__edt.setText(oldname)
        self.__edt.selectAll()
        self.__edt.setFocus()

        self.exec()

