#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
#
# Copyright (c) 2013-2014,2016 gamesun
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#
#     * Redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above
# copyright notice, this list of conditions and the following disclaimer
# in the documentation and/or other materials provided with the
# distribution.
#     * Neither the name of gamesun nor the names of its contributors
# may be used to endorse or promote products derived from this software
# without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY GAMESUN "AS IS" AND ANY EXPRESS OR
# IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL GAMESUN BE LIABLE FOR ANY DIRECT,
# INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
# HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
# STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING
# IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#

import sys, os
import threading

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox
from PyQt5.QtCore import QThread, pyqtSignal

import appInfo
from gui_qt5.ui_mainwindow import Ui_MainWindow

import serial

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
                        text = text + data.decode('unicode_escape')
                    except UnicodeDecodeError:
                        pass
                    if -1 != text.find('\r\n'):
                        print(repr(text))
                        text = text.replace('\r\n', '\n')
                        text = text.replace('\n\n', '\n')
                        if text[0] == '\n':
                            text = text[1:]
                        self.read.emit(text)
                        text = str()
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
        self.serialport = serial.Serial()
        self.receiver_thread = readerThread()
        self.receiver_thread.setPort(self.serialport)

        self.setupUi(self)
        self.onEnumPorts()
        self.moveScreenCenter()


        self.actionOpen.triggered.connect(self.onOpen)

        self.btnOpen.clicked.connect(self.onOpen)
        self.btnEnumPorts.clicked.connect(self.onEnumPorts)
        self.actionShow_Hex_Transmit_Panel.triggered.connect(self.onHideHexPnl)
        self.receiver_thread.read.connect(self.receive)
        self.receiver_thread.exception.connect(self.readerExcept)

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

if __name__ == '__main__':
    app = QApplication(sys.argv)
    frame = MainWindow()
    frame.show()
    app.exec_()
