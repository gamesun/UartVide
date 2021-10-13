#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
#
#############################################################################
##
## Copyright (c) 2013-2021, gamesun
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
from balloontip import BalloonTip

class ParseTableVerticalHeader(QHeaderView):
    def __init__(self, parent = None):
        super(ParseTableVerticalHeader, self).__init__(Qt.Vertical, parent)
        self.chkboxlist = [None]

    def paintSection(self, painter, rect, logicalIndex):
        super(ParseTableVerticalHeader, self).paintSection(painter, rect, logicalIndex)
        # print('paintSection', logicalIndex)
        
        if len(self.chkboxlist) < logicalIndex + 1:
            self.chkboxlist.extend([None]*(logicalIndex + 1 - len(self.chkboxlist)))
        if self.chkboxlist[logicalIndex] == None:
            self.chkboxlist[logicalIndex] = QCheckBox(self)
        
        self.fixPos(logicalIndex)
        if self.chkboxlist[logicalIndex].isHidden():
            self.chkboxlist[logicalIndex].show()

    # def showEvent(self, evt):
    #     super(ParseTableVerticalHeader, self).showEvent(evt)

    def fixPos(self, logicalIndex):
        self.chkboxlist[logicalIndex].setGeometry(0, self.sectionViewportPosition(logicalIndex), self.width(), self.sectionSize(logicalIndex))


class ParseTableHorizontalHeader(QHeaderView):
    def __init__(self, parent = None):
        super(ParseTableHorizontalHeader, self).__init__(Qt.Horizontal, parent)

        self.label = QLabel('Unpack Format <a href="unpack_format">(?)</a>', self)
        self.label.linkActivated.connect(self.onHeaderClicked)
        self.label.setStyleSheet('background-color: transparent; color: #202020;')
        self.label.setAlignment(Qt.AlignCenter)

    def paintSection(self, painter, rect, logicalIndex):
        super(ParseTableHorizontalHeader, self).paintSection(painter, rect, logicalIndex)
        if logicalIndex == 2:
            self.fixPos()

    def showEvent(self, evt):
        self.fixPos()
        self.label.show()
        super(ParseTableHorizontalHeader, self).showEvent(evt)

    # def scrollContentsBy(self, dx, dy):
    #     super(ParseTableHorizontalHeader, self).scrollContentsBy(dx, dy)
    #     if dx:
    #         self.fixPos()

    def fixPos(self):
        self.label.setGeometry(self.sectionViewportPosition(2)+5, 1, self.sectionSize(2) - 10, self.height() - 2)

    def onHeaderClicked(self, href):
        if href == 'unpack_format':
            BalloonTip.showBalloon(None, None, UNPACK_FORMAT_REF, self.cursor().pos(), 10000, False)

    def sectionSizeFromContents(self, logicalIndex):
        size = super(ParseTableHorizontalHeader, self).sectionSizeFromContents(logicalIndex)
        if logicalIndex == 2:
            metric = QFontMetrics(self.label.font())
            textSize = metric.width('Unpack Format (?)')
            minimunSize = textSize + 4
            if size.width() < minimunSize:
                size.setWidth(minimunSize)
        return size


UNPACK_FORMAT_REF = '''
<html><head><style type="text/css">
    table.full-width-table {width: 100%;}
    table       {line-height:10px;}
    th          {background: #dddddd; font-weight: normal;font-size:80%;}
    td          {background: #ffffff;font-size:80%;}
    body        {font-size:80%;}
</style></head>
<body><h4>Byte Order, Size, and Alignment</h4>
<table border="0" cellspacing="1" cellpadding='3' bgcolor="#c0c0c0">
<colgroup>
<col style="width: 20%" /><col style="width: 43%" /><col style="width: 18%" /><col style="width: 20%" />
</colgroup>
<thead>
<tr><th><p>Character</p></th><th><p>Byte order</p></th><th><p>Size</p></th><th><p>Alignment</p></th></tr>
</thead>
<tbody>
<!--
<tr><td align="center"><p><code>&#64;</code></p></td><td><p>native</p></td><td><p>native</p></td><td><p>native</p></td></tr>
<tr><td align="center"><p><code>=</code></p></td><td><p>native</p></td><td><p>standard</p></td><td><p>none</p></td></tr>
-->
<tr><td align="center"><p><code>&lt;</code></p></td><td><p>little-endian</p></td><td><p>standard</p></td><td><p>none</p></td></tr>
<tr><td align="center"><p><code>&gt;</code></p></td><td><p>big-endian</p></td><td><p>standard</p></td><td><p>none</p></td></tr>
<!--
<tr><td align="center"><p><code>!</code></p></td><td><p>network (= big-endian)</p></td><td><p>standard</p></td><td><p>none</p></td></tr>
-->
</tbody></table>
<h4>Format Characters</h4>
<table border="0" cellspacing="1" cellpadding='3' bgcolor="#c0c0c0">
<colgroup>
<col style="width: 11%" /><col style="width: 30%" /><col style="width: 9%" />
<col style="width: 11%" /><col style="width: 30%" /><col style="width: 9%" />
</colgroup>
<thead>
<tr><th><p>Format</p></th><th><p>C Type</p></th><th><p>Size</p></th><th><p>Format</p></th><th><p>C Type</p></th><th><p>Size</p></th></tr>
</thead>
<tbody>
<tr><td align="center"><p><code>x</code></p></td><td><p><code>pad byte</code></p></td><td align="center"></td>
<td align="center"><p><code>q</code></p></td><td><p><code>long long</code></p></td><td align="center"><p>8</p></td>
</tr>
<tr><td align="center"><p><code>c</code></p></td><td><p><code>char</code></p></td><td align="center"><p>1</p></td>
<td align="center"><p><code>Q</code></p></td><td><p><code>unsigned long long</code></p></td><td align="center"><p>8</p></td>
</tr>
<tr><td align="center"><p><code>b</code></p></td><td><p><code>signed char</code></p></td><td align="center"><p>1</p></td>
<td align="center"><p><code>n</code></p></td><td><p><code>ssize_t</code></p></td><td align="center"></td>
</tr>
<tr><td align="center"><p><code>B</code></p></td><td><p><code>unsigned char</code></p></td><td align="center"><p>1</p></td>
<td align="center"><p><code>N</code></p></td><td><p><code>size_t</code></p></td><td align="center"></td>
</tr>
<tr><td align="center"><p><code>?</code></p></td><td><p><code>_Bool</code></p></td><td align="center"><p>1</p></td>
<td align="center"><p><code>e</code></p></td><td><p><code>half precision</code></p></td><td align="center"><p>2</p></td>
</tr>
<tr><td align="center"><p><code>h</code></p></td><td><p><code>short</code></p></td><td align="center"><p>2</p></td>
<td align="center"><p><code>f</code></p></td><td><p><code>float</code></p></td><td align="center"><p>4</p></td>
</tr>
<tr><td align="center"><p><code>H</code></p></td><td><p><code>unsigned short</code></p></td><td align="center"><p>2</p></td>
<td align="center"><p><code>d</code></p></td><td><p><code>double</code></p></td><td align="center"><p>8</p></td>
</tr>
<tr><td align="center"><p><code>i</code></p></td><td><p><code>int</code></p></td><td align="center"><p>4</p></td>
<td align="center"><p><code>s</code></p></td><td><p><code>char[]</code></p></td><td align="center"></td>
</tr>
<tr><td align="center"><p><code>I</code></p></td><td><p><code>unsigned int</code></p></td><td align="center"><p>4</p></td>
<td align="center"><p><code>p</code></p></td><td><p><code>char[]</code></p></td><td align="center"></td>
</tr>
<tr><td align="center"><p><code>l</code></p></td><td><p><code>long</code></p></td><td align="center"><p>4</p></td>
<td align="center"><p><code>P</code></p></td><td><p><code>void *</code></p></td><td align="center"></td>
</tr>
<tr><td align="center"><p><code>L</code></p></td><td><p><code>unsigned long</code></p></td><td align="center"><p>4</p></td>
<td/><td/><td/>
</tr></tbody></table>
<h4>Examples</h4>
<p><code>Data:00 01 00 02 00 00 00 03  Format:hhl<br/>Output:1, 2, 3</code></p>
</body>
</html>
'''
