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
import PySide2.QtCore
from PySide2.QtGui import *
import PySide2.QtGui
from PySide2.QtWidgets import *
from qfluentwidgets import *

from .elidedlineedit import ElidedLineEdit
from .rename_dailog import RenameDailog
from .rightanglecombobox import RightAngleComboBox
import csv
from functools import partial



class IndexClickEvent():
    
    def __init__(self, pos: QPoint, index: int) -> None:
        self._pos = pos
        self._index = index
    
    def pos(self):
        return self._pos
    
    def index(self):
        return self._index

class IndexButton(ToolButton):
    clicked = Signal(IndexClickEvent)
    rightClicked = Signal(IndexClickEvent)

    def __init__(self, parent=None, index: int=0, text: str=''):
        super(IndexButton, self).__init__(parent)
        self._index = index
        self.setText(text)
        # self.setMouseTracking(True)
        self.setStyleSheet('''
            QToolButton, QPushButton {
                background-color:#27b798;
                font-family:Tahoma;
                font-size:10pt;
            }
            QToolButton:hover, QPushButton:hover {
                background-color:#3bd5b4;
            }
            QToolButton:pressed, QPushButton:pressed {
                background-color:#1d8770;
                padding-top: 2px;
                padding-left: 2px;
            }
        ''')
       
    def setIndex(self, index: int):
        self._index = index

    def mousePressEvent(self, mouseEvent):
        print('press')
        if mouseEvent.button() == Qt.LeftButton:
            self.clicked.emit(IndexClickEvent(mouseEvent.globalPos(), self._index))
        if mouseEvent.button() == Qt.RightButton:
            self.rightClicked.emit(IndexClickEvent(mouseEvent.globalPos(), self._index))
        
        super().mousePressEvent(mouseEvent)

    def mouseReleaseEvent(self, arg__1: QMouseEvent) -> None:
        return super().mouseReleaseEvent(arg__1)
    
    def leaveEvent(self, arg__1: QEvent) -> None:
        me = QMouseEvent(QEvent.Type.MouseButtonRelease, QCursor.pos(), Qt.LeftButton, Qt.LeftButton, Qt.NoModifier)
        self.mouseReleaseEvent(me)
        return super().leaveEvent(arg__1)

class FormatComboBox(RightAngleComboBox):
    rightClicked = Signal(IndexClickEvent)
    dictFormat = {
        'HEX':'H', 
        'Ascii':'A', 
        'Ascii and \\n \\r \\t...':'AS', 
        'text file in HEX':'HF', 
        'text file in Ascii':'AF', 
        'Bin file; All file':'BF'
    }

    def __init__(self, parent=None, index: int=0, text: str=''):
        super().__init__(parent)
        self._index = index
        self.setStyleSheet('''
            ComboBox {
                padding: 2px 2px 3px 4px;
                color: white;
                background-color: #27b798;
                text-align: center;
            }
            ComboBox:hover { background-color: #3bd5b4; }
            ComboBox:pressed { background-color: #1d8770; }

            ComboBoxMenu>MenuActionListWidget {
                border: 1px solid rgba(0, 0, 0, 0.1);
                background-color: rgb(249, 249, 249);
                outline: none;
                font-size:10pt;
            }

            ComboBoxMenu>MenuActionListWidget::item {
                margin-top: 0px;
                padding-left: 0px;
                padding-right: 0px;
                border: none;
                color: black;
                font-size:10pt;
            }

            ComboBoxMenu>MenuActionListWidget::item:disabled {
                padding-left: 0px;
                padding-right: 0px;
                border: none;
                color: black;
            }

            ComboBoxMenu>MenuActionListWidget::item:hover {
                background-color: rgba(0, 0, 0, 9);
            }

            ComboBoxMenu>MenuActionListWidget::item:selected {
                background-color: rgba(0, 0, 0, 7);
                color: black;
            }

            ComboBoxMenu>MenuActionListWidget::item:selected:active {
                background-color: rgba(0, 0, 0, 0.06);
                color: rgba(0, 0, 0, 0.7);
            }
            
            LineEdit {
                color: black;
                font-size:10pt;
                background-color: rgba(255, 255, 255, 0.7);
                border: none;
                padding: 0px 0px 2px 0px;
            }
            LineEdit:hover { background-color: rgba(249, 249, 249, 0.5); }
            LineEdit:focus { background-color: white; }
            LineEdit:disabled { color: rgba(0, 0, 0, 150); background-color: rgba(249, 249, 249, 0.3); }
            #lineEditButton { background-color: transparent; margin: 0; }
            #lineEditButton:hover { background-color: rgba(0, 0, 0, 9); }
            #lineEditButton:pressed { background-color: rgba(0, 0, 0, 6); }
        ''')

        self.addItems(list(self.dictFormat.keys()))
        self.setMaximumWidth(30)
    
    def setIndex(self, index: int):
        self._index = index

    def setText(self, text):
        if text in self.dictFormat.keys():
            abbreviation = self.dictFormat[text]
            super().setText(abbreviation)
        else:
            idx = 0
            for i, (k, value) in enumerate(self.dictFormat.items()):
                    if value == text:
                        idx = i
            super().setCurrentIndex(idx)
            super().setText(text)

    def mousePressEvent(self, mouseEvent):
        if mouseEvent.button() == Qt.RightButton:
            self.rightClicked.emit(IndexClickEvent(mouseEvent.globalPos(), self._index))
        super().mousePressEvent(mouseEvent)

    def paintEvent(self, e):
        QPushButton.paintEvent(self, e)
        painter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing)
        if self.isHover:
            painter.setOpacity(0.8)
        elif self.isPressed:
            painter.setOpacity(0.7)

        # rect = QRectF(self.width()-16, self.height()/2-5+self.arrowAni.y, 10, 10)
        # FIF.ARROW_DOWN.render(painter, rect)

class QckSndRow():
    def __init__(self, row: int,  name='', fmt='', data='', parent=None):
        self.has_setup = False
        self.send_btn = IndexButton(parent, row, name)
        self.fmt_cmb = FormatComboBox(parent, row, fmt)
        self.data_edt = ElidedLineEdit(parent, data)
        self.path_btn = IndexButton(parent, row, '...')
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
        self.scrollDelegate = SmoothScrollDelegate(self)
        self._rowList: list[QckSndRow] = []
        self._qckSnd_RawData = []
        self._send_func = None
        self._menu_func = None
        self._path_func = None
        
        self.initMenu()

        self.setStyleSheet("""
            QToolButton, QPushButton {
                background-color:#27b798;
                font-family:Tahoma;
                font-size:10pt;
            }
            QToolButton:hover, QPushButton:hover {
                background-color:#3bd5b4;
            }
            QToolButton:pressed, QPushButton:pressed {
                /* background-color:#1d8770; */
                padding-top: 2px;
                padding-left: 2px;
            }
        """)

    def initMenu(self):
        self.actionRename = QtWidgets.QAction("Rename", self)
        self.actionRename.triggered.connect(self.onRename)

        self.actionInsertRow = QtWidgets.QAction("Insert row", self)
        self.actionInsertRow.triggered.connect(self.onInsertRow)

        self.actionDeleteRow = QtWidgets.QAction("Delete row", self)
        self.actionDeleteRow.triggered.connect(self.onRemoveRow)

        self.menuRightClick = RoundMenu(parent=self)
        self.menuRightClick.addAction(self.actionRename)
        self.menuRightClick.addAction(self.actionInsertRow)
        self.menuRightClick.addAction(self.actionDeleteRow)


        # self.actionSend_Hex = QtWidgets.QAction("HEX", self)
        # self.actionSend_Hex.triggered.connect(partial(self.onSelectFormat, 'H'))

        # self.actionSend_Asc = QtWidgets.QAction("ASCII", self)
        # self.actionSend_Asc.triggered.connect(partial(self.onSelectFormat, 'A'))

        # self.actionSend_AscS = QtWidgets.QAction(r"ASCII and \n \r \t...", self)
        # self.actionSend_AscS.triggered.connect(partial(self.onSelectFormat, 'AS'))
        
        # self.actionSend_HF = QtWidgets.QAction(self)
        # self.actionSend_HF.setText("HEX text File")
        # self.actionSend_HF.setStatusTip('Send text file in HEX form("31 32 FF ...")')
        # self.actionSend_HF.triggered.connect(partial(self.onSelectFormat, 'HF'))
        
        # self.actionSend_AF = QtWidgets.QAction(self)
        # self.actionSend_AF.setText("ASCII text file")
        # self.actionSend_AF.setStatusTip('Send text file in ASCII form("abc123...")')
        # self.actionSend_AF.triggered.connect(partial(self.onSelectFormat, 'AF'))
        
        # self.actionSend_BF = QtWidgets.QAction("Bin file; All file", self)
        # self.actionSend_BF.triggered.connect(partial(self.onSelectFormat, 'BF'))

        # self.menuFormat = RoundMenu(parent=self)
        # self.menuFormat.addAction(self.actionSend_Hex)
        # self.menuFormat.addAction(self.actionSend_Asc)
        # self.menuFormat.addAction(self.actionSend_AscS)
        # self.menuFormat.addAction(self.actionSend_HF)
        # self.menuFormat.addAction(self.actionSend_AF)
        # self.menuFormat.addAction(self.actionSend_BF)

    # def onSelectFormat(self, fmt):
    #     self.setText(self._selectingRow, 1, fmt)

    def onRename(self):
        item = self._rowList[self._selectingRow].send_btn
        oldname = item.text()
        pos = item.mapToGlobal(QPoint(30, 10))
        newname = RenameDailog.getNewName(oldname, pos)
        if newname:
            item.setText(newname)
            self.resizeColumnsToContents()

    def onInsertRow(self):
        self.insertRow(self._selectingRow)

    def onRemoveRow(self):
        self.removeRow(self._selectingRow)

    def text(self, row: int, column: int):
        if column == 0:
            return self._rowList[row].send_btn.text()
        elif column == 1:
            return self._rowList[row].fmt_cmb.text()
        elif column == 2:
            return self._rowList[row].data_edt.text()

    def setText(self, row, column, text):
        if column == 0:
            self._rowList[row].send_btn.setText(text)
        elif column == 1:
            self._rowList[row].fmt_cmb.setText(text)
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

    # def setMenuFunc(self, menu_func: callable):
    #     self._menu_func = menu_func
    #     for r in self._rowList:
    #         r.fmt_cmb.clicked.connect(self._menu_func)

    def onRightClicked(self, indexClickEvent):
        self._selectingRow = indexClickEvent.index()
        self.menuRightClick.popup(indexClickEvent.pos())

    # def onSelectFormat(self, indexClickEvent):
    #     self._selectingRow = indexClickEvent.index()
    #     self.menuFormat.popup(indexClickEvent.pos())

    def onSelectFile(self, indexClickEvent):
        old_path = self.text(indexClickEvent.index(), 2)
        fileName = QFileDialog.getOpenFileName(self, "Select a file",
            old_path, "All Files (*.*)")[0]
        if fileName:
            self.setText(indexClickEvent.index(), 2, fileName)

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
                self.setRowContent(i, ['%d' % i, 'H', ''])
        elif rows < len(self._rowList):
            del self._rowList[rows:]

    def refreshWidgets(self, row):
        self.removeCellWidget(row, 0)
        self.removeCellWidget(row, 1)
        self.removeCellWidget(row, 2)
        self.setCellWidget(row, 0, self._rowList[row].send_btn)
        self.setCellWidget(row, 1, self._rowList[row].fmt_cmb)
        self.setCellWidget(row, 2, self._rowList[row].frame)

    def setRowContent(self, row: int, text_lst):
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
            self._rowList[row].fmt_cmb.setText(fmt)
            self._rowList[row].data_edt.setText(data)
            self._rowList[row].send_btn.clicked.connect(self._send_func)
            self._rowList[row].send_btn.rightClicked.connect(self.onRightClicked)
            # self._rowList[row].fmt_cmb.changed.connect(self.onSelectFormat)
            self._rowList[row].fmt_cmb.rightClicked.connect(self.onRightClicked)
            self._rowList[row].path_btn.clicked.connect(self.onSelectFile)

            self.setCellWidget(row, 0, self._rowList[row].send_btn)
            self.setCellWidget(row, 1, self._rowList[row].fmt_cmb)
            self.setCellWidget(row, 2, self._rowList[row].frame)
            
            if 'F' in fmt:
                self._rowList[row].path_btn.show()
            else:
                self._rowList[row].path_btn.hide()

            self.setRowHeight(row, 20)

            self._rowList[row].has_setup = True
    
    def refreshButtonIndex(self, row):
            self._rowList[row].send_btn.setIndex(row)
            self._rowList[row].fmt_cmb.setIndex(row)
            self._rowList[row].path_btn.setIndex(row)

    def insertRow(self, row):
        super(QuickSendTable, self).insertRow(row)
        self._rowList.insert(row, QckSndRow(row, parent=self))
        self.setRowContent(row, ['new', 'H', ''])
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
                    self.setRowContent(i, text_lst=one_line)

    def saveToCSV(self, fileName: str):
        rows = self.rowCount()

        save_data = [[self._rowList[row].send_btn.text(), self._rowList[row].fmt_cmb.text(),
                        self._rowList[row].data_edt.text()] for row in range(rows)]

        #import pprint
        #pprint.pprint(save_data, width=120, compact=True)

        with open(fileName, 'w') as csvfile:
            csvwriter = csv.writer(csvfile, delimiter=',', lineterminator='\n')
            csvwriter.writerows(save_data)
