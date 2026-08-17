#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
#
#############################################################################
##
## Copyright (c) 2013-2026, gamesun
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


theSolitaryRenameDailog = None

theSolitaryConfirmDialog = None

class ConfirmDialog(FramelessDialog):

    def __init__(self, *args, **kwargs):
        super(ConfirmDialog, self).__init__(*args, **kwargs)

        self.titleBar.closeBtn.hide()

        self.setAttribute(Qt.WA_DeleteOnClose)
        self.destroyed.connect(self.close)

        self.confirmed = False

        self.__icon = QLabel(self)
        self.__icon.setFixedSize(QSize(24, 24))
        self.__icon.setPixmap(FluentIcon.INFO.icon().pixmap(24, 24))
        self.__icon.setStyleSheet('QLabel { border: none; }')

        self.__lbl = QLabel()
        self.__lbl.setWordWrap(True)
        self.__lbl.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.__lbl.setStyleSheet('QLabel { border: none; padding: 8px; color: #202020; font-family: Tahoma; font-size: 10.5pt; }')

        contentLayout = QHBoxLayout()
        contentLayout.setContentsMargins(0, 0, 0, 0)
        contentLayout.setSpacing(10)
        contentLayout.addWidget(self.__icon)
        contentLayout.addWidget(self.__lbl, 1)

        vLayout = QVBoxLayout(self)
        vLayout.setContentsMargins(12, 12, 12, 12)
        vLayout.setSpacing(10)
        vLayout.addLayout(contentLayout)

        btnOK = PushButton('OK')
        btnOK.setFixedSize(QSize(70, 28))
        btnOK.clicked.connect(self.onOK)

        btnCancel = PushButton('Cancel')
        btnCancel.setFixedSize(QSize(70, 28))
        btnCancel.clicked.connect(self.onCancel)

        hLayout = QHBoxLayout()
        hLayout.setContentsMargins(0, 0, 0, 0)
        hLayout.addStretch(1)
        hLayout.addWidget(btnOK)
        hLayout.addWidget(btnCancel)

        vLayout.addLayout(hLayout)

        self.setStyleSheet('QWidget { background-color: white; outline: none; border: 1px solid rgba(0, 0, 0, 0.1); }')
        self.setFixedSize(QSize(280, 120))

    def onOK(self):
        self.confirmed = True
        self.close()

    def onCancel(self):
        self.confirmed = False
        self.close()

    @staticmethod
    def confirm(message, pos):
        global theSolitaryConfirmDialog
        theSolitaryConfirmDialog = ConfirmDialog()
        theSolitaryConfirmDialog.__confirm(message, pos)
        return theSolitaryConfirmDialog.confirmed

    def __confirm(self, message, pos):
        self.move(pos.x(), pos.y())
        self.__lbl.setText(message)
        self.exec_()


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

