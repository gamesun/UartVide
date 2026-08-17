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
import PySide2.QtCore
from PySide2.QtGui import *
import PySide2.QtGui
from PySide2.QtWidgets import *
from qfluentwidgets import *

from .elidedlineedit import ElidedLineEdit
from .dialog import RenameDailog, ConfirmDialog
from .rightanglecombobox import RightAngleComboBox
from .uvcolorpicker import UVColorPicker
import csv
from functools import partial
import json



class IndexButton(ToolButton):
    clicked = Signal(int)
    rightClicked = Signal(QPoint, int)

    def __init__(self, parent=None, index: int=0, text: str='', color=QColor("#27b798")):
        super(IndexButton, self).__init__(parent)
        self._index = index
        self.setText(text)
        # self.setMouseTracking(True)
        self.setColor(color)
    
    def setColor(self, color: QColor):
        text_color = QColor(255, 255, 255) if color.lightness() < 128 else QColor(0, 0, 0)
        self.setStyleSheet(f'''
            QToolButton {{
                background-color: {color.name()};
                color: {text_color.name()};
                font-family:Tahoma;
                font-size:10pt;
            }}
            QToolButton:hover {{
                background-color: {color.lighter(120).name()};
            }}
            QToolButton:pressed {{
                background-color: {color.darker(120).name()};
                padding-top: 2px;
                padding-left: 2px;
            }}
        ''')

    def setIndex(self, index: int):
        self._index = index

    def mousePressEvent(self, mouseEvent):
        if mouseEvent.button() == Qt.LeftButton:
            self.clicked.emit(self._index)
        if mouseEvent.button() == Qt.RightButton:
            self.rightClicked.emit(mouseEvent.globalPos(), self._index)
        
        super().mousePressEvent(mouseEvent)

    def mouseReleaseEvent(self, arg__1: QMouseEvent) -> None:
        return super().mouseReleaseEvent(arg__1)
    
    def leaveEvent(self, arg__1: QEvent) -> None:
        me = QMouseEvent(QEvent.Type.MouseButtonRelease, QCursor.pos(), Qt.LeftButton, Qt.LeftButton, Qt.NoModifier)
        self.mouseReleaseEvent(me)
        return super().leaveEvent(arg__1)

class FormatComboBox(RightAngleComboBox):
    rightClicked = Signal(QPoint, int)
    formatChanged = Signal(str, int)
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
        self.currentTextChanged.connect(self.onCurrentTextChanged)
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
        self.setFixedWidth(24)
    
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
        
    def onCurrentTextChanged(self, text):
        self.formatChanged.emit(text, self._index)

    def mousePressEvent(self, mouseEvent):
        if mouseEvent.button() == Qt.RightButton:
            self.rightClicked.emit(mouseEvent.globalPos(), self._index)
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
    def __init__(self, parent=None, row: int=0,  name='', fmt='', data='', color=QColor("#27b798")):
        self.has_setup = False
        self.send_btn = IndexButton(parent, row, name, color)
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


class QuickSendTablePage(QTableWidget):
    """单个快速发送表格页面"""
    
    def __init__(self, parent=None):
        super(QuickSendTablePage, self).__init__(parent)
        self.scrollDelegate = SmoothScrollDelegate(self, True)
        self._rowList: list[QckSndRow] = []
        self._send_func = None
        self.setColumnCount(3)

        font1 = QFont()
        font1.setFamily(u"Consolas")
        font1.setPointSize(10)
        font1.setKerning(True)
        font1.setStyleStrategy(QFont.PreferAntialias)
        self.setFont(font1)
        self.setMouseTracking(True)
        self.setEditTriggers(QAbstractItemView.AllEditTriggers)
        self.setSelectionMode(QAbstractItemView.NoSelection)
        self.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.setRowCount(0)
        self.setColumnCount(3)
        self.horizontalHeader().setVisible(False)
        self.horizontalHeader().setMinimumSectionSize(16)
        self.horizontalHeader().setStretchLastSection(True)
        self.verticalHeader().setVisible(False)
        self.verticalHeader().setMinimumSectionSize(16)
        self.verticalHeader().setDefaultSectionSize(16)

        
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
                padding-top: 2px;
                padding-left: 2px;
            }
        """)

    def initMenu(self):
        self.actionRename = Action(FluentIcon.EDIT, "Rename", self)
        self.actionRename.triggered.connect(self.onRename)

        self.actionInsertRow = Action(FluentIcon.ADD, "Insert row", self)
        self.actionInsertRow.triggered.connect(self.onInsertRow)

        self.actionDeleteRow = Action(FluentIcon.DELETE, "Delete row", self)
        self.actionDeleteRow.triggered.connect(self.onRemoveRow)

        self.actionChgBtnColor = Action(FluentIcon.PALETTE, "Change color", self)
        self.actionChgBtnColor.triggered.connect(self.onChgBtnColor)

        self.actionRstBtnColor = Action(FluentIcon.PALETTE, "Reset color", self)
        self.actionRstBtnColor.triggered.connect(self.onRstBtnColor)

        self.menuRightClick = RoundMenu(parent=self)
        self.menuRightClick.addAction(self.actionRename)
        self.menuRightClick.addAction(self.actionInsertRow)
        self.menuRightClick.addAction(self.actionDeleteRow)
        self.menuRightClick.addAction(self.actionChgBtnColor)
        self.menuRightClick.addAction(self.actionRstBtnColor)

    def getPageData(self):
        """获取页面数据，用于保存"""
        rows = self.rowCount()
        data = []
        for row in range(rows):
            if row < len(self._rowList):
                data.append([
                    self._rowList[row].send_btn.text(),
                    self._rowList[row].fmt_cmb.text(),
                    self._rowList[row].data_edt.text(),
                    self._rowList[row].send_btn.palette().button().color().name()
                ])
        return data

    def setPageData(self, data):
        """设置页面数据，用于加载"""
        self.clearContents()
        self.setRowCount(0)
        self._rowList.clear()
        for i, row_data in enumerate(data):
            if len(row_data) < 4:
                row_data = row_data + [''] * (4 - len(row_data))
            if 4 < len(row_data):
                row_data = row_data[:4]
            self.setRowContent(i, text_lst=row_data)
        self.resizeColumnsToContents()

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

    def onChgBtnColor(self):
        item = self._rowList[self._selectingRow].send_btn
        cp = UVColorPicker(True, False)
        new_color = cp.getColor(item.palette().button().color().getRgb()[:3])
        new_qcolor = QColor(int(new_color[0]), int(new_color[1]), int(new_color[2]))
        item.setColor(new_qcolor)

    def onRstBtnColor(self):
        item = self._rowList[self._selectingRow].send_btn
        item.setColor(QColor("#27b798"))

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

    def onRightClicked(self, pos: QPoint, row: int):
        self._selectingRow = row
        self.menuRightClick.popup(pos)

    def onFormatChanged(self, text, row):
        if 'F' in text:
            self._rowList[row].path_btn.show()
        else:
            self._rowList[row].path_btn.hide()

    def onSelectFile(self, row: int):
        old_path = self.text(row, 2)
        fileName = QFileDialog.getOpenFileName(self, "Select a file",
            old_path, "All Files (*.*)")[0]
        if fileName:
            self.setText(row, 2, fileName)

    def setPathButtonHidden(self, row, hidden: bool):
        if hidden:
            self._rowList[row].path_btn.hide()
        else:
            self._rowList[row].path_btn.show()

    def setRowCount(self, rows: int):
        super(QuickSendTablePage, self).setRowCount(rows)

        if len(self._rowList) < rows:
            for i in range(len(self._rowList), rows):
                self._rowList.append(QckSndRow(parent=self, row=i))
                self.setRowContent(i, ['%d' % i, 'H', '', "#27b798"])
        elif rows < len(self._rowList):
            del self._rowList[rows:]

        self.resizeColumnsToContents()

    def refreshWidgets(self, row):
        self.removeCellWidget(row, 0)
        self.removeCellWidget(row, 1)
        self.removeCellWidget(row, 2)
        self.setCellWidget(row, 0, self._rowList[row].send_btn)
        self.setCellWidget(row, 1, self._rowList[row].fmt_cmb)
        self.setCellWidget(row, 2, self._rowList[row].frame)

    def setRowContent(self, row: int, text_lst):
        if len(text_lst) < 4:
            text_lst = text_lst + [''] * (4 - len(text_lst))
        name = text_lst[0]
        fmt = text_lst[1]
        data = text_lst[2]
        color_str = text_lst[3]
        try:
            if len(color_str) == 7 and color_str[0] == '#':
                color = QColor(color_str)
            else:
                color = QColor("#27b798")
        except:
            color = QColor("#27b798")

        if len(self._rowList) <= row:
            self._rowList.append(QckSndRow(parent=self, row=row, name=name, fmt=fmt, data=data, color=color))
            super(QuickSendTablePage, self).setRowCount(len(self._rowList))

        if not self._rowList[row].has_setup:
            self._rowList[row].row = row
            self._rowList[row].send_btn.setText(name)
            self._rowList[row].fmt_cmb.setText(fmt)
            self._rowList[row].data_edt.setText(data)
            self._rowList[row].send_btn.clicked.connect(self._send_func)
            self._rowList[row].send_btn.rightClicked.connect(self.onRightClicked)
            self._rowList[row].fmt_cmb.rightClicked.connect(self.onRightClicked)
            self._rowList[row].fmt_cmb.formatChanged.connect(self.onFormatChanged)
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
        else:
            self._rowList[row].send_btn.setText(name)
            self._rowList[row].fmt_cmb.setText(fmt)
            self._rowList[row].data_edt.setText(data)

            if 'F' in fmt:
                self._rowList[row].path_btn.show()
            else:
                self._rowList[row].path_btn.hide()
    
    def refreshButtonIndex(self, row):
            self._rowList[row].send_btn.setIndex(row)
            self._rowList[row].fmt_cmb.setIndex(row)
            self._rowList[row].path_btn.setIndex(row)

    def insertRow(self, row):
        super(QuickSendTablePage, self).insertRow(row)
        self._rowList.insert(row, QckSndRow(parent=self, row = row))
        self.setRowContent(row, ['new', 'H', '', "#27b798"])
        rowCnt = len(self._rowList)
        super(QuickSendTablePage, self).setRowCount(rowCnt)
        for i in range(row, rowCnt):
            self.refreshButtonIndex(i)

    def removeRow(self, row):
        super(QuickSendTablePage, self).removeRow(row)
        del self._rowList[row]
        rowCnt = len(self._rowList)
        super(QuickSendTablePage, self).setRowCount(rowCnt)
        for i in range(row, rowCnt):
            self.refreshButtonIndex(i)

    def loadFromCSV(self, fileName: str):
        with open(fileName, newline='') as csvfile:
            csvData = csv.reader(csvfile)
            if csvData:
                for i, one_line in enumerate(csvData):
                    if len(one_line) < 4:
                        one_line = one_line + [''] * (4 - len(one_line))
                    if 4 < len(one_line):
                        one_line = one_line[:4]
                    self.setRowContent(i, text_lst=one_line)
        self.resizeColumnsToContents()

    def saveToCSV(self, fileName: str):
        rows = self.rowCount()

        save_data = [[self._rowList[row].send_btn.text(), 
                      self._rowList[row].fmt_cmb.text(),
                      self._rowList[row].data_edt.text(),
                      self._rowList[row].send_btn.palette().button().color().name()
                     ] for row in range(rows) if row < len(self._rowList)]

        with open(fileName, 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile, delimiter=',', lineterminator='\n')
            csvwriter.writerows(save_data)


class QuickSendTable(QWidget):
    """多页快速发送表格，使用 TabWidget 管理多个页面"""
    
    def __init__(self, parent=None):
        super(QuickSendTable, self).__init__(parent)
        self._send_func = None
        self._pages: list[QuickSendTablePage] = []
        self._page_names: list[str] = []
        
        self.initUI()
        self.initMenu()
        
    def initUI(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(2)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # 创建 TabWidget
        self.tabWidget = QTabWidget(self)
        self.tabWidget.setTabPosition(QTabWidget.North)
        self.tabWidget.setMovable(True)
        self.tabWidget.setTabsClosable(False)
        self.tabWidget.setUsesScrollButtons(True)
        self.tabWidget.setTabBarAutoHide(False)
        self.tabWidget.tabBar().setElideMode(Qt.ElideNone)
        self.tabWidget.tabBar().setDocumentMode(False)
        self.tabWidget.tabBar().setExpanding(True)
        self.tabWidget.tabBar().setMinimumHeight(30)
        self.tabWidget.tabBar().setStyleSheet("QTabBar { background: transparent; } ")
        self.tabWidget.tabCloseRequested.connect(self.onTabCloseRequested)
        self.tabWidget.tabBarDoubleClicked.connect(self.onTabRename)
        layout.addWidget(self.tabWidget)
        
        # 创建 "+" 按钮用于添加新页面
        self.btnAddPage = QToolButton(self)
        self.btnAddPage.setText("+")
        self.btnAddPage.setFixedSize(20, 20)
        self.btnAddPage.clicked.connect(self.onAddPage)

        self.btnAddPageLayout = QWidget(self)
        self.btnAddPageLayout.setContentsMargins(0, 0, 3, 2)
        self.btnAddPageLayout.setFixedSize(22, 22)

        add_page_layout = QHBoxLayout(self.btnAddPageLayout)
        add_page_layout.setContentsMargins(0, 0, 0, 0)
        add_page_layout.setSpacing(0)
        add_page_layout.addWidget(self.btnAddPage, 0, Qt.AlignRight | Qt.AlignBottom)
        
        # 将 + 按钮添加到 tab bar 右侧
        self.tabWidget.setCornerWidget(self.btnAddPageLayout, Qt.TopRightCorner)
        
        # 创建默认页面
        self.addPage("Page 1")
        
    def initMenu(self):
        # 页面右键菜单
        self.actionRenamePage = Action(FluentIcon.EDIT, "Rename Page", self)
        self.actionRenamePage.triggered.connect(self.onRenameCurrentPage)

        self.actionAddPage = Action(FluentIcon.ADD, "Add Page", self)
        self.actionAddPage.triggered.connect(self.onAddPage)

        self.actionDeletePage = Action(FluentIcon.DELETE, "Delete Page", self)
        self.actionDeletePage.triggered.connect(self.onDeleteCurrentPage)

        self.menuPageRightClick = RoundMenu(parent=self)
        self.menuPageRightClick.addAction(self.actionRenamePage)
        self.menuPageRightClick.addAction(self.actionAddPage)
        self.menuPageRightClick.addAction(self.actionDeletePage)
        
        # 安装事件过滤器以捕获 tab bar 右键
        self.tabWidget.tabBar().installEventFilter(self)
        
    def eventFilter(self, obj, event):
        if obj == self.tabWidget.tabBar() and event.type() == QEvent.Type.ContextMenu:
            index = self.tabWidget.tabBar().tabAt(event.pos())
            if index >= 0:
                self._contextMenuIndex = index
                self.menuPageRightClick.popup(event.globalPos())
            return True
        return super().eventFilter(obj, event)

    def addPage(self, name: str = None) -> QuickSendTablePage:
        """添加新页面"""
        if name is None:
            name = f"Page {self.tabWidget.count() + 1}"

        current_page = self.currentPage()
        default_columns = 3
        default_rows = 10
        if current_page:
            current_columns = current_page.columnCount()
            current_rows = current_page.rowCount()
            if current_columns > 0:
                default_columns = current_columns
            if current_rows > 0:
                default_rows = current_rows

        page = QuickSendTablePage(self)
        page.setColumnCount(default_columns)
        page.setRowCount(default_rows)
        if self._send_func:
            page.setSendFunc(self._send_func)
            
        self.tabWidget.addTab(page, name)
        self._pages.append(page)
        self._page_names.append(name)
        
        return page
        
    def onAddPage(self):
        """添加新页面按钮点击"""
        self.addPage()
        
    def onTabCloseRequested(self, index: int):
        """关闭标签页"""
        if self.tabWidget.count() <= 1:
            # 至少保留一个页面
            return
        self.removePage(index)
        
    def removePage(self, index: int):
        """移除指定页面"""
        if 0 <= index < len(self._pages):
            self._pages.pop(index)
            self._page_names.pop(index)
            self.tabWidget.removeTab(index)
            
    def onDeleteCurrentPage(self):
        """删除当前页面，需确认，且删除后不可恢复"""
        index = getattr(self, '_contextMenuIndex', self.tabWidget.currentIndex())
        if not (0 <= index < self.tabWidget.count()):
            return

        if self.tabWidget.count() <= 1:
            return

        page_name = self.tabWidget.tabText(index)
        tab_rect = self.tabWidget.tabBar().tabRect(index)
        pos = self.tabWidget.tabBar().mapToGlobal(tab_rect.bottomLeft())
        msg = f"Delete page '{page_name}'?\nThis action cannot be undone."

        if ConfirmDialog.confirm(msg, pos):
            self.onTabCloseRequested(index)
            self._contextMenuIndex = self.tabWidget.currentIndex()
            
    def onTabRename(self, index: int):
        """双击重命名标签"""
        self._contextMenuIndex = index
        self.onRenameCurrentPage()
        
    def onRenameCurrentPage(self):
        """重命名当前页面"""
        if hasattr(self, '_contextMenuIndex'):
            index = self._contextMenuIndex
            old_name = self.tabWidget.tabText(index)
            
            # 获取 tab 的位置用于显示对话框
            tab_rect = self.tabWidget.tabBar().tabRect(index)
            pos = self.tabWidget.tabBar().mapToGlobal(tab_rect.bottomLeft())
            
            new_name = RenameDailog.getNewName(old_name, pos)
            if new_name:
                self.tabWidget.setTabText(index, new_name)
                self._page_names[index] = new_name
                
    def setSendFunc(self, send_func: callable):
        """设置发送函数到所有页面"""
        self._send_func = send_func
        for page in self._pages:
            page.setSendFunc(send_func)
            
    def currentPage(self) -> QuickSendTablePage:
        """获取当前页面"""
        current_index = self.tabWidget.currentIndex()
        if 0 <= current_index < len(self._pages):
            return self._pages[current_index]
        return None
        
    def page(self, index: int) -> QuickSendTablePage:
        """获取指定索引的页面"""
        if 0 <= index < len(self._pages):
            return self._pages[index]
        return None
        
    def pageCount(self) -> int:
        """获取页面数量"""
        return len(self._pages)
        
    # 委托方法到当前页面
    def rowCount(self) -> int:
        page = self.currentPage()
        return page.rowCount() if page else 0
        
    def setRowCount(self, rows: int):
        page = self.currentPage()
        if page:
            page.setRowCount(rows)
            
    def columnCount(self) -> int:
        page = self.currentPage()
        return page.columnCount() if page else 3
        
    def setColumnCount(self, columns: int):
        page = self.currentPage()
        if page:
            page.setColumnCount(columns)
        # 设置所有页面的列数
        for p in self._pages:
            p.setColumnCount(columns)
            
    def setRowContent(self, row: int, text_lst):
        page = self.currentPage()
        if page:
            page.setRowContent(row, text_lst)
            
    def text(self, row: int, column: int):
        page = self.currentPage()
        return page.text(row, column) if page else ""
        
    def setText(self, row, column, text):
        page = self.currentPage()
        if page:
            page.setText(row, column, text)
            
    def horizontalHeader(self):
        page = self.currentPage()
        return page.horizontalHeader() if page else None
        
    def verticalHeader(self):
        page = self.currentPage()
        return page.verticalHeader() if page else None
        
    def resizeColumnsToContents(self):
        for page in self._pages:
            page.resizeColumnsToContents()
            
    def setFont(self, font):
        for page in self._pages:
            page.setFont(font)
            
    def setMouseTracking(self, enable):
        super().setMouseTracking(enable)
        for page in self._pages:
            page.setMouseTracking(enable)
            
    def setEditTriggers(self, triggers):
        for page in self._pages:
            page.setEditTriggers(triggers)
            
    def setSelectionMode(self, mode):
        for page in self._pages:
            page.setSelectionMode(mode)
            
    def setVerticalScrollMode(self, mode):
        for page in self._pages:
            page.setVerticalScrollMode(mode)
            
    def setHorizontalScrollMode(self, mode):
        for page in self._pages:
            page.setHorizontalScrollMode(mode)
            
    def loadFromCSV(self, fileName: str):
        """加载 CSV 到当前页面（向后兼容）"""
        page = self.currentPage()
        if page:
            page.loadFromCSV(fileName)
            
    def saveToCSV(self, fileName: str):
        """保存当前页面到 CSV（向后兼容）"""
        page = self.currentPage()
        if page:
            page.saveToCSV(fileName)
            
    def saveAllToJSON(self, fileName: str):
        """保存所有页面到 JSON"""
        data = {
            'pages': []
        }
        for i, page in enumerate(self._pages):
            page_data = {
                'name': self._page_names[i] if i < len(self._page_names) else f'Page {i+1}',
                'rows': page.getPageData()
            }
            data['pages'].append(page_data)
            
        with open(fileName, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            
    def loadAllFromJSON(self, fileName: str):
        """从 JSON 加载所有页面"""
        try:
            with open(fileName, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            # 清除现有页面
            while self.tabWidget.count() > 0:
                self.tabWidget.removeTab(0)
            self._pages.clear()
            self._page_names.clear()
            
            # 加载页面
            for page_data in data.get('pages', []):
                name = page_data.get('name', 'Page')
                rows = page_data.get('rows', [])
                
                page = self.addPage(name)
                page.setPageData(rows)
                
            # 如果没有页面，创建一个默认页面
            if not self._pages:
                self.addPage('Page 1')
                
        except Exception as e:
            print(f"Error loading JSON: {e}")
            # 创建默认页面
            if not self._pages:
                self.addPage('Page 1')
