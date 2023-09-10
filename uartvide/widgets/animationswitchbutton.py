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


buttonStyle_Rect = 0
buttonStyle_CircleIn = 1
buttonStyle_CircleOut = 2
        
class AnimationSwitchButton(QtWidgets.QToolButton):
    stateChanged = Signal(bool)
    
    def __init__(self, parent = None):
        super(AnimationSwitchButton, self).__init__(parent)
        
        self.space = 2
        self.rectRadius = 12
        self.checked = False
        self.showText = False
        self.showCircle = False
        self.buttonStyle = buttonStyle_CircleIn

        self.bgColorOff = QColor('#6F7A7E')
        self.bgColorOn = QColor('#0072BB') #QColor('#22A3A9')
        self.sliderColorOff = QColor('#FEFEFE')
        self.sliderColorOn = QColor('#FEFEFE') #QColor('#22A3A9') 
        self.textColorOff = QColor('#f0f')
        self.textColorOn = QColor('#ff0')

        self.textOff = 'off'
        self.textOn = 'on'

        self.sliderX = None
        
        self.slider_animation = QVariantAnimation(self)
        self.slider_animation.setDuration(90)
        #self.slider_animation.setEasingCurve()
        self.slider_animation.valueChanged.connect(self.onSliderAnimationValueChanged)
        #self.slider_animation.stateChanged.connect(self.onSliderAnimationStateChanged)

    def setChecked(self, a0:bool):
        self.checked = a0
        if QVariantAnimation.Running == self.slider_animation.state():
            self.slider_animation.stop()
        self.slider_animation.setEndValue(0 if self.checked else (self.width() - self.height()))
        self.slider_animation.start()

    #def onSliderAnimationStateChanged(self, a, b):
    #    print('currentValue', self.slider_animation.currentValue())

    def onSliderAnimationValueChanged(self, value):
        if value != None:
            self.sliderX = value
            self.update()
    
    def mousePressEvent(self, mouseEvent):
        if mouseEvent.button() == Qt.LeftButton:
            self.checked = not self.checked
            self.slider_animation.setStartValue(self.sliderX)
            self.slider_animation.setEndValue(0 if self.checked else (self.width() - self.height()))
            self.slider_animation.start()
            self.stateChanged.emit(self.checked)
        mouseEvent.accept()

    def paintEvent(self, paintEvent):
        if None == self.sliderX:
            self.sliderX = 0 if self.checked else (self.width() - self.height())
        
        painter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing | QPainter.TextAntialiasing)

        self.drawBg(painter)
        self.drawSlider(painter)

    def drawBg(self, painter):
        painter.save()
        painter.setPen(Qt.NoPen)

        bgColor = self.checked and self.bgColorOn or self.bgColorOff
        if not self.isEnabled():
            bgColor.setAlpha(60)

        painter.setBrush(bgColor)

        if self.buttonStyle == buttonStyle_Rect:
            painter.drawRoundedRect(self.rect(), self.rectRadius, self.rectRadius)
        elif self.buttonStyle == buttonStyle_CircleIn:
            rect = QRect(0, 0, self.width(), self.height())
            side = min(rect.width(), rect.height())

            path1 = QPainterPath()
            path1.addEllipse(rect.x(), rect.y(), side, side)
            path2 = QPainterPath()
            path2.addEllipse(rect.width() - side, rect.y(), side, side)
            path3 = QPainterPath()
            path3.addRect(rect.x() + side // 2, rect.y(), rect.width() - side, rect.height())

            path = QPainterPath()
            path = path3 + path1 + path2
            painter.drawPath(path)
        elif self.buttonStyle == buttonStyle_CircleOut:
            rect = QRect(self.height() // 2, self.space, self.width() - self.height(), self.height() - self.space * 2)
            painter.drawRoundedRect(rect, self.rectRadius, self.rectRadius)

        if self.buttonStyle == buttonStyle_Rect or self.buttonStyle == buttonStyle_CircleIn:
            if self.showText:
                sliderWidth = min(self.width(), self.height()) - self.space * 2
                if self.buttonStyle == buttonStyle_Rect:
                    sliderWidth = self.width() // 2 - 5
                elif self.buttonStyle == buttonStyle_CircleIn:
                    sliderWidth -= 5

                if self.checked:
                    textRect = QRect(0, 0, self.width() - sliderWidth, self.height())
                    painter.setPen(self.textColorOn)
                    painter.drawText(textRect, Qt.AlignCenter, self.textOn)
                else:
                    textRect = QRect(sliderWidth, 0, self.width() - sliderWidth, self.height())
                    painter.setPen(self.textColorOff)
                    painter.drawText(textRect, Qt.AlignCenter, self.textOff)
            elif self.showCircle:
                side = min(self.width(), self.height()) // 2
                y = (self.height() - side) // 2

                if self.checked:
                    circleRect = QRect(side // 2, y, side, side)
                    pen = QPen(self.textColorOn, 2)
                    painter.setPen(pen)
                    painter.setBrush(Qt.NoBrush)
                    painter.drawEllipse(circleRect)
                else:
                    circleRect = QRect(int(self.width() - (side * 1.5)), y, side, side)
                    pen = QPen(self.textColorOff, 2)
                    painter.setPen(pen)
                    painter.setBrush(Qt.NoBrush)
                    painter.drawEllipse(circleRect)

        painter.restore()

    def drawSlider(self, painter):
        painter.save()
        painter.setPen(Qt.NoPen)

        if not self.checked:
            painter.setBrush(self.sliderColorOff)
        else:
            painter.setBrush(self.sliderColorOn)

        if self.buttonStyle == buttonStyle_Rect:
            sliderWidth = self.width() // 2 - self.space * 2
            sliderHeight = self.height() - self.space * 2
            sliderRect = QRect(self.sliderX + self.space, self.space, sliderWidth , sliderHeight)
            painter.drawRoundedRect(sliderRect, self.rectRadius, self.rectRadius)
        elif self.buttonStyle == buttonStyle_CircleIn:
            rect = QRect(0, 0, self.width(), self.height())
            sliderWidth = min(rect.width(), rect.height()) - self.space * 2
            sliderRect = QRect(self.sliderX + self.space, self.space, sliderWidth, sliderWidth)
            painter.drawEllipse(sliderRect)
        elif self.buttonStyle == buttonStyle_CircleOut:
            sliderWidth = self.height()
            sliderRect = QRect(self.sliderX, 0, sliderWidth, sliderWidth)

            color1 = self.checked and Qt.white or self.bgColorOff
            color2 = self.checked and self.sliderColorOn or self.sliderColorOff

            radialGradient = QRadialGradient(sliderRect.center(), sliderWidth // 2)
            radialGradient.setColorAt(0, self.checked and color1 or color2)
            radialGradient.setColorAt(0.5, self.checked and color1 or color2)
            radialGradient.setColorAt(0.6, self.checked and color2 or color1)
            radialGradient.setColorAt(1.0, self.checked and color2 or color1)
            painter.setBrush(radialGradient)

            painter.drawEllipse(sliderRect)

        painter.restore()
