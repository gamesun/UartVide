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

from elidedlineedit import ElidedLineEdit
from functools import partial
import csv


class IndexButton(QToolButton):
    ibClicked = Signal(int)

    def __init__(self, row: int, *args, **kwargs):
        super(IndexButton, self).__init__(*args, **kwargs)
        super(IndexButton, self).clicked.connect(self.onClicked)
        self._row = row

    def setRow(self, row: int):
        self._row = row

    def onClicked(self):
        print('IndexButton:onClicked')
        self.ibClicked.emit(self._row)

class QckSndRow():
    def __init__(self, row: int):
        self.has_setup = False
        self.row = row
        self.name = ''
        self.format = ''
        self.data = ''
        
        self.send_btn = IndexButton(row)
        self.menu_btn = IndexButton(row)
        
        self.data_edit = ElidedLineEdit()
        self.path_btn = IndexButton(row)
        self.path_btn.setFixedSize(QSize(17, 17))
        hLayout = QHBoxLayout()
        hLayout.addWidget(self.data_edit)
        hLayout.addWidget(self.path_btn)
        hLayout.setSpacing(0)
        hLayout.setContentsMargins(0, 0, 1, 0)
        self.frame = QFrame()
        self.frame.setLayout(hLayout)


class TableWidget(QTableWidget):
    
    def __init__(self, *args, **kwargs):
        super(TableWidget, self).__init__(*args, **kwargs)
        self._rowList = []
        self._qckSnd_RawData = []
        self._send_func = None
        self._menu_func = None
        self._path_func = None

    def mouseMoveEvent(self, event):
        pass
        # super(TableWidget, self).mouseMoveEvent(event)

    def setSendFunc(self, send_func: callable):
        self._send_func = send_func

    def setMenuFunc(self, menu_func: callable):
        self._menu_func = menu_func

    def setPathFunc(self, path_func):
        self._path_func = path_func

    def setRowCount(self, rows: int):
        super(TableWidget, self).setRowCount(rows)
        print('setRowCount', rows)
        if len(self._rowList) < rows:
            for i in range(len(self._rowList), rows):
                self._rowList.append(QckSndRow(i))
                self.initRow(i, name='%d' % i)
        elif rows < len(self._rowList):
            del self._rowList[rows:]

    def initRow(self, row: int, name: str='', format: str='H', data: str=''):
        print('initRow', row)
        if not self._rowList[row].has_setup:
            self._rowList[row].row = row
            self._rowList[row].name = name
            self._rowList[row].format = format
            self._rowList[row].data = data
            self._rowList[row].send_btn.setText(name)
            self._rowList[row].menu_btn.setText(format)
            self._rowList[row].data_edit.setText(data)
            self._rowList[row].send_btn.ibClicked.connect(self._send_func)
            self._rowList[row].menu_btn.ibClicked.connect(self._menu_func)
            self._rowList[row].path_btn.ibClicked.connect(self._path_func)

            self.setCellWidget(row, 0, self._rowList[row].send_btn)
            self.setCellWidget(row, 1, self._rowList[row].menu_btn)
            self.setCellWidget(row, 2, self._rowList[row].frame)

            self._rowList[row].has_setup = True
        else:
            old_row = self._rowList[row].row
            self._rowList[row].row = row
            self._rowList[row].name = name
            self._rowList[row].format = format
            self._rowList[row].data = data
            self._rowList[row].send_btn.setText(name)
            self._rowList[row].send_btn.setRow(row)
            self._rowList[row].menu_btn.setText(format)
            self._rowList[row].menu_btn.setRow(row)
            self._rowList[row].data_edit.setText(data)
            self._rowList[row].data_edit.setRow(row)

            self.setCellWidget(row, 0, self._rowList[row].send_btn)
            self.setCellWidget(row, 1, self._rowList[row].menu_btn)
            self.setCellWidget(row, 2, self._rowList[row].frame)


    def loadFromCSV(self, fileName: str):
        with open(fileName) as csvfile:
            csvData = csv.reader(csvfile)
            if csvData:
                self._qckSnd_RawData = []
                for row in csvData:
                    if len(row) < 3:
                        row = row + [''] * (3 - len(row))
                    if 3 < len(row):
                        row = row[:3]
                    self._qckSnd_RawData.append(row)
                self.setRowCount(len(self._qckSnd_RawData))

    def saveToCSV(self, fileName: str):
        rows = self.rowCount()

        save_data = [[self._rowList[row].name,
                      self._rowList[row].format,
                      self._rowList[row].data] for row in range(rows)]

        #import pprint
        #pprint.pprint(save_data, width=120, compact=True)

        with open(fileName, 'w') as csvfile:
            csvwriter = csv.writer(csvfile, delimiter=',', lineterminator='\n')
            csvwriter.writerows(save_data)
