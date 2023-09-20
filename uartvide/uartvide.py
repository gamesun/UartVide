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

import sys, os
extension = os.path.splitext(sys.argv[0])[1]
if extension != '.py':
    import except_logger
    sys.excepthook = except_logger.exceptHook
    
    # if os.name == 'nt':
    #     app_path = os.path.dirname(os.path.abspath(__file__))
    #     try:os.mkdir(app_path+"\\DLLs\\")
    #     except: pass
        
    #     os.add_dll_directory(app_path+"\\DLLs\\")
    #     sys.path.append(app_path+"\\DLLs\\")

        #import ctypes
        #dll_lst = [f for f in os.listdir(app_path+"\\DLLs\\") if f.endswith(".dll")]
        #for d in dll_lst:
            #try:ctypes.WinDLL(app_path+"\\DLLs\\"+d)
            #except:pass

from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from qfluentwidgets import *
from qframelesswindow import *
from res import resources_rc
from ui.mainwindow_ui import Ui_MainWindow

from functools import partial
from widgets.rightanglecombobox import RightAngleComboBox
from widgets.animationswitchbutton import AnimationSwitchButton
from rename_dailog import RenameDailog

import datetime
import pickle
import csv
from lxml import etree as ET
import defusedxml.ElementTree as safeET 
import appInfo
from configpath import get_config_path

import serial
from serial.tools.list_ports import comports
from time import sleep
import re


if os.name == 'nt':
    CODE_FONT = "Consolas"
    UI_FONT = "Tahoma"
elif os.name == 'posix':
    CODE_FONT = "Monospace"
    UI_FONT = "Ubuntu"

class MainWindow(FramelessMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__()
        self._csvFilePath = ""
        self.serialport = serial.Serial()
        self.readerThread = ReaderThread(self)
        self.readerThread.setPort(self.serialport)
        self.portMonitorThread = PortMonitorThread(self)
        self.portMonitorThread.start()
        self.loopSendThread = LoopSendThread(self)
        self._is_always_on_top = False
        self._viewMode = 'HEX'
        self._is_loop_sending = False
        self._is_timestamp = False
        self._qckSnd_SelectingRow = 0

        self.setupUi(self)
        self.setCorner(Qt.TopLeftCorner, Qt.LeftDockWidgetArea)
        self.setCorner(Qt.BottomLeftCorner, Qt.LeftDockWidgetArea)

        # fdb=QFontDatabase()
        # fontId = fdb.addApplicationFont(".ttf")
        # print("fontId = ", fontId)
        # fontFamily = QFontDatabase.applicationFontFamilies(fontId)[0]
        # print("fontFamily = ", fontFamily)
        # self.setFont(QFont(msyh))

        font1 = QFont(UI_FONT, 10, QFont.Normal, False)
        font1.setKerning(True)
        font1.setStyleStrategy(QFont.PreferAntialias)
        self.setFont(font1)

        self.initMoreSettingsMenu()
        self.initQckSndOptMenu()
        self.setupFlatUi()
        self.setupTitleBar()

        font2 = QFont(CODE_FONT, 9, QFont.Normal, False)
        font2.setKerning(True)
        font2.setStyleStrategy(QFont.PreferAntialias)
        self.txtEdtOutput.setFont(font2)
        self.txtEdtInput.setFont(font2)
        #self.qckSndTbl.setFont(font2)
        
        icon = QIcon(":/uartvide-icon/uartvide.ico")
        self.setWindowIcon(icon)
        self.actionAbout.setIcon(icon)

        self.defaultStyleWidget = QWidget()
        self.defaultStyleWidget.setWindowIcon(icon)

        # bind events
        self.dockWidget_QuickSend.visibilityChanged.connect(self.onVisibleQckSndPnl)
        self.dockWidget_Send.visibilityChanged.connect(self.onVisibleSndPnl)
        # self.dockWidget_QuickSend.dockLocationChanged.connect(self.onDockLocationChanged)

        self.cmbBaudRate.currentTextChanged.connect(self.onBaudRateChanged)
        self.cmbDataBits.currentTextChanged.connect(self.onDataBitsChanged)
        self.cmbStopBits.currentTextChanged.connect(self.onStopBitsChanged)
        self.cmbParity.currentTextChanged.connect(self.onParityChanged)
        self.chkRTSCTS.stateChanged.connect(self.onRTSCTSChanged)
        self.chkXonXoff.stateChanged.connect(self.onXonXoffChanged)
        
        self.btnSend.clicked.connect(self.onSend)
        
        self.loopSendThread.trigger.connect(self.onPeriodTrigger)

        self.readerThread.read.connect(self.onReceive)
        self.readerThread.exception.connect(self.onReaderExcept)

        self.portMonitorThread.portsListChanged.connect(self.onPortsListChanged)
        self.portMonitorThread.exception.connect(self.onPortMonitorExcept)

        # initial action
        self.setTabWidth(4)
        self.initQuickSend()
        self.restoreLayout()
        self.moveScreenCenter()
        self.syncMenu()
        self.setPortCfgBarVisible(False)
        
        self.rdoHEX.setChecked(True)
        self._is_loop_mode = False
        self.spnPeriod.setEnabled(False)

        self.loadSettings()
        self.onEnumPorts()
        # self.onClearRxTxCnt()

        self.titleBar.raise_()

    def setTabWidth(self, n):
        fm = QFontMetrics(self.txtEdtOutput.fontMetrics())
        if hasattr(fm, 'horizontalAdvance'):
            w = fm.horizontalAdvance(' ')
        else:
            w = fm.width(' ')
        self.txtEdtOutput.setTabStopWidth(n * w)
        
        fm = QFontMetrics(self.txtEdtInput.fontMetrics())
        if hasattr(fm, 'horizontalAdvance'):
            w = fm.horizontalAdvance(' ')
        else:
            w = fm.width(' ')
        self.txtEdtInput.setTabStopWidth(n * w)

    def onBaudRateChanged(self, text):
        try:
            prev_baudrate = self.serialport.baudrate
            self.serialport.baudrate = self.cmbBaudRate.currentText()
        except Exception as e:
            self.cmbBaudRate.setCurrentText(str(prev_baudrate))
        
    def onDataBitsChanged(self, text):
        self.serialport.bytesize = self.getDataBits()
        
    def onStopBitsChanged(self, text):
        try:
            self.serialport.stopbits = self.getStopBits()
        except ValueError:
            self.cmbStopBits.setCurrentText('1')
        except Exception as e:
            self.cmbStopBits.setCurrentText('1')
    
    def onParityChanged(self, text):
        self.serialport.parity = self.getParity()
        
    def onRTSCTSChanged(self, state):
        self.serialport.rtscts = self.chkRTSCTS.isChecked()
        
    def onXonXoffChanged(self, state):
        self.serialport.xonxoff = self.chkXonXoff.isChecked()

    def initMoreSettingsMenu(self):
        self.actionSave_Log = Action(FluentIcon.SAVE, self.tr('Save Log'))
        self.actionSave_Log.triggered.connect(self.onSaveLog)

        self.actionExit = Action(FluentIcon.CLOSE, self.tr('Exit'))
        self.actionExit.triggered.connect(self.close)   # -> closeEvent

        self.actionSend_Panel = Action(FluentIcon.VIEW, self.tr('Send Panel'))
        self.actionSend_Panel.setCheckable(True)
        self.actionSend_Panel.triggered.connect(self.onToggleSndPnl)

        self.actionAbout = Action(self.tr('About'))
        self.actionAbout.triggered.connect(self.onAbout)

        self.actionOpen_Cmd_File = Action(FluentIcon.EDIT, self.tr('Load Quick Send CSV'))
        self.actionOpen_Cmd_File.triggered.connect(self.openQuickSendFile)

        self.actionQuick_Send_Panel = Action(FluentIcon.VIEW, self.tr('Quick Send Panel'))
        self.actionQuick_Send_Panel.setCheckable(True)
        self.actionQuick_Send_Panel.triggered.connect(self.onToggleQckSndPnl)
        
        # self.actionParse_Panel = Action(FluentIcon., self.tr('Parse Panel'))

        self.menuMoreSettings = CheckableMenu(self.titleBar)
        self.menuMoreSettings.addAction(self.actionOpen_Cmd_File)
        self.menuMoreSettings.addAction(self.actionSave_Log)
        self.menuMoreSettings.addSeparator()
        self.menuMoreSettings.addAction(self.actionQuick_Send_Panel)
        self.menuMoreSettings.addAction(self.actionSend_Panel)
        self.menuMoreSettings.addSeparator()
        self.menuMoreSettings.addAction(self.actionAbout)
        self.menuMoreSettings.addSeparator()
        self.menuMoreSettings.addAction(self.actionExit)
        # self.menuMoreSettings.setStyleSheet('''
        #     QMenu {margin: 2px;color: #202020;background: #eeeeee;}
        #     /*QMenu::item {padding: 2px 22px 2px 2px;border: 1px solid transparent;}*/
        #     QMenu::item:selected {background: #51c0d1;}
        #     QMenu::icon {background: transparent;border: 2px inset transparent;}
        #     QMenu::item:disabled {color: #808080;background: #eeeeee;}''')

    def initQckSndOptMenu(self):
        self.actionRename = QtWidgets.QAction("Rename", self)
        self.actionRename.triggered.connect(self.onQckSnd_Rename)

        self.actionInsertRow = QtWidgets.QAction("Insert row", self)
        self.actionInsertRow.triggered.connect(self.onQckSnd_InsertRow)

        self.actionDeleteRow = QtWidgets.QAction("Delete row", self)
        self.actionDeleteRow.triggered.connect(self.onQckSnd_RemoveRow)

        self.actionSend_Hex = QtWidgets.QAction("HEX", self)
        self.actionSend_Hex.triggered.connect(partial(self.onQckSnd_SelectFormat, 'H'))

        self.actionSend_Asc = QtWidgets.QAction("ASCII", self)
        self.actionSend_Asc.triggered.connect(partial(self.onQckSnd_SelectFormat, 'A'))

        self.actionSend_AscS = QtWidgets.QAction(r"ASCII and \n \r \t...", self)
        self.actionSend_AscS.triggered.connect(partial(self.onQckSnd_SelectFormat, 'AS'))
        
        self.actionSend_HF = QtWidgets.QAction(self)
        self.actionSend_HF.setText("HEX text File")
        self.actionSend_HF.setStatusTip('Send text file in HEX form("31 32 FF ...")')
        self.actionSend_HF.triggered.connect(partial(self.onQckSnd_SelectFormat, 'HF'))
        
        self.actionSend_AF = QtWidgets.QAction(self)
        self.actionSend_AF.setText("ASCII text file")
        self.actionSend_AF.setStatusTip('Send text file in ASCII form("abc123...")')
        self.actionSend_AF.triggered.connect(partial(self.onQckSnd_SelectFormat, 'AF'))
        
        self.actionSend_BF = QtWidgets.QAction("Bin file; All file", self)
        self.actionSend_BF.triggered.connect(partial(self.onQckSnd_SelectFormat, 'BF'))

        # self.actSendFormat = RoundMenu('Send Format', parent=self)

        # self.actSendFormat.addAction(self.actionSend_Hex)
        # self.actSendFormat.addAction(self.actionSend_Asc)
        # self.actSendFormat.addAction(self.actionSend_AscS)
        # self.actSendFormat.addAction(self.actionSend_HF)
        # self.actSendFormat.addAction(self.actionSend_AF)
        # self.actSendFormat.addAction(self.actionSend_BF)

        self.menuSendOpt = RoundMenu(parent=self)
        self.menuSendOpt.addAction(self.actionRename)
        self.menuSendOpt.addAction(self.actionInsertRow)
        self.menuSendOpt.addAction(self.actionDeleteRow)
        
        self.menuSendOpt.addSeparator()
        self.menuSendOpt.addAction(self.actionSend_Hex)
        self.menuSendOpt.addAction(self.actionSend_Asc)
        self.menuSendOpt.addAction(self.actionSend_AscS)
        self.menuSendOpt.addAction(self.actionSend_HF)
        self.menuSendOpt.addAction(self.actionSend_AF)
        self.menuSendOpt.addAction(self.actionSend_BF)

    def setupFlatUi(self):
        self._dragPos = self.pos()
        self._isDragging = False
        self._isResizing = False
        self._resizeArea = 0
        self.setMouseTracking(True)
        self.setStyleSheet("""
            QWidget { background-color: %(BackgroundColor)s; outline: none; }
            QToolBar { border: none; }
            QLabel { color:%(TextColor)s; font-size:10pt; font-family:%(UIFont)s; }

            QComboBox {
                color:%(TextColor)s;
                font-size:10pt;
                font-family:%(UIFont)s;
                border: none;
                padding: 1px 1px 1px 3px;
            }
            QComboBox:editable { background: white; }
            QComboBox:!editable, QComboBox::drop-down:editable { background: #62c7e0; }
            QComboBox:!editable:hover, QComboBox::drop-down:editable:hover { background: #c7eaf3; }
            QComboBox:!editable:pressed, QComboBox::drop-down:editable:pressed { background: #35b6d7; }
            QComboBox:!editable:disabled, QComboBox::drop-down:editable:disabled { background: #c0c0c0; }
            QComboBox:on { padding-top: 3px; padding-left: 4px; font-size:10pt;}
            QComboBox::drop-down { subcontrol-origin: padding; subcontrol-position: top right; 
                width: 16px; border: none; font-size: 10pt; }
            QComboBox::down-arrow { image: url(:/images/downarrow.png); }
            QComboBox::down-arrow:on { image: url(:/images/uparrow.png); }
            QComboBox QAbstractItemView { font-family:%(UIFont)s; outline: none; color:%(TextColor)s; 
                background: white; font-size:10pt; margin-top: 2px; margin-bottom: 1px;
                padding-left: 2px; padding-right: 2px; }
            QComboBox QAbstractItemView::item:selected { color:%(TextColor)s; 
                background-color: rgba(0, 0, 0, 12); border-radius: 4px; }

            QSpinBox {
                border: none;
                background: white;
                color:%(TextColor)s;
                font-size:10pt;
                font-family:%(UIFont)s;
            }
            QSpinBox::up-button { image: url(:/images/uparrow.png); height: 12px; }
            QSpinBox::down-button { image: url(:/images/downarrow.png); height: 12px; }
            QSpinBox::up-button, QSpinBox::down-button { background: #62c7e0; }
            QSpinBox::up-button:hover, QSpinBox::down-button:hover { background: #c7eaf3; }
            QSpinBox::up-button:pressed, QSpinBox::down-button:pressed { background: #35b6d7; }
            QSpinBox::up-button:disabled, QSpinBox::up-button:off, 
            QSpinBox::down-button:disabled, QSpinBox::down-button:off { background: #c0c0c0; }
            QSpinBox:disabled { background: #e0e0e0; }
            
            QGroupBox {
                color:%(TextColor)s;
                font-size:10pt;
                font-family:%(UIFont)s;
                border: 1px solid gray;
                margin-top: 15px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                left:5px;
                top:3px;
            }
            
            QCheckBox { color:%(TextColor)s; spacing: 5px; font-size:10pt; font-family:%(UIFont)s; }
            QCheckBox::indicator:unchecked { image: url(:/images/checkbox_unchecked.png); }
            QCheckBox::indicator:unchecked:hover { image: url(:/images/checkbox_unchecked_hover.png); }
            QCheckBox::indicator:unchecked:pressed { image: url(:/images/checkbox_unchecked_pressed.png); }
            QCheckBox::indicator:checked { image: url(:/images/checkbox_checked.png); }
            QCheckBox::indicator:checked:hover { image: url(:/images/checkbox_checked_hover.png); }
            QCheckBox::indicator:checked:pressed { image: url(:/images/checkbox_checked_pressed.png); }
            
            QRadioButton { color:%(TextColor)s; spacing: 4px; font-size:10pt; font-family:%(UIFont)s; }
            QRadioButton::indicator:unchecked { image: url(:/images/radiobutton_unchecked.png); }
            QRadioButton::indicator:unchecked:hover { image: url(:/images/radiobutton_unchecked_hover.png); }
            QRadioButton::indicator:unchecked:pressed { image: url(:/images/radiobutton_unchecked_pressed.png); }
            QRadioButton::indicator:checked { image: url(:/images/radiobutton_checked.png); }
            QRadioButton::indicator:checked:hover { image: url(:/images/radiobutton_checked_hover.png); }
            QRadioButton::indicator:checked:pressed { image: url(:/images/radiobutton_checked_pressed.png); }
            
            QScrollBar:horizontal {
                background-color:%(BackgroundColor)s;
                border: none;
                height: 15px;
                margin: 0px 20px 0 20px;
            }
            QScrollBar::handle:horizontal {
                background: %(ScrollBar_Handle)s;
                min-width: 20px;
            }
            QScrollBar::add-line:horizontal {
                image: url(:/images/rightarrow.png);
                border: none;
                background: %(ScrollBar_Line)s;
                width: 20px;
                subcontrol-position: right;
                subcontrol-origin: margin;
            }
            QScrollBar::sub-line:horizontal {
                image: url(:/images/leftarrow.png);
                border: none;
                background: %(ScrollBar_Line)s;
                width: 20px;
                subcontrol-position: left;
                subcontrol-origin: margin;
            }
            
            QScrollBar:vertical {
                background-color:%(BackgroundColor)s;
                border: none;
                width: 15px;
                margin: 20px 0px 20px 0px;
            }
            QScrollBar::handle::vertical {
                background: %(ScrollBar_Handle)s;
                min-height: 20px;
            }
            QScrollBar::add-line::vertical {
                image: url(:/images/downarrow.png);
                border: none;
                background: %(ScrollBar_Line)s;
                height: 20px;
                subcontrol-position: bottom;
                subcontrol-origin: margin;
            }
            QScrollBar::sub-line::vertical {
                image: url(:/images/uparrow.png);
                border: none;
                background: %(ScrollBar_Line)s;
                height: 20px;
                subcontrol-position: top;
                subcontrol-origin: margin;
            }
            
            QTableView {
                background-color: white;
                /*selection-background-color: #FF92BB;*/
                border: 1px solid %(TableView_Border)s;
                color: %(TextColor)s;
            }
            QTableView::focus {
                /*border: 1px solid #2a7fff;*/
            }
            QTableView QTableCornerButton::section {
                border: none;
                border-right: 1px solid %(TableView_Border)s;
                border-bottom: 1px solid %(TableView_Border)s;
                background-color: %(TableView_Corner)s;
            }
            QTableView QWidget {
                background-color: white;
            }
            QTableView::item:focus {
                border: 1px red;
                background-color: transparent;
                color: %(TextColor)s;
            }
            QHeaderView::section {
                border: none;
                border-right: 1px solid %(TableView_Border)s;
                border-bottom: 1px solid %(TableView_Border)s;
                padding-left: 2px;
                padding-right: 2px;
                color: %(TextColor)s;
                background-color: %(TableView_Header)s;
            }
            QTextEdit {
                background-color:white;
                color:%(TextColor)s;
                border-top: none;
                border-bottom: none;
                border-left: 2px solid %(BackgroundColor)s;
                border-right: 2px solid %(BackgroundColor)s;
            }
            QTextEdit::focus {
            }
            
            QToolButton, QPushButton {
                background-color:#30a7b8;
                border:none;
                color:#ffffff;
                font-size:10pt;
                font-family:%(UIFont)s;
            }
            QToolButton:hover, QPushButton:hover {
                background-color:#51c0d1;
            }
            QToolButton:pressed, QPushButton:pressed {
                background-color:#3a9ecc;
            }
            
            QMenuBar {
                color: %(TextColor)s;
                height: 24px;
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
            
            QMenu {margin: 2px;color: #202020;background: #eeeeee;}
            QMenu::item {padding: 2px 12px 2px 12px;border: 1px solid transparent;}
            QMenu::item:selected {background: #51c0d1;}
            QMenu::icon {background: transparent;border: 2px inset transparent;}
            QMenu::item:disabled {color: #808080;background: #eeeeee;}
            
            QDockWidget {
                font-size:10pt;
                font-family:%(UIFont)s;
                color: %(TextColor)s;
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
                image: url(:/images/restore_inactive.png);
            }
            QDockWidget::float-button:hover {
                background-color:#227582;
                image: url(:/images/restore_active.png);
            }
            QDockWidget::float-button:pressed {
                padding: 0;
                background-color:#14464e;
                image: url(:/images/restore_active.png);
            }
            QDockWidget::close-button {
                max-width: 12px;
                max-height: 12px;
                background-color:transparent;
                border:none;
                image: url(:/images/close_inactive.png);
            }
            QDockWidget::close-button:hover {
                background-color:#ea5e00;
                image: url(:/images/close_active.png);
            }
            QDockWidget::close-button:pressed {
                background-color:#994005;
                image: url(:/images/close_active.png);
                padding: 0;
            }
            
            QTabBar { qproperty-drawBase: 0; }  /* remove the mysterious unstyled horizontal line */
            
            QTabBar::tab {
                font-size:10pt;
                font-family:%(UIFont)s;
                color: #202020;
                background-color: #6fcae1;
                /*border: 2px solid #99d9ea;*/
                /*min-width: 22ex;*/
                padding: 4px 12px 4px 12px;
                margin: 2px;
            }
            QTabBar::tab:selected, QTabBar::tab:hover { background-color:#f8f8f8;color: #202020; }
            
        """ % dict(
            BackgroundColor =  '#99d9ea',
            TextColor =        '#202020',
            ScrollBar_Handle = '#61b9e1',
            ScrollBar_Line =   '#7ecfe4',
            TableView_Corner = '#8ae6d2',
            TableView_Header = '#8ae6d2',
            TableView_Border = '#eeeeee',
            UIFont = UI_FONT,
        ))

        self.chkbtn_SSTemplate = """
            QPushButton, QToolButton { background-color:%(BG)s; border:none; border-radius: 6px; }
            QPushButton:hover, QToolButton:hover { background-color:%(HBG)s; }
            QPushButton:pressed, QToolButton:pressed { background-color:#b8e5f1; }
        """

        self.btnLoop.setStyleSheet(self.chkbtn_SSTemplate % {'BG':'transparent', 'HBG':'#51c0d1'})
        self.btnLoop.setIcon(QIcon(":/images/loop.png"))
        self.btnLoop.setIconSize(QtCore.QSize(20, 20))
        self.btnLoop.clicked.connect(self.onLoopChanged)
        self.btnLoop.setToolTip("Loop Send")
        self.btnLoop.setCursor(Qt.PointingHandCursor)

        self.dockWidget_QuickSend.setStyleSheet("""
            QToolButton, QPushButton {
                background-color:#27b798;
                font-family:Tahoma;
                font-size:10pt;
                /*min-width:46px;*/
            }
            QToolButton:hover, QPushButton:hover {
                background-color:#3bd5b4;
            }
            QToolButton:pressed, QPushButton:pressed {
                background-color:#1d8770;
            }
        """)
        self.dockWidgetContents_2.setStyleSheet("""
            QPushButton {
                min-height:23px;
                min-width:50px;
            }
        """)

        # self.cmbBaudRate.setView(QListView())
        # self.cmbDataBits.setView(QListView())
        # self.cmbParity.setView(QListView())
        # self.cmbStopBits.setView(QListView())

    def setupTitleBar(self):
        self.lblIcon = QLabel(self)
        self.lblIcon.setFixedSize(QSize(24, 24))
        self.lblIcon.setMinimumSize(QSize(24, 24))
        self.lblIcon.setMaximumSize(QSize(24, 24))

        self.lblIcon.setPixmap(QIcon(":/uartvide-icon/uartvide.ico").pixmap(20, 20))
        
        self.lblTitle = QLabel(self)
        self.lblTitle.setText(appInfo.title)

        self.btnRefresh = QPushButton(self.titleBar)
        self.btnRefresh.setFixedSize(QSize(24, 24))
        self.btnRefresh.setStyleSheet("""
            QPushButton { background-color:transparent; border:none; 
                          border-top-left-radius:6px;
                          border-bottom-left-radius:6px; }
            QPushButton:hover { background-color:#51c0d1; }
            QPushButton:pressed { background-color:#b8e5f1; }
        """)
        self.btnRefresh.setIcon(QIcon(":/images/refresh.png"))
        self.btnRefresh.setIconSize(QtCore.QSize(24, 24))
        self.btnRefresh.setToolTip("Refresh Ports")
        self.btnRefresh.setCursor(Qt.PointingHandCursor)
        self.btnRefresh.clicked.connect(self.onRefreshPorts)
        
        self.cmbPort = RightAngleComboBox(self.titleBar)
        self.cmbPort.setCurrentText("")
        self.cmbPort.setMinimumSize(QSize(0, 24))
        self.cmbPort.setMaximumSize(QSize(150, 24))
        self.cmbPort.listShowEntered.connect(self.onEnumPorts)
        self.cmbPort.currentTextChanged.connect(self.onPortChanged)
        self.cmbPort.setToolTip("Select/Input Port")
        self.cmbPort.setCursor(Qt.PointingHandCursor)
    
        self.asbtnOpen = AnimationSwitchButton(self.titleBar)
        self.asbtnOpen.setFixedSize(QSize(30, 18))
        self.asbtnOpen.stateChanged.connect(self.onOpen)
        self.asbtnOpen.setToolTip("Open Port")
        self.asbtnOpen.setCursor(Qt.PointingHandCursor)

        self.btnTogglePortCfgBar = QPushButton(self.titleBar)
        self.btnTogglePortCfgBar.setIcon(QIcon(':/images/up.png'))
        self.btnTogglePortCfgBar.setFixedSize(QSize(24, 24))
        self.btnTogglePortCfgBar.setIconSize(QtCore.QSize(23, 23))
        self.btnTogglePortCfgBar.setStyleSheet("""
            QPushButton { background-color:transparent; border:none; border-radius: 6px; }
            QPushButton:hover { background-color:#51c0d1; }
            QPushButton:pressed { background-color:#b8e5f1; }
        """)
        self.btnTogglePortCfgBar.clicked.connect(self.onTogglePortCfgBar)
        self.btnTogglePortCfgBar.setToolTip("Toggle Port Config Bar")
        self.btnTogglePortCfgBar.setCursor(Qt.PointingHandCursor)

        self.cmbViewMode = RightAngleComboBox(self.titleBar)
        # self.cmbViewMode.setView(QListView())
        self.cmbViewMode.addItems(['Ascii', 'HEX', 'hex'])
        self.cmbViewMode.setCurrentIndex(1)
        self.cmbViewMode.setFixedSize(QSize(60, 24))
        self.cmbViewMode.currentTextChanged.connect(self.onViewModeChanged)
        self.cmbViewMode.setToolTip("Select hexadecimal/ASCII")
        self.cmbViewMode.setCursor(Qt.PointingHandCursor)

        self.btnTimestamp = QPushButton(self.titleBar)
        self.btnTimestamp.setFixedSize(QSize(24, 24))
        self.btnTimestamp.setStyleSheet(self.chkbtn_SSTemplate % {'BG':'transparent', 'HBG':'#51c0d1'})
        self.btnTimestamp.setIcon(QIcon(":/images/timestamp.png"))
        self.btnTimestamp.setIconSize(QtCore.QSize(20, 20))
        self.btnTimestamp.clicked.connect(self.onTimestamp)
        self.btnTimestamp.setToolTip("Timestamp")
        self.btnTimestamp.setCursor(Qt.PointingHandCursor)

        self.btnSaveLog = QPushButton(self.titleBar)
        self.btnSaveLog.setParent(self)
        self.btnSaveLog.setFixedSize(QSize(24, 24))
        self.btnSaveLog.setStyleSheet("""
            QPushButton { background-color:transparent; border:none; border-radius: 6px; }
            QPushButton:hover { background-color:#51c0d1; }
            QPushButton:pressed { background-color:#b8e5f1; }
        """)
        self.btnSaveLog.setIcon(QIcon(":/images/save.png"))
        self.btnSaveLog.setIconSize(QtCore.QSize(20, 20))
        self.btnSaveLog.setToolTip("Save Log As")
        self.btnSaveLog.setCursor(Qt.PointingHandCursor)
        self.btnSaveLog.clicked.connect(self.onSaveLog)

        self.btnClear = QPushButton(self.titleBar)
        self.btnClear.setFixedSize(QSize(24, 24))
        self.btnClear.setStyleSheet("""
            QPushButton { background-color:transparent; border:none; border-radius: 6px; }
            QPushButton:hover { background-color:#51c0d1; }
            QPushButton:pressed { background-color:#b8e5f1; }
        """)
        self.btnClear.setIcon(QIcon(":/images/eraser.png"))
        self.btnClear.setIconSize(QtCore.QSize(20, 20))
        self.btnClear.setToolTip("Clear Log")
        self.btnClear.setCursor(Qt.PointingHandCursor)
        self.btnClear.clicked.connect(self.onClear)

        self.btnClearRxTxCnt = QPushButton(self.titleBar)
        self.btnClearRxTxCnt.setFixedSize(QSize(24, 24))
        self.btnClearRxTxCnt.setStyleSheet("""
            QPushButton { background-color:#3a9ecc; border:none; 
                          border-top-left-radius:6px;
                          border-bottom-left-radius:6px; }
            QPushButton:hover { background-color:#51c0d1; }
            QPushButton:pressed { background-color:#b8e5f1; }
        """)
        self.btnClearRxTxCnt.setIcon(QIcon(":/images/clear.png"))
        self.btnClearRxTxCnt.setIconSize(QtCore.QSize(22, 22))
        self.btnClearRxTxCnt.setToolTip("Clear RX/TX counters")
        self.btnClearRxTxCnt.setCursor(Qt.PointingHandCursor)
        self.btnClearRxTxCnt.clicked.connect(self.onClearRxTxCnt)

        self.RxTxCnt = [0, 0]
        # self.lblRxTxCnt_textlen = 0
        self.lblRxTxCnt = QLabel(self.titleBar)
        self.lblRxTxCnt.setMinimumSize(QSize(20, 24))
        self.lblRxTxCnt.setMaximumSize(QSize(200, 24))
        self.lblRxTxCnt.setStyleSheet("""
            QLabel { background-color:transparent; border: 1px solid #3a9ecc; 
                     border-top-right-radius:6px;
                     border-bottom-right-radius:6px;
                     font-size:10pt; padding: 0px 0px 2px 0px; }
        """)
        self.lblRxTxCnt.setText('R:0 T:0')
        self.lblRxTxCnt.setToolTip("RX/TX data counters")
        self.lblRxTxCnt.setMouseTracking(True)

        self.btnMenu = QPushButton(self.titleBar)
        self.btnMenu.setFixedSize(QSize(26, 26))
        self.btnMenu.setStyleSheet("""
            QPushButton { background-color:transparent; border:none; border-radius: 1.5px; }
            QPushButton:hover { background-color:#51c0d1; }
            QPushButton:pressed { background-color:#b8e5f1; }
        """)
        self.btnMenu.setIcon(QIcon(":/images/menu.png"))
        self.btnMenu.setIconSize(QtCore.QSize(24, 24))
        self.btnMenu.setToolTip("More Settings...")
        self.btnMenu.setCursor(Qt.PointingHandCursor)
        self.btnMenu.clicked.connect(self.onMoreSettings)

        self.hBxLyt_tb_1_1 = QHBoxLayout()
        self.hBxLyt_tb_1_1.setObjectName('hBxLyt_tb_1_1')
        self.hBxLyt_tb_1_1.setSpacing(0)
        self.hBxLyt_tb_1_1.setContentsMargins(1, 0, 0, 0)
        self.hBxLyt_tb_1_1.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)

        self.hBxLyt_tb_1_1.addWidget(self.lblIcon)
        self.hBxLyt_tb_1_1.addWidget(self.lblTitle)

        self.hBxLyt_tb_1_2 = QHBoxLayout()
        self.hBxLyt_tb_1_2.setObjectName('hBxLyt_tb_1_2')
        self.hBxLyt_tb_1_2.setSpacing(0)
        self.hBxLyt_tb_1_2.setContentsMargins(4, 0, 0, 0)
        self.hBxLyt_tb_1_2.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)
        
        self.hBxLyt_tb_1_2.addWidget(self.btnRefresh, 0, Qt.AlignLeft)
        self.hBxLyt_tb_1_2.addWidget(self.cmbPort, 0, Qt.AlignLeft)
        
        self.hBxLyt_tb_1_3 = QHBoxLayout()
        self.hBxLyt_tb_1_3.setObjectName('hBxLyt_tb_1_3')
        self.hBxLyt_tb_1_3.setSpacing(0)
        self.hBxLyt_tb_1_3.setContentsMargins(0, 0, 0, 0)
        self.hBxLyt_tb_1_3.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)
        
        self.hBxLyt_tb_1_3.addWidget(self.btnClearRxTxCnt, 0, Qt.AlignLeft)
        self.hBxLyt_tb_1_3.addWidget(self.lblRxTxCnt, 0, Qt.AlignLeft)
        
        self.hBxLyt_tb_1 = QHBoxLayout()
        self.hBxLyt_tb_1.setObjectName('hBxLyt_tb_1')
        self.hBxLyt_tb_1.setSpacing(6)
        self.hBxLyt_tb_1.setContentsMargins(6, 3, 0, 0)
        self.hBxLyt_tb_1.setAlignment(Qt.AlignLeft)

        self.hBxLyt_tb_1.addLayout(self.hBxLyt_tb_1_1)
        self.hBxLyt_tb_1.addLayout(self.hBxLyt_tb_1_2)
        self.hBxLyt_tb_1.addWidget(self.asbtnOpen, 0, Qt.AlignLeft)
        self.hBxLyt_tb_1.addWidget(self.btnTogglePortCfgBar, 0, Qt.AlignLeft)
        self.hBxLyt_tb_1.addWidget(self.cmbViewMode, 0, Qt.AlignLeft)
        
        self.hBxLyt_tb_1.addWidget(self.btnTimestamp, 0, Qt.AlignLeft)
        self.hBxLyt_tb_1.addWidget(self.btnSaveLog, 0, Qt.AlignLeft)
        self.hBxLyt_tb_1.addWidget(self.btnClear, 0, Qt.AlignLeft)
        self.hBxLyt_tb_1.addLayout(self.hBxLyt_tb_1_3)
        self.hBxLyt_tb_1.addWidget(self.btnMenu, 0, Qt.AlignLeft)

        self.hBxLyt_tb_1.addStretch(1)

        self.titleBar.hBoxLayout.insertLayout(0, self.hBxLyt_tb_1, 0)

        self.btnPin = TransparentToggleToolButton(self.titleBar)
        self.btnPin.setFixedSize(QSize(26, 26))

        self.btnPin.setIcon(QIcon(":/images/pin.png"))
        self.btnPin.setIconSize(QtCore.QSize(24, 24))
        self.btnPin.setToolTip("Always On Top")
        self.btnPin.setCursor(Qt.PointingHandCursor)
        self.btnPin.clicked.connect(self.onAlwaysOnTop)

        self.titleBar.hBoxLayout.insertWidget(2, self.btnPin, 0, Qt.AlignRight)

        if os.name == 'posix':
            self.fixComboViewSize(self.cmbBaudRate)
            self.fixComboViewSize(self.cmbDataBits)
            self.fixComboViewSize(self.cmbParity)
            self.fixComboViewSize(self.cmbStopBits)

    def resizeEvent(self, event):
        self.setMinimumWidth(self.titleBar.hBoxLayout.sizeHint().width() + 30)
        super().resizeEvent(event)

    # def onDockLocationChanged(self, area):
    #     # print('onDockLocationChanged', area)
    #     self.dockWidget_QuickSend.adjustSize()
    #     self.dockWidget.adjustSize()
    
    def onMoreSettings(self):
        self.menuMoreSettings.popup(self.btnMenu.mapToGlobal(QPoint(0, self.btnMenu.size().height())))

    def onClearRxTxCnt(self):
        self.RxTxCnt = [0, 0]
        self.updateRxTxCnt()

    def fixComboViewSize(self, widget):
        fm = QFontMetrics(widget.fontMetrics())
        maxlen = 0
        for id in range(widget.count()):
            text = widget.itemText(id)
            if hasattr(fm, 'horizontalAdvance'):
                l = fm.horizontalAdvance(text)
            else:
                l = fm.width(text)
            if maxlen < l:
                maxlen = l
        widget.view().setFixedWidth(maxlen + 44)

    def onTimestamp(self):
        self._is_timestamp = not self._is_timestamp
        self.setTimestampEnabled(self._is_timestamp)
    
    def setTimestampEnabled(self, enabled):
        if enabled:
            self._is_timestamp = True
            self.btnTimestamp.setStyleSheet(self.chkbtn_SSTemplate % {'BG':'#3a9ecc', 'HBG':'#51c0d1'})
        else:
            self._is_timestamp = False
            self.btnTimestamp.setStyleSheet(self.chkbtn_SSTemplate % {'BG':'transparent', 'HBG':'#51c0d1'})
        
        self.readerThread.setTimestampEnable(self._is_timestamp)

    def onTogglePortCfgBar(self):
        #self.pos_animation.start()
        if self.frame_PortCfg.isVisible():
            self.setPortCfgBarVisible(False)
        else:
            self.setPortCfgBarVisible(True)

    def setPortCfgBarVisible(self, visible):
        if visible:
            self.frame_PortCfg.show()
            self.btnTogglePortCfgBar.setIcon(QIcon(':/images/up.png'))
        else:
            self.frame_PortCfg.hide()
            self.btnTogglePortCfgBar.setIcon(QIcon(':/images/down.png'))

    def onPortChanged(self, text):
        pos = text.find(' ')
        if 0 < pos:
            port_name = text[:pos]
            self.cmbPort.setCurrentText(port_name)

    def saveSettings(self):
        root = ET.Element(appInfo.title)
        GUISettings = ET.SubElement(root, "GUISettings")

        PortCfg = ET.SubElement(GUISettings, "PortConfig")
        ET.SubElement(PortCfg, "port").text = self.cmbPort.currentText()
        ET.SubElement(PortCfg, "baudrate").text = self.cmbBaudRate.currentText()
        ET.SubElement(PortCfg, "databits").text = self.cmbDataBits.currentText()
        ET.SubElement(PortCfg, "parity").text = self.cmbParity.currentText()
        ET.SubElement(PortCfg, "stopbits").text = self.cmbStopBits.currentText()
        ET.SubElement(PortCfg, "rtscts").text = self.chkRTSCTS.isChecked() and "on" or "off"
        ET.SubElement(PortCfg, "xonxoff").text = self.chkXonXoff.isChecked() and "on" or "off"

        ET.SubElement(GUISettings, "ViewMode").text = self._viewMode
        ET.SubElement(GUISettings, "Timestamp").text = "on" if self._is_timestamp else "off"
        ET.SubElement(GUISettings, "SendAsHex").text = "on" if self.rdoHEX.isChecked() else "off"
        ET.SubElement(GUISettings, "LoopTime").text = '{}'.format(self.spnPeriod.value())
        
        Contents = ET.SubElement(root, "Contents")
        Send = ET.SubElement(Contents, "Send")
        ET.SubElement(Send, "Value").text = self.txtEdtInput.toPlainText()

        try:
            with open(get_config_path(appInfo.title+'.xml'), 'w') as f:
                f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
                f.write(ET.tostring(root, encoding='utf-8', pretty_print=True).decode("utf-8"))
        except Exception as e:
            #print("{}".format(e))
            print("(line {}){}".format(sys.exc_info()[-1].tb_lineno, str(e)))

    def loadSettings(self):
        if os.path.isfile(get_config_path(appInfo.title+".xml")):
            try:
                with open(get_config_path(appInfo.title+".xml"), 'r') as f:
                    tree = safeET.parse(f)
            except Exception as e:
                print("(line {}){}".format(sys.exc_info()[-1].tb_lineno, str(e)))
            else:
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

                self._viewMode = tree.findtext('GUISettings/ViewMode', default='HEX')
                if self._viewMode == '':
                    self._viewMode = 'Ascii'
                id = self.cmbViewMode.findText(self._viewMode)
                if id != -1:
                    self.cmbViewMode.setCurrentIndex(id)

                ts = tree.findtext('GUISettings/Timestamp', default='on')
                self.setTimestampEnabled(True if ts == "on" else False)

                sah = tree.findtext('GUISettings/SendAsHex', default='off')
                self.rdoHEX.setChecked(True if sah == "on" else False)
                self.rdoASC.setChecked(True if sah == "off" else False)

                lt = tree.findtext('GUISettings/LoopTime', default='1000')
                self.spnPeriod.setValue(int(lt))

                send_text = tree.findtext('Contents/Send/Value', default='')
                self.txtEdtInput.setText(send_text)

    def initQuickSend(self):
        self.qckSndTbl.setSendFunc(self.onQuickSend)
        self.qckSndTbl.setMenuFunc(self.onQuickSendOptions)
        self.qckSndTbl.setPathFunc(self.onQuickSendSelectFile)

        if os.path.isfile(get_config_path('QuickSend.csv')):
            self.loadQuickSendByFile(get_config_path('QuickSend.csv'))
        else:
            self.qckSndTbl.setRowCount(10)

        self.qckSndTbl.resizeColumnsToContents()
        self.qckSndTbl.update()

    def onQckSnd_SelectFormat(self, fmt):
        self.qckSndTbl.setText(self._qckSnd_SelectingRow, 1, fmt)

    def onQuickSendOptions(self, row):
        self._qckSnd_SelectingRow = row
        item = self.qckSndTbl.cellWidget(row, 1)
        self.menuSendOpt.popup(item.mapToGlobal(QPoint(item.size().width(), item.size().height())))

    def onQuickSendSelectFile(self, row):
        old_path = self.qckSndTbl.text(row, 2)
        fileName = QFileDialog.getOpenFileName(self.defaultStyleWidget, "Select a file",
            old_path, "All Files (*.*)")[0]
        if fileName:
            self.qckSndTbl.setText(row, 2, fileName)

    def openQuickSendFile(self):
        fileName = QFileDialog.getOpenFileName(self.defaultStyleWidget, "Select a file",
            os.getcwd(), "CSV Files (*.csv)")[0]
        if fileName:
            self.loadQuickSendByFile(fileName, notifyExcept = True)

    def saveQuickSend(self):
        try:
            self.qckSndTbl.saveToCSV(get_config_path('QuickSend.csv'))
        except Exception as e:
            print("(line {}){}".format(sys.exc_info()[-1].tb_lineno, str(e)))
            raise

    def loadQuickSendByFile(self, path, notifyExcept = False):
        try:
            self.qckSndTbl.loadFromCSV(path)
        except Exception as e:
            print("(line {}){}".format(sys.exc_info()[-1].tb_lineno, str(e)))
            raise
            if notifyExcept:
                QMessageBox.critical(self.defaultStyleWidget, "Load failed",
                    str(e), QMessageBox.Close)

    def onQuickSend(self, row):
        try:
            if self.serialport.isOpen():
                data = self.qckSndTbl.text(row, 2)
                fmt = self.qckSndTbl.text(row, 1)
                if 'H' == fmt:
                    self.transmitHex(data)
                elif 'A' == fmt:
                    self.transmitAsc(data)
                elif 'AS' == fmt:
                    self.transmitAscS(data)
                else:
                    self.transmitFile(data, fmt)
        except Exception as e:
            print("(line {}){}".format(sys.exc_info()[-1].tb_lineno, str(e)))
            InfoBar.warning(
                title='Send Failed',
                content=str(e),
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.BOTTOM,
                duration=2000,
                parent=self
            )
    
    def onQuickSendRightClick(self, row):
        item = self.qckSndTbl.cellWidget(row, 0)
        oldname = item.text()
        pos = item.mapToGlobal(QPoint(30, 10))
        newname = RenameDailog.getNewName(oldname, pos)
        if newname:
            item.setText(newname)
            self.qckSndTbl.resizeColumnsToContents()

    def onQckSnd_Rename(self):
        self.onQuickSendRightClick(self._qckSnd_SelectingRow)

    def onQckSnd_InsertRow(self):
        self.qckSndTbl.insertRow(self._qckSnd_SelectingRow)

    def onQckSnd_RemoveRow(self):
        self.qckSndTbl.removeRow(self._qckSnd_SelectingRow)

    def transmitFile(self, filepath, form):
        try:
            with open(filepath, 'rb' if 'BF' == form else 'rt') as f:
                content = f.read()
        except Exception as e:
            #QMessageBox.critical(self.defaultStyleWidget, "Open failed", str(e), QMessageBox.Close)
            raise e
        else:
            self.appendOutput(self.timestamp(), "sending %s [%s]" % (filepath, form))
            self.repaint()
            
            sent_len = 0
            if 'HF' == form:
                sent_len = self.transmitHex(content, echo = False)
            elif 'AF' == form:
                sent_len = self.transmitAsc(content, echo = False)
            elif 'BF' == form:
                sent_len = self.transmitBytearray(content)
            
            self.appendOutput(self.timestamp(), "%d bytes sent" % (sent_len))

    def onLoopChanged(self):
        if self._is_loop_mode:
            if self._is_loop_sending:
                self.stopLoopSend()
            self._is_loop_mode = False
            self.btnLoop.setStyleSheet(self.chkbtn_SSTemplate % {'BG':'transparent', 'HBG':'#51c0d1'})
            self.btnSend.setText('Send')
        else:
            self._is_loop_mode = True
            self.btnLoop.setStyleSheet(self.chkbtn_SSTemplate % {'BG':'#0072BB', 'HBG':'#51c0d1'})
            self.btnSend.setText('Start')
        self.spnPeriod.setEnabled(self._is_loop_mode)

    def startLoopSend(self):
        period_spacing = self.spnPeriod.value() / 1000.0
        self.loopSendThread.start(period_spacing)
        self.btnSend.setStyleSheet('''
            QToolButton, QPushButton {
                background-color:#0072BB;
                border:none;
                color:#ffffff;
                font-size:10pt;
                font-family:%(UIFont)s;
            }
            QToolButton:hover, QPushButton:hover {
                background-color:#0088e0;
            }
            QToolButton:pressed, QPushButton:pressed {
                background-color:#015f9b;
            }''' % dict(UIFont = 'Microsoft YaHei UI'))
        self.btnSend.setText('Stop')
        self._is_loop_sending = True

    def stopLoopSend(self):
        self.loopSendThread.join()
        self.btnSend.setStyleSheet('''
            QToolButton, QPushButton {
                background-color:#30a7b8;
                border:none;
                color:#ffffff;
                font-size:10pt;
                font-family:%(UIFont)s;
            }
            QToolButton:hover, QPushButton:hover {
                background-color:#51c0d1;
            }
            QToolButton:pressed, QPushButton:pressed {
                background-color:#3a9ecc;
            }''' % dict(UIFont = 'Microsoft YaHei UI'))
        self.btnSend.setText('Start')
        self._is_loop_sending = False

    def onPeriodTrigger(self):
        self.send()

    def onSend(self):
        if self.serialport.isOpen():
            if self._is_loop_mode:
                if self._is_loop_sending:
                    self.stopLoopSend()
                else:
                    self.startLoopSend()
            else:
                self.send()

    def send(self):
        try:
            if self.serialport.isOpen():
                sendstring = self.txtEdtInput.toPlainText()
                if self.rdoHEX.isChecked():
                    self.transmitHex(sendstring)
                else:
                    self.transmitAsc(sendstring)
        except Exception as e:
            if self._is_loop_sending:
                self.stopLoopSend()
            InfoBar.warning(
                title='Send Failed',
                content=str(e),
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.BOTTOM,
                duration=2000,
                parent=self
            )

    def transmitHex(self, hexstring, echo = True):
        if len(hexstring) > 0:
            hexarray = string_to_hex(hexstring)
            if echo:
                text = ''.join('%02X ' % t for t in hexarray)
                self.appendOutput(self.timestamp(), text)
            return self.transmitBytearray(bytearray(hexarray))

    def transmitAsc(self, text, echo = True):
        if len(text) > 0:
            byteArray = [ord(char) for char in text]
            if echo:
                self.appendOutput(self.timestamp(), text)
            return self.transmitBytearray(bytearray(byteArray))

    def transmitAscS(self, text, echo = True):
        if len(text) > 0:
            t = text.replace(r'\r', '\r')
            t = t.replace(r'\n', '\n')
            t = t.replace(r'\t', '\t')
            t = t.replace(r'\'', "'")
            t = t.replace(r'\"', '"')
            t = t.replace(r'\\', '\\')
            self.transmitAsc(t, echo)

    def transmitBytearray(self, byteArray):
        if self.serialport.isOpen():
            try:
                self.serialport.write(byteArray)
            except Exception as e:
                #QMessageBox.critical(self.defaultStyleWidget,
                #    "Exception in transmit", str(e), QMessageBox.Close)
                #print("Exception in transmitBytearray(%s)" % byteArray)
                #return 0
                raise e
            else:
                self.RxTxCnt[1] = self.RxTxCnt[1] + len(byteArray)
                self.updateRxTxCnt()
                return len(byteArray)

    def onReaderExcept(self, e):
        self.closePort()
        InfoBar.warning(
            title='Read Failed',
            content=str(e),
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.BOTTOM,
            duration=2000,
            parent=self
        )

    def timestamp(self):
        if self._is_timestamp:
            ts = datetime.datetime.now().time()
            if ts.microsecond:
                return ts.isoformat()[:-3]+':'
            else:
                return ts.isoformat() + '.000:'
        else:
            return ''

    def updateRxTxCnt(self):
        self.lblRxTxCnt.setText('R:{} T:{}'.format(self.RxTxCnt[0], self.RxTxCnt[1]))
        # cnt_text = 'R:{} T:{}'.format(self.RxTxCnt[0], self.RxTxCnt[1])
        # textlen = len(cnt_text)
        # if self.lblRxTxCnt_textlen != textlen:
        #     fm = QFontMetrics(self.lblRxTxCnt.fontMetrics())
        #     if hasattr(fm, 'horizontalAdvance'):
        #         w = fm.horizontalAdvance(cnt_text+'   ')
        #     else:
        #         w = fm.width(cnt_text+'   ')
        #     rect = QRect(self.lblRxTxCnt.geometry())
        #     rect.setWidth(w)
        #     self.lblRxTxCnt.setGeometry(rect)
        # self.lblRxTxCnt.setText(cnt_text)
        # self.lblRxTxCnt_textlen = textlen

    def onReceive(self, data):
        ts = data[0]
        ts_text = ''
        if type(ts) == datetime.time:
            if ts.microsecond:
                ts_text = ts.isoformat()[:-3]+':'
            else:
                ts_text = ts.isoformat() + '.000:'

        self.RxTxCnt[0] = self.RxTxCnt[0] + len(data[1])
        self.updateRxTxCnt()

        if self._viewMode == 'Ascii':
            text = ''.join(chr(b) if b != 0 else ' ' for b in data[1])
        elif self._viewMode == 'hex':
            text = ''.join('%02x ' % b for b in data[1])
        elif self._viewMode == 'HEX':
            text = ''.join('%02X ' % b for b in data[1])

        self.appendOutput(ts_text, text, 'R')

    def appendOutput(self, ts_text, data_text, data_type = 'T'):
        self.txtEdtOutput.moveCursor(QtGui.QTextCursor.End)
        if data_type == 'R':
            self.txtEdtOutput.setTextColor(QtGui.QColor('#800000'))
            self.txtEdtOutput.insertPlainText(ts_text)
            self.txtEdtOutput.setTextColor(QtGui.QColor('#000000'))
            self.txtEdtOutput.insertPlainText(data_text)
        elif data_type == 'T':
            self.txtEdtOutput.setTextColor(QtGui.QColor('#800000'))
            self.txtEdtOutput.insertPlainText(ts_text)
            self.txtEdtOutput.setTextColor(QtGui.QColor('#0000ff'))
            self.txtEdtOutput.insertPlainText(data_text)
        self.txtEdtOutput.insertPlainText('\n')
        self.txtEdtOutput.moveCursor(QtGui.QTextCursor.End)

    def appendOutputText(self, data, color=Qt.black):
        # the qEditText's "append" methon will add a unnecessary newline.
        # self.txtEdtOutput.append(data.decode('utf-8'))

        tc = self.txtEdtOutput.textColor()
        self.txtEdtOutput.moveCursor(QtGui.QTextCursor.End)
        self.txtEdtOutput.setTextColor(QtGui.QColor(color))
        self.txtEdtOutput.insertPlainText(data)
        self.txtEdtOutput.moveCursor(QtGui.QTextCursor.End)
        self.txtEdtOutput.setTextColor(tc)

    def getPort(self):
        return self.cmbPort.currentText()

    def getDataBits(self):
        return {'5':serial.FIVEBITS,
                '6':serial.SIXBITS,
                '7':serial.SEVENBITS, 
                '8':serial.EIGHTBITS}[self.cmbDataBits.currentText()]

    def getParity(self):
        return {'None' :serial.PARITY_NONE,
                'Even' :serial.PARITY_EVEN,
                'Odd'  :serial.PARITY_ODD,
                'Mark' :serial.PARITY_MARK,
                'Space':serial.PARITY_SPACE}[self.cmbParity.currentText()]

    def getStopBits(self):
        return {'1'  :serial.STOPBITS_ONE,
                '1.5':serial.STOPBITS_ONE_POINT_FIVE,
                '2'  :serial.STOPBITS_TWO}[self.cmbStopBits.currentText()]

    def openPort(self):
        if self.serialport.isOpen():
            return

        _port = self.getPort()
        if '' == _port:
            InfoBar.warning(
                title='Port is empty',
                content='',
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.BOTTOM,
                duration=2000,
                parent=self
            )
            self.asbtnOpen.setChecked(False)
            return

        _baudrate = self.cmbBaudRate.currentText()
        if '' == _baudrate:
            InfoBar.warning(
                title='Baudrate is empty',
                content='',
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.BOTTOM,
                duration=2000,
                parent=self
            )
            self.asbtnOpen.setChecked(False)
            return

        self.serialport.port     = _port
        self.serialport.baudrate = _baudrate
        self.serialport.bytesize = self.getDataBits()
        self.serialport.stopbits = self.getStopBits()
        self.serialport.parity   = self.getParity()
        self.serialport.rtscts   = self.chkRTSCTS.isChecked()
        self.serialport.xonxoff  = self.chkXonXoff.isChecked()
        self.serialport.timeout  = 0.5
        # self.serialport.writeTimeout = 1.0
        try:
            self.serialport.open()
        except Exception as e:
            msg = str(e)
            if 'Permission denied' in msg:
                msg = msg + '\n\n Try "sudo chmod 777 {}"'.format(_port)
            InfoBar.warning(
                title='Open port failed',
                content=msg,
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.BOTTOM,
                duration=2000,
                parent=self
            )
            self.asbtnOpen.setChecked(False)
            #print(str(e))
            print("(line {}){}".format(sys.exc_info()[-1].tb_lineno, str(e)))
        else:
            self.readerThread.start()
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
            self.cmbPort.setEnabled(False)

    def closePort(self):
        if self.serialport.isOpen():
            if self._is_loop_sending:
                self.stopLoopSend()
            self.readerThread.join()
            self.serialport.cancel_write()
            self.serialport.cancel_read()
            self.serialport.close()
            
            self.setWindowTitle(appInfo.title)
            self.cmbPort.setEnabled(True)
            self.asbtnOpen.setChecked(False)

    def onToggleQckSndPnl(self):
        if self.actionQuick_Send_Panel.isChecked():
            self.dockWidget_QuickSend.show()
        else:
            self.dockWidget_QuickSend.hide()

    def onToggleSndPnl(self):
        if self.actionSend_Panel.isChecked():
            self.dockWidget_Send.show()
        else:
            self.dockWidget_Send.hide()

    def onVisibleQckSndPnl(self, visible):
        self.actionQuick_Send_Panel.setChecked(visible)

    def onVisibleSndPnl(self, visible):
        self.actionSend_Panel.setChecked(visible)

    def onAlwaysOnTop(self):
        self._is_always_on_top = not self._is_always_on_top
        self.setWindowFlag(Qt.WindowStaysOnTopHint, self._is_always_on_top)
        # if self._is_always_on_top:
        #     self.btnPin.setStyleSheet(self.chkbtn_SSTemplate % {'BG':'#3a9ecc', 'HBG':'#51c0d1'})
        # else:
        #     self.btnPin.setStyleSheet(self.chkbtn_SSTemplate % {'BG':'transparent', 'HBG':'#51c0d1'})
        if os.name == 'posix':
            self.destroy()
            self.create()
        self.show()

    def onOpen(self, state):
        if state:
            if not self.serialport.isOpen():
                self.openPort()
        else:
            if self.serialport.isOpen():
                self.closePort()

    def onClear(self):
        self.txtEdtOutput.clear()

    def onSaveLog(self):
        fileName = QFileDialog.getSaveFileName(self.defaultStyleWidget, "Save log as", os.getcwd(),
            "Log files (*.log);;Text files (*.txt);;All files (*.*)")[0]
        if fileName:
            import codecs
            try:
                with codecs.open(fileName, 'w', 'utf-8') as f:
                    f.write(self.txtEdtOutput.toPlainText())
            except Exception as e:
                print("(line {}){}".format(sys.exc_info()[-1].tb_lineno, str(e)))

    def moveScreenCenter(self):
        w = self.frameGeometry().width()
        h = self.frameGeometry().height()
        screen = app.primaryScreen().geometry()
        screenW = screen.width()
        screenH = screen.height()
        self.setGeometry((screenW-w)//2, (screenH-h)//2, w, h)

        w = self.defaultStyleWidget.frameGeometry().width()
        h = self.defaultStyleWidget.frameGeometry().height()
        self.defaultStyleWidget.setGeometry((screenW-w)//2, (screenH-h)//2, w, h)

    def onPortMonitorExcept(self, e):
        print('PortMonitorExcept', str(e))

    def onPortsListChanged(self, ports_lst):
        self.updatePortComboText(ports_lst[0])

        for inc in ports_lst[1]:
            InfoBar.success(
                title='%s is found' % inc,
                content='',
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.BOTTOM_LEFT,
                duration=3000,
                parent=self
            )
        
        for dec in ports_lst[2]:
            InfoBar.warning(
                title='%s is lost' % dec,
                content='',
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.BOTTOM_LEFT,
                duration=3000,
                parent=self
            )

    def onRefreshPorts(self):
        ports_lst = [[port, desc, is_port_busy(port)] for port, desc, _ in sorted(comports())]
        
        text = ''
        for port, desc, _ in sorted(comports()):
            text = text + port + ('⛔ ' if is_port_busy(port) else '🟢  ') + '\n'

        InfoBar.info(
            title='{} Port(s) Found'.format(len(ports_lst)),
            content=text,
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.BOTTOM_LEFT,
            duration=2000,
            parent=self
        )

    def onEnumPorts(self):
        ports_lst = [[port, desc, is_port_busy(port)] for port, desc, _ in sorted(comports())]
        self.updatePortComboText(ports_lst)

    def updatePortComboText(self, ports_lst):
        # print(ports_lst)
        sel = self.cmbPort.currentText()
        # fm = QFontMetrics(self.cmbPort.fontMetrics())
        # maxlen = 0
        self.cmbPort.clear()
        for port, desc, isbusy in ports_lst:
            state = '⛔ ' if isbusy else '🟢 '
            text = port + ' ' + state + desc
            self.cmbPort.addItem(text)
            # l = fm.horizontalAdvance(text)
            # if maxlen < l:
            #     maxlen = l
        # self.cmbPort.view().setFixedWidth(maxlen*1.4)
        # self.cmbPort.view().setFixedHeight(len(ports_lst) * 18)
        
        idx = self.cmbPort.findText(sel, Qt.MatchContains)
        if idx != -1:
            self.cmbPort.setCurrentIndex(idx)

    def onAbout(self):
        QMessageBox.about(self.defaultStyleWidget, "About UartVide", appInfo.aboutme)

    def onAboutQt(self):
        QMessageBox.aboutQt(self.defaultStyleWidget)

    def closeEvent(self, event):
        if self.serialport.isOpen():
            self.closePort()
        
        self.portMonitorThread.join()
        self.saveLayout()
        self.saveQuickSend()
        self.saveSettings()
        event.accept()

    def restoreLayout(self):
        if os.path.isfile(get_config_path("UILayout.dat")):
            try:
                f=open(get_config_path("UILayout.dat"), 'rb')
                geometry, state=pickle.load(f)
                self.restoreGeometry(geometry)
                self.restoreState(state)
            except Exception as e:
                print("Exception on restoreLayout, {}".format(e))
        else:
            try:
                f=QFile(':/default_layout.dat')
                f.open(QIODevice.ReadOnly)
                geometry, state=pickle.loads(f.readAll())
                self.restoreGeometry(geometry)
                self.restoreState(state)
            except Exception as e:
                print("Exception on restoreLayout, {}".format(e))

    def saveLayout(self):
        try:
            with open(get_config_path("UILayout.dat"), 'wb') as f:
                pickle.dump((self.saveGeometry(), self.saveState()), f)
        except Exception as e:
            print("(line {}){}".format(sys.exc_info()[-1].tb_lineno, str(e)))

    def syncMenu(self):
        self.actionQuick_Send_Panel.setChecked(not self.dockWidget_QuickSend.isHidden())
        self.actionSend_Panel.setChecked(not self.dockWidget_Send.isHidden())

    def onViewModeChanged(self, sel):
        self._viewMode = sel


def is_port_busy(port):
    try:
        se = serial.Serial(port)
    except IOError as e:
        #print(e)
        return True
    else:
        return False

def is_hex(s):
    try:
        int(s, 16)
        return True
    except ValueError:
        return False

def string_to_hex(hexstring):
    hexarray = []
    if len(hexstring) > 0:
        _hexstring = hexstring.replace(' ', '')
        _hexstring = _hexstring.replace('\r', '')
        _hexstring = _hexstring.replace('\n', '')
        for i in range(0, len(_hexstring), 2):
            word = _hexstring[i:i+2]
            if is_hex(word):
                hexarray.append(int(word, 16))
            else:
                raise Exception("'%s' is not hexadecimal." % (word))
    return hexarray

class ReaderThread(QThread):
    """loop and copy serial->GUI"""
    read = Signal(list)
    exception = Signal(str)

    def __init__(self, parent=None):
        super(ReaderThread, self).__init__(parent)
        self._alive = False
        self._stopped = True
        self._serialport = None
        self._ts_enabled = False

    def setPort(self, port):
        self._serialport = port

    def setTimestampEnable(self, enabled):
        self._ts_enabled = enabled

    def calcWaitTime(self):
        bits = 1 + self._serialport.bytesize + (0 if self._serialport.parity == 'N' else 1) + self._serialport.stopbits
        return min(0.2, max(0.005, (32 + 10) * bits / self._serialport.baudrate))

    def start(self, priority = QThread.InheritPriority):
        if not self._alive:
            self._alive = True
            super(ReaderThread, self).start(priority)

    def __del__(self):
        if self._alive:
            self._alive = False
            if hasattr(self._serialport, 'cancel_read'):
                self._serialport.cancel_read()
            else:
                self._serialport.close()
        if not self._stopped:
            self.wait()

    def join(self):
        self.__del__()

    def run(self):
        self._stopped = False
        ts = None
        try:
            while self._alive:
                bytes_data = self._serialport.read(self._serialport.inWaiting() or 1)
                wait_time = self.calcWaitTime()
                if self._ts_enabled:
                    ts = datetime.datetime.now().time()
                else:
                    ts = None
                if not self._alive:
                    return
                else:
                    sleep(wait_time)
                while self._serialport.inWaiting():
                    bytes_data = bytes_data + self._serialport.read(self._serialport.inWaiting())
                    if 4096 < len(bytes_data):
                        break
                    sleep(wait_time)
                    
                if bytes_data:
                    self.read.emit([ts, bytes_data])
        except Exception as e:
            self.exception.emit('{}'.format(e))
        self._stopped = True

class PortMonitorThread(QThread):
    portsListChanged = Signal(list)
    exception = Signal(str)

    def __init__(self, parent=None):
        super(PortMonitorThread, self).__init__(parent)
        self._alive = None
        self._stopped = True
        self._ports_set = set()

    def start(self, priority = QThread.InheritPriority):
        if not self._alive:
            self._alive = True
            super(PortMonitorThread, self).start(priority)

    def __del__(self):
        self._alive = False
        if not self._stopped:
            self.wait()

    def join(self):
        self.__del__()

    def run(self):
        self._stopped = False
        while self._alive:
            try:
                new_lst = [[port, desc, is_port_busy(port)] for port, desc, _ in sorted(comports())]
                new_set = set([port for port, _, _ in new_lst])
                if new_set != self._ports_set:
                    increased = new_set - self._ports_set
                    decreased = self._ports_set - new_set
                    self.portsListChanged.emit([new_lst, increased, decreased])

                    self._ports_set = new_set
                sleep(1)
            except Exception as e:
                self.exception.emit('{}'.format(e))
        self._stopped = True

class LoopSendThread(QThread):
    trigger = Signal()
    exception = Signal(str)
    
    def __init__(self, parent=None):
        super(LoopSendThread, self).__init__(parent)
        self._alive = False
        self._stopped = True
        self._spacing = 1.0

    def start(self, period_spacing, priority = QThread.InheritPriority):
        if not self._alive:
            self._alive = True
            self._spacing = period_spacing
            super(LoopSendThread, self).start(priority)

    def __del__(self):
        self._alive = False
        if not self._stopped:
            self.wait()

    def join(self):
        self.__del__()

    def run(self):
        self._stopped = False
        while self._alive:
            try:
                self.trigger.emit()
                sleep(self._spacing)
            except Exception as e:
                self.exception.emit('{}'.format(e))
        self._stopped = True

if __name__ == '__main__':
    QApplication.setHighDpiScaleFactorRoundingPolicy(
            Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
    app = QApplication(sys.argv)
    app.setAttribute(Qt.AA_DontCreateNativeWidgetSiblings)
    frame = MainWindow()
    frame.show()
    app.exec_()
