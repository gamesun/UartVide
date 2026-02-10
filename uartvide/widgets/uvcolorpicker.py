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

from vcolorpicker import ColorPicker, hsv2rgb, hsv2hex
from qtpy import QtCore, QtWidgets
from qtpy.QtCore import QPoint, Qt


class UVColorPicker(ColorPicker):
    def __init__(self, lightTheme: bool = False, useAlpha: bool = False):
        super(UVColorPicker, self).__init__(lightTheme, useAlpha)
        self.ui.drop_shadow_frame.setStyleSheet("QFrame{background-color: #fff}")
        self.ui.drop_shadow_frame.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.ui.drop_shadow_frame.setFrameShadow(QtWidgets.QFrame.Plain)
        self.ui.verticalLayout_3.setSpacing(4)

        self.ui.title_bar.setStyleSheet("background-color: #99d9ea;")
        self.ui.title_bar.setMinimumSize(QtCore.QSize(0, 30))
        self.ui.content_bar.setStyleSheet("background-color: #fff")
        self.ui.black_overlay.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(0, 0, 0, 0), stop:1 rgba(0, 0, 0, 255));")
        self.ui.black_overlay.setMinimumSize(QtCore.QSize(200, 200))
        self.ui.black_overlay.setMaximumSize(QtCore.QSize(200, 200))
        self.ui.hue_selector.setStyleSheet("background-color: none;border: 2px solid black")
        self.ui.hue_bg.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:1, x2:0, y2:0, stop:0 rgba(255, 0, 0, 255), stop:0.166 rgba(255, 255, 0, 255), stop:0.333 rgba(0, 255, 0, 255), stop:0.5 rgba(0, 255, 255, 255), stop:0.666 rgba(0, 0, 255, 255), stop:0.833 rgba(255, 0, 255, 255), stop:1 rgba(255, 0, 0, 255));")
        self.ui.button_bar.setStyleSheet("QFrame{background-color: #fff}")

        self.ui.horizontalLayout.setContentsMargins(10, 6, 0, 2)
        self.ui.horizontalLayout.setSpacing(0)

        self.ui.hue_bg.setGeometry(QtCore.QRect(18, 0, 20, 200))
        self.ui.hue_selector.setGeometry(QtCore.QRect(15, 185, 26, 15))
        self.ui.hue.setGeometry(QtCore.QRect(15, 0, 26, 200))

        self.ui.horizontalLayout_3.setContentsMargins(100, 0, 100, 4)

    def hsvChanged(self):
        h,s,v = (100 - self.ui.hue_selector.y() / 1.85, (self.ui.selector.x() + 6) / 2.0, (194 - self.ui.selector.y()) / 2.0)
        r,g,b = hsv2rgb(h,s,v)
        self.color = (h,s,v)
        self.setRGB((r,g,b))
        self.setHex(hsv2hex(self.color))
        self.ui.color_vis.setStyleSheet(f"background-color: rgb({r},{g},{b})")
        self.ui.color_view.setStyleSheet(f"background-color: qlineargradient(x1:1, x2:0, stop:0 hsl({h}%,100%,50%), stop:1 #fff);")

    def setHSV(self, c):
        self.ui.hue_selector.move(15, int((100 - c[0]) * 1.85))
        self.ui.color_view.setStyleSheet(f"background-color: qlineargradient(x1:1, x2:0, stop:0 hsl({c[0]}%,100%,50%), stop:1 #fff);")
        self.ui.selector.move(int(c[1] * 2 - 6), int((200 - c[2] * 2) - 6))

    def moveHueSelector(self, event):
        if event.buttons() == Qt.LeftButton:
            pos = event.pos().y() - 7
            if pos < 0: pos = 0
            if pos > 185: pos = 185
            self.ui.hue_selector.move(QPoint(15, pos))
            self.hsvChanged()

if __name__ == '__main__':
    cp = UVColorPicker(True, False)
    cp.getColor((39, 183, 152))