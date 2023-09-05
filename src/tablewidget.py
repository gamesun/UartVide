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

from functools import partial
import csv


class RowButton(QToolButton):
    def __init__(self, row: int, *args, **kwargs):
        super(RowButton, self).__init__(*args, **kwargs)

        # self.setText(name)
        self.setCursor(Qt.PointingHandCursor)
        self.func = partial(self.onQuickSend, row)
        self.clicked.connect(self.func)
        
        # btn1.rightClicked.connect(lambda : self.onQuickSendRightClick(row))
        
        self.quickSendTable.setCellWidget(row, 0, btn1)
    
    def setRow(self, row: int):
        self.clicked.disconnect(self.func)
        self.func = partial(self.onQuickSend, row)
        self.clicked.connect(self.func)

class QckSndRow():
    def __init__(self, row: int):
        self.name = ''
        self.format = ''
        self.data = ''
        self.send_btn = RowButton(row)
        self.send_func = None
        self.menu_btn = None
        self.menu_func = None
        self.data_edit = None
        self.frame = None
    



class TableWidget(QTableWidget):
    
    def __init__(self, *args, **kwargs):
        super(TableWidget, self).__init__(*args, **kwargs)
        self._rowList = [QckSndRow()] * 50
        self._qckSnd_RawData = []
        self._send_func = None
        self._menu_func = None

    def mouseMoveEvent(self, event):
        pass
        # super(TableWidget, self).mouseMoveEvent(event)

    def setSendFunc(self, send_func: function):
        self._send_func = send_func

    def setMenuFunc(self, menu_func: function):
        self._menu_func = menu_func

    def setRowCount(self, rows: int):
        super(TableWidget, self).setRowCount(rows)
        if len(self._rowList) < rows:
            self._rowList = self._rowList + [QckSndRow()] * (rows - len(self._rowList))
        elif rows < len(self._rowList):
            del self._rowList[rows:]

    def setRow(self, row: int, name: str, format: str='H', data: str='', 
               name_clicked_func: function=None, format_clicked_func: function = None):
        self._rowList[row].name = name
        self._rowList[row].format = format
        self._rowList[row].data = data
        self._rowList[row].send_btn = 
        self._rowList[row].send_func = partial(self._send_func, row)
        self._rowList[row].menu_btn = 
        self._rowList[row].menu_func = partial(self._menu_func, row)


    def loadFromCSV(self, fileName: str):
        with open(fileName) as csvfile:
            csvData = csv.reader(csvfile)
            self.setRowCount(len(csvData))
            self._qckSnd_RawData = []
            for row in csvData:
                if len(row) < 3:
                    row = row + [''] * (3 - len(row))
                if 3 < len(row):
                    row = row[:3]
                self._qckSnd_RawData.append(row)

    def saveToCSV(self, fileName: str):
        rows = self.rowCount()

        save_data = [[self.cellWidget(row, 0).text(),
                      self.cellWidget(row, 1).text(),
                      self._qckSnd_EdtLst[row].text()] for row in range(rows)]

        #import pprint
        #pprint.pprint(save_data, width=120, compact=True)

        with open(fileName, 'w') as csvfile:
            csvwriter = csv.writer(csvfile, delimiter=',', lineterminator='\n')
            csvwriter.writerows(save_data)
