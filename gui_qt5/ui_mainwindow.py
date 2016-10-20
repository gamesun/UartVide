# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.7
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        MainWindow.setWindowTitle("MyTerm")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.centerFrame = QtWidgets.QFrame(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centerFrame.sizePolicy().hasHeightForWidth())
        self.centerFrame.setSizePolicy(sizePolicy)
        self.centerFrame.setObjectName("centerFrame")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.centerFrame)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.txtEdtOutput = QtWidgets.QTextEdit(self.centerFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(3)
        sizePolicy.setHeightForWidth(self.txtEdtOutput.sizePolicy().hasHeightForWidth())
        self.txtEdtOutput.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Courier 10 Pitch")
        font.setPointSize(10)
        self.txtEdtOutput.setFont(font)
        self.txtEdtOutput.setObjectName("txtEdtOutput")
        self.verticalLayout_2.addWidget(self.txtEdtOutput)
        self.horizontalLayout_2.addWidget(self.centerFrame)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 25))
        self.menubar.setNativeMenuBar(True)
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setTitle("&File")
        self.menuFile.setObjectName("menuFile")
        self.menuPort = QtWidgets.QMenu(self.menubar)
        self.menuPort.setTitle("&Port")
        self.menuPort.setObjectName("menuPort")
        self.menuView = QtWidgets.QMenu(self.menubar)
        self.menuView.setTitle("&View")
        self.menuView.setObjectName("menuView")
        self.menuReceive_View = QtWidgets.QMenu(self.menuView)
        self.menuReceive_View.setTitle("Receive View")
        self.menuReceive_View.setObjectName("menuReceive_View")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setTitle("&Help")
        self.menuHelp.setObjectName("menuHelp")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.dockWidget_PortConfig = QtWidgets.QDockWidget(MainWindow)
        self.dockWidget_PortConfig.setWindowTitle("Port Config")
        self.dockWidget_PortConfig.setObjectName("dockWidget_PortConfig")
        self.dockWidgetContents = QtWidgets.QWidget()
        self.dockWidgetContents.setObjectName("dockWidgetContents")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.dockWidgetContents)
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_6.setSpacing(0)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.frame = QtWidgets.QFrame(self.dockWidgetContents)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frame.setObjectName("frame")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout_8.setContentsMargins(3, 3, 3, 3)
        self.verticalLayout_8.setSpacing(1)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.verticalLayout_1 = QtWidgets.QVBoxLayout()
        self.verticalLayout_1.setContentsMargins(1, 1, 1, 1)
        self.verticalLayout_1.setSpacing(0)
        self.verticalLayout_1.setObjectName("verticalLayout_1")
        self.btnEnumPorts = QtWidgets.QPushButton(self.frame)
        self.btnEnumPorts.setText("Enum Ports")
        self.btnEnumPorts.setObjectName("btnEnumPorts")
        self.verticalLayout_1.addWidget(self.btnEnumPorts)
        self.label_1 = QtWidgets.QLabel(self.frame)
        self.label_1.setMinimumSize(QtCore.QSize(0, 20))
        self.label_1.setMaximumSize(QtCore.QSize(16777215, 20))
        self.label_1.setText("Port")
        self.label_1.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft)
        self.label_1.setObjectName("label_1")
        self.verticalLayout_1.addWidget(self.label_1)
        self.cmbPort = QtWidgets.QComboBox(self.frame)
        self.cmbPort.setMinimumSize(QtCore.QSize(120, 0))
        self.cmbPort.setEditable(True)
        self.cmbPort.setCurrentText("")
        self.cmbPort.setObjectName("cmbPort")
        self.verticalLayout_1.addWidget(self.cmbPort)
        self.label_2 = QtWidgets.QLabel(self.frame)
        self.label_2.setMinimumSize(QtCore.QSize(0, 20))
        self.label_2.setMaximumSize(QtCore.QSize(16777215, 20))
        self.label_2.setText("Baud Rate")
        self.label_2.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_1.addWidget(self.label_2)
        self.cmbBaudRate = QtWidgets.QComboBox(self.frame)
        self.cmbBaudRate.setEditable(True)
        self.cmbBaudRate.setMaxVisibleItems(30)
        self.cmbBaudRate.setObjectName("cmbBaudRate")
        self.cmbBaudRate.addItem("")
        self.cmbBaudRate.setItemText(0, "50")
        self.cmbBaudRate.addItem("")
        self.cmbBaudRate.setItemText(1, "75")
        self.cmbBaudRate.addItem("")
        self.cmbBaudRate.setItemText(2, "110")
        self.cmbBaudRate.addItem("")
        self.cmbBaudRate.setItemText(3, "134")
        self.cmbBaudRate.addItem("")
        self.cmbBaudRate.setItemText(4, "150")
        self.cmbBaudRate.addItem("")
        self.cmbBaudRate.setItemText(5, "200")
        self.cmbBaudRate.addItem("")
        self.cmbBaudRate.setItemText(6, "300")
        self.cmbBaudRate.addItem("")
        self.cmbBaudRate.setItemText(7, "600")
        self.cmbBaudRate.addItem("")
        self.cmbBaudRate.setItemText(8, "1200")
        self.cmbBaudRate.addItem("")
        self.cmbBaudRate.setItemText(9, "1800")
        self.cmbBaudRate.addItem("")
        self.cmbBaudRate.setItemText(10, "2400")
        self.cmbBaudRate.addItem("")
        self.cmbBaudRate.setItemText(11, "4800")
        self.cmbBaudRate.addItem("")
        self.cmbBaudRate.setItemText(12, "9600")
        self.cmbBaudRate.addItem("")
        self.cmbBaudRate.setItemText(13, "19200")
        self.cmbBaudRate.addItem("")
        self.cmbBaudRate.setItemText(14, "38400")
        self.cmbBaudRate.addItem("")
        self.cmbBaudRate.setItemText(15, "57600")
        self.cmbBaudRate.addItem("")
        self.cmbBaudRate.setItemText(16, "115200")
        self.cmbBaudRate.addItem("")
        self.cmbBaudRate.setItemText(17, "230400")
        self.cmbBaudRate.addItem("")
        self.cmbBaudRate.setItemText(18, "460800")
        self.cmbBaudRate.addItem("")
        self.cmbBaudRate.setItemText(19, "500000")
        self.cmbBaudRate.addItem("")
        self.cmbBaudRate.setItemText(20, "576000")
        self.cmbBaudRate.addItem("")
        self.cmbBaudRate.setItemText(21, "921600")
        self.cmbBaudRate.addItem("")
        self.cmbBaudRate.setItemText(22, "1000000")
        self.cmbBaudRate.addItem("")
        self.cmbBaudRate.setItemText(23, "1152000")
        self.cmbBaudRate.addItem("")
        self.cmbBaudRate.setItemText(24, "1500000")
        self.cmbBaudRate.addItem("")
        self.cmbBaudRate.setItemText(25, "2000000")
        self.cmbBaudRate.addItem("")
        self.cmbBaudRate.setItemText(26, "2500000")
        self.cmbBaudRate.addItem("")
        self.cmbBaudRate.setItemText(27, "3000000")
        self.cmbBaudRate.addItem("")
        self.cmbBaudRate.setItemText(28, "3500000")
        self.cmbBaudRate.addItem("")
        self.cmbBaudRate.setItemText(29, "4000000")
        self.verticalLayout_1.addWidget(self.cmbBaudRate)
        self.label_3 = QtWidgets.QLabel(self.frame)
        self.label_3.setMinimumSize(QtCore.QSize(0, 20))
        self.label_3.setMaximumSize(QtCore.QSize(16777215, 20))
        self.label_3.setText("Data Bits")
        self.label_3.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_1.addWidget(self.label_3)
        self.cmbDataBits = QtWidgets.QComboBox(self.frame)
        self.cmbDataBits.setCurrentText("8")
        self.cmbDataBits.setObjectName("cmbDataBits")
        self.cmbDataBits.addItem("")
        self.cmbDataBits.setItemText(0, "8")
        self.cmbDataBits.addItem("")
        self.cmbDataBits.setItemText(1, "7")
        self.cmbDataBits.addItem("")
        self.cmbDataBits.setItemText(2, "6")
        self.cmbDataBits.addItem("")
        self.cmbDataBits.setItemText(3, "5")
        self.verticalLayout_1.addWidget(self.cmbDataBits)
        self.label_4 = QtWidgets.QLabel(self.frame)
        self.label_4.setMinimumSize(QtCore.QSize(0, 20))
        self.label_4.setMaximumSize(QtCore.QSize(16777215, 20))
        self.label_4.setText("Parity")
        self.label_4.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_1.addWidget(self.label_4)
        self.cmbParity = QtWidgets.QComboBox(self.frame)
        self.cmbParity.setCurrentText("None")
        self.cmbParity.setObjectName("cmbParity")
        self.cmbParity.addItem("")
        self.cmbParity.setItemText(0, "None")
        self.cmbParity.addItem("")
        self.cmbParity.setItemText(1, "Even")
        self.cmbParity.addItem("")
        self.cmbParity.setItemText(2, "Odd")
        self.cmbParity.addItem("")
        self.cmbParity.setItemText(3, "Mark")
        self.cmbParity.addItem("")
        self.cmbParity.setItemText(4, "Space")
        self.verticalLayout_1.addWidget(self.cmbParity)
        self.label_5 = QtWidgets.QLabel(self.frame)
        self.label_5.setMinimumSize(QtCore.QSize(0, 20))
        self.label_5.setMaximumSize(QtCore.QSize(16777215, 20))
        self.label_5.setText("Stop Bits")
        self.label_5.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft)
        self.label_5.setObjectName("label_5")
        self.verticalLayout_1.addWidget(self.label_5)
        self.cmbStopBits = QtWidgets.QComboBox(self.frame)
        self.cmbStopBits.setCurrentText("1")
        self.cmbStopBits.setObjectName("cmbStopBits")
        self.cmbStopBits.addItem("")
        self.cmbStopBits.setItemText(0, "1")
        self.cmbStopBits.addItem("")
        self.cmbStopBits.setItemText(1, "1.5")
        self.cmbStopBits.addItem("")
        self.cmbStopBits.setItemText(2, "2")
        self.verticalLayout_1.addWidget(self.cmbStopBits)
        spacerItem = QtWidgets.QSpacerItem(0, 5, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout_1.addItem(spacerItem)
        self.groupBox = QtWidgets.QGroupBox(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setTitle("HandShake")
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout_7.setContentsMargins(2, 2, 2, 2)
        self.verticalLayout_7.setSpacing(0)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.chkRTSCTS = QtWidgets.QCheckBox(self.groupBox)
        self.chkRTSCTS.setMaximumSize(QtCore.QSize(16777215, 22))
        self.chkRTSCTS.setText("RTS/CTS")
        self.chkRTSCTS.setObjectName("chkRTSCTS")
        self.verticalLayout_7.addWidget(self.chkRTSCTS)
        self.chkXonXoff = QtWidgets.QCheckBox(self.groupBox)
        self.chkXonXoff.setMaximumSize(QtCore.QSize(16777215, 22))
        self.chkXonXoff.setText("Xon/Xoff")
        self.chkXonXoff.setObjectName("chkXonXoff")
        self.verticalLayout_7.addWidget(self.chkXonXoff)
        self.verticalLayout_1.addWidget(self.groupBox)
        spacerItem1 = QtWidgets.QSpacerItem(0, 5, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout_1.addItem(spacerItem1)
        self.btnOpen = QtWidgets.QPushButton(self.frame)
        self.btnOpen.setEnabled(True)
        self.btnOpen.setText("Open")
        self.btnOpen.setObjectName("btnOpen")
        self.verticalLayout_1.addWidget(self.btnOpen)
        spacerItem2 = QtWidgets.QSpacerItem(0, 5, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout_1.addItem(spacerItem2)
        self.btnClear = QtWidgets.QPushButton(self.frame)
        self.btnClear.setText("Clear")
        self.btnClear.setObjectName("btnClear")
        self.verticalLayout_1.addWidget(self.btnClear)
        spacerItem3 = QtWidgets.QSpacerItem(0, 5, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout_1.addItem(spacerItem3)
        self.btnSaveLog = QtWidgets.QPushButton(self.frame)
        self.btnSaveLog.setText("Save Log")
        self.btnSaveLog.setObjectName("btnSaveLog")
        self.verticalLayout_1.addWidget(self.btnSaveLog)
        spacerItem4 = QtWidgets.QSpacerItem(0, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_1.addItem(spacerItem4)
        self.verticalLayout_8.addLayout(self.verticalLayout_1)
        self.verticalLayout_6.addWidget(self.frame)
        self.dockWidget_PortConfig.setWidget(self.dockWidgetContents)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(1), self.dockWidget_PortConfig)
        self.dockWidget_SendHex = QtWidgets.QDockWidget(MainWindow)
        self.dockWidget_SendHex.setWindowTitle("Send Hex")
        self.dockWidget_SendHex.setObjectName("dockWidget_SendHex")
        self.dockWidgetContents_2 = QtWidgets.QWidget()
        self.dockWidgetContents_2.setObjectName("dockWidgetContents_2")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.dockWidgetContents_2)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(-1, -1, 2, -1)
        self.horizontalLayout.setSpacing(2)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.txtEdtInput = QtWidgets.QTextEdit(self.dockWidgetContents_2)
        self.txtEdtInput.setObjectName("txtEdtInput")
        self.horizontalLayout.addWidget(self.txtEdtInput)
        self.btnSendHex = QtWidgets.QPushButton(self.dockWidgetContents_2)
        self.btnSendHex.setText("Send")
        self.btnSendHex.setObjectName("btnSendHex")
        self.horizontalLayout.addWidget(self.btnSendHex)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.dockWidget_SendHex.setWidget(self.dockWidgetContents_2)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(8), self.dockWidget_SendHex)
        self.dockWidget_QuickSend = QtWidgets.QDockWidget(MainWindow)
        self.dockWidget_QuickSend.setWindowTitle("Quick Send")
        self.dockWidget_QuickSend.setObjectName("dockWidget_QuickSend")
        self.dockWidgetContents_3 = QtWidgets.QWidget()
        self.dockWidgetContents_3.setObjectName("dockWidgetContents_3")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.dockWidgetContents_3)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.quickSendTable = QtWidgets.QTableWidget(self.dockWidgetContents_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.quickSendTable.sizePolicy().hasHeightForWidth())
        self.quickSendTable.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Courier 10 Pitch")
        font.setPointSize(10)
        self.quickSendTable.setFont(font)
        self.quickSendTable.setRowCount(10)
        self.quickSendTable.setColumnCount(5)
        self.quickSendTable.setObjectName("quickSendTable")
        self.quickSendTable.horizontalHeader().setDefaultSectionSize(40)
        self.quickSendTable.horizontalHeader().setMinimumSectionSize(25)
        self.verticalLayout_3.addWidget(self.quickSendTable)
        self.dockWidget_QuickSend.setWidget(self.dockWidgetContents_3)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(2), self.dockWidget_QuickSend)
        self.actionSave_Log = QtWidgets.QAction(MainWindow)
        self.actionSave_Log.setText("Save Log")
        self.actionSave_Log.setIconText("Save Log")
        self.actionSave_Log.setToolTip("Save Log")
        self.actionSave_Log.setStatusTip("Save Log")
        self.actionSave_Log.setObjectName("actionSave_Log")
        self.actionExit = QtWidgets.QAction(MainWindow)
        self.actionExit.setText("Exit")
        self.actionExit.setIconText("Exit")
        self.actionExit.setToolTip("Exit")
        self.actionExit.setStatusTip("Exit")
        self.actionExit.setObjectName("actionExit")
        self.actionOpen = QtWidgets.QAction(MainWindow)
        self.actionOpen.setText("Open")
        self.actionOpen.setIconText("Open")
        self.actionOpen.setToolTip("Open the port")
        self.actionOpen.setStatusTip("Open the port")
        self.actionOpen.setObjectName("actionOpen")
        self.actionClose = QtWidgets.QAction(MainWindow)
        self.actionClose.setText("Close")
        self.actionClose.setIconText("Close")
        self.actionClose.setToolTip("Close the port")
        self.actionClose.setStatusTip("Close the port")
        self.actionClose.setObjectName("actionClose")
        self.actionPort_Config_Panel = QtWidgets.QAction(MainWindow)
        self.actionPort_Config_Panel.setCheckable(True)
        self.actionPort_Config_Panel.setText("Port Config Panel")
        self.actionPort_Config_Panel.setIconText("Show Port Config")
        self.actionPort_Config_Panel.setToolTip("Show or hide Port Config Panel")
        self.actionPort_Config_Panel.setStatusTip("Show or hide Port Config Panel")
        self.actionPort_Config_Panel.setObjectName("actionPort_Config_Panel")
        self.actionAlways_On_Top = QtWidgets.QAction(MainWindow)
        self.actionAlways_On_Top.setCheckable(True)
        self.actionAlways_On_Top.setText("Always On Top")
        self.actionAlways_On_Top.setIconText("Always on top")
        self.actionAlways_On_Top.setToolTip("Always on most top")
        self.actionAlways_On_Top.setStatusTip("Always on most top")
        self.actionAlways_On_Top.setObjectName("actionAlways_On_Top")
        self.actionLocal_Echo = QtWidgets.QAction(MainWindow)
        self.actionLocal_Echo.setCheckable(True)
        self.actionLocal_Echo.setText("Local Echo")
        self.actionLocal_Echo.setIconText("Local echo")
        self.actionLocal_Echo.setToolTip("Local Echo")
        self.actionLocal_Echo.setStatusTip("Echo what you typed")
        self.actionLocal_Echo.setObjectName("actionLocal_Echo")
        self.actionAscii = QtWidgets.QAction(MainWindow)
        self.actionAscii.setCheckable(True)
        self.actionAscii.setText("Ascii")
        self.actionAscii.setIconText("Ascii")
        self.actionAscii.setToolTip("Show as ascii")
        self.actionAscii.setStatusTip("Show as ascii")
        self.actionAscii.setObjectName("actionAscii")
        self.actionHex_lowercase = QtWidgets.QAction(MainWindow)
        self.actionHex_lowercase.setCheckable(True)
        self.actionHex_lowercase.setText("hex(lowercase)")
        self.actionHex_lowercase.setIconText("hex(lowercase)")
        self.actionHex_lowercase.setToolTip("Show as hex(lowercase)")
        self.actionHex_lowercase.setStatusTip("Show as hex(lowercase)")
        self.actionHex_lowercase.setObjectName("actionHex_lowercase")
        self.actionHEX_UPPERCASE = QtWidgets.QAction(MainWindow)
        self.actionHEX_UPPERCASE.setCheckable(True)
        self.actionHEX_UPPERCASE.setText("HEX(UPPERCASE)")
        self.actionHEX_UPPERCASE.setIconText("HEX(UPPERCASE)")
        self.actionHEX_UPPERCASE.setToolTip("Show as HEX(UPPERCASE)")
        self.actionHEX_UPPERCASE.setStatusTip("Show as HEX(UPPERCASE)")
        self.actionHEX_UPPERCASE.setObjectName("actionHEX_UPPERCASE")
        self.actionSend_Hex_Panel = QtWidgets.QAction(MainWindow)
        self.actionSend_Hex_Panel.setCheckable(True)
        self.actionSend_Hex_Panel.setText("Send Hex Panel")
        self.actionSend_Hex_Panel.setIconText("Send Hex Panel")
        self.actionSend_Hex_Panel.setToolTip("Show or hide Send Hex Panel")
        self.actionSend_Hex_Panel.setStatusTip("Show or hide Hex Transmit Panel")
        self.actionSend_Hex_Panel.setObjectName("actionSend_Hex_Panel")
        self.actionAbout = QtWidgets.QAction(MainWindow)
        self.actionAbout.setText("About MyTerm")
        self.actionAbout.setIconText("About MyTerm")
        self.actionAbout.setToolTip("About MyTerm")
        self.actionAbout.setStatusTip("About MyTerm")
        self.actionAbout.setObjectName("actionAbout")
        self.actionAbout_Qt = QtWidgets.QAction(MainWindow)
        self.actionAbout_Qt.setText("About Qt")
        self.actionAbout_Qt.setIconText("About Qt")
        self.actionAbout_Qt.setToolTip("About Qt")
        self.actionAbout_Qt.setStatusTip("About Qt")
        self.actionAbout_Qt.setObjectName("actionAbout_Qt")
        self.actionOpen_Cmd_File = QtWidgets.QAction(MainWindow)
        self.actionOpen_Cmd_File.setText("Open Cmd File")
        self.actionOpen_Cmd_File.setIconText("Open Cmd File")
        self.actionOpen_Cmd_File.setToolTip("Open Cmd File")
        self.actionOpen_Cmd_File.setStatusTip("Open Cmd File")
        self.actionOpen_Cmd_File.setObjectName("actionOpen_Cmd_File")
        self.actionQuick_Send_Panel = QtWidgets.QAction(MainWindow)
        self.actionQuick_Send_Panel.setCheckable(True)
        self.actionQuick_Send_Panel.setText("Quick Send Panel")
        self.actionQuick_Send_Panel.setIconText("Quick Send Panel")
        self.actionQuick_Send_Panel.setToolTip("Show or hide Quick Send Panel")
        self.actionQuick_Send_Panel.setStatusTip("Show or hide Quick Send Panel")
        self.actionQuick_Send_Panel.setObjectName("actionQuick_Send_Panel")
        self.menuFile.addAction(self.actionOpen_Cmd_File)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionSave_Log)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExit)
        self.menuPort.addAction(self.actionOpen)
        self.menuPort.addAction(self.actionClose)
        self.menuReceive_View.addAction(self.actionAscii)
        self.menuReceive_View.addAction(self.actionHex_lowercase)
        self.menuReceive_View.addAction(self.actionHEX_UPPERCASE)
        self.menuView.addAction(self.actionPort_Config_Panel)
        self.menuView.addAction(self.actionQuick_Send_Panel)
        self.menuView.addAction(self.actionSend_Hex_Panel)
        self.menuView.addSeparator()
        self.menuView.addAction(self.actionLocal_Echo)
        self.menuView.addAction(self.menuReceive_View.menuAction())
        self.menuView.addAction(self.actionAlways_On_Top)
        self.menuHelp.addAction(self.actionAbout)
        self.menuHelp.addAction(self.actionAbout_Qt)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuPort.menuAction())
        self.menubar.addAction(self.menuView.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        self.cmbBaudRate.setCurrentIndex(12)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        pass

