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


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(903, 612)
        MainWindow.setWindowTitle(u"UartVide")
        self.actionSave_Log = QAction(MainWindow)
        self.actionSave_Log.setObjectName(u"actionSave_Log")
        self.actionSave_Log.setText(u"Save Log")
        self.actionSave_Log.setIconText(u"Save Log")
#if QT_CONFIG(tooltip)
        self.actionSave_Log.setToolTip(u"Save Log")
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(statustip)
        self.actionSave_Log.setStatusTip(u"Save Log")
#endif // QT_CONFIG(statustip)
        self.actionExit = QAction(MainWindow)
        self.actionExit.setObjectName(u"actionExit")
        self.actionExit.setText(u"Exit")
        self.actionExit.setIconText(u"Exit")
#if QT_CONFIG(tooltip)
        self.actionExit.setToolTip(u"Exit")
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(statustip)
        self.actionExit.setStatusTip(u"Exit")
#endif // QT_CONFIG(statustip)
        self.actionOpen = QAction(MainWindow)
        self.actionOpen.setObjectName(u"actionOpen")
        self.actionOpen.setText(u"Open")
        self.actionOpen.setIconText(u"Open")
#if QT_CONFIG(tooltip)
        self.actionOpen.setToolTip(u"Open the port")
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(statustip)
        self.actionOpen.setStatusTip(u"Open the port")
#endif // QT_CONFIG(statustip)
        self.actionClose = QAction(MainWindow)
        self.actionClose.setObjectName(u"actionClose")
        self.actionClose.setText(u"Close")
        self.actionClose.setIconText(u"Close")
#if QT_CONFIG(tooltip)
        self.actionClose.setToolTip(u"Close the port")
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(statustip)
        self.actionClose.setStatusTip(u"Close the port")
#endif // QT_CONFIG(statustip)
        self.actionPort_Config_Panel = QAction(MainWindow)
        self.actionPort_Config_Panel.setObjectName(u"actionPort_Config_Panel")
        self.actionPort_Config_Panel.setCheckable(True)
        self.actionPort_Config_Panel.setText(u"Port Config Panel")
        self.actionPort_Config_Panel.setIconText(u"Show Port Config")
#if QT_CONFIG(tooltip)
        self.actionPort_Config_Panel.setToolTip(u"Show or hide Port Config Panel")
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(statustip)
        self.actionPort_Config_Panel.setStatusTip(u"Show or hide Port Config Panel")
#endif // QT_CONFIG(statustip)
        self.actionAlways_On_Top = QAction(MainWindow)
        self.actionAlways_On_Top.setObjectName(u"actionAlways_On_Top")
        self.actionAlways_On_Top.setCheckable(True)
        self.actionAlways_On_Top.setText(u"Always On Top")
        self.actionAlways_On_Top.setIconText(u"Always on top")
#if QT_CONFIG(tooltip)
        self.actionAlways_On_Top.setToolTip(u"Always on most top")
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(statustip)
        self.actionAlways_On_Top.setStatusTip(u"Always on most top")
#endif // QT_CONFIG(statustip)
        self.actionLocal_Echo = QAction(MainWindow)
        self.actionLocal_Echo.setObjectName(u"actionLocal_Echo")
        self.actionLocal_Echo.setCheckable(True)
        self.actionLocal_Echo.setText(u"Local Echo")
        self.actionLocal_Echo.setIconText(u"Local echo")
#if QT_CONFIG(tooltip)
        self.actionLocal_Echo.setToolTip(u"Local Echo")
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(statustip)
        self.actionLocal_Echo.setStatusTip(u"Echo what you typed")
#endif // QT_CONFIG(statustip)
        self.actionAscii = QAction(MainWindow)
        self.actionAscii.setObjectName(u"actionAscii")
        self.actionAscii.setCheckable(True)
        self.actionAscii.setText(u"Ascii")
        self.actionAscii.setIconText(u"Ascii")
#if QT_CONFIG(tooltip)
        self.actionAscii.setToolTip(u"Show as ascii")
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(statustip)
        self.actionAscii.setStatusTip(u"Show as ascii")
#endif // QT_CONFIG(statustip)
        self.actionHex_lowercase = QAction(MainWindow)
        self.actionHex_lowercase.setObjectName(u"actionHex_lowercase")
        self.actionHex_lowercase.setCheckable(True)
        self.actionHex_lowercase.setText(u"hex(lowercase)")
        self.actionHex_lowercase.setIconText(u"hex(lowercase)")
#if QT_CONFIG(tooltip)
        self.actionHex_lowercase.setToolTip(u"Show as hex(lowercase)")
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(statustip)
        self.actionHex_lowercase.setStatusTip(u"Show as hex(lowercase)")
#endif // QT_CONFIG(statustip)
        self.actionHEX_UPPERCASE = QAction(MainWindow)
        self.actionHEX_UPPERCASE.setObjectName(u"actionHEX_UPPERCASE")
        self.actionHEX_UPPERCASE.setCheckable(True)
        self.actionHEX_UPPERCASE.setText(u"HEX(UPPERCASE)")
        self.actionHEX_UPPERCASE.setIconText(u"HEX(UPPERCASE)")
#if QT_CONFIG(tooltip)
        self.actionHEX_UPPERCASE.setToolTip(u"Show as HEX(UPPERCASE)")
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(statustip)
        self.actionHEX_UPPERCASE.setStatusTip(u"Show as HEX(UPPERCASE)")
#endif // QT_CONFIG(statustip)
        self.actionSend_Hex_Panel = QAction(MainWindow)
        self.actionSend_Hex_Panel.setObjectName(u"actionSend_Hex_Panel")
        self.actionSend_Hex_Panel.setCheckable(True)
        self.actionSend_Hex_Panel.setText(u"Send Hex Panel")
        self.actionSend_Hex_Panel.setIconText(u"Send Hex Panel")
#if QT_CONFIG(tooltip)
        self.actionSend_Hex_Panel.setToolTip(u"Show or hide Send Hex Panel")
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(statustip)
        self.actionSend_Hex_Panel.setStatusTip(u"Show or hide Hex Transmit Panel")
#endif // QT_CONFIG(statustip)
        self.actionAbout = QAction(MainWindow)
        self.actionAbout.setObjectName(u"actionAbout")
        self.actionAbout.setText(u"About UartVide")
        self.actionAbout.setIconText(u"About UartVide")
#if QT_CONFIG(tooltip)
        self.actionAbout.setToolTip(u"About UartVide")
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(statustip)
        self.actionAbout.setStatusTip(u"About UartVide")
#endif // QT_CONFIG(statustip)
        self.actionAbout_Qt = QAction(MainWindow)
        self.actionAbout_Qt.setObjectName(u"actionAbout_Qt")
        self.actionAbout_Qt.setText(u"About Qt")
        self.actionAbout_Qt.setIconText(u"About Qt")
#if QT_CONFIG(tooltip)
        self.actionAbout_Qt.setToolTip(u"About Qt")
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(statustip)
        self.actionAbout_Qt.setStatusTip(u"About Qt")
#endif // QT_CONFIG(statustip)
        self.actionOpen_Cmd_File = QAction(MainWindow)
        self.actionOpen_Cmd_File.setObjectName(u"actionOpen_Cmd_File")
        self.actionOpen_Cmd_File.setText(u"Open Quick Send File")
        self.actionOpen_Cmd_File.setIconText(u"Open Cmd File")
#if QT_CONFIG(tooltip)
        self.actionOpen_Cmd_File.setToolTip(u"Load Quick Send Settings")
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(statustip)
        self.actionOpen_Cmd_File.setStatusTip(u"Open Cmd File")
#endif // QT_CONFIG(statustip)
        self.actionQuick_Send_Panel = QAction(MainWindow)
        self.actionQuick_Send_Panel.setObjectName(u"actionQuick_Send_Panel")
        self.actionQuick_Send_Panel.setCheckable(True)
        self.actionQuick_Send_Panel.setText(u"Quick Send Panel")
        self.actionQuick_Send_Panel.setIconText(u"Quick Send Panel")
#if QT_CONFIG(tooltip)
        self.actionQuick_Send_Panel.setToolTip(u"Show or hide Quick Send Panel")
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(statustip)
        self.actionQuick_Send_Panel.setStatusTip(u"Show or hide Quick Send Panel")
#endif // QT_CONFIG(statustip)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout_2 = QHBoxLayout(self.centralwidget)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(1, 0, 1, 0)
        self.centerFrame = QFrame(self.centralwidget)
        self.centerFrame.setObjectName(u"centerFrame")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centerFrame.sizePolicy().hasHeightForWidth())
        self.centerFrame.setSizePolicy(sizePolicy)
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
#if QT_CONFIG(tooltip)
        self.label_2.setToolTip(u"Baud Rate")
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(statustip)
        self.label_2.setStatusTip(u"Baud Rate")
#endif // QT_CONFIG(statustip)
        self.label_2.setText(u"BR")
        self.label_2.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_4.addWidget(self.label_2)

        self.cmbBaudRate = QComboBox(self.frame_PortCfg)
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
#if QT_CONFIG(tooltip)
        self.cmbBaudRate.setToolTip(u"Baud Rate")
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(statustip)
        self.cmbBaudRate.setStatusTip(u"Baud Rate")
#endif // QT_CONFIG(statustip)
        self.cmbBaudRate.setEditable(True)
        self.cmbBaudRate.setMaxVisibleItems(30)

        self.horizontalLayout_4.addWidget(self.cmbBaudRate)

        self.label_3 = QLabel(self.frame_PortCfg)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setMinimumSize(QSize(0, 20))
        self.label_3.setMaximumSize(QSize(16777215, 20))
#if QT_CONFIG(tooltip)
        self.label_3.setToolTip(u"Data Bits")
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(statustip)
        self.label_3.setStatusTip(u"Data Bits")
#endif // QT_CONFIG(statustip)
        self.label_3.setText(u"D")
        self.label_3.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_4.addWidget(self.label_3)

        self.cmbDataBits = QComboBox(self.frame_PortCfg)
        self.cmbDataBits.addItem(u"8")
        self.cmbDataBits.addItem(u"7")
        self.cmbDataBits.addItem(u"6")
        self.cmbDataBits.addItem(u"5")
        self.cmbDataBits.setObjectName(u"cmbDataBits")
        sizePolicy1.setHeightForWidth(self.cmbDataBits.sizePolicy().hasHeightForWidth())
        self.cmbDataBits.setSizePolicy(sizePolicy1)
        self.cmbDataBits.setMinimumSize(QSize(0, 23))
        self.cmbDataBits.setMaximumSize(QSize(16777215, 23))
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
#if QT_CONFIG(tooltip)
        self.label_4.setToolTip(u"Parity")
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(statustip)
        self.label_4.setStatusTip(u"Parity")
#endif // QT_CONFIG(statustip)
        self.label_4.setText(u"P")
        self.label_4.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_4.addWidget(self.label_4)

        self.cmbParity = QComboBox(self.frame_PortCfg)
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
#if QT_CONFIG(tooltip)
        self.label_5.setToolTip(u"Stop Bits")
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(statustip)
        self.label_5.setStatusTip(u"Stop Bits")
#endif // QT_CONFIG(statustip)
        self.label_5.setText(u"S")
        self.label_5.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_4.addWidget(self.label_5)

        self.cmbStopBits = QComboBox(self.frame_PortCfg)
        self.cmbStopBits.addItem(u"1")
        self.cmbStopBits.addItem(u"1.5")
        self.cmbStopBits.addItem(u"2")
        self.cmbStopBits.setObjectName(u"cmbStopBits")
        self.cmbStopBits.setMinimumSize(QSize(0, 23))
        self.cmbStopBits.setMaximumSize(QSize(16777215, 23))
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
        self.chkRTSCTS.setText(u"RTS/CTS")

        self.horizontalLayout_4.addWidget(self.chkRTSCTS)

        self.chkXonXoff = QCheckBox(self.frame_PortCfg)
        self.chkXonXoff.setObjectName(u"chkXonXoff")
        self.chkXonXoff.setMaximumSize(QSize(16777215, 22))
        self.chkXonXoff.setText(u"Xon/Xoff")

        self.horizontalLayout_4.addWidget(self.chkXonXoff)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_2)


        self.horizontalLayout_3.addLayout(self.horizontalLayout_4)


        self.verticalLayout_2.addWidget(self.frame_PortCfg)

        self.txtEdtOutput = QTextEdit(self.centerFrame)
        self.txtEdtOutput.setObjectName(u"txtEdtOutput")
        sizePolicy2 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(3)
        sizePolicy2.setHeightForWidth(self.txtEdtOutput.sizePolicy().hasHeightForWidth())
        self.txtEdtOutput.setSizePolicy(sizePolicy2)
        font = QFont()
        font.setFamily(u"Courier 10 Pitch")
        font.setPointSize(10)
        self.txtEdtOutput.setFont(font)

        self.verticalLayout_2.addWidget(self.txtEdtOutput)


        self.horizontalLayout_2.addWidget(self.centerFrame)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.dockWidget_SendHex = QDockWidget(MainWindow)
        self.dockWidget_SendHex.setObjectName(u"dockWidget_SendHex")
        self.dockWidget_SendHex.setContextMenuPolicy(Qt.PreventContextMenu)
        self.dockWidget_SendHex.setAllowedAreas(Qt.BottomDockWidgetArea|Qt.LeftDockWidgetArea|Qt.RightDockWidgetArea)
        self.dockWidget_SendHex.setWindowTitle(u"Send")
        self.dockWidgetContents_2 = QWidget()
        self.dockWidgetContents_2.setObjectName(u"dockWidgetContents_2")
        self.verticalLayout = QVBoxLayout(self.dockWidgetContents_2)
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 2, 4, 0)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(2, 0, 2, 0)
        self.rdoASC = QRadioButton(self.dockWidgetContents_2)
        self.rdoASC.setObjectName(u"rdoASC")
        self.rdoASC.setMinimumSize(QSize(0, 22))
        self.rdoASC.setMaximumSize(QSize(16777215, 22))
        self.rdoASC.setText(u"ASC")

        self.horizontalLayout.addWidget(self.rdoASC)

        self.rdoHEX = QRadioButton(self.dockWidgetContents_2)
        self.rdoHEX.setObjectName(u"rdoHEX")
        self.rdoHEX.setMinimumSize(QSize(0, 22))
        self.rdoHEX.setMaximumSize(QSize(16777215, 22))
        self.rdoHEX.setText(u"HEX")

        self.horizontalLayout.addWidget(self.rdoHEX)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.spnPeriod = QSpinBox(self.dockWidgetContents_2)
        self.spnPeriod.setObjectName(u"spnPeriod")
        self.spnPeriod.setMinimumSize(QSize(0, 22))
        self.spnPeriod.setMaximumSize(QSize(16777215, 22))
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

        self.btnLoop = QToolButton(self.dockWidgetContents_2)
        self.btnLoop.setObjectName(u"btnLoop")
        self.btnLoop.setMinimumSize(QSize(26, 22))
        self.btnLoop.setMaximumSize(QSize(26, 22))

        self.horizontalLayout.addWidget(self.btnLoop)

        self.btnSend = QToolButton(self.dockWidgetContents_2)
        self.btnSend.setObjectName(u"btnSend")
        self.btnSend.setMinimumSize(QSize(50, 22))
        self.btnSend.setMaximumSize(QSize(50, 22))
        self.btnSend.setText(u"Send")

        self.horizontalLayout.addWidget(self.btnSend)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.txtEdtInput = QTextEdit(self.dockWidgetContents_2)
        self.txtEdtInput.setObjectName(u"txtEdtInput")
        self.txtEdtInput.setFrameShape(QFrame.NoFrame)
        self.txtEdtInput.setFrameShadow(QFrame.Plain)
        self.txtEdtInput.setLineWidth(0)

        self.verticalLayout.addWidget(self.txtEdtInput)

        self.verticalLayout.setStretch(1, 1)
        self.dockWidget_SendHex.setWidget(self.dockWidgetContents_2)
        MainWindow.addDockWidget(Qt.RightDockWidgetArea, self.dockWidget_SendHex)
        self.dockWidget_QuickSend = QDockWidget(MainWindow)
        self.dockWidget_QuickSend.setObjectName(u"dockWidget_QuickSend")
        self.dockWidget_QuickSend.setContextMenuPolicy(Qt.PreventContextMenu)
        self.dockWidget_QuickSend.setAllowedAreas(Qt.LeftDockWidgetArea|Qt.RightDockWidgetArea)
        self.dockWidget_QuickSend.setWindowTitle(u"Quick Send")
        self.dockWidgetContents_3 = QWidget()
        self.dockWidgetContents_3.setObjectName(u"dockWidgetContents_3")
        self.verticalLayout_3 = QVBoxLayout(self.dockWidgetContents_3)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.quickSendTable = QTableWidget(self.dockWidgetContents_3)
        if (self.quickSendTable.columnCount() < 2):
            self.quickSendTable.setColumnCount(2)
        if (self.quickSendTable.rowCount() < 10):
            self.quickSendTable.setRowCount(10)
        self.quickSendTable.setObjectName(u"quickSendTable")
        font1 = QFont()
        font1.setFamily(u"Consolas")
        self.quickSendTable.setFont(font1)
        self.quickSendTable.setEditTriggers(QAbstractItemView.AllEditTriggers)
        self.quickSendTable.setSelectionMode(QAbstractItemView.NoSelection)
        self.quickSendTable.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.quickSendTable.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.quickSendTable.setRowCount(10)
        self.quickSendTable.setColumnCount(2)
        self.quickSendTable.horizontalHeader().setVisible(False)
        self.quickSendTable.horizontalHeader().setMinimumSectionSize(16)
        self.quickSendTable.horizontalHeader().setStretchLastSection(True)
        self.quickSendTable.verticalHeader().setVisible(False)
        self.quickSendTable.verticalHeader().setMinimumSectionSize(16)
        self.quickSendTable.verticalHeader().setDefaultSectionSize(16)

        self.verticalLayout_3.addWidget(self.quickSendTable)

        self.dockWidget_QuickSend.setWidget(self.dockWidgetContents_3)
        MainWindow.addDockWidget(Qt.RightDockWidgetArea, self.dockWidget_QuickSend)
        self.toolBar = QToolBar(MainWindow)
        self.toolBar.setObjectName(u"toolBar")
        self.toolBar.setMinimumSize(QSize(0, 34))
        self.toolBar.setMaximumSize(QSize(16777215, 34))
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




        pass
    # retranslateUi

