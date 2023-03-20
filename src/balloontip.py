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

import os
from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
import shiboken2

if os.name == 'nt':
    UI_FONT = "Microsoft YaHei UI"
elif os.name == 'posix':
    UI_FONT = None

theSolitaryBalloonTip = None

class BalloonTip(QWidget):
    def __init__(self, icon, title, msg, *args, **kwargs):
        super(BalloonTip, self).__init__(*args, **kwargs)
        
        self.__pixmap = None
        self.__timerId = -1
        self.__showArrow = True
    
        # self.setWindowOpacity(0.9)
        self.setMouseTracking(True)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Popup)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.destroyed.connect(self.close)

        if title != None:
            titleLabel = QLabel(self)
            titleLabel.installEventFilter(self)
            titleLabel.setText(title)
        
            if UI_FONT:
                font = QFont()
                font.setFamily(UI_FONT)
                font.setPointSize(9)
            else:
                font = titleLabel.font()
            font.setBold(True)
            titleLabel.setFont(font)
            titleLabel.setTextFormat(Qt.AutoText)
    
        iconSize = 18
        # closeButtonSize = 15
        # closeButton = QPushButton()
        # closeButton.setIcon(self.style().standardIcon(QStyle.SP_TitleBarCloseButton))
        # closeButton.setIconSize(QSize(closeButtonSize, closeButtonSize))
        # closeButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        # closeButton.setFixedSize(closeButtonSize, closeButtonSize)
        # closeButton.clicked.connect(self.close)
    
        msgLabel = QLabel(self)
        if UI_FONT:
            font = QFont(UI_FONT)
        else:
            font = msgLabel.font()
        font.setPointSize(9)
        msgLabel.setFont(font)
        msgLabel.installEventFilter(self)
        msgLabel.setText(msg)
        msgLabel.setTextFormat(Qt.AutoText)
        msgLabel.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        # smart size for the message label
        #limit = QDesktopWidgetPrivate.availableGeometry(msgLabel).size().width() // 3
        # if msgLabel.sizeHint().width() > limit:
        #     msgLabel.setWordWrap(True)
        #     if msgLabel.sizeHint().width() > limit:
        #         msgLabel.d_func().ensureTextControl()
        #         control = msgLabel.d_func().control
        #         opt = control.document().defaultTextOption()
        #         opt.setWrapMode(Qt.QTextOption.WrapAnywhere)
        #         control.document().setDefaultTextOption(opt)

        #     # Here we allow the text being much smaller than the balloon widget
        #     # to emulate the weird standard windows behavior.
        #     msgLabel.setFixedSize(limit, msgLabel.heightForWidth(limit))
        
        layout = QGridLayout()
        if icon != None:
            iconLabel = QLabel()
            iconLabel.setPixmap(icon.pixmap(iconSize, iconSize))
            iconLabel.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            iconLabel.setMargin(2)
            layout.addWidget(iconLabel, 0, 0)
            if title != None:
                layout.addWidget(titleLabel, 0, 1)
        else:
            if title != None:
                layout.addWidget(titleLabel, 0, 0, 1, 2)
    
        #layout.addWidget(closeButton, 0, 2)
        layout.addWidget(msgLabel, 1, 0, 1, 3)
        layout.setSizeConstraint(QLayout.SetFixedSize)
        layout.setContentsMargins(3, 3, 3, 3)
        self.setLayout(layout)
        pal = self.palette()
        pal.setColor(QPalette.Window, QColor('#b8e5f1'))
        pal.setColor(QPalette.WindowText, QColor('#202020'))
        self.setPalette(pal)

    def mousePressEvent(self, event):
        super(BalloonTip, self).mousePressEvent(event)

    @staticmethod
    def showBalloon(icon, title, msg, pos, timeout, showArrow = True):
        global theSolitaryBalloonTip
        BalloonTip.hideBalloon()
        if msg == '' and title == '':
            return
        theSolitaryBalloonTip = BalloonTip(icon, title, msg)
        if timeout < 0:
            timeout = 10000 #10 s default
        theSolitaryBalloonTip.__balloon(pos, timeout, showArrow)

    @staticmethod
    def hideBalloon():
        global theSolitaryBalloonTip
        if theSolitaryBalloonTip == None or not shiboken2.isValid(theSolitaryBalloonTip):
            return
        theSolitaryBalloonTip.hide()
        theSolitaryBalloonTip = None
    
    @staticmethod
    def updateBalloonPosition(pos):
        global theSolitaryBalloonTip
        if theSolitaryBalloonTip == None or not shiboken2.isValid(theSolitaryBalloonTip):
            return
        theSolitaryBalloonTip.hide()
        theSolitaryBalloonTip.__balloon(pos, 0, theSolitaryBalloonTip.__showArrow)
    
    @staticmethod
    def isBalloonVisible():
        global theSolitaryBalloonTip
        return theSolitaryBalloonTip != None and shiboken2.isValid(theSolitaryBalloonTip)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(self.rect(), self.__pixmap)
    
    def resizeEvent(self, ev):
        super(BalloonTip, self).resizeEvent(ev)
    
    def __balloon(self, pos, msecs, showArrow):
        self.__showArrow = showArrow
        scr = QApplication.instance().primaryScreen().availableGeometry()
        sh = self.sizeHint()
        border = 1
        ah = 18
        ao = 18
        aw = 18
        rc = 0
        arrowAtTop = (pos.y() + sh.height() + ah < scr.height())
        arrowAtLeft = (pos.x() + sh.width() - ao < scr.width())
        self.setContentsMargins(border + 3,  border + (ah if arrowAtTop else 0) + 2, 
            border + 3, border + (0 if arrowAtTop else ah) + 2)
        self.updateGeometry()
        sh = self.sizeHint()
        sz = self.sizeHint()
        if not arrowAtTop:
            ml = mt = 0
            mr = sz.width() - 1
            mb = sz.height() - ah - 1
        else:
            ml = 0
            mt = ah
            mr = sz.width() - 1
            mb = sz.height() - 1
        path = QPainterPath()
        path.moveTo(ml + rc, mt)
        if arrowAtTop and arrowAtLeft:
            if showArrow:
                path.lineTo(ml + ao, mt)
                path.lineTo(ml + ao, mt - ah)
                path.lineTo(ml + ao + aw, mt)
            
            self.move(max(pos.x() - ao, scr.left() + 2), pos.y())
        elif arrowAtTop and (not arrowAtLeft):
            if showArrow:
                path.lineTo(mr - ao - aw, mt)
                path.lineTo(mr - ao, mt - ah)
                path.lineTo(mr - ao, mt)
            
            self.move(min(pos.x() - sh.width() + ao, scr.right() - sh.width() - 2), pos.y())
        
        path.lineTo(mr - rc, mt)
        path.arcTo(QRect(mr - rc*2, mt, rc*2, rc*2), 90, -90)
        path.lineTo(mr, mb - rc)
        path.arcTo(QRect(mr - rc*2, mb - rc*2, rc*2, rc*2), 0, -90)
        if not arrowAtTop and not arrowAtLeft:
            if showArrow:
                path.lineTo(mr - ao, mb)
                path.lineTo(mr - ao, mb + ah)
                path.lineTo(mr - ao - aw, mb)
            
            self.move(min(pos.x() - sh.width() + ao, scr.right() - sh.width() - 2),
                pos.y() - sh.height())
        elif not arrowAtTop and arrowAtLeft:
            if showArrow:
                path.lineTo(ao + aw, mb)
                path.lineTo(ao, mb + ah)
                path.lineTo(ao, mb)
            
            self.move(max(pos.x() - ao, scr.x() + 2), pos.y() - sh.height())
        
        path.lineTo(ml + rc, mb)
        path.arcTo(QRect(ml, mb - rc*2, rc*2, rc*2), -90, -90)
        path.lineTo(ml, mt + rc)
        path.arcTo(QRect(ml, mt, rc*2, rc*2), 180, -90)
        # Set the mask
        bitmap = QBitmap(self.sizeHint())
        bitmap.fill(Qt.color0)
        painter1 = QPainter(bitmap)
        painter1.setPen(QPen(Qt.color1, border))
        painter1.setBrush(QBrush(Qt.color1))
        painter1.drawPath(path)
        painter1.end()
        self.setMask(bitmap)
        # Draw the border
        self.__pixmap = QPixmap(sz)
        painter2 = QPainter(self.__pixmap)
        painter2.setPen(QPen(self.palette().color(QPalette.Window).darker(160), border))
        painter2.setBrush(self.palette().color(QPalette.Window))
        painter2.drawPath(path)
        painter2.end()
        if msecs > 0:
            self.__timerId = self.startTimer(msecs)
        self.show()
    
    def mousePressEvent(self, e):
        self.close()
    
    def timerEvent(self, e):
        if e.timerId() == self.__timerId:
            self.killTimer(self.__timerId)
            if not self.underMouse():
                self.close()
            return
        
        super(BalloonTip, self).timerEvent(e)

