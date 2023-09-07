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
import csv


class IndexButton(QToolButton):
    clicked = Signal(int)

    def __init__(self, row: int, text: str='', parent=None):
        super(IndexButton, self).__init__(parent)
        super(IndexButton, self).clicked.connect(self.onClicked)
        self._row = row
        self.setText(text)

    def setRow(self, row: int):
        self._row = row

    def onClicked(self):
        self.clicked.emit(self._row)


class QckSndRow():
    def __init__(self, row: int,  name='', fmt='', data='', parent=None):
        self.has_setup = False
        self.send_btn = IndexButton(row, name, parent)
        self.menu_btn = IndexButton(row, fmt, parent)
        self.data_edt = ElidedLineEdit(data, parent)
        self.path_btn = IndexButton(row, '...', parent)
        self.path_btn.setFixedSize(QSize(17, 17))
        hLayout = QHBoxLayout()
        hLayout.addWidget(self.data_edt)
        hLayout.addWidget(self.path_btn)
        hLayout.setSpacing(0)
        hLayout.setContentsMargins(0, 0, 1, 0)
        self.frame = QFrame(parent)
        self.frame.setLayout(hLayout)


class QuickSendTable(QTableWidget):
    
    def __init__(self, parent=None):
        super(QuickSendTable, self).__init__(parent)
        self._rowList: list[QckSndRow] = []
        self._qckSnd_RawData = []
        self._send_func = None
        self._menu_func = None
        self._path_func = None

    def text(self, row, column):
        if column == 0:
            return self._rowList[row].send_btn.text()
        elif column == 1:
            return self._rowList[row].menu_btn.text()
        elif column == 2:
            return self._rowList[row].data_edt.text()

    def setText(self, row, column, text):
        if column == 0:
            self._rowList[row].send_btn.setText(text)
        elif column == 1:
            self._rowList[row].menu_btn.setText(text)
            if 'F' in text:
                self._rowList[row].path_btn.show()
            else:
                self._rowList[row].path_btn.hide()
        elif column == 2:
            self._rowList[row].data_edt.setText(text)

    def mouseMoveEvent(self, event):
        pass
        # super(TableWidget, self).mouseMoveEvent(event)

    def setSendFunc(self, send_func: callable):
        self._send_func = send_func
        for r in self._rowList:
            r.send_btn.clicked.connect(self._send_func)

    def setMenuFunc(self, menu_func: callable):
        self._menu_func = menu_func
        for r in self._rowList:
            r.menu_btn.clicked.connect(self._menu_func)

    def setPathFunc(self, path_func):
        self._path_func = path_func
        for r in self._rowList:
            r.path_btn.clicked.connect(self._path_func)

    def setPathButtonHidden(self, row, hidden: bool):
        if hidden:
            self._rowList[row].path_btn.hide()
        else:
            self._rowList[row].path_btn.show()

    def setRowCount(self, rows: int):
        super(QuickSendTable, self).setRowCount(rows)
        
        if len(self._rowList) < rows:
            for i in range(len(self._rowList), rows):
                self._rowList.append(QckSndRow(i, parent=self))
                self.setRow(i, ['%d' % i, 'H', ''])
        elif rows < len(self._rowList):
            del self._rowList[rows:]

    def refreshWidgets(self, row):
        self.removeCellWidget(row, 0)
        self.removeCellWidget(row, 1)
        self.removeCellWidget(row, 2)
        self.setCellWidget(row, 0, self._rowList[row].send_btn)
        self.setCellWidget(row, 1, self._rowList[row].menu_btn)
        self.setCellWidget(row, 2, self._rowList[row].frame)

    def setRow(self, row: int, text_lst: list[str]):
        if len(text_lst) < 3:
            text_lst = text_lst + [''] * (3 - len(text_lst))
        name = text_lst[0]
        fmt = text_lst[1]
        data = text_lst[2]

        if len(self._rowList) <= row:
            self._rowList.append(QckSndRow(row, name, fmt, data, parent=self))
            super(QuickSendTable, self).setRowCount(len(self._rowList))

        if not self._rowList[row].has_setup:
            self._rowList[row].row = row
            # self._rowList[row].name = name
            # self._rowList[row].format = fmt
            self._rowList[row].send_btn.setText(name)
            self._rowList[row].menu_btn.setText(fmt)
            self._rowList[row].data_edt.setText(data)
            self._rowList[row].send_btn.clicked.connect(self._send_func)
            self._rowList[row].menu_btn.clicked.connect(self._menu_func)
            self._rowList[row].path_btn.clicked.connect(self._path_func)

            self.setCellWidget(row, 0, self._rowList[row].send_btn)
            self.setCellWidget(row, 1, self._rowList[row].menu_btn)
            self.setCellWidget(row, 2, self._rowList[row].frame)
            
            if 'F' in fmt:
                self._rowList[row].path_btn.show()
            else:
                self._rowList[row].path_btn.hide()

            self.setRowHeight(row, 20)

            self._rowList[row].has_setup = True
    
    def refreshButtonIndex(self, row):
            self._rowList[row].send_btn.setRow(row)
            self._rowList[row].menu_btn.setRow(row)
            self._rowList[row].path_btn.setRow(row)

    def insertRow(self, row):
        super(QuickSendTable, self).insertRow(row)
        self._rowList.insert(row, QckSndRow(row, parent=self))
        self.setRow(row, ['new', 'H', ''])
        rowCnt = len(self._rowList)
        super(QuickSendTable, self).setRowCount(rowCnt)
        for i in range(row, rowCnt):
            self.refreshButtonIndex(i)

    def removeRow(self, row):
        super(QuickSendTable, self).removeRow(row)
        del self._rowList[row]
        rowCnt = len(self._rowList)
        super(QuickSendTable, self).setRowCount(rowCnt)
        for i in range(row, rowCnt):
            self.refreshButtonIndex(i)

    def loadFromCSV(self, fileName: str):
        with open(fileName) as csvfile:
            csvData = csv.reader(csvfile)
            if csvData:
                for i, one_line in enumerate(csvData):
                    if len(one_line) < 3:
                        one_line = one_line + [''] * (3 - len(one_line))
                    if 3 < len(one_line):
                        one_line = one_line[:3]
                    self.setRow(i, text_lst=one_line)

    def saveToCSV(self, fileName: str):
        rows = self.rowCount()

        save_data = [[self._rowList[row].send_btn.text(), self._rowList[row].menu_btn.text(),
                        self._rowList[row].data_edt.text()] for row in range(rows)]

        #import pprint
        #pprint.pprint(save_data, width=120, compact=True)

        with open(fileName, 'w') as csvfile:
            csvwriter = csv.writer(csvfile, delimiter=',', lineterminator='\n')
            csvwriter.writerows(save_data)
