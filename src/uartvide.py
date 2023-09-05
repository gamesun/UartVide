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

# PySide2
from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from qfluentwidgets import *
from qframelesswindow import *
import resources
from ui_mainwindow import Ui_MainWindow


from combo import Combo
from animationswitchbutton import AnimationSwitchButton
from toolbutton import ToolButton
from rename_dailog import RenameDailog
from elidedlineedit import ElidedLineEdit

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
    UI_FONT = "Segoe UI"
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
        self.portMonitorThread.setPort(self.serialport)
        self.loopSendThread = LoopSendThread(self)
        self._is_always_on_top = False
        self._viewMode = None
        self._is_loop_sending = False
        self._is_timestamp = False
        
        self._qckSnd_OptRow = 1
        self._qckSnd_RawData = []
        self._qckSnd_EdtLst = []
        self._qckSnd_PathBtnLst = []

        self.setupUi(self)
        self.setCorner(Qt.TopLeftCorner, Qt.LeftDockWidgetArea)
        self.setCorner(Qt.BottomLeftCorner, Qt.LeftDockWidgetArea)

        font1 = QFont()
        font1.setFamily(UI_FONT)
        font1.setKerning(True)
        font1.setStyleStrategy(QFont.PreferAntialias)
        self.setFont(font1)

        self.initMoreSettingsMenu()
        self.initQuickSndOptMenu()
        self.setupFlatUi()
        self.setupTitleBar()

        font2 = QFont()
        font2.setFamily(CODE_FONT)
        font2.setPointSize(9)
        self.txtEdtOutput.setFont(font2)
        self.txtEdtInput.setFont(font2)
        #self.quickSendTable.setFont(font2)
        
        icon = QIcon(":/uartvide-icon/uartvide.ico")
        self.setWindowIcon(icon)
        self.actionAbout.setIcon(icon)

        self.defaultStyleWidget = QWidget()
        self.defaultStyleWidget.setWindowIcon(icon)

        # bind events
        self.actionOpen_Cmd_File.triggered.connect(self.openQuickSendFile)
        self.actionSave_Log.triggered.connect(self.onSaveLog)
        self.actionExit.triggered.connect(self.close)   # -> closeEvent

        self.actionQuick_Send_Panel.triggered.connect(self.onToggleQckSndPnl)
        self.actionSend_Panel.triggered.connect(self.onToggleSndPnl)
        self.dockWidget_QuickSend.visibilityChanged.connect(self.onVisibleQckSndPnl)
        self.dockWidget_Send.visibilityChanged.connect(self.onVisibleSndPnl)
        # self.dockWidget_QuickSend.dockLocationChanged.connect(self.onDockLocationChanged)

        self.actionAbout.triggered.connect(self.onAbout)

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

    def onRefreshPorts(self):
        ports_cnt, ports_info = self.onEnumPorts()
        InfoBar.info(
            title='{} Port(s) Found'.format(ports_cnt),
            content=ports_info,
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.BOTTOM,
            duration=2000,
            parent=self
        )

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
        self.actionExit = Action(FluentIcon.CLOSE, self.tr('Exit'))
        self.actionSend_Panel = Action(FluentIcon.VIEW, self.tr('Send Panel'))
        self.actionSend_Panel.setCheckable(True)
        self.actionAbout = Action(self.tr('About'))
        self.actionOpen_Cmd_File = Action(FluentIcon.EDIT, self.tr('Open Cmd File'))
        self.actionQuick_Send_Panel = Action(FluentIcon.VIEW, self.tr('Quick Send Panel'))
        self.actionQuick_Send_Panel.setCheckable(True)
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

    def initQuickSndOptMenu(self):
        self.actionRename = QtWidgets.QAction("Rename", self)
        self.actionRename.triggered.connect(self.onQuickSndRename)

        self.actionInsertRow = QtWidgets.QAction("Insert row", self)
        self.actionInsertRow.triggered.connect(self.onQuickSndInsertRow)

        self.actionDeleteRow = QtWidgets.QAction("Delete row", self)
        self.actionDeleteRow.triggered.connect(self.onQuickSndDeleteRow)

        self.actionSend_Hex = QtWidgets.QAction("HEX", self)
        self.actionSend_Hex.triggered.connect(self.onSetSendHex)

        self.actionSend_Asc = QtWidgets.QAction("ASCII", self)
        self.actionSend_Asc.triggered.connect(self.onSetSendAsc)

        self.actionSend_AscS = QtWidgets.QAction(r"ASCII and \n \r \t...", self)
        self.actionSend_AscS.triggered.connect(self.onSetSendAscS)
        
        self.actionSend_HF = QtWidgets.QAction(self)
        self.actionSend_HF.setText("HEX text File")
        self.actionSend_HF.setStatusTip('Send text file in HEX form("31 32 FF ...")')
        self.actionSend_HF.triggered.connect(self.onSetSendHF)
        
        self.actionSend_AF = QtWidgets.QAction(self)
        self.actionSend_AF.setText("ASCII text file")
        self.actionSend_AF.setStatusTip('Send text file in ASCII form("abc123...")')
        self.actionSend_AF.triggered.connect(self.onSetSendAF)
        
        self.actionSend_BF = QtWidgets.QAction("All file", self)
        self.actionSend_BF.triggered.connect(self.onSetSendBF)

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
            QLabel { color:%(TextColor)s; font-size:9pt; font-family:%(UIFont)s; }

            QComboBox {
                color:%(TextColor)s;
                font-size:9pt;
                font-family:%(UIFont)s;
                border: none;
                padding: 1px 1px 1px 3px;
            }
            QComboBox:editable { background: white; }
            QComboBox:!editable, QComboBox::drop-down:editable { background: #62c7e0; }
            QComboBox:!editable:hover, QComboBox::drop-down:editable:hover { background: #c7eaf3; }
            QComboBox:!editable:pressed, QComboBox::drop-down:editable:pressed { background: #35b6d7; }
            QComboBox:!editable:disabled, QComboBox::drop-down:editable:disabled { background: #c0c0c0; }
            QComboBox:on { padding-top: 3px; padding-left: 4px; }
            QComboBox::drop-down { subcontrol-origin: padding; subcontrol-position: top right; width: 16px; border: none; }
            QComboBox::down-arrow { image: url(:/downarrow.png); }
            QComboBox::down-arrow:on { image: url(:/uparrow.png); }
            QComboBox QAbstractItemView { background: white; }

            QSpinBox {
                border: none;
                background: white;
                color:%(TextColor)s;
                font-size:9pt;
                font-family:%(UIFont)s;
            }
            QSpinBox::up-button { image: url(:/uparrow.png); height: 12px; }
            QSpinBox::down-button { image: url(:/downarrow.png); height: 12px; }
            QSpinBox::up-button, QSpinBox::down-button { background: #62c7e0; }
            QSpinBox::up-button:hover, QSpinBox::down-button:hover { background: #c7eaf3; }
            QSpinBox::up-button:pressed, QSpinBox::down-button:pressed { background: #35b6d7; }
            QSpinBox::up-button:disabled, QSpinBox::up-button:off, 
            QSpinBox::down-button:disabled, QSpinBox::down-button:off { background: #c0c0c0; }
            QSpinBox:disabled { background: #e0e0e0; }
            
            QGroupBox {
                color:%(TextColor)s;
                font-size:8pt;
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
            
            QCheckBox { color:%(TextColor)s; spacing: 5px; font-size:9pt; font-family:%(UIFont)s; }
            QCheckBox::indicator:unchecked { image: url(:/checkbox_unchecked.png); }
            QCheckBox::indicator:unchecked:hover { image: url(:/checkbox_unchecked_hover.png); }
            QCheckBox::indicator:unchecked:pressed { image: url(:/checkbox_unchecked_pressed.png); }
            QCheckBox::indicator:checked { image: url(:/checkbox_checked.png); }
            QCheckBox::indicator:checked:hover { image: url(:/checkbox_checked_hover.png); }
            QCheckBox::indicator:checked:pressed { image: url(:/checkbox_checked_pressed.png); }
            
            QRadioButton { color:%(TextColor)s; spacing: 4px; font-size:9pt; font-family:%(UIFont)s; }
            QRadioButton::indicator:unchecked { image: url(:/radiobutton_unchecked.png); }
            QRadioButton::indicator:unchecked:hover { image: url(:/radiobutton_unchecked_hover.png); }
            QRadioButton::indicator:unchecked:pressed { image: url(:/radiobutton_unchecked_pressed.png); }
            QRadioButton::indicator:checked { image: url(:/radiobutton_checked.png); }
            QRadioButton::indicator:checked:hover { image: url(:/radiobutton_checked_hover.png); }
            QRadioButton::indicator:checked:pressed { image: url(:/radiobutton_checked_pressed.png); }
            
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
                image: url(:/rightarrow.png);
                border: none;
                background: %(ScrollBar_Line)s;
                width: 20px;
                subcontrol-position: right;
                subcontrol-origin: margin;
            }
            QScrollBar::sub-line:horizontal {
                image: url(:/leftarrow.png);
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
                image: url(:/downarrow.png);
                border: none;
                background: %(ScrollBar_Line)s;
                height: 20px;
                subcontrol-position: bottom;
                subcontrol-origin: margin;
            }
            QScrollBar::sub-line::vertical {
                image: url(:/uparrow.png);
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
                font-size:9pt;
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
                font-size:9pt;
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
            
            QTabBar { qproperty-drawBase: 0; }  /* remove the mysterious unstyled horizontal line */
            
            QTabBar::tab {
                font-size:9pt;
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
        self.btnLoop.setIcon(QIcon(":/loop.png"))
        self.btnLoop.setIconSize(QtCore.QSize(20, 20))
        self.btnLoop.clicked.connect(self.onLoopChanged)
        self.btnLoop.setToolTip("Loop Send")
        self.btnLoop.setCursor(Qt.PointingHandCursor)

        self.dockWidget_QuickSend.setStyleSheet("""
            QToolButton, QPushButton {
                background-color:#27b798;
                font-family:Tahoma;
                font-size:8pt;
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
        self.btnRefresh.setIcon(QIcon(":/refresh.png"))
        self.btnRefresh.setIconSize(QtCore.QSize(24, 24))
        self.btnRefresh.setToolTip("Refresh Ports")
        self.btnRefresh.setCursor(Qt.PointingHandCursor)
        self.btnRefresh.clicked.connect(self.onRefreshPorts)
        
        self.cmbPort = Combo(self.titleBar)
        self.cmbPort.setEditable(True)
        self.cmbPort.setCurrentText("")
        self.cmbPort.setFixedSize(QSize(80, 24))
        self.cmbPort.setMinimumSize(QSize(80, 24))
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
        self.btnTogglePortCfgBar.setIcon(QIcon(':/up.png'))
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

        self.cmbViewMode = QComboBox(self.titleBar)
        self.cmbViewMode.addItems(['Ascii', 'HEX', 'hex'])
        self.cmbViewMode.setFixedSize(QSize(50, 24))
        self.cmbViewMode.currentTextChanged.connect(self.onViewModeChanged)
        self.cmbViewMode.setToolTip("Select hexadecimal/ASCII")
        self.cmbViewMode.setCursor(Qt.PointingHandCursor)

        self.btnTimestamp = QPushButton(self.titleBar)
        self.btnTimestamp.setFixedSize(QSize(24, 24))
        self.btnTimestamp.setStyleSheet(self.chkbtn_SSTemplate % {'BG':'transparent', 'HBG':'#51c0d1'})
        self.btnTimestamp.setIcon(QIcon(":/timestamp.png"))
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
        self.btnSaveLog.setIcon(QIcon(":/save.png"))
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
        self.btnClear.setIcon(QIcon(":/eraser.png"))
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
        self.btnClearRxTxCnt.setIcon(QIcon(":/clear.png"))
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
        self.btnMenu.setIcon(QIcon(":/menu.png"))
        self.btnMenu.setIconSize(QtCore.QSize(24, 24))
        self.btnMenu.setToolTip("More Settings...")
        self.btnMenu.setCursor(Qt.PointingHandCursor)
        self.btnMenu.clicked.connect(self.onMoreSettings)

        self.hBxLyt_tb_0 = QHBoxLayout()
        self.hBxLyt_tb_0.setObjectName('hBxLyt_tb_0')
        self.hBxLyt_tb_0.setSpacing(6)
        self.hBxLyt_tb_0.setContentsMargins(6, 0, 0, 0)
        self.hBxLyt_tb_0.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)

        self.hBxLyt_tb_1 = QHBoxLayout()
        self.hBxLyt_tb_1.setObjectName('hBxLyt_tb_1')
        self.hBxLyt_tb_1.setSpacing(0)
        self.hBxLyt_tb_1.setContentsMargins(10, 0, 0, 0)
        self.hBxLyt_tb_1.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)
        
        self.hBxLyt_tb_1.addWidget(self.btnRefresh, 0, Qt.AlignLeft)
        self.hBxLyt_tb_1.addWidget(self.cmbPort, 0, Qt.AlignLeft)
        
        self.hBxLyt_tb_2 = QHBoxLayout()
        self.hBxLyt_tb_2.setObjectName('hBxLyt_tb_2')
        self.hBxLyt_tb_2.setSpacing(0)
        self.hBxLyt_tb_2.setContentsMargins(0, 0, 0, 0)
        self.hBxLyt_tb_2.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)
        
        self.hBxLyt_tb_2.addWidget(self.btnClearRxTxCnt, 0, Qt.AlignLeft)
        self.hBxLyt_tb_2.addWidget(self.lblRxTxCnt, 0, Qt.AlignLeft)

        self.hBxLyt_tb_0.addWidget(self.lblIcon, 0, Qt.AlignLeft)
        self.hBxLyt_tb_0.addWidget(self.lblTitle, 0, Qt.AlignLeft)
        self.hBxLyt_tb_0.addLayout(self.hBxLyt_tb_1)
        self.hBxLyt_tb_0.addWidget(self.asbtnOpen, 0, Qt.AlignLeft)
        self.hBxLyt_tb_0.addWidget(self.btnTogglePortCfgBar, 0, Qt.AlignLeft)
        self.hBxLyt_tb_0.addWidget(self.cmbViewMode, 0, Qt.AlignLeft)
        
        self.hBxLyt_tb_0.addWidget(self.btnTimestamp, 0, Qt.AlignLeft)
        self.hBxLyt_tb_0.addWidget(self.btnSaveLog, 0, Qt.AlignLeft)
        self.hBxLyt_tb_0.addWidget(self.btnClear, 0, Qt.AlignLeft)
        self.hBxLyt_tb_0.addLayout(self.hBxLyt_tb_2)
        self.hBxLyt_tb_0.addWidget(self.btnMenu, 0, Qt.AlignLeft)

        self.hBxLyt_tb_0.addStretch(1)

        self.titleBar.hBoxLayout.insertLayout(0, self.hBxLyt_tb_0, 0)

        self.btnPin = TransparentToggleToolButton(self.titleBar)
        self.btnPin.setFixedSize(QSize(26, 26))

        self.btnPin.setIcon(QIcon(":/pin.png"))
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
            self.btnTogglePortCfgBar.setIcon(QIcon(':/up.png'))
        else:
            self.frame_PortCfg.hide()
            self.btnTogglePortCfgBar.setIcon(QIcon(':/down.png'))

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
        if os.path.isfile(get_config_path('QuickSend.csv')):
            self.loadQuickSendByFile(get_config_path('QuickSend.csv'))
        else:
            for row in range(500):
                self._qckSnd_RawData.append(['%d' % (row+1), 'H', ''])
                # self.initQuickSendButton(row, cmd = '%d' % (row+1))
        
        self.quickSendTable.setColumnCount(3)
        self.quickSendTable.setRowCount(len(self._qckSnd_RawData))

        self.qckSnd_CreateButtons()

        self.quickSendTable.resizeColumnsToContents()

    def qckSnd_CreateButtons(self):
        for i in range(len(self._qckSnd_RawData)):
            self.initQuickSendButton(i, self._qckSnd_RawData[i][0], self._qckSnd_RawData[i][1], 
                                        self._qckSnd_RawData[i][2], force_new = True)

    def initQuickSendButton(self, row, cmd = 'cmd', opt = 'H', dat = '', force_new=False):
        if force_new or self.quickSendTable.cellWidget(row, 0) is None:
            btn1 = ToolButton(self)
            btn1.setText(cmd)
            btn1.setCursor(Qt.PointingHandCursor)
            btn1.clicked.connect(lambda : self.onQuickSend(row))
            btn1.rightClicked.connect(lambda : self.onQuickSendRightClick(row))
            self.quickSendTable.setCellWidget(row, 0, btn1)
        else:
            btn1 = self.quickSendTable.cellWidget(row, 0)
            btn1.setText(cmd)
            # btn1.clicked.connect(lambda : self.onQuickSend(row))
            # btn1.rightClicked.connect(lambda : self.onQuickSendRightClick(row))

        if force_new or self.quickSendTable.cellWidget(row, 1) is None:
            btn2 = QToolButton(self)
            btn2.setText(opt)
            btn2.setCursor(Qt.PointingHandCursor)
            #item.setMaximumSize(QtCore.QSize(16, 16))
            btn2.clicked.connect(lambda : self.onQuickSendOptions(row))
            self.quickSendTable.setCellWidget(row, 1, btn2)
        else:
            btn2 = self.quickSendTable.cellWidget(row, 1)
            btn2.setText(opt)
            # btn2.clicked.connect(lambda : self.onQuickSendOptions(row))

        if force_new or self.quickSendTable.cellWidget(row, 2) is None:
            item = ElidedLineEdit(dat)
            item.setStyleSheet('''
                QLineEdit {border: none;font-size:9pt;font-family:%(Code_Font)s;}
                QMenu {margin: 2px;color: #202020;background: #eeeeee;}
                QMenu::item {padding: 2px 12px 2px 12px;border: 1px solid transparent;}
                QMenu::item:selected {background: #51c0d1;}
                QMenu::icon {background: transparent;border: 2px inset transparent;}
                QMenu::item:disabled {color: #808080;background: #eeeeee;}''' % dict(Code_Font = CODE_FONT))
            self._qckSnd_EdtLst.append(item)
            btnPath = QPushButton('...')
            btnPath.setMinimumSize(QSize(17, 17))
            btnPath.setMaximumSize(QSize(17, 17))
            btnPath.clicked.connect(lambda : self.onQuickSendSelectFile(row))
            self._qckSnd_PathBtnLst.append(btnPath)
            hLayout = QHBoxLayout()
            hLayout.addWidget(item)
            hLayout.addWidget(btnPath)
            hLayout.setSpacing(0)
            hLayout.setContentsMargins(0, 0, 1, 0)
            frame = QFrame()
            frame.setLayout(hLayout)
            self.quickSendTable.setCellWidget(row, 2, frame)
        else:
            self._qckSnd_EdtLst[row].setText(dat)

        if opt == 'HF' or opt == 'AF' or opt == 'BF':
            self._qckSnd_PathBtnLst[row].show()
        else:
            self._qckSnd_PathBtnLst[row].hide()

        self.quickSendTable.setRowHeight(row, 20)

    def onSetSendHex(self):
        self.quickSendTable.cellWidget(self._qckSnd_OptRow, 1).setText('H')
        self._qckSnd_PathBtnLst[self._qckSnd_OptRow].hide()

    def onSetSendAsc(self):
        self.quickSendTable.cellWidget(self._qckSnd_OptRow, 1).setText('A')
        self._qckSnd_PathBtnLst[self._qckSnd_OptRow].hide()
        
    def onSetSendAscS(self):
        self.quickSendTable.cellWidget(self._qckSnd_OptRow, 1).setText('AS')
        self._qckSnd_PathBtnLst[self._qckSnd_OptRow].hide()

    def onSetSendHF(self):
        self.quickSendTable.cellWidget(self._qckSnd_OptRow, 1).setText('HF')
        self._qckSnd_PathBtnLst[self._qckSnd_OptRow].show()

    def onSetSendAF(self):
        self.quickSendTable.cellWidget(self._qckSnd_OptRow, 1).setText('AF')
        self._qckSnd_PathBtnLst[self._qckSnd_OptRow].show()

    def onSetSendBF(self):
        self.quickSendTable.cellWidget(self._qckSnd_OptRow, 1).setText('BF')
        self._qckSnd_PathBtnLst[self._qckSnd_OptRow].show()

    def onQuickSendOptions(self, row):
        print('onQuickSendOptions', row)
        self._qckSnd_OptRow = row
        item = self.quickSendTable.cellWidget(row, 1)
        self.menuSendOpt.popup(item.mapToGlobal(QPoint(item.size().width(), item.size().height())))

    def onQuickSendSelectFile(self, row):
        print('onQuickSendSelectFile', row)
        old_path = self._qckSnd_EdtLst[row].text()
        fileName = QFileDialog.getOpenFileName(self.defaultStyleWidget, "Select a file",
            old_path, "All Files (*.*)")[0]
        if fileName:
            self._qckSnd_EdtLst[row].setText(fileName)

    def openQuickSendFile(self):
        fileName = QFileDialog.getOpenFileName(self.defaultStyleWidget, "Select a file",
            os.getcwd(), "CSV Files (*.csv)")[0]
        if fileName:
            self.loadQuickSendByFile(fileName, notifyExcept = True)

    def saveQuickSend(self):
        try:
            self.quickSendTable.saveToCSV(get_config_path('QuickSend.csv'))
        except Exception as e:
            print("(line {}){}".format(sys.exc_info()[-1].tb_lineno, str(e)))

    def loadQuickSendByFile(self, path, notifyExcept = False):
        try:
            self.quickSendTable.loadFromCSV(path)
        except Exception as e:
            print("(line {}){}".format(sys.exc_info()[-1].tb_lineno, str(e)))
            if notifyExcept:
                QMessageBox.critical(self.defaultStyleWidget, "Load failed",
                    str(e), QMessageBox.Close)

    def onQuickSend(self, row):
        print('onQuickSend', row)
        try:
            if self.serialport.isOpen():
                if self.quickSendTable.cellWidget(row, 2) != None:
                    tablestring = self._qckSnd_EdtLst[row].text()
                    form = self.quickSendTable.cellWidget(row, 1).text()
                    if 'H' == form:
                        self.transmitHex(tablestring)
                    elif 'A' == form:
                        self.transmitAsc(tablestring)
                    elif 'AS' == form:
                        self.transmitAscS(tablestring)
                    else:
                        self.transmitFile(tablestring, form)
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
        print('onQuickSendRightClick', row)
        item = self.quickSendTable.cellWidget(row, 0)
        oldname = item.text()
        pos = item.mapToGlobal(QPoint(30, 10))
        newname = RenameDailog.getNewName(oldname, pos)
        if newname:
            item.setText(newname)
            self.quickSendTable.resizeColumnsToContents()

    def onQuickSndRename(self):
        self.onQuickSendRightClick(self._qckSnd_OptRow)

    def onQuickSndInsertRow(self):
        self._qckSnd_RawData.insert(self._qckSnd_OptRow, ['new', 'H', ''])
        self._qckSnd_EdtLst = []
        self._qckSnd_PathBtnLst = []
        self.quickSendTable.setRowCount(len(self._qckSnd_RawData))
        self.qckSnd_CreateButtons()

    def onQuickSndDeleteRow(self):
        # self.quickSendTable.removeRow(self._qckSnd_OptRow)

        del self._qckSnd_RawData[self._qckSnd_OptRow]
        self._qckSnd_EdtLst = []
        self._qckSnd_PathBtnLst = []
        self.quickSendTable.setRowCount(len(self._qckSnd_RawData))
        self.qckSnd_CreateButtons()

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
                font-size:9pt;
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
                font-size:9pt;
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
            self.portMonitorThread.join()
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
                #print("{}".format(e))
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

    def onEnumPorts(self):
        sel = self.cmbPort.currentText()
        self.cmbPort.clear()
        ports_cnt = 0
        ports_info = ''
        for port, desc, _ in sorted(comports()):
            state = ' (Busy)' if self.isPortBusy(port) else ''
            self.cmbPort.addItem(port + '  ' + desc + state)
            ports_info = ports_info + port + '  ' + desc + state + '\n'
            ports_cnt = ports_cnt + 1

        self.fixComboViewSize(self.cmbPort)
        
        idx = self.cmbPort.findText(sel, Qt.MatchContains)
        if idx != -1:
            self.cmbPort.setCurrentIndex(idx)
        else:
            self.cmbPort.setCurrentText('')

        return ports_cnt, ports_info

    def isPortBusy(self, port):
        try:
            se = serial.Serial(port)
        except IOError as e:
            #print(e)
            return True
        else:
            return False

    def onAbout(self):
        QMessageBox.about(self.defaultStyleWidget, "About UartVide", appInfo.aboutme)

    def onAboutQt(self):
        QMessageBox.aboutQt(self.defaultStyleWidget)

    def closeEvent(self, event):
        if self.serialport.isOpen():
            self.closePort()
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
            #print("{}".format(e))
            print("(line {}){}".format(sys.exc_info()[-1].tb_lineno, str(e)))

    def syncMenu(self):
        self.actionQuick_Send_Panel.setChecked(not self.dockWidget_QuickSend.isHidden())
        self.actionSend_Panel.setChecked(not self.dockWidget_Send.isHidden())

    def onViewModeChanged(self, sel):
        self._viewMode = sel

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
    portPlugOut = Signal()
    exception = Signal(str)
    
    def __init__(self, parent=None):
        super(PortMonitorThread, self).__init__(parent)
        self._alive = False
        self._stopped = True
        self._serialport = None

    def setPort(self, port):
        self._serialport = port

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
                port_lst = [port for port, desc, hwid in sorted(comports())]
                if self._serialport.portstr not in port_lst:
                    self.portPlugOut.emit()
                sleep(0.5)
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
