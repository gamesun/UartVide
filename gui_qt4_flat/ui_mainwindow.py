# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(800, 600)
        MainWindow.setWindowTitle(_fromUtf8("MyTerm"))
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_2.setMargin(0)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.centerFrame = QtGui.QFrame(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centerFrame.sizePolicy().hasHeightForWidth())
        self.centerFrame.setSizePolicy(sizePolicy)
        self.centerFrame.setObjectName(_fromUtf8("centerFrame"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.centerFrame)
        self.verticalLayout_2.setMargin(0)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.txtEdtOutput = QtGui.QTextEdit(self.centerFrame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(3)
        sizePolicy.setHeightForWidth(self.txtEdtOutput.sizePolicy().hasHeightForWidth())
        self.txtEdtOutput.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Courier 10 Pitch"))
        font.setPointSize(10)
        self.txtEdtOutput.setFont(font)
        self.txtEdtOutput.setObjectName(_fromUtf8("txtEdtOutput"))
        self.verticalLayout_2.addWidget(self.txtEdtOutput)
        self.horizontalLayout_2.addWidget(self.centerFrame)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = FMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setNativeMenuBar(True)
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setTitle(_fromUtf8("&File"))
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        self.menuPort = QtGui.QMenu(self.menubar)
        self.menuPort.setTitle(_fromUtf8("&Port"))
        self.menuPort.setObjectName(_fromUtf8("menuPort"))
        self.menuView = QtGui.QMenu(self.menubar)
        self.menuView.setTitle(_fromUtf8("&View"))
        self.menuView.setObjectName(_fromUtf8("menuView"))
        self.menuReceive_View = QtGui.QMenu(self.menuView)
        self.menuReceive_View.setTitle(_fromUtf8("Receive View"))
        self.menuReceive_View.setObjectName(_fromUtf8("menuReceive_View"))
        self.menuSkin = QtGui.QMenu(self.menuView)
        self.menuSkin.setTitle(_fromUtf8("Skin"))
        self.menuSkin.setObjectName(_fromUtf8("menuSkin"))
        self.menuHelp = QtGui.QMenu(self.menubar)
        self.menuHelp.setTitle(_fromUtf8("&Help"))
        self.menuHelp.setObjectName(_fromUtf8("menuHelp"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.dockWidget_PortConfig = QtGui.QDockWidget(MainWindow)
        self.dockWidget_PortConfig.setWindowTitle(_fromUtf8("Port Config"))
        self.dockWidget_PortConfig.setObjectName(_fromUtf8("dockWidget_PortConfig"))
        self.dockWidgetContents = QtGui.QWidget()
        self.dockWidgetContents.setObjectName(_fromUtf8("dockWidgetContents"))
        self.verticalLayout_6 = QtGui.QVBoxLayout(self.dockWidgetContents)
        self.verticalLayout_6.setMargin(0)
        self.verticalLayout_6.setSpacing(0)
        self.verticalLayout_6.setObjectName(_fromUtf8("verticalLayout_6"))
        self.frame = QtGui.QFrame(self.dockWidgetContents)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.verticalLayout_8 = QtGui.QVBoxLayout(self.frame)
        self.verticalLayout_8.setContentsMargins(6, 3, 3, 3)
        self.verticalLayout_8.setSpacing(1)
        self.verticalLayout_8.setObjectName(_fromUtf8("verticalLayout_8"))
        self.verticalLayout_1 = QtGui.QVBoxLayout()
        self.verticalLayout_1.setMargin(1)
        self.verticalLayout_1.setSpacing(0)
        self.verticalLayout_1.setObjectName(_fromUtf8("verticalLayout_1"))
        self.btnEnumPorts = QtGui.QPushButton(self.frame)
        self.btnEnumPorts.setText(_fromUtf8("Enum Ports"))
        self.btnEnumPorts.setObjectName(_fromUtf8("btnEnumPorts"))
        self.verticalLayout_1.addWidget(self.btnEnumPorts)
        self.label_1 = QtGui.QLabel(self.frame)
        self.label_1.setMinimumSize(QtCore.QSize(0, 20))
        self.label_1.setMaximumSize(QtCore.QSize(16777215, 20))
        self.label_1.setText(_fromUtf8("Port"))
        self.label_1.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft)
        self.label_1.setObjectName(_fromUtf8("label_1"))
        self.verticalLayout_1.addWidget(self.label_1)
        self.cmbPort = QtGui.QComboBox(self.frame)
        self.cmbPort.setMinimumSize(QtCore.QSize(120, 0))
        self.cmbPort.setEditable(True)
        self.cmbPort.setCurrentText(_fromUtf8(""))
        self.cmbPort.setObjectName(_fromUtf8("cmbPort"))
        self.verticalLayout_1.addWidget(self.cmbPort)
        self.label_2 = QtGui.QLabel(self.frame)
        self.label_2.setMinimumSize(QtCore.QSize(0, 20))
        self.label_2.setMaximumSize(QtCore.QSize(16777215, 20))
        self.label_2.setText(_fromUtf8("Baud Rate"))
        self.label_2.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.verticalLayout_1.addWidget(self.label_2)
        self.cmbBaudRate = QtGui.QComboBox(self.frame)
        self.cmbBaudRate.setEditable(True)
        self.cmbBaudRate.setMaxVisibleItems(30)
        self.cmbBaudRate.setObjectName(_fromUtf8("cmbBaudRate"))
        self.cmbBaudRate.addItem(_fromUtf8(""))
        self.cmbBaudRate.setItemText(0, _fromUtf8("50"))
        self.cmbBaudRate.addItem(_fromUtf8(""))
        self.cmbBaudRate.setItemText(1, _fromUtf8("75"))
        self.cmbBaudRate.addItem(_fromUtf8(""))
        self.cmbBaudRate.setItemText(2, _fromUtf8("110"))
        self.cmbBaudRate.addItem(_fromUtf8(""))
        self.cmbBaudRate.setItemText(3, _fromUtf8("134"))
        self.cmbBaudRate.addItem(_fromUtf8(""))
        self.cmbBaudRate.setItemText(4, _fromUtf8("150"))
        self.cmbBaudRate.addItem(_fromUtf8(""))
        self.cmbBaudRate.setItemText(5, _fromUtf8("200"))
        self.cmbBaudRate.addItem(_fromUtf8(""))
        self.cmbBaudRate.setItemText(6, _fromUtf8("300"))
        self.cmbBaudRate.addItem(_fromUtf8(""))
        self.cmbBaudRate.setItemText(7, _fromUtf8("600"))
        self.cmbBaudRate.addItem(_fromUtf8(""))
        self.cmbBaudRate.setItemText(8, _fromUtf8("1200"))
        self.cmbBaudRate.addItem(_fromUtf8(""))
        self.cmbBaudRate.setItemText(9, _fromUtf8("1800"))
        self.cmbBaudRate.addItem(_fromUtf8(""))
        self.cmbBaudRate.setItemText(10, _fromUtf8("2400"))
        self.cmbBaudRate.addItem(_fromUtf8(""))
        self.cmbBaudRate.setItemText(11, _fromUtf8("4800"))
        self.cmbBaudRate.addItem(_fromUtf8(""))
        self.cmbBaudRate.setItemText(12, _fromUtf8("9600"))
        self.cmbBaudRate.addItem(_fromUtf8(""))
        self.cmbBaudRate.setItemText(13, _fromUtf8("19200"))
        self.cmbBaudRate.addItem(_fromUtf8(""))
        self.cmbBaudRate.setItemText(14, _fromUtf8("38400"))
        self.cmbBaudRate.addItem(_fromUtf8(""))
        self.cmbBaudRate.setItemText(15, _fromUtf8("57600"))
        self.cmbBaudRate.addItem(_fromUtf8(""))
        self.cmbBaudRate.setItemText(16, _fromUtf8("115200"))
        self.cmbBaudRate.addItem(_fromUtf8(""))
        self.cmbBaudRate.setItemText(17, _fromUtf8("230400"))
        self.cmbBaudRate.addItem(_fromUtf8(""))
        self.cmbBaudRate.setItemText(18, _fromUtf8("460800"))
        self.cmbBaudRate.addItem(_fromUtf8(""))
        self.cmbBaudRate.setItemText(19, _fromUtf8("500000"))
        self.cmbBaudRate.addItem(_fromUtf8(""))
        self.cmbBaudRate.setItemText(20, _fromUtf8("576000"))
        self.cmbBaudRate.addItem(_fromUtf8(""))
        self.cmbBaudRate.setItemText(21, _fromUtf8("921600"))
        self.cmbBaudRate.addItem(_fromUtf8(""))
        self.cmbBaudRate.setItemText(22, _fromUtf8("1000000"))
        self.cmbBaudRate.addItem(_fromUtf8(""))
        self.cmbBaudRate.setItemText(23, _fromUtf8("1152000"))
        self.cmbBaudRate.addItem(_fromUtf8(""))
        self.cmbBaudRate.setItemText(24, _fromUtf8("1500000"))
        self.cmbBaudRate.addItem(_fromUtf8(""))
        self.cmbBaudRate.setItemText(25, _fromUtf8("2000000"))
        self.cmbBaudRate.addItem(_fromUtf8(""))
        self.cmbBaudRate.setItemText(26, _fromUtf8("2500000"))
        self.cmbBaudRate.addItem(_fromUtf8(""))
        self.cmbBaudRate.setItemText(27, _fromUtf8("3000000"))
        self.cmbBaudRate.addItem(_fromUtf8(""))
        self.cmbBaudRate.setItemText(28, _fromUtf8("3500000"))
        self.cmbBaudRate.addItem(_fromUtf8(""))
        self.cmbBaudRate.setItemText(29, _fromUtf8("4000000"))
        self.verticalLayout_1.addWidget(self.cmbBaudRate)
        self.label_3 = QtGui.QLabel(self.frame)
        self.label_3.setMinimumSize(QtCore.QSize(0, 20))
        self.label_3.setMaximumSize(QtCore.QSize(16777215, 20))
        self.label_3.setText(_fromUtf8("Data Bits"))
        self.label_3.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.verticalLayout_1.addWidget(self.label_3)
        self.cmbDataBits = QtGui.QComboBox(self.frame)
        self.cmbDataBits.setCurrentText(_fromUtf8("8"))
        self.cmbDataBits.setObjectName(_fromUtf8("cmbDataBits"))
        self.cmbDataBits.addItem(_fromUtf8(""))
        self.cmbDataBits.setItemText(0, _fromUtf8("8"))
        self.cmbDataBits.addItem(_fromUtf8(""))
        self.cmbDataBits.setItemText(1, _fromUtf8("7"))
        self.cmbDataBits.addItem(_fromUtf8(""))
        self.cmbDataBits.setItemText(2, _fromUtf8("6"))
        self.cmbDataBits.addItem(_fromUtf8(""))
        self.cmbDataBits.setItemText(3, _fromUtf8("5"))
        self.verticalLayout_1.addWidget(self.cmbDataBits)
        self.label_4 = QtGui.QLabel(self.frame)
        self.label_4.setMinimumSize(QtCore.QSize(0, 20))
        self.label_4.setMaximumSize(QtCore.QSize(16777215, 20))
        self.label_4.setText(_fromUtf8("Parity"))
        self.label_4.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.verticalLayout_1.addWidget(self.label_4)
        self.cmbParity = QtGui.QComboBox(self.frame)
        self.cmbParity.setCurrentText(_fromUtf8("None"))
        self.cmbParity.setObjectName(_fromUtf8("cmbParity"))
        self.cmbParity.addItem(_fromUtf8(""))
        self.cmbParity.setItemText(0, _fromUtf8("None"))
        self.cmbParity.addItem(_fromUtf8(""))
        self.cmbParity.setItemText(1, _fromUtf8("Even"))
        self.cmbParity.addItem(_fromUtf8(""))
        self.cmbParity.setItemText(2, _fromUtf8("Odd"))
        self.cmbParity.addItem(_fromUtf8(""))
        self.cmbParity.setItemText(3, _fromUtf8("Mark"))
        self.cmbParity.addItem(_fromUtf8(""))
        self.cmbParity.setItemText(4, _fromUtf8("Space"))
        self.verticalLayout_1.addWidget(self.cmbParity)
        self.label_5 = QtGui.QLabel(self.frame)
        self.label_5.setMinimumSize(QtCore.QSize(0, 20))
        self.label_5.setMaximumSize(QtCore.QSize(16777215, 20))
        self.label_5.setText(_fromUtf8("Stop Bits"))
        self.label_5.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.verticalLayout_1.addWidget(self.label_5)
        self.cmbStopBits = QtGui.QComboBox(self.frame)
        self.cmbStopBits.setCurrentText(_fromUtf8("1"))
        self.cmbStopBits.setObjectName(_fromUtf8("cmbStopBits"))
        self.cmbStopBits.addItem(_fromUtf8(""))
        self.cmbStopBits.setItemText(0, _fromUtf8("1"))
        self.cmbStopBits.addItem(_fromUtf8(""))
        self.cmbStopBits.setItemText(1, _fromUtf8("1.5"))
        self.cmbStopBits.addItem(_fromUtf8(""))
        self.cmbStopBits.setItemText(2, _fromUtf8("2"))
        self.verticalLayout_1.addWidget(self.cmbStopBits)
        spacerItem = QtGui.QSpacerItem(0, 5, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        self.verticalLayout_1.addItem(spacerItem)
        self.groupBox = QtGui.QGroupBox(self.frame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setTitle(_fromUtf8("HandShake"))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.verticalLayout_7 = QtGui.QVBoxLayout(self.groupBox)
        self.verticalLayout_7.setMargin(2)
        self.verticalLayout_7.setSpacing(0)
        self.verticalLayout_7.setObjectName(_fromUtf8("verticalLayout_7"))
        self.chkRTSCTS = QtGui.QCheckBox(self.groupBox)
        self.chkRTSCTS.setMaximumSize(QtCore.QSize(16777215, 22))
        self.chkRTSCTS.setText(_fromUtf8("RTS/CTS"))
        self.chkRTSCTS.setObjectName(_fromUtf8("chkRTSCTS"))
        self.verticalLayout_7.addWidget(self.chkRTSCTS)
        self.chkXonXoff = QtGui.QCheckBox(self.groupBox)
        self.chkXonXoff.setMaximumSize(QtCore.QSize(16777215, 22))
        self.chkXonXoff.setText(_fromUtf8("Xon/Xoff"))
        self.chkXonXoff.setObjectName(_fromUtf8("chkXonXoff"))
        self.verticalLayout_7.addWidget(self.chkXonXoff)
        self.verticalLayout_1.addWidget(self.groupBox)
        spacerItem1 = QtGui.QSpacerItem(0, 8, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        self.verticalLayout_1.addItem(spacerItem1)
        self.btnOpen = QtGui.QPushButton(self.frame)
        self.btnOpen.setEnabled(True)
        self.btnOpen.setText(_fromUtf8("Open"))
        self.btnOpen.setObjectName(_fromUtf8("btnOpen"))
        self.verticalLayout_1.addWidget(self.btnOpen)
        spacerItem2 = QtGui.QSpacerItem(0, 8, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        self.verticalLayout_1.addItem(spacerItem2)
        self.btnClear = QtGui.QPushButton(self.frame)
        self.btnClear.setText(_fromUtf8("Clear"))
        self.btnClear.setObjectName(_fromUtf8("btnClear"))
        self.verticalLayout_1.addWidget(self.btnClear)
        spacerItem3 = QtGui.QSpacerItem(0, 8, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        self.verticalLayout_1.addItem(spacerItem3)
        self.btnSaveLog = QtGui.QPushButton(self.frame)
        self.btnSaveLog.setText(_fromUtf8("Save Log"))
        self.btnSaveLog.setObjectName(_fromUtf8("btnSaveLog"))
        self.verticalLayout_1.addWidget(self.btnSaveLog)
        spacerItem4 = QtGui.QSpacerItem(0, 10, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_1.addItem(spacerItem4)
        self.verticalLayout_8.addLayout(self.verticalLayout_1)
        self.verticalLayout_6.addWidget(self.frame)
        self.dockWidget_PortConfig.setWidget(self.dockWidgetContents)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(1), self.dockWidget_PortConfig)
        self.dockWidget_SendHex = QtGui.QDockWidget(MainWindow)
        self.dockWidget_SendHex.setWindowTitle(_fromUtf8("Send Hex"))
        self.dockWidget_SendHex.setObjectName(_fromUtf8("dockWidget_SendHex"))
        self.dockWidgetContents_2 = QtGui.QWidget()
        self.dockWidgetContents_2.setObjectName(_fromUtf8("dockWidgetContents_2"))
        self.verticalLayout = QtGui.QVBoxLayout(self.dockWidgetContents_2)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(-1, -1, 2, -1)
        self.horizontalLayout.setSpacing(2)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.txtEdtInput = QtGui.QTextEdit(self.dockWidgetContents_2)
        self.txtEdtInput.setObjectName(_fromUtf8("txtEdtInput"))
        self.horizontalLayout.addWidget(self.txtEdtInput)
        self.btnSendHex = QtGui.QPushButton(self.dockWidgetContents_2)
        self.btnSendHex.setText(_fromUtf8("Send"))
        self.btnSendHex.setObjectName(_fromUtf8("btnSendHex"))
        self.horizontalLayout.addWidget(self.btnSendHex)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.dockWidget_SendHex.setWidget(self.dockWidgetContents_2)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(8), self.dockWidget_SendHex)
        self.dockWidget_QuickSend = QtGui.QDockWidget(MainWindow)
        self.dockWidget_QuickSend.setWindowTitle(_fromUtf8("Quick Send"))
        self.dockWidget_QuickSend.setObjectName(_fromUtf8("dockWidget_QuickSend"))
        self.dockWidgetContents_3 = QtGui.QWidget()
        self.dockWidgetContents_3.setObjectName(_fromUtf8("dockWidgetContents_3"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.dockWidgetContents_3)
        self.verticalLayout_3.setMargin(0)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.quickSendTable = QtGui.QTableWidget(self.dockWidgetContents_3)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.quickSendTable.sizePolicy().hasHeightForWidth())
        self.quickSendTable.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Courier 10 Pitch"))
        font.setPointSize(10)
        self.quickSendTable.setFont(font)
        self.quickSendTable.setRowCount(10)
        self.quickSendTable.setColumnCount(5)
        self.quickSendTable.setObjectName(_fromUtf8("quickSendTable"))
        self.quickSendTable.horizontalHeader().setDefaultSectionSize(40)
        self.quickSendTable.horizontalHeader().setMinimumSectionSize(25)
        self.verticalLayout_3.addWidget(self.quickSendTable)
        self.dockWidget_QuickSend.setWidget(self.dockWidgetContents_3)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(2), self.dockWidget_QuickSend)
        self.actionSave_Log = QtGui.QAction(MainWindow)
        self.actionSave_Log.setText(_fromUtf8("Save Log"))
        self.actionSave_Log.setIconText(_fromUtf8("Save Log"))
        self.actionSave_Log.setToolTip(_fromUtf8("Save Log"))
        self.actionSave_Log.setStatusTip(_fromUtf8("Save Log"))
        self.actionSave_Log.setObjectName(_fromUtf8("actionSave_Log"))
        self.actionExit = QtGui.QAction(MainWindow)
        self.actionExit.setText(_fromUtf8("Exit"))
        self.actionExit.setIconText(_fromUtf8("Exit"))
        self.actionExit.setToolTip(_fromUtf8("Exit"))
        self.actionExit.setStatusTip(_fromUtf8("Exit"))
        self.actionExit.setObjectName(_fromUtf8("actionExit"))
        self.actionOpen = QtGui.QAction(MainWindow)
        self.actionOpen.setText(_fromUtf8("Open"))
        self.actionOpen.setIconText(_fromUtf8("Open"))
        self.actionOpen.setToolTip(_fromUtf8("Open the port"))
        self.actionOpen.setStatusTip(_fromUtf8("Open the port"))
        self.actionOpen.setObjectName(_fromUtf8("actionOpen"))
        self.actionClose = QtGui.QAction(MainWindow)
        self.actionClose.setText(_fromUtf8("Close"))
        self.actionClose.setIconText(_fromUtf8("Close"))
        self.actionClose.setToolTip(_fromUtf8("Close the port"))
        self.actionClose.setStatusTip(_fromUtf8("Close the port"))
        self.actionClose.setObjectName(_fromUtf8("actionClose"))
        self.actionPort_Config_Panel = QtGui.QAction(MainWindow)
        self.actionPort_Config_Panel.setCheckable(True)
        self.actionPort_Config_Panel.setText(_fromUtf8("Port Config Panel"))
        self.actionPort_Config_Panel.setIconText(_fromUtf8("Show Port Config"))
        self.actionPort_Config_Panel.setToolTip(_fromUtf8("Show or hide Port Config Panel"))
        self.actionPort_Config_Panel.setStatusTip(_fromUtf8("Show or hide Port Config Panel"))
        self.actionPort_Config_Panel.setObjectName(_fromUtf8("actionPort_Config_Panel"))
        self.actionAlways_On_Top = QtGui.QAction(MainWindow)
        self.actionAlways_On_Top.setCheckable(True)
        self.actionAlways_On_Top.setText(_fromUtf8("Always On Top"))
        self.actionAlways_On_Top.setIconText(_fromUtf8("Always on top"))
        self.actionAlways_On_Top.setToolTip(_fromUtf8("Always on most top"))
        self.actionAlways_On_Top.setStatusTip(_fromUtf8("Always on most top"))
        self.actionAlways_On_Top.setObjectName(_fromUtf8("actionAlways_On_Top"))
        self.actionLocal_Echo = QtGui.QAction(MainWindow)
        self.actionLocal_Echo.setCheckable(True)
        self.actionLocal_Echo.setText(_fromUtf8("Local Echo"))
        self.actionLocal_Echo.setIconText(_fromUtf8("Local echo"))
        self.actionLocal_Echo.setToolTip(_fromUtf8("Local Echo"))
        self.actionLocal_Echo.setStatusTip(_fromUtf8("Echo what you typed"))
        self.actionLocal_Echo.setObjectName(_fromUtf8("actionLocal_Echo"))
        self.actionAscii = QtGui.QAction(MainWindow)
        self.actionAscii.setCheckable(True)
        self.actionAscii.setText(_fromUtf8("Ascii"))
        self.actionAscii.setIconText(_fromUtf8("Ascii"))
        self.actionAscii.setToolTip(_fromUtf8("Show as ascii"))
        self.actionAscii.setStatusTip(_fromUtf8("Show as ascii"))
        self.actionAscii.setObjectName(_fromUtf8("actionAscii"))
        self.actionHex_lowercase = QtGui.QAction(MainWindow)
        self.actionHex_lowercase.setCheckable(True)
        self.actionHex_lowercase.setText(_fromUtf8("hex(lowercase)"))
        self.actionHex_lowercase.setIconText(_fromUtf8("hex(lowercase)"))
        self.actionHex_lowercase.setToolTip(_fromUtf8("Show as hex(lowercase)"))
        self.actionHex_lowercase.setStatusTip(_fromUtf8("Show as hex(lowercase)"))
        self.actionHex_lowercase.setObjectName(_fromUtf8("actionHex_lowercase"))
        self.actionHEX_UPPERCASE = QtGui.QAction(MainWindow)
        self.actionHEX_UPPERCASE.setCheckable(True)
        self.actionHEX_UPPERCASE.setText(_fromUtf8("HEX(UPPERCASE)"))
        self.actionHEX_UPPERCASE.setIconText(_fromUtf8("HEX(UPPERCASE)"))
        self.actionHEX_UPPERCASE.setToolTip(_fromUtf8("Show as HEX(UPPERCASE)"))
        self.actionHEX_UPPERCASE.setStatusTip(_fromUtf8("Show as HEX(UPPERCASE)"))
        self.actionHEX_UPPERCASE.setObjectName(_fromUtf8("actionHEX_UPPERCASE"))
        self.actionSend_Hex_Panel = QtGui.QAction(MainWindow)
        self.actionSend_Hex_Panel.setCheckable(True)
        self.actionSend_Hex_Panel.setText(_fromUtf8("Send Hex Panel"))
        self.actionSend_Hex_Panel.setIconText(_fromUtf8("Send Hex Panel"))
        self.actionSend_Hex_Panel.setToolTip(_fromUtf8("Show or hide Send Hex Panel"))
        self.actionSend_Hex_Panel.setStatusTip(_fromUtf8("Show or hide Hex Transmit Panel"))
        self.actionSend_Hex_Panel.setObjectName(_fromUtf8("actionSend_Hex_Panel"))
        self.actionAbout = QtGui.QAction(MainWindow)
        self.actionAbout.setText(_fromUtf8("About MyTerm"))
        self.actionAbout.setIconText(_fromUtf8("About MyTerm"))
        self.actionAbout.setToolTip(_fromUtf8("About MyTerm"))
        self.actionAbout.setStatusTip(_fromUtf8("About MyTerm"))
        self.actionAbout.setObjectName(_fromUtf8("actionAbout"))
        self.actionAbout_Qt = QtGui.QAction(MainWindow)
        self.actionAbout_Qt.setText(_fromUtf8("About Qt"))
        self.actionAbout_Qt.setIconText(_fromUtf8("About Qt"))
        self.actionAbout_Qt.setToolTip(_fromUtf8("About Qt"))
        self.actionAbout_Qt.setStatusTip(_fromUtf8("About Qt"))
        self.actionAbout_Qt.setObjectName(_fromUtf8("actionAbout_Qt"))
        self.actionOpen_Cmd_File = QtGui.QAction(MainWindow)
        self.actionOpen_Cmd_File.setText(_fromUtf8("Open Cmd File"))
        self.actionOpen_Cmd_File.setIconText(_fromUtf8("Open Cmd File"))
        self.actionOpen_Cmd_File.setToolTip(_fromUtf8("Open Cmd File"))
        self.actionOpen_Cmd_File.setStatusTip(_fromUtf8("Open Cmd File"))
        self.actionOpen_Cmd_File.setObjectName(_fromUtf8("actionOpen_Cmd_File"))
        self.actionQuick_Send_Panel = QtGui.QAction(MainWindow)
        self.actionQuick_Send_Panel.setCheckable(True)
        self.actionQuick_Send_Panel.setText(_fromUtf8("Quick Send Panel"))
        self.actionQuick_Send_Panel.setIconText(_fromUtf8("Quick Send Panel"))
        self.actionQuick_Send_Panel.setToolTip(_fromUtf8("Show or hide Quick Send Panel"))
        self.actionQuick_Send_Panel.setStatusTip(_fromUtf8("Show or hide Quick Send Panel"))
        self.actionQuick_Send_Panel.setObjectName(_fromUtf8("actionQuick_Send_Panel"))
        self.actionDefault = QtGui.QAction(MainWindow)
        self.actionDefault.setCheckable(True)
        self.actionDefault.setText(_fromUtf8("default"))
        self.actionDefault.setIconText(_fromUtf8("default"))
        self.actionDefault.setToolTip(_fromUtf8("default"))
        self.actionDefault.setObjectName(_fromUtf8("actionDefault"))
        self.actionFlat_green = QtGui.QAction(MainWindow)
        self.actionFlat_green.setCheckable(True)
        self.actionFlat_green.setText(_fromUtf8("Flat-green"))
        self.actionFlat_green.setIconText(_fromUtf8("Flat-green"))
        self.actionFlat_green.setToolTip(_fromUtf8("Flat-green"))
        self.actionFlat_green.setObjectName(_fromUtf8("actionFlat_green"))
        self.actionFlat_bule = QtGui.QAction(MainWindow)
        self.actionFlat_bule.setCheckable(True)
        self.actionFlat_bule.setText(_fromUtf8("Flat-bule"))
        self.actionFlat_bule.setIconText(_fromUtf8("Flat-bule"))
        self.actionFlat_bule.setToolTip(_fromUtf8("Flat-bule"))
        self.actionFlat_bule.setObjectName(_fromUtf8("actionFlat_bule"))
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
        self.menuSkin.addAction(self.actionDefault)
        self.menuSkin.addAction(self.actionFlat_green)
        self.menuSkin.addAction(self.actionFlat_bule)
        self.menuView.addAction(self.actionPort_Config_Panel)
        self.menuView.addAction(self.actionQuick_Send_Panel)
        self.menuView.addAction(self.actionSend_Hex_Panel)
        self.menuView.addSeparator()
        self.menuView.addAction(self.actionLocal_Echo)
        self.menuView.addAction(self.menuReceive_View.menuAction())
        self.menuView.addAction(self.actionAlways_On_Top)
        self.menuView.addSeparator()
        self.menuView.addAction(self.menuSkin.menuAction())
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

from flat_ui import FMenuBar
