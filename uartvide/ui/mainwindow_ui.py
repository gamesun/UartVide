# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from widgets.quicksendtable import QuickSendTable
from widgets.rightanglecombobox import RightAngleComboBox
from widgets.uvtextedit import UVTextEdit
from widgets.uvtogglebutton import UVToggleButton


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(884, 612)
        font = QFont()
        font.setFamily(u"Tahoma")
        font.setPointSize(10)
        font.setKerning(True)
        font.setStyleStrategy(QFont.PreferAntialias)
        MainWindow.setFont(font)
        MainWindow.setMouseTracking(True)
        MainWindow.setWindowTitle(u"UartVide")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralwidget.setMouseTracking(True)
        self.horizontalLayout_2 = QHBoxLayout(self.centralwidget)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(2, 0, 2, 3)
        self.centerFrame = QFrame(self.centralwidget)
        self.centerFrame.setObjectName(u"centerFrame")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centerFrame.sizePolicy().hasHeightForWidth())
        self.centerFrame.setSizePolicy(sizePolicy)
        self.centerFrame.setMouseTracking(True)
        self.verticalLayout_2 = QVBoxLayout(self.centerFrame)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.frame_PortCfg = QFrame(self.centerFrame)
        self.frame_PortCfg.setObjectName(u"frame_PortCfg")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.frame_PortCfg.sizePolicy().hasHeightForWidth())
        self.frame_PortCfg.setSizePolicy(sizePolicy1)
        self.frame_PortCfg.setMinimumSize(QSize(0, 29))
        self.frame_PortCfg.setMaximumSize(QSize(16777215, 29))
        self.frame_PortCfg.setMouseTracking(True)
        self.frame_PortCfg.setFrameShape(QFrame.NoFrame)
        self.frame_PortCfg.setFrameShadow(QFrame.Raised)
        self.frame_PortCfg.setLineWidth(0)
        self.horizontalLayout_3 = QHBoxLayout(self.frame_PortCfg)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(4, 0, 4, 2)
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setSpacing(6)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label_2 = QLabel(self.frame_PortCfg)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMinimumSize(QSize(0, 20))
        self.label_2.setMaximumSize(QSize(16777215, 20))
        self.label_2.setMouseTracking(True)
#if QT_CONFIG(tooltip)
        self.label_2.setToolTip(u"Baud Rate")
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(statustip)
        self.label_2.setStatusTip(u"Baud Rate")
#endif // QT_CONFIG(statustip)
        self.label_2.setText(u"BR")
        self.label_2.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_4.addWidget(self.label_2)

        self.cmbBaudRate = RightAngleComboBox(self.frame_PortCfg)
        self.cmbBaudRate.addItem(u"50")
        self.cmbBaudRate.addItem(u"75")
        self.cmbBaudRate.addItem(u"110")
        self.cmbBaudRate.addItem(u"134")
        self.cmbBaudRate.addItem(u"150")
        self.cmbBaudRate.addItem(u"200")
        self.cmbBaudRate.addItem(u"300")
        self.cmbBaudRate.addItem(u"600")
        self.cmbBaudRate.addItem(u"1200")
        self.cmbBaudRate.addItem(u"1800")
        self.cmbBaudRate.addItem(u"2400")
        self.cmbBaudRate.addItem(u"4800")
        self.cmbBaudRate.addItem(u"9600")
        self.cmbBaudRate.addItem(u"19200")
        self.cmbBaudRate.addItem(u"38400")
        self.cmbBaudRate.addItem(u"57600")
        self.cmbBaudRate.addItem(u"115200")
        self.cmbBaudRate.addItem(u"230400")
        self.cmbBaudRate.addItem(u"460800")
        self.cmbBaudRate.addItem(u"500000")
        self.cmbBaudRate.addItem(u"576000")
        self.cmbBaudRate.addItem(u"921600")
        self.cmbBaudRate.addItem(u"1000000")
        self.cmbBaudRate.addItem(u"1152000")
        self.cmbBaudRate.addItem(u"1500000")
        self.cmbBaudRate.addItem(u"2000000")
        self.cmbBaudRate.addItem(u"2500000")
        self.cmbBaudRate.addItem(u"3000000")
        self.cmbBaudRate.addItem(u"3500000")
        self.cmbBaudRate.addItem(u"4000000")
        self.cmbBaudRate.setObjectName(u"cmbBaudRate")
        sizePolicy1.setHeightForWidth(self.cmbBaudRate.sizePolicy().hasHeightForWidth())
        self.cmbBaudRate.setSizePolicy(sizePolicy1)
        self.cmbBaudRate.setMinimumSize(QSize(0, 23))
        self.cmbBaudRate.setMaximumSize(QSize(16777215, 23))
        self.cmbBaudRate.setMouseTracking(True)
#if QT_CONFIG(tooltip)
        self.cmbBaudRate.setToolTip(u"Baud Rate")
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(statustip)
        self.cmbBaudRate.setStatusTip(u"Baud Rate")
#endif // QT_CONFIG(statustip)
        self.cmbBaudRate.setMaxVisibleItems(30)

        self.horizontalLayout_4.addWidget(self.cmbBaudRate)

        self.label_3 = QLabel(self.frame_PortCfg)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setMinimumSize(QSize(0, 20))
        self.label_3.setMaximumSize(QSize(16777215, 20))
        self.label_3.setMouseTracking(True)
#if QT_CONFIG(tooltip)
        self.label_3.setToolTip(u"Data Bits")
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(statustip)
        self.label_3.setStatusTip(u"Data Bits")
#endif // QT_CONFIG(statustip)
        self.label_3.setText(u"D")
        self.label_3.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_4.addWidget(self.label_3)

        self.cmbDataBits = RightAngleComboBox(self.frame_PortCfg)
        self.cmbDataBits.addItem(u"8")
        self.cmbDataBits.addItem(u"7")
        self.cmbDataBits.addItem(u"6")
        self.cmbDataBits.addItem(u"5")
        self.cmbDataBits.setObjectName(u"cmbDataBits")
        sizePolicy1.setHeightForWidth(self.cmbDataBits.sizePolicy().hasHeightForWidth())
        self.cmbDataBits.setSizePolicy(sizePolicy1)
        self.cmbDataBits.setMinimumSize(QSize(0, 23))
        self.cmbDataBits.setMaximumSize(QSize(16777215, 23))
        self.cmbDataBits.setMouseTracking(True)
#if QT_CONFIG(tooltip)
        self.cmbDataBits.setToolTip(u"Data Bits")
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(statustip)
        self.cmbDataBits.setStatusTip(u"Data Bits")
#endif // QT_CONFIG(statustip)
        self.cmbDataBits.setCurrentText(u"8")

        self.horizontalLayout_4.addWidget(self.cmbDataBits)

        self.label_4 = QLabel(self.frame_PortCfg)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setMinimumSize(QSize(0, 20))
        self.label_4.setMaximumSize(QSize(16777215, 20))
        self.label_4.setMouseTracking(True)
#if QT_CONFIG(tooltip)
        self.label_4.setToolTip(u"Parity")
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(statustip)
        self.label_4.setStatusTip(u"Parity")
#endif // QT_CONFIG(statustip)
        self.label_4.setText(u"P")
        self.label_4.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_4.addWidget(self.label_4)

        self.cmbParity = RightAngleComboBox(self.frame_PortCfg)
        self.cmbParity.addItem(u"None")
        self.cmbParity.addItem(u"Even")
        self.cmbParity.addItem(u"Odd")
        self.cmbParity.addItem(u"Mark")
        self.cmbParity.addItem(u"Space")
        self.cmbParity.setObjectName(u"cmbParity")
        sizePolicy1.setHeightForWidth(self.cmbParity.sizePolicy().hasHeightForWidth())
        self.cmbParity.setSizePolicy(sizePolicy1)
        self.cmbParity.setMinimumSize(QSize(0, 23))
        self.cmbParity.setMaximumSize(QSize(16777215, 23))
        self.cmbParity.setMouseTracking(True)
#if QT_CONFIG(tooltip)
        self.cmbParity.setToolTip(u"Parity")
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(statustip)
        self.cmbParity.setStatusTip(u"Parity")
#endif // QT_CONFIG(statustip)
        self.cmbParity.setCurrentText(u"None")

        self.horizontalLayout_4.addWidget(self.cmbParity)

        self.label_5 = QLabel(self.frame_PortCfg)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setMinimumSize(QSize(0, 20))
        self.label_5.setMaximumSize(QSize(16777215, 20))
        self.label_5.setMouseTracking(True)
#if QT_CONFIG(tooltip)
        self.label_5.setToolTip(u"Stop Bits")
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(statustip)
        self.label_5.setStatusTip(u"Stop Bits")
#endif // QT_CONFIG(statustip)
        self.label_5.setText(u"S")
        self.label_5.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_4.addWidget(self.label_5)

        self.cmbStopBits = RightAngleComboBox(self.frame_PortCfg)
        self.cmbStopBits.addItem(u"1")
        self.cmbStopBits.addItem(u"1.5")
        self.cmbStopBits.addItem(u"2")
        self.cmbStopBits.setObjectName(u"cmbStopBits")
        self.cmbStopBits.setMinimumSize(QSize(0, 23))
        self.cmbStopBits.setMaximumSize(QSize(16777215, 23))
        self.cmbStopBits.setMouseTracking(True)
#if QT_CONFIG(tooltip)
        self.cmbStopBits.setToolTip(u"Stop Bits")
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(statustip)
        self.cmbStopBits.setStatusTip(u"Stop Bits")
#endif // QT_CONFIG(statustip)
        self.cmbStopBits.setCurrentText(u"1")

        self.horizontalLayout_4.addWidget(self.cmbStopBits)

        self.chkRTSCTS = QCheckBox(self.frame_PortCfg)
        self.chkRTSCTS.setObjectName(u"chkRTSCTS")
        self.chkRTSCTS.setMaximumSize(QSize(16777215, 22))
        self.chkRTSCTS.setMouseTracking(True)
        self.chkRTSCTS.setText(u"RTS/CTS")

        self.horizontalLayout_4.addWidget(self.chkRTSCTS)

        self.chkXonXoff = QCheckBox(self.frame_PortCfg)
        self.chkXonXoff.setObjectName(u"chkXonXoff")
        self.chkXonXoff.setMaximumSize(QSize(16777215, 22))
        self.chkXonXoff.setMouseTracking(True)
        self.chkXonXoff.setText(u"Xon/Xoff")

        self.horizontalLayout_4.addWidget(self.chkXonXoff)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_2)


        self.horizontalLayout_3.addLayout(self.horizontalLayout_4)


        self.verticalLayout_2.addWidget(self.frame_PortCfg)

        self.txtEdtOutput = UVTextEdit(self.centerFrame)
        self.txtEdtOutput.setObjectName(u"txtEdtOutput")
        sizePolicy2 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(3)
        sizePolicy2.setHeightForWidth(self.txtEdtOutput.sizePolicy().hasHeightForWidth())
        self.txtEdtOutput.setSizePolicy(sizePolicy2)
        self.txtEdtOutput.setMouseTracking(True)

        self.verticalLayout_2.addWidget(self.txtEdtOutput)


        self.horizontalLayout_2.addWidget(self.centerFrame)

        MainWindow.setCentralWidget(self.centralwidget)
        self.dockWidget_Send = QDockWidget(MainWindow)
        self.dockWidget_Send.setObjectName(u"dockWidget_Send")
        self.dockWidget_Send.setMouseTracking(True)
        self.dockWidget_Send.setContextMenuPolicy(Qt.PreventContextMenu)
        self.dockWidget_Send.setAllowedAreas(Qt.BottomDockWidgetArea|Qt.LeftDockWidgetArea|Qt.RightDockWidgetArea)
        self.dockWidget_Send.setWindowTitle(u"Send")
        self.dockWidgetContents_2 = QWidget()
        self.dockWidgetContents_2.setObjectName(u"dockWidgetContents_2")
        self.dockWidgetContents_2.setMouseTracking(True)
        self.verticalLayout = QVBoxLayout(self.dockWidgetContents_2)
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 2, 0, 3)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(2, 0, 2, 0)
        self.rdoASC = QRadioButton(self.dockWidgetContents_2)
        self.rdoASC.setObjectName(u"rdoASC")
        self.rdoASC.setMinimumSize(QSize(0, 22))
        self.rdoASC.setMaximumSize(QSize(16777215, 22))
        self.rdoASC.setMouseTracking(True)
        self.rdoASC.setText(u"ASC")

        self.horizontalLayout.addWidget(self.rdoASC)

        self.rdoHEX = QRadioButton(self.dockWidgetContents_2)
        self.rdoHEX.setObjectName(u"rdoHEX")
        self.rdoHEX.setMinimumSize(QSize(0, 22))
        self.rdoHEX.setMaximumSize(QSize(16777215, 22))
        self.rdoHEX.setMouseTracking(True)
        self.rdoHEX.setText(u"HEX")

        self.horizontalLayout.addWidget(self.rdoHEX)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.spnPeriod = QSpinBox(self.dockWidgetContents_2)
        self.spnPeriod.setObjectName(u"spnPeriod")
        self.spnPeriod.setMinimumSize(QSize(0, 22))
        self.spnPeriod.setMaximumSize(QSize(16777215, 22))
        self.spnPeriod.setMouseTracking(True)
#if QT_CONFIG(tooltip)
        self.spnPeriod.setToolTip(u"Period")
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(statustip)
        self.spnPeriod.setStatusTip(u"Period")
#endif // QT_CONFIG(statustip)
        self.spnPeriod.setSuffix(u"ms")
        self.spnPeriod.setMinimum(10)
        self.spnPeriod.setMaximum(999999)
        self.spnPeriod.setValue(1000)

        self.horizontalLayout.addWidget(self.spnPeriod)

        self.btnLoop = UVToggleButton(self.dockWidgetContents_2)
        self.btnLoop.setObjectName(u"btnLoop")
        self.btnLoop.setMinimumSize(QSize(26, 22))
        self.btnLoop.setMaximumSize(QSize(26, 22))
        self.btnLoop.setMouseTracking(True)

        self.horizontalLayout.addWidget(self.btnLoop)

        self.btnLoopCnt = UVToggleButton(self.dockWidgetContents_2)
        self.btnLoopCnt.setObjectName(u"btnLoopCnt")
        self.btnLoopCnt.setMinimumSize(QSize(26, 22))
        self.btnLoopCnt.setMaximumSize(QSize(26, 22))
        self.btnLoopCnt.setMouseTracking(True)

        self.horizontalLayout.addWidget(self.btnLoopCnt)

        self.btnSend = QToolButton(self.dockWidgetContents_2)
        self.btnSend.setObjectName(u"btnSend")
        self.btnSend.setMinimumSize(QSize(50, 22))
        self.btnSend.setMaximumSize(QSize(50, 22))
        self.btnSend.setMouseTracking(True)
        self.btnSend.setText(u"Send")

        self.horizontalLayout.addWidget(self.btnSend)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.frame_LoopCounter = QFrame(self.dockWidgetContents_2)
        self.frame_LoopCounter.setObjectName(u"frame_LoopCounter")
        self.frame_LoopCounter.setMouseTracking(True)
        self.frame_LoopCounter.setFrameShape(QFrame.StyledPanel)
        self.frame_LoopCounter.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_5 = QHBoxLayout(self.frame_LoopCounter)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(2, 0, 2, 0)
        self.label = QLabel(self.frame_LoopCounter)
        self.label.setObjectName(u"label")

        self.horizontalLayout_5.addWidget(self.label)

        self.spnFrom = QSpinBox(self.frame_LoopCounter)
        self.spnFrom.setObjectName(u"spnFrom")
        self.spnFrom.setAlignment(Qt.AlignCenter)
        self.spnFrom.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.spnFrom.setMinimum(-99999)
        self.spnFrom.setMaximum(99999)

        self.horizontalLayout_5.addWidget(self.spnFrom)

        self.label_6 = QLabel(self.frame_LoopCounter)
        self.label_6.setObjectName(u"label_6")

        self.horizontalLayout_5.addWidget(self.label_6)

        self.spnTo = QSpinBox(self.frame_LoopCounter)
        self.spnTo.setObjectName(u"spnTo")
        self.spnTo.setAlignment(Qt.AlignCenter)
        self.spnTo.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.spnTo.setMinimum(-99999)
        self.spnTo.setMaximum(99999)
        self.spnTo.setValue(100)

        self.horizontalLayout_5.addWidget(self.spnTo)

        self.label_7 = QLabel(self.frame_LoopCounter)
        self.label_7.setObjectName(u"label_7")

        self.horizontalLayout_5.addWidget(self.label_7)

        self.spnStep = QSpinBox(self.frame_LoopCounter)
        self.spnStep.setObjectName(u"spnStep")
        self.spnStep.setAlignment(Qt.AlignCenter)
        self.spnStep.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.spnStep.setMinimum(-99999)
        self.spnStep.setMaximum(99999)
        self.spnStep.setValue(1)

        self.horizontalLayout_5.addWidget(self.spnStep)

        self.label_8 = QLabel(self.frame_LoopCounter)
        self.label_8.setObjectName(u"label_8")

        self.horizontalLayout_5.addWidget(self.label_8)

        self.spnNext = QSpinBox(self.frame_LoopCounter)
        self.spnNext.setObjectName(u"spnNext")
        self.spnNext.setAlignment(Qt.AlignCenter)
        self.spnNext.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.spnNext.setMinimum(-99999)
        self.spnNext.setMaximum(99999)

        self.horizontalLayout_5.addWidget(self.spnNext)

        self.horizontalLayout_5.setStretch(1, 1)
        self.horizontalLayout_5.setStretch(3, 1)
        self.horizontalLayout_5.setStretch(5, 1)
        self.horizontalLayout_5.setStretch(7, 1)

        self.verticalLayout.addWidget(self.frame_LoopCounter)

        self.txtEdtInput = UVTextEdit(self.dockWidgetContents_2)
        self.txtEdtInput.setObjectName(u"txtEdtInput")
        self.txtEdtInput.setMouseTracking(True)
        self.txtEdtInput.setFrameShape(QFrame.NoFrame)
        self.txtEdtInput.setFrameShadow(QFrame.Plain)
        self.txtEdtInput.setLineWidth(0)

        self.verticalLayout.addWidget(self.txtEdtInput)

        self.verticalLayout.setStretch(2, 1)
        self.dockWidget_Send.setWidget(self.dockWidgetContents_2)
        MainWindow.addDockWidget(Qt.RightDockWidgetArea, self.dockWidget_Send)
        self.dockWidget_QuickSend = QDockWidget(MainWindow)
        self.dockWidget_QuickSend.setObjectName(u"dockWidget_QuickSend")
        self.dockWidget_QuickSend.setMouseTracking(True)
        self.dockWidget_QuickSend.setContextMenuPolicy(Qt.PreventContextMenu)
        self.dockWidget_QuickSend.setAllowedAreas(Qt.LeftDockWidgetArea|Qt.RightDockWidgetArea)
        self.dockWidget_QuickSend.setWindowTitle(u"Quick Send")
        self.dockWidgetContents_3 = QWidget()
        self.dockWidgetContents_3.setObjectName(u"dockWidgetContents_3")
        self.dockWidgetContents_3.setMouseTracking(True)
        self.verticalLayout_3 = QVBoxLayout(self.dockWidgetContents_3)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 3)
        self.qckSndTbl = QuickSendTable(self.dockWidgetContents_3)
        if (self.qckSndTbl.columnCount() < 3):
            self.qckSndTbl.setColumnCount(3)
        self.qckSndTbl.setObjectName(u"qckSndTbl")
        font1 = QFont()
        font1.setFamily(u"Consolas")
        font1.setPointSize(10)
        font1.setKerning(True)
        font1.setStyleStrategy(QFont.PreferAntialias)
        self.qckSndTbl.setFont(font1)
        self.qckSndTbl.setMouseTracking(True)
        self.qckSndTbl.setEditTriggers(QAbstractItemView.AllEditTriggers)
        self.qckSndTbl.setSelectionMode(QAbstractItemView.NoSelection)
        self.qckSndTbl.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.qckSndTbl.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.qckSndTbl.setRowCount(0)
        self.qckSndTbl.setColumnCount(3)
        self.qckSndTbl.horizontalHeader().setVisible(False)
        self.qckSndTbl.horizontalHeader().setMinimumSectionSize(16)
        self.qckSndTbl.horizontalHeader().setStretchLastSection(True)
        self.qckSndTbl.verticalHeader().setVisible(False)
        self.qckSndTbl.verticalHeader().setMinimumSectionSize(16)
        self.qckSndTbl.verticalHeader().setDefaultSectionSize(16)

        self.verticalLayout_3.addWidget(self.qckSndTbl)

        self.dockWidget_QuickSend.setWidget(self.dockWidgetContents_3)
        MainWindow.addDockWidget(Qt.RightDockWidgetArea, self.dockWidget_QuickSend)
        self.toolBar = QToolBar(MainWindow)
        self.toolBar.setObjectName(u"toolBar")
        self.toolBar.setMinimumSize(QSize(0, 34))
        self.toolBar.setMaximumSize(QSize(16777215, 34))
        self.toolBar.setMouseTracking(True)
        self.toolBar.setContextMenuPolicy(Qt.PreventContextMenu)
        self.toolBar.setWindowTitle(u"toolBar")
        self.toolBar.setMovable(False)
        self.toolBar.setAllowedAreas(Qt.TopToolBarArea)
        self.toolBar.setFloatable(False)
        MainWindow.addToolBar(Qt.TopToolBarArea, self.toolBar)

        self.retranslateUi(MainWindow)

        self.cmbBaudRate.setCurrentIndex(12)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):




        self.label.setText(QCoreApplication.translate("MainWindow", u"From", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"To", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"Step", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"Next", None))
        pass
    # retranslateUi

