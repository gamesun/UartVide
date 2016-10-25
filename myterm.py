#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
#
#############################################################################
##
## Copyright (c) 2013-2016, gamesun
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
import threading
import pickle
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, \
    QFileDialog, QTableWidgetItem, QPushButton, QActionGroup, QDesktopWidget
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QSignalMapper

import appInfo
from gui_qt5.ui_mainwindow import Ui_MainWindow
from res import resources
from enum_ports import enum_ports

import serial

if os.name == 'nt':
    FONT_FAMILY = "Consolas"
elif os.name == 'posix':
    FONT_FAMILY = "Courier 10 Pitch"

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
        self._viewMode = None

    def setPort(self, port):
        self.serialport = port

    def setViewMode(self, mode):
        self._viewMode = mode

    def start(self, priority = QThread.InheritPriority):
        self._alive = True
        super(readerThread, self).start(priority)

    def __del__(self):
        if self._alive:
            self._alive = False
            if hasattr(self.serialport, 'cancel_read'):
                self.serialport.cancel_read()
        self.wait()

    def join(self):
        self.__del__()

    def run(self):
        # print("readerThread id:{}".format(self.currentThreadId()))
        text = str()
        try:
            while self._alive:
                # read all that is there or wait for one byte
                data = self.serialport.read(self.serialport.in_waiting or 1)
                if data:
                    # self.txtEdtOutput.append(data.decode('utf-8'))
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
        self.receiver_thread = readerThread()
        self.receiver_thread.setPort(self.serialport)
        self._table_cols = 0
        self._table_rows = 0
        self._localEcho = None

        self.setupUi(self)
        self.setCorner(Qt.TopLeftCorner, Qt.LeftDockWidgetArea)
        self.setCorner(Qt.BottomLeftCorner, Qt.LeftDockWidgetArea)
        font = QtGui.QFont()
        font.setFamily(FONT_FAMILY)
        font.setPointSize(10)
        self.txtEdtOutput.setFont(font)
        self.quickSendTable.setFont(font)
        self.onEnumPorts()
        self.moveScreenCenter()

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
        self.syncMenu()

    def closeEvent(self, event):
        self.saveLayout()
        super(MainWindow, self).closeEvent(event)

    def tableClick(self, row):
        self.sendTableRow(row)

    def initQuickSend(self):
#        self.quickSendTable.horizontalHeader().setDefaultSectionSize(40)
#        self.quickSendTable.horizontalHeader().setMinimumSectionSize(25)
        self._table_cols = 20
        self._table_rows = 50
        self.quickSendTable.setRowCount(self._table_rows)
        self.quickSendTable.setColumnCount(self._table_cols)
        
        for row in range(self._table_rows):
            item = QPushButton(str("Send"))
            item.clicked.connect(self._signalMap.map)
            self._signalMap.setMapping(item, row)
            self.quickSendTable.setCellWidget(row, 0, item)
            self.quickSendTable.setRowHeight(row, 20)

        self.quickSendTable.resizeColumnsToContents()
        
    def openCSV(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Select a file",
            os.getcwd(), "CSV Files (*.csv)")
        if fileName:
            self.loadCSV(fileName)

    def loadCSV(self, path):
        import csv
        data = []
        rows = 0
        cols = 0
        try:
            with open(path) as csvfile:
                csvData = csv.reader(csvfile)
                for row in csvData:
                    data.append(row)
                    rows = rows + 1
                    if len(row) > cols:
                        cols = len(row)
        except IOError as e:
            print("({})".format(e))
            return

        self._csvFilePath = path
        if self._table_cols < cols:
            self._table_cols = cols + 10
            self.quickSendTable.setColumnCount(self._table_cols)
        if self._table_rows < rows:
            self._table_rows = rows + 20
            self.quickSendTable.setRowCount(self._table_rows)
        
        for row, rowdat in enumerate(data):
            if rowdat[1] == '':
                self.quickSendTable.setItem(row, 0, QTableWidgetItem(str(rowdat[0])))
            else:
                item = QPushButton(str(rowdat[0]))
                item.clicked.connect(self._signalMap.map)
                self._signalMap.setMapping(item, row)
                self.quickSendTable.setCellWidget(row, 0, item)
                self.quickSendTable.setRowHeight(row, 20)
                for col, cell in enumerate(rowdat[1:], 1):
                    self.quickSendTable.setItem(row, col, QTableWidgetItem(str(cell)))

        self.quickSendTable.resizeColumnsToContents()
        #self.quickSendTable.resizeRowsToContents()

    def sendTableRow(self, row):
        try:
            data = ['0' + self.quickSendTable.item(row, col).text()
                for col in range(1, self._table_cols)
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
        QMessageBox.critical(self, "Read failed", str(e), QMessageBox.Close)
        self.closePort()

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
        # if sys.platform == 'win32':
        #     r = regex_matchPort.search(self.frame.cmbPort.GetValue())
        #     if r:
        #         return int(r.group('port')) - 1
        #     return
        # elif sys.platform.startswith('linux'):
        #     return self.frame.cmbPort.GetValue()
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

        if '' == self.GetPort():
            QMessageBox.information(self, "Invalid parameters", "Port is empty!")
            return

        _baudrate = self.cmbBaudRate.currentText()
        if _baudrate == '':
            QMessageBox.information(self, "Invalid parameters", "Baudrate is empty!")
            return

        self.serialport.port     = self.GetPort()
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
        # start serial->console thread
        # self.receiver_thread = threading.Thread(target=self.reader, name='rx')
        # self.receiver_thread.daemon = True
        # self.receiver_thread.start()
        self.receiver_thread.start()

    def _stop_reader(self):
        """Stop reader thread only, wait for clean exit of thread"""
        # if hasattr(self.serialport, 'cancel_read'):
        #     self.serialport.cancel_read()
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
        fileName, _ = QFileDialog.getSaveFileName(self, "Save as", os.getcwd(), 
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
        QMessageBox.about(self, "", "")


    def onAboutQt(self):
        QMessageBox.aboutQt(self)

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
