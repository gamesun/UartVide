#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
#
#############################################################################
##
## Copyright (c) 2013-2017, gamesun
## All right reserved.
##
## This file is part of MyTerm.
##
## MyTerm is free software: you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation, either version 3 of the License, or
## (at your option) any later version.
##
## MyTerm is distributed in the hope that it will be useful, but
## WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with MyTerm.  If not, see <http://www.gnu.org/licenses/>.
##
#############################################################################


import sys, os
import datetime
import pickle
import csv
from lxml import etree as ET
import defusedxml.cElementTree as safeET
from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import QMainWindow, QApplication, QMessageBox, QWidget, \
    QFileDialog, QTableWidgetItem, QPushButton, QActionGroup, QDesktopWidget
from PyQt4.QtCore import Qt, QThread, pyqtSignal, QSignalMapper

import appInfo
#from gui_qt4.ui_mainwindow import Ui_MainWindow
from gui_qt4_flat.ui_mainwindow import Ui_MainWindow
from res import resources_pyqt4
from enum_ports import enum_ports
import serial

extension = os.path.splitext(sys.argv[0])[1]
if extension != '.py':
    import except_logger
    sys.excepthook = except_logger.exceptHook

if os.name == 'nt':
    EDITOR_FONT = "Consolas"
    UI_FONT = "Meiryo UI"
elif os.name == 'posix':
    EDITOR_FONT = "Courier 10 Pitch"
    UI_FONT = None

VIEWMODE_ASCII           = 0
VIEWMODE_HEX_LOWERCASE   = 1
VIEWMODE_HEX_UPPERCASE   = 2

class readerThread(QThread):
    """loop and copy serial->GUI"""
    read = pyqtSignal(str)
    exception = pyqtSignal(str)

    def __init__(self, parent=None):
        super(readerThread, self).__init__(parent)
        self._alive = None
        self._serialport = None
        self._viewMode = None

    def setPort(self, port):
        self._serialport = port

    def setViewMode(self, mode):
        self._viewMode = mode

    def start(self, priority = QThread.InheritPriority):
        self._alive = True
        super(readerThread, self).start(priority)

    def __del__(self):
        if self._alive:
            self._alive = False
            if hasattr(self._serialport, 'cancel_read'):
                self._serialport.cancel_read()
        self.wait()

    def join(self):
        self.__del__()

    def run(self):
        # print("readerThread id:{}".format(self.currentThreadId()))
        text = str()
        try:
            while self._alive:
                # read all that is there or wait for one byte
                data = self._serialport.read(self._serialport.in_waiting or 1)
                if data:
                    try:
                        text = data.decode('unicode_escape')
                    except UnicodeDecodeError:
                        pass
                    else:
                        self.read.emit(text)
                    # if -1 != text.find('\r\n'):
                    #     print(repr(text))
                    #     text = text.replace('\r\n', '\n')
                    #     text = text.replace('\n\n', '\n')
                    #     if text[0] == '\n':
                    #         text = text[1:]
                    #     self.read.emit(text)
                    #     text = str()
                    # if self.raw:
                    #     self.console.write_bytes(data)
                    # else:
                    #     text = self.rx_decoder.decode(data)
                    #     for transformation in self.rx_transformations:
                    #         text = transformation.rx(text)
                    #     self.console.write(text)
        except serial.SerialException as e:
            self.exception.emit('{}'.format(e))
            # raise       # XXX handle instead of re-raise?

class MainWindow(QMainWindow, Ui_MainWindow):
    """docstring for MainWindow."""
    def __init__(self, parent=None):
        super(MainWindow, self).__init__()
        self._csvFilePath = ""
        self.serialport = serial.Serial()
        self.receiver_thread = readerThread(self)
        self.receiver_thread.setPort(self.serialport)
        self._localEcho = None

        self.setupUi(self)
        self.setCorner(Qt.TopLeftCorner, Qt.LeftDockWidgetArea)
        self.setCorner(Qt.BottomLeftCorner, Qt.LeftDockWidgetArea)
        font = QtGui.QFont()
        font.setFamily(EDITOR_FONT)
        font.setPointSize(10)
        self.txtEdtOutput.setFont(font)
        self.txtEdtInput.setFont(font)
        self.quickSendTable.setFont(font)
        if UI_FONT is not None:
            font = QtGui.QFont()
            font.setFamily(UI_FONT)
            font.setPointSize(9)
            self.dockWidget_PortConfig.setFont(font)
            self.dockWidget_SendHex.setFont(font)
            self.dockWidget_QuickSend.setFont(font)
        self.setupFlatUi()
        self.onEnumPorts()

        icon = QtGui.QIcon(":/icon.ico")
        self.setWindowIcon(icon)
        self.actionAbout.setIcon(icon)

        icon = QtGui.QIcon(":/qt_logo_16.ico")
        self.actionAbout_Qt.setIcon(icon)

        self._viewGroup = QActionGroup(self)
        self._viewGroup.addAction(self.actionAscii)
        self._viewGroup.addAction(self.actionHex_lowercase)
        self._viewGroup.addAction(self.actionHEX_UPPERCASE)
        self._viewGroup.setExclusive(True)

        # bind events
        self.actionOpen_Cmd_File.triggered.connect(self.openCSV)
        self.actionSave_Log.triggered.connect(self.onSaveLog)
        self.actionExit.triggered.connect(self.onExit)

        self.actionOpen.triggered.connect(self.openPort)
        self.actionClose.triggered.connect(self.closePort)

        self.actionPort_Config_Panel.triggered.connect(self.onTogglePrtCfgPnl)
        self.actionQuick_Send_Panel.triggered.connect(self.onToggleQckSndPnl)
        self.actionSend_Hex_Panel.triggered.connect(self.onToggleHexPnl)
        self.dockWidget_PortConfig.visibilityChanged.connect(self.onVisiblePrtCfgPnl)
        self.dockWidget_QuickSend.visibilityChanged.connect(self.onVisibleQckSndPnl)
        self.dockWidget_SendHex.visibilityChanged.connect(self.onVisibleHexPnl)
        self.actionLocal_Echo.triggered.connect(self.onLocalEcho)
        self.actionAlways_On_Top.triggered.connect(self.onAlwaysOnTop)

        self.actionAscii.triggered.connect(self.onViewChanged)
        self.actionHex_lowercase.triggered.connect(self.onViewChanged)
        self.actionHEX_UPPERCASE.triggered.connect(self.onViewChanged)

        self.actionAbout.triggered.connect(self.onAbout)
        self.actionAbout_Qt.triggered.connect(self.onAboutQt)

        self.btnOpen.clicked.connect(self.onOpen)
        self.btnClear.clicked.connect(self.onClear)
        self.btnSaveLog.clicked.connect(self.onSaveLog)
        self.btnEnumPorts.clicked.connect(self.onEnumPorts)
        self.btnSendHex.clicked.connect(self.sendHex)

        self.receiver_thread.read.connect(self.receive)
        self.receiver_thread.exception.connect(self.readerExcept)
        self._signalMap = QSignalMapper(self)
        self._signalMap.mapped[int].connect(self.tableClick)

        # initial action
        self.actionHEX_UPPERCASE.setChecked(True)
        self.receiver_thread.setViewMode(VIEWMODE_HEX_UPPERCASE)
        self.initQuickSend()
        self.restoreLayout()
        self.moveScreenCenter()
        self.syncMenu()
        
        if self.isMaximized():
            self.setMaximizeButton("restore")
        else:
            self.setMaximizeButton("maximize")
            
        self.LoadSettings()

    def setupFlatUi(self):
        self._dragPos = self.pos()
        self._isDragging = False
        self.setMouseTracking(True)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setStyleSheet("""
            QWidget {
                background-color:#99d9ea;
                /*background-image: url(:/background.png);*/
                outline: 1px solid #0057ff;
            }
            QLabel {
                color:#202020;
                font-size:13px;
                font-family:Century;
            }
            
            QComboBox {
                color:#202020;
                font-size:13px;
                font-family:Century Schoolbook;
            }
            QComboBox {
                border: none;
                padding: 1px 18px 1px 3px;
            }
            QComboBox:editable {
                background: white;
            }
            QComboBox:!editable, QComboBox::drop-down:editable {
                background: #62c7e0;
            }
            QComboBox:!editable:hover, QComboBox::drop-down:editable:hover {
                background: #c7eaf3;
            }
            QComboBox:!editable:pressed, QComboBox::drop-down:editable:pressed {
                background: #35b6d7;
            }
            QComboBox:on {
                padding-top: 3px;
                padding-left: 4px;
            }
            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 16px;
                border: none;
            }
            QComboBox::down-arrow {
                image: url(:/downarrow.png);
            }
            QComboBox::down-arrow:on {
                image: url(:/uparrow.png);
            }
            
            QGroupBox {
                color:#202020;
                font-size:12px;
                font-family:Century Schoolbook;
                border: 1px solid gray;
                margin-top: 15px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                left:5px;
                top:3px;
            }
            
            QCheckBox {
                color:#202020;
                spacing: 5px;
                font-size:12px;
                font-family:Century Schoolbook;
            }

            QScrollBar:horizontal {
                background-color:#99d9ea;
                border: none;
                height: 15px;
                margin: 0px 20px 0 20px;
            }
            QScrollBar::handle:horizontal {
                background: #61b9e1;
                min-width: 20px;
            }
            QScrollBar::add-line:horizontal {
                image: url(:/rightarrow.png);
                border: none;
                background: #7ecfe4;
                width: 20px;
                subcontrol-position: right;
                subcontrol-origin: margin;
            }
            QScrollBar::sub-line:horizontal {
                image: url(:/leftarrow.png);
                border: none;
                background: #7ecfe4;
                width: 20px;
                subcontrol-position: left;
                subcontrol-origin: margin;
            }
            
            QScrollBar:vertical {
                background-color:#99d9ea;
                border: none;
                width: 15px;
                margin: 20px 0px 20px 0px;
            }
            QScrollBar::handle::vertical {
                background: #61b9e1;
                min-height: 20px;
            }
            QScrollBar::add-line::vertical {
                image: url(:/downarrow.png);
                border: none;
                background: #7ecfe4;
                height: 20px;
                subcontrol-position: bottom;
                subcontrol-origin: margin;
            }
            QScrollBar::sub-line::vertical {
                image: url(:/uparrow.png);
                border: none;
                background: #7ecfe4;
                height: 20px;
                subcontrol-position: top;
                subcontrol-origin: margin;
            }
            
            QTableView {
                background-color: white;
                /*selection-background-color: #FF92BB;*/
                border: 1px solid #eeeeee;
                color: #2f2f2f;
            }
            QTableView::focus {
                /*border: 1px solid #2a7fff;*/
            }
            QTableView QTableCornerButton::section {
                border: none;
                border-right: 1px solid #eeeeee;
                border-bottom: 1px solid #eeeeee;
                background-color: #8ae6d2;
            }
            QTableView QWidget {
                background-color: white;
            }
            QTableView::item:focus {
                border: 1px red;
                background-color: transparent;
                color: #2f2f2f;
            }
            QHeaderView::section {
                border: none;
                border-right: 1px solid #eeeeee;
                border-bottom: 1px solid #eeeeee;
                padding-left: 2px;
                padding-right: 2px;
                color: #444444;
                background-color: #8ae6d2;
            }
            QTextEdit {
                background-color:white;
                color:#2f2f2f;
                border: 1px solid white;
            }
            QTextEdit::focus {
                border: 1px solid #2a7fff;
            }
            
            QPushButton {
                background-color:#30a7b8;
                border:none;
                color:#ffffff;
                font-size:14px;
                font-family:Century Schoolbook;
            }
            QPushButton:hover {
                background-color:#51c0d1;
            }
            QPushButton:pressed {
                background-color:#3a9ecc;
            }
            
            QMenuBar {
                color: #2f2f2f;
            }
            QMenuBar::item {
                background-color: transparent;
                margin: 8px 0px 0px 0px;
                padding: 1px 8px 1px 8px;
                height: 15px;
            }
            QMenuBar::item:selected {
                background: #51c0d1;
            }
            QMenuBar::item:pressed {
                
            }
            QMenu {
                color: #2f2f2f;
            }
            QMenu {
                margin: 2px;
            }
            QMenu::item {
                padding: 2px 25px 2px 21px;
                border: 1px solid transparent;
            }
            QMenu::item:selected {
                background: #51c0d1;
            }
            QMenu::icon {
                background: transparent;
                border: 2px inset transparent;
            }

            QDockWidget {
                font-size:13px;
                font-family:Century;
                color: #202020;
                titlebar-close-icon: none;
                titlebar-normal-icon: none;
            }
            QDockWidget::title {
                margin: 0;
                padding: 2px;
                subcontrol-origin: content;
                subcontrol-position: right top;
                text-align: left;
                background: #67baed;
                
            }
            QDockWidget::float-button {
                max-width: 12px;
                max-height: 12px;
                background-color:transparent;
                border:none;
                image: url(:/restore_inactive.png);
            }
            QDockWidget::float-button:hover {
                background-color:#227582;
                image: url(:/restore_active.png);
            }
            QDockWidget::float-button:pressed {
                padding: 0;
                background-color:#14464e;
                image: url(:/restore_active.png);
            }
            QDockWidget::close-button {
                max-width: 12px;
                max-height: 12px;
                background-color:transparent;
                border:none;
                image: url(:/close_inactive.png);
            }
            QDockWidget::close-button:hover {
                background-color:#ea5e00;
                image: url(:/close_active.png);
            }
            QDockWidget::close-button:pressed {
                background-color:#994005;
                image: url(:/close_active.png);
                padding: 0;
            }
            
        """)
        self.dockWidgetContents.setStyleSheet("""
            QPushButton {
                min-height:23px;
            }
        """)
        self.dockWidget_QuickSend.setStyleSheet("""
            QPushButton {
                background-color:#27b798;
                font-family:Consolas;
                font-size:12px;
                min-width:46px;
            }
            QPushButton:hover {
                background-color:#3bd5b4;
            }
            QPushButton:pressed {
                background-color:#1d8770;
            }
        """)
        self.dockWidgetContents_2.setStyleSheet("""
            QPushButton {
                min-height:23px;
                min-width:50px;
            }
        """)

        w = self.frameGeometry().width()
        self._minBtn = QPushButton(self)
        self._minBtn.setGeometry(w-103,0,28,24)
        self._minBtn.clicked.connect(self.onMinimize)
        self._minBtn.setStyleSheet("""
            QPushButton {
                background-color:transparent;
                border:none;
                outline: none;
                image: url(:/minimize_inactive.png);
            }
            QPushButton:hover {
                background-color:#227582;
                image: url(:/minimize_active.png);
            }
            QPushButton:pressed {
                background-color:#14464e;
                image: url(:/minimize_active.png);
            }
        """)
        
        self._maxBtn = QPushButton(self)
        self._maxBtn.setGeometry(w-74,0,28,24)
        self._maxBtn.clicked.connect(self.onMaximize)
        self.setMaximizeButton("maximize")
        
        self._closeBtn = QPushButton(self)
        self._closeBtn.setGeometry(w-45,0,36,24)
        self._closeBtn.clicked.connect(self.onExit)
        self._closeBtn.setStyleSheet("""
            QPushButton {
                background-color:transparent;
                border:none;
                outline: none;
                image: url(:/close_inactive.png);
            }
            QPushButton:hover {
                background-color:#ea5e00;
                image: url(:/close_active.png);
            }
            QPushButton:pressed {
                background-color:#994005;
                image: url(:/close_active.png);
            }
        """)

    def resizeEvent(self, event):
        w = event.size().width()
        self._minBtn.move(w-103,0)
        self._maxBtn.move(w-74,0)
        self._closeBtn.move(w-45,0)

    def onMinimize(self):
        self.showMinimized()
    
    def isMaximized(self):
        return ((self.windowState() == Qt.WindowMaximized))
    
    def onMaximize(self):
        if self.isMaximized():
            self.showNormal()
            self.setMaximizeButton("maximize")
        else:
            self.showMaximized()
            self.setMaximizeButton("restore")
    
    def setMaximizeButton(self, style):
        if "maximize" == style:
            self._maxBtn.setStyleSheet("""
                QPushButton {
                    background-color:transparent;
                    border:none;
                    outline: none;
                    image: url(:/maximize_inactive.png);
                }
                QPushButton:hover {
                    background-color:#227582;
                    image: url(:/maximize_active.png);
                }
                QPushButton:pressed {
                    background-color:#14464e;
                    image: url(:/maximize_active.png);
                }
            """)
        elif "restore" == style:
            self._maxBtn.setStyleSheet("""
                QPushButton {
                    background-color:transparent;
                    border:none;
                    outline: none;
                    image: url(:/restore_inactive.png);
                }
                QPushButton:hover {
                    background-color:#227582;
                    image: url(:/restore_active.png);
                }
                QPushButton:pressed {
                    background-color:#14464e;
                    image: url(:/restore_active.png);
                }
            """)
    
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._isDragging = True
            self._dragPos = event.globalPos() - self.pos()
        event.accept()
        
    def mouseMoveEvent(self, event):
        if event.buttons() and Qt.LeftButton and self._isDragging and not self.isMaximized():
            self.move(event.globalPos() - self._dragPos)
        event.accept()

    def mouseReleaseEvent(self, event):
        self._isDragging = False
        event.accept()

    def SaveSettings(self):
        root = ET.Element("MyTerm")
        GUISettings = ET.SubElement(root, "GUISettings")

        PortCfg = ET.SubElement(GUISettings, "PortConfig")
        ET.SubElement(PortCfg, "port").text = self.cmbPort.currentText()
        ET.SubElement(PortCfg, "baudrate").text = self.cmbBaudRate.currentText()
        ET.SubElement(PortCfg, "databits").text = self.cmbDataBits.currentText()
        ET.SubElement(PortCfg, "parity").text = self.cmbParity.currentText()
        ET.SubElement(PortCfg, "stopbits").text = self.cmbStopBits.currentText()
        ET.SubElement(PortCfg, "rtscts").text = self.chkRTSCTS.isChecked() and "on" or "off"
        ET.SubElement(PortCfg, "xonxoff").text = self.chkXonXoff.isChecked() and "on" or "off"

        View = ET.SubElement(GUISettings, "View")
        ET.SubElement(View, "LocalEcho").text = self.actionLocal_Echo.isChecked() and "on" or "off"
        ET.SubElement(View, "ReceiveView").text = self._viewGroup.checkedAction().text()

        with open('settings.xml', 'w') as f:
            f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
            f.write(ET.tostring(root, encoding='utf-8', pretty_print=True).decode("utf-8"))

    def LoadSettings(self):
        if os.path.isfile("settings.xml"):
            with open('settings.xml', 'r') as f:
                tree = safeET.parse(f)

            port = tree.findtext('GUISettings/PortConfig/port', default='')
            if port != '':
                self.cmbPort.setCurrentText(port)

            baudrate = tree.findtext('GUISettings/PortConfig/baudrate', default='38400')
            if baudrate != '':
                self.cmbBaudRate.setCurrentText(baudrate)

            databits = tree.findtext('GUISettings/PortConfig/databits', default='8')
            id = self.cmbDataBits.findText(databits)
            if id >= 0:
                self.cmbDataBits.setCurrentIndex(id)

            parity = tree.findtext('GUISettings/PortConfig/parity', default='None')
            id = self.cmbParity.findText(parity)
            if id >= 0:
                self.cmbParity.setCurrentIndex(id)

            stopbits = tree.findtext('GUISettings/PortConfig/stopbits', default='1')
            id = self.cmbStopBits.findText(stopbits)
            if id >= 0:
                self.cmbStopBits.setCurrentIndex(id)

            rtscts = tree.findtext('GUISettings/PortConfig/rtscts', default='off')
            if 'on' == rtscts:
                self.chkRTSCTS.setChecked(True)
            else:
                self.chkRTSCTS.setChecked(False)

            xonxoff = tree.findtext('GUISettings/PortConfig/xonxoff', default='off')
            if 'on' == xonxoff:
                self.chkXonXoff.setChecked(True)
            else:
                self.chkXonXoff.setChecked(False)

            LocalEcho = tree.findtext('GUISettings/View/LocalEcho', default='off')
            if 'on' == LocalEcho:
                self.actionLocal_Echo.setChecked(True)
                self._localEcho = True
            else:
                self.actionLocal_Echo.setChecked(False)
                self._localEcho = False

            ReceiveView = tree.findtext('GUISettings/View/ReceiveView', default='HEX(UPPERCASE)')
            if 'Ascii' in ReceiveView:
                self.actionAscii.setChecked(True)
            elif 'lowercase' in ReceiveView:
                self.actionHex_lowercase.setChecked(True)
            elif 'UPPERCASE' in ReceiveView:
                self.actionHEX_UPPERCASE.setChecked(True)

    def closeEvent(self, event):
        self.saveLayout()
        self.saveCSV()
        self.SaveSettings()
        event.accept()

    def tableClick(self, row):
        self.sendTableRow(row)

    def initQuickSend(self):
        #self.quickSendTable.horizontalHeader().setDefaultSectionSize(40)
        #self.quickSendTable.horizontalHeader().setMinimumSectionSize(25)
        self.quickSendTable.setRowCount(50)
        self.quickSendTable.setColumnCount(20)

        for row in range(50):
            item = QPushButton(str("Send"))
            item.clicked.connect(self._signalMap.map)
            self._signalMap.setMapping(item, row)
            self.quickSendTable.setCellWidget(row, 0, item)
            self.quickSendTable.setRowHeight(row, 20)

        if os.path.isfile('QckSndBckup.csv'):
            self.loadCSV('QckSndBckup.csv')

        self.quickSendTable.resizeColumnsToContents()

    def openCSV(self):
        fileName = QFileDialog.getOpenFileName(self, "Select a file",
            os.getcwd(), "CSV Files (*.csv)")
        if fileName:
            self.loadCSV(fileName, notifyExcept = True)

    def saveCSV(self):
        # scan table
        rows = self.quickSendTable.rowCount()
        cols = self.quickSendTable.columnCount()

        tmp_data = [[self.quickSendTable.item(row, col) is not None
                    and self.quickSendTable.item(row, col).text() or ''
                    for col in range(1, cols)] for row in range(rows)]

        data = []
        # delete trailing blanks
        for row in tmp_data:
            for idx, d in enumerate(row[::-1]):
                if '' != d:
                    break
            new_row = row[:len(row) - idx]
            data.append(new_row)

        #import pprint
        #pprint.pprint(data, width=120, compact=True)

        # write to file
        with open('QckSndBckup.csv', 'w') as csvfile:
            csvwriter = csv.writer(csvfile, delimiter=',', lineterminator='\n')
            csvwriter.writerows(data)

    def loadCSV(self, path, notifyExcept = False):
        data = []
        set_rows = 0
        set_cols = 0
        try:
            with open(path) as csvfile:
                csvData = csv.reader(csvfile)
                for row in csvData:
                    data.append(row)
                    set_rows = set_rows + 1
                    if len(row) > set_cols:
                        set_cols = len(row)
        except IOError as e:
            print("({})".format(e))
            if notifyExcept:
                QMessageBox.critical(self, "Open failed", str(e), QMessageBox.Close)
            return

        rows = self.quickSendTable.rowCount()
        cols = self.quickSendTable.columnCount()
        # clear table
        for col in range(cols):
            for row in range(rows):
                self.quickSendTable.setItem(row, col, QTableWidgetItem(""))

        self._csvFilePath = path
        if (cols - 1) < set_cols:   # first colume is used by the "send" buttons.
            cols = set_cols + 10
            self.quickSendTable.setColumnCount(cols)
        if rows < set_rows:
            rows = set_rows + 20
            self.quickSendTable.setRowCount(rows)

        for row, rowdat in enumerate(data):
            if len(rowdat) > 0:
                for col, cell in enumerate(rowdat, 1):
                    self.quickSendTable.setItem(row, col, QTableWidgetItem(str(cell)))

        self.quickSendTable.resizeColumnsToContents()
        #self.quickSendTable.resizeRowsToContents()

    def sendTableRow(self, row):
        cols = self.quickSendTable.columnCount()
        try:
            data = ['0' + self.quickSendTable.item(row, col).text()
                for col in range(1, cols)
                if self.quickSendTable.item(row, col) is not None
                    and self.quickSendTable.item(row, col).text() is not '']
        except:
            print("Exception in get table data(row = %d)" % (row + 1))
        else:
            tmp = [d[-2] + d[-1] for d in data if len(d) >= 2]
            for t in tmp:
                if not is_hex(t):
                    QMessageBox.critical(self, "Error",
                        "'%s' is not hexadecimal." % (t), QMessageBox.Close)
                    return

            h = [int(t, 16) for t in tmp]
            self.transmitHex(h)

    def sendHex(self):
        hexStr = self.txtEdtInput.toPlainText()
        hexStr = ''.join(hexStr.split(" "))

        hexarray = []
        for i in range(0, len(hexStr), 2):
            hexarray.append(int(hexStr[i:i+2], 16))

        self.transmitHex(hexarray)

    def readerExcept(self, e):
        self.closePort()
        QMessageBox.critical(self, "Read failed", str(e), QMessageBox.Close)

    def timestamp(self):
        return datetime.datetime.now().time().isoformat()[:-3]

    def receive(self, data):
        self.appendOutputText("\n%s R<-:%s" % (self.timestamp(), data))

    def appendOutputText(self, data, color=Qt.black):
        # the qEditText's "append" methon will add a unnecessary newline.
        # self.txtEdtOutput.append(data.decode('utf-8'))

        tc=self.txtEdtOutput.textColor()
        self.txtEdtOutput.moveCursor(QtGui.QTextCursor.End)
        self.txtEdtOutput.setTextColor(QtGui.QColor(color))
        self.txtEdtOutput.insertPlainText(data)
        self.txtEdtOutput.moveCursor(QtGui.QTextCursor.End)
        self.txtEdtOutput.setTextColor(tc)

    def transmitHex(self, hexarray):
        if len(hexarray) > 0:
            byteArray = bytearray(hexarray)
            if self.serialport.isOpen():
                try:
                    self.serialport.write(byteArray)
                except serial.SerialException as e:
                    print("Exception in transmitHex(%s)" % repr(hexarray))
                    QMessageBox.critical(self, "Exception in transmitHex", str(e),
                        QMessageBox.Close)
                else:
                    # self.txCount += len( b )
                    # self.frame.statusbar.SetStatusText('Tx:%d' % self.txCount, 2)

                    text = ''.join(['%02X ' % i for i in hexarray])
                    self.appendOutputText("\n%s T->:%s" % (self.timestamp(), text),
                        Qt.blue)

    def GetPort(self):
        return self.cmbPort.currentText()

    def GetDataBits(self):
        s = self.cmbDataBits.currentText()
        if s == '5':
            return serial.FIVEBITS
        elif s == '6':
            return serial.SIXBITS
        elif s == '7':
            return serial.SEVENBITS
        elif s == '8':
            return serial.EIGHTBITS

    def GetParity(self):
        s = self.cmbParity.currentText()
        if s == 'None':
            return serial.PARITY_NONE
        elif s == 'Even':
            return serial.PARITY_EVEN
        elif s == 'Odd':
            return serial.PARITY_ODD
        elif s == 'Mark':
            return serial.PARITY_MARK
        elif s == 'Space':
            return serial.PARITY_SPACE

    def GetStopBits(self):
        s = self.cmbStopBits.currentText()
        if s == '1':
            return serial.STOPBITS_ONE
        elif s == '1.5':
            return serial.STOPBITS_ONE_POINT_FIVE
        elif s == '2':
            return serial.STOPBITS_TWO

    def openPort(self):
        if self.serialport.isOpen():
            return

        _port = self.GetPort()
        if '' == _port:
            QMessageBox.information(self, "Invalid parameters", "Port is empty.")
            return

        _baudrate = self.cmbBaudRate.currentText()
        if '' == _baudrate:
            QMessageBox.information(self, "Invalid parameters", "Baudrate is empty.")
            return

        self.serialport.port     = _port
        self.serialport.baudrate = _baudrate
        self.serialport.bytesize = self.GetDataBits()
        self.serialport.stopbits = self.GetStopBits()
        self.serialport.parity   = self.GetParity()
        self.serialport.rtscts   = self.chkRTSCTS.isChecked()
        self.serialport.xonxoff  = self.chkXonXoff.isChecked()
        # self.serialport.timeout  = THREAD_TIMEOUT
        # self.serialport.writeTimeout = SERIAL_WRITE_TIMEOUT
        try:
            self.serialport.open()
        except serial.SerialException as e:
            QMessageBox.critical(self, "Could not open serial port", str(e),
                QMessageBox.Close)
        else:
            self._start_reader()
            self.setWindowTitle("%s on %s [%s, %s%s%s%s%s]" % (
                appInfo.title,
                self.serialport.portstr,
                self.serialport.baudrate,
                self.serialport.bytesize,
                self.serialport.parity,
                self.serialport.stopbits,
                self.serialport.rtscts and ' RTS/CTS' or '',
                self.serialport.xonxoff and ' Xon/Xoff' or '',
                )
            )
            pal = self.btnOpen.palette()
            pal.setColor(QtGui.QPalette.Button, QtGui.QColor(0,0xff,0x7f))
            self.btnOpen.setAutoFillBackground(True)
            self.btnOpen.setPalette(pal)
            self.btnOpen.setText('Close')
            self.btnOpen.update()

    def closePort(self):
        if self.serialport.isOpen():
            self._stop_reader()
            self.serialport.close()
            self.setWindowTitle(appInfo.title)
            pal = self.btnOpen.style().standardPalette()
            self.btnOpen.setAutoFillBackground(True)
            self.btnOpen.setPalette(pal)
            self.btnOpen.setText('Open')
            self.btnOpen.update()

    def _start_reader(self):
        """Start reader thread"""
        self.receiver_thread.start()

    def _stop_reader(self):
        """Stop reader thread only, wait for clean exit of thread"""
        self.receiver_thread.join()

    def onTogglePrtCfgPnl(self):
        if self.actionPort_Config_Panel.isChecked():
            self.dockWidget_PortConfig.show()
        else:
            self.dockWidget_PortConfig.hide()

    def onToggleQckSndPnl(self):
        if self.actionQuick_Send_Panel.isChecked():
            self.dockWidget_QuickSend.show()
        else:
            self.dockWidget_QuickSend.hide()

    def onToggleHexPnl(self):
        if self.actionSend_Hex_Panel.isChecked():
            self.dockWidget_SendHex.show()
        else:
            self.dockWidget_SendHex.hide()

    def onVisiblePrtCfgPnl(self, visible):
        self.actionPort_Config_Panel.setChecked(visible)

    def onVisibleQckSndPnl(self, visible):
        self.actionQuick_Send_Panel.setChecked(visible)

    def onVisibleHexPnl(self, visible):
        self.actionSend_Hex_Panel.setChecked(visible)

    def onLocalEcho(self):
        self._localEcho = self.actionLocal_Echo.isChecked()

    def onAlwaysOnTop(self):
        if self.actionAlways_On_Top.isChecked():
            style = self.windowFlags()
            self.setWindowFlags(style|Qt.WindowStaysOnTopHint)
            self.show()
        else:
            style = self.windowFlags()
            self.setWindowFlags(style & ~Qt.WindowStaysOnTopHint)
            self.show()

    def onOpen(self):
        if self.serialport.isOpen():
            self.closePort()
        else:
            self.openPort()

    def onClear(self):
        self.txtEdtOutput.clear()

    def onSaveLog(self):
        fileName = QFileDialog.getSaveFileName(self, "Save as", os.getcwd(),
            "Log files (*.log);;Text files (*.txt);;All files (*.*)")
        if fileName:
            import codecs
            f = codecs.open(fileName, 'w', 'utf-8')
            f.write(self.txtEdtOutput.toPlainText())
            f.close()

    def moveScreenCenter(self):
        w = self.frameGeometry().width()
        h = self.frameGeometry().height()
        desktop = QDesktopWidget()
        screenW = desktop.screen().width()
        screenH = desktop.screen().height()
        self.setGeometry((screenW-w)/2, (screenH-h)/2, w, h)

    def onEnumPorts(self):
        for p in enum_ports():
            self.cmbPort.addItem(p)
        # self.cmbPort.update()

    def onAbout(self):
        q = QWidget()
        icon = QtGui.QIcon(":/icon.ico")
        q.setWindowIcon(icon)
        QMessageBox.about(q, "About MyTerm", appInfo.aboutme)

    def onAboutQt(self):
        QMessageBox.aboutQt(None)

    def onExit(self):
        if self.serialport.isOpen():
            self.closePort()
        self.close()

    def restoreLayout(self):
        if os.path.isfile("layout.dat"):
            try:
                f=open("layout.dat", 'rb')
                geometry, state=pickle.load(f)
                self.restoreGeometry(geometry)
                self.restoreState(state)
            except Exception as e:
                print("Exception on restoreLayout, {}".format(e))

    def saveLayout(self):
        with open("layout.dat", 'wb') as f:
            pickle.dump((self.saveGeometry(), self.saveState()), f)

    def syncMenu(self):
        self.actionPort_Config_Panel.setChecked(not self.dockWidget_PortConfig.isHidden())
        self.actionQuick_Send_Panel.setChecked(not self.dockWidget_QuickSend.isHidden())
        self.actionSend_Hex_Panel.setChecked(not self.dockWidget_SendHex.isHidden())

    def onViewChanged(self):
        checked = self._viewGroup.checkedAction()
        if checked is None:
            self.actionHEX_UPPERCASE.setChecked(True)
            self.receiver_thread.setViewMode(VIEWMODE_HEX_UPPERCASE)
        else:
            if 'Ascii' in checked.text():
                self.receiver_thread.setViewMode(VIEWMODE_ASCII)
            elif 'lowercase' in checked.text():
                self.receiver_thread.setViewMode(VIEWMODE_HEX_LOWERCASE)
            elif 'UPPERCASE' in checked.text():
                self.receiver_thread.setViewMode(VIEWMODE_HEX_UPPERCASE)

def is_hex(s):
    try:
        int(s, 16)
        return True
    except ValueError:
        return False

if __name__ == '__main__':
    app = QApplication(sys.argv)
    frame = MainWindow()
    frame.show()
    app.exec_()
