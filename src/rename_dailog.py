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


# PySide2
from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

theSolitaryRenameDailog = None

class RenameDailog(QDialog):

    def __init__(self, *args, **kwargs):
        super(RenameDailog, self).__init__(*args, **kwargs)

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Popup)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.destroyed.connect(self.close)

        self.newname = None

        self.__edt = QLineEdit()
        self.__edt.setMinimumSize(QSize(200, 24))
        self.__edt.setMaximumSize(QSize(16777215, 24))
        
        vLayout = QVBoxLayout()
        vLayout.addWidget(self.__edt)

        btnOK = QPushButton('OK')
        btnOK.clicked.connect(self.onOK)
        
        btnCancel = QPushButton('Cancel')
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

        self.setLayout(vLayout)

        pal = self.palette()
        pal.setColor(QPalette.Window, QColor('#b8e5f1'))
        pal.setColor(QPalette.WindowText, QColor('#202020'))
        self.setPalette(pal)

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

