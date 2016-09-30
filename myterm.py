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
import threading

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, \
    QFileDialog, QTableWidgetItem, QPushButton
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QSignalMapper

import appInfo
from gui_qt5.ui_mainwindow import Ui_MainWindow

import serial

if os.name == 'nt':
    FONT_FAMILY = "Consolas"
elif os.name == 'posix':
    FONT_FAMILY = "Courier 10 Pitch"


class readerThread(QThread):
    """loop and copy serial->GUI"""
    read = pyqtSignal(str)
    exception = pyqtSignal(str)

    def __init__(self, parent=None):
        super(readerThread, self).__init__(parent)
        self._alive = None

    def setPort(self, port):
        self.serialport = port

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

        self.setupUi(self)
        self.setCorner(Qt.TopLeftCorner, Qt.LeftDockWidgetArea)
        self.setCorner(Qt.BottomLeftCorner, Qt.LeftDockWidgetArea)
        font = QtGui.QFont()
        font.setFamily(FONT_FAMILY)
        font.setPointSize(10)
        self.txtEdtOutput.setFont(font)
        self.onEnumPorts()
        self.moveScreenCenter()


        self.actionOpen.triggered.connect(self.onOpen)
        self.actionAbout.triggered.connect(self.onAbout)
        self.actionAbout_Qt.triggered.connect(self.onAboutQt)
        self.actionExit.triggered.connect(self.onExit)

        self.btnOpen.clicked.connect(self.onOpen)

        self.btnEnumPorts.clicked.connect(self.onEnumPorts)
        self.actionShow_Hex_Transmit_Panel.triggered.connect(self.onHideHexPnl)
        self.receiver_thread.read.connect(self.receive)
        self.receiver_thread.exception.connect(self.readerExcept)
        self._signalMap = QSignalMapper(self)
        self._signalMap.mapped[int].connect(self.tableClick)

        self.openCSV()

    def tableClick(self, row):
        self.sendTableRow(row)

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
                self._table_cols = cols
        except IOError as e:
            print("({})".format(e))
            return

        self._csvFilePath = path
        self.table.setRowCount(rows)
        self.table.setColumnCount(cols)

        for row, rowdat in enumerate(data):
            if rowdat[1] == '':
                self.table.setItem(row, 0, QTableWidgetItem(str(rowdat[0])))
            else:
                item = QPushButton(str(rowdat[0]))
                item.clicked.connect(self._signalMap.map)
                self._signalMap.setMapping(item, row)
                self.table.setCellWidget(row, 0, item)
                self.table.setRowHeight(row, 20)
                for col, cell in enumerate(rowdat[1:], 1):
                    self.table.setItem(row, col, QTableWidgetItem(str(cell)))

        self.table.resizeColumnsToContents()
        #self.table.resizeRowsToContents()

    def sendTableRow(self, row):
        try:
            data = ['0' + self.table.item(row, col).text()
                for col in range(self._table_cols)
                if self.table.item(row, col) is not None]
        except:
            raise
            # print("Exception in sendTableRow(row = %d)" % (row + 1))
        else:
            # print(data)
            h = [int(d[-2] + d[-1], 16) for d in data if d is not '']
            # print(repr(h))
            b = bytearray(h)
            # str = ''.join([chr(m) for m in data])
            # print(repr(b))

            if self.serialport.isOpen():
                try:
                    self.serialport.write(b)
                    print(repr(b))
                except serial.SerialException as e:
                    raise
                    # evt = SerialExceptEvent(self.frame.GetId(), e)
                    # self.frame.GetEventHandler().AddPendingEvent(evt)
                else:
                    # self.txCount += len( b )
                    # self.frame.statusbar.SetStatusText('Tx:%d' % self.txCount, 2)

                    import datetime
                    text = ''.join(['%02X ' % i for i in h])
                    # self.frame.txtctlMain.SetDefaultStyle(wx.TextAttr(colText=(0, 0, 255), alignment = wx.TEXT_ATTR_TEXT_COLOUR))
                    self.receive("\n%s T->:%s" % (datetime.datetime.now().time().isoformat()[:-3], text))
                    # self.frame.txtctlMain.SetDefaultStyle(wx.TextAttr(colText=(0, 0, 0), alignment = wx.TEXT_ATTR_TEXT_COLOUR))

    def readerExcept(self, e):
        QMessageBox.critical(self, "Read failed", str(e), QMessageBox.Close)
        self.closePort()

    def receive(self, data):
        # the "append" methon will add a newline which is unnecessarily.
        # self.txtEdtOutput.append(data.decode('utf-8'))

        # print(repr(data))
        self.txtEdtOutput.moveCursor(QtGui.QTextCursor.End)
        self.txtEdtOutput.insertPlainText(data)
        self.txtEdtOutput.moveCursor(QtGui.QTextCursor.End)

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

    def onHideHexPnl(self):
        if self.txtEdtInput.isVisible():
            self.txtEdtInput.hide()
        else:
            self.txtEdtInput.show()

    def onOpen(self):
        if self.serialport.isOpen():
            self.closePort()
        else:
            self.openPort()

    def moveScreenCenter(self):
        w = self.frameGeometry().width()
        h = self.frameGeometry().height()
        desktop = QtWidgets.QDesktopWidget()
        screenW = desktop.screen().width()
        screenH = desktop.screen().height()
        self.setGeometry((screenW-w)/2, (screenH-h)/2, w, h)

    def onEnumPorts(self):
        from enum_ports import enum_ports
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

if __name__ == '__main__':
    app = QApplication(sys.argv)
    frame = MainWindow()
    frame.show()
    app.exec_()
