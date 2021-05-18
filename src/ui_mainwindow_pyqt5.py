# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '../ui/mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(865, 612)
        MainWindow.setWindowTitle("UartVide")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_2.setContentsMargins(1, 0, 1, 0)
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
        self.frame_PortCfg = QtWidgets.QFrame(self.centerFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_PortCfg.sizePolicy().hasHeightForWidth())
        self.frame_PortCfg.setSizePolicy(sizePolicy)
        self.frame_PortCfg.setMinimumSize(QtCore.QSize(0, 29))
        self.frame_PortCfg.setMaximumSize(QtCore.QSize(16777215, 29))
        self.frame_PortCfg.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_PortCfg.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_PortCfg.setLineWidth(0)
        self.frame_PortCfg.setObjectName("frame_PortCfg")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.frame_PortCfg)
        self.horizontalLayout_3.setContentsMargins(4, 0, 4, 2)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setSpacing(6)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_2 = QtWidgets.QLabel(self.frame_PortCfg)
        self.label_2.setMinimumSize(QtCore.QSize(0, 20))
        self.label_2.setMaximumSize(QtCore.QSize(16777215, 20))
        self.label_2.setToolTip("Baud Rate")
        self.label_2.setStatusTip("Baud Rate")
        self.label_2.setText("BR")
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_4.addWidget(self.label_2)
        self.cmbBaudRate = QtWidgets.QComboBox(self.frame_PortCfg)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cmbBaudRate.sizePolicy().hasHeightForWidth())
        self.cmbBaudRate.setSizePolicy(sizePolicy)
        self.cmbBaudRate.setMinimumSize(QtCore.QSize(0, 23))
        self.cmbBaudRate.setMaximumSize(QtCore.QSize(16777215, 23))
        self.cmbBaudRate.setToolTip("Baud Rate")
        self.cmbBaudRate.setStatusTip("Baud Rate")
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
        self.horizontalLayout_4.addWidget(self.cmbBaudRate)
        self.label_3 = QtWidgets.QLabel(self.frame_PortCfg)
        self.label_3.setMinimumSize(QtCore.QSize(0, 20))
        self.label_3.setMaximumSize(QtCore.QSize(16777215, 20))
        self.label_3.setToolTip("Data Bits")
        self.label_3.setStatusTip("Data Bits")
        self.label_3.setText("D")
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_4.addWidget(self.label_3)
        self.cmbDataBits = QtWidgets.QComboBox(self.frame_PortCfg)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cmbDataBits.sizePolicy().hasHeightForWidth())
        self.cmbDataBits.setSizePolicy(sizePolicy)
        self.cmbDataBits.setMinimumSize(QtCore.QSize(0, 23))
        self.cmbDataBits.setMaximumSize(QtCore.QSize(16777215, 23))
        self.cmbDataBits.setToolTip("Data Bits")
        self.cmbDataBits.setStatusTip("Data Bits")
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
        self.horizontalLayout_4.addWidget(self.cmbDataBits)
        self.label_4 = QtWidgets.QLabel(self.frame_PortCfg)
        self.label_4.setMinimumSize(QtCore.QSize(0, 20))
        self.label_4.setMaximumSize(QtCore.QSize(16777215, 20))
        self.label_4.setToolTip("Parity")
        self.label_4.setStatusTip("Parity")
        self.label_4.setText("P")
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_4.addWidget(self.label_4)
        self.cmbParity = QtWidgets.QComboBox(self.frame_PortCfg)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cmbParity.sizePolicy().hasHeightForWidth())
        self.cmbParity.setSizePolicy(sizePolicy)
        self.cmbParity.setMinimumSize(QtCore.QSize(0, 23))
        self.cmbParity.setMaximumSize(QtCore.QSize(16777215, 23))
        self.cmbParity.setToolTip("Parity")
        self.cmbParity.setStatusTip("Parity")
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
        self.horizontalLayout_4.addWidget(self.cmbParity)
        self.label_5 = QtWidgets.QLabel(self.frame_PortCfg)
        self.label_5.setMinimumSize(QtCore.QSize(0, 20))
        self.label_5.setMaximumSize(QtCore.QSize(16777215, 20))
        self.label_5.setToolTip("Stop Bits")
        self.label_5.setStatusTip("Stop Bits")
        self.label_5.setText("S")
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_4.addWidget(self.label_5)
        self.cmbStopBits = QtWidgets.QComboBox(self.frame_PortCfg)
        self.cmbStopBits.setMinimumSize(QtCore.QSize(0, 23))
        self.cmbStopBits.setMaximumSize(QtCore.QSize(16777215, 23))
        self.cmbStopBits.setToolTip("Stop Bits")
        self.cmbStopBits.setStatusTip("Stop Bits")
        self.cmbStopBits.setCurrentText("1")
        self.cmbStopBits.setObjectName("cmbStopBits")
        self.cmbStopBits.addItem("")
        self.cmbStopBits.setItemText(0, "1")
        self.cmbStopBits.addItem("")
        self.cmbStopBits.setItemText(1, "1.5")
        self.cmbStopBits.addItem("")
        self.cmbStopBits.setItemText(2, "2")
        self.horizontalLayout_4.addWidget(self.cmbStopBits)
        self.chkRTSCTS = QtWidgets.QCheckBox(self.frame_PortCfg)
        self.chkRTSCTS.setMaximumSize(QtCore.QSize(16777215, 22))
        self.chkRTSCTS.setText("RTS/CTS")
        self.chkRTSCTS.setObjectName("chkRTSCTS")
        self.horizontalLayout_4.addWidget(self.chkRTSCTS)
        self.chkXonXoff = QtWidgets.QCheckBox(self.frame_PortCfg)
        self.chkXonXoff.setMaximumSize(QtCore.QSize(16777215, 22))
        self.chkXonXoff.setText("Xon/Xoff")
        self.chkXonXoff.setObjectName("chkXonXoff")
        self.horizontalLayout_4.addWidget(self.chkXonXoff)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem)
        self.horizontalLayout_3.addLayout(self.horizontalLayout_4)
        self.verticalLayout_2.addWidget(self.frame_PortCfg)
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
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.dockWidget_SendHex = QtWidgets.QDockWidget(MainWindow)
        self.dockWidget_SendHex.setContextMenuPolicy(QtCore.Qt.PreventContextMenu)
        self.dockWidget_SendHex.setAllowedAreas(QtCore.Qt.BottomDockWidgetArea|QtCore.Qt.LeftDockWidgetArea|QtCore.Qt.RightDockWidgetArea)
        self.dockWidget_SendHex.setWindowTitle("Send")
        self.dockWidget_SendHex.setObjectName("dockWidget_SendHex")
        self.dockWidgetContents_2 = QtWidgets.QWidget()
        self.dockWidgetContents_2.setObjectName("dockWidgetContents_2")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.dockWidgetContents_2)
        self.verticalLayout.setContentsMargins(0, 2, 4, 0)
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(2, 0, 2, 0)
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.rdoASC = QtWidgets.QRadioButton(self.dockWidgetContents_2)
        self.rdoASC.setMinimumSize(QtCore.QSize(0, 22))
        self.rdoASC.setMaximumSize(QtCore.QSize(16777215, 22))
        self.rdoASC.setText("ASC")
        self.rdoASC.setObjectName("rdoASC")
        self.horizontalLayout.addWidget(self.rdoASC)
        self.rdoHEX = QtWidgets.QRadioButton(self.dockWidgetContents_2)
        self.rdoHEX.setMinimumSize(QtCore.QSize(0, 22))
        self.rdoHEX.setMaximumSize(QtCore.QSize(16777215, 22))
        self.rdoHEX.setText("HEX")
        self.rdoHEX.setObjectName("rdoHEX")
        self.horizontalLayout.addWidget(self.rdoHEX)
        self.chkLoop = QtWidgets.QCheckBox(self.dockWidgetContents_2)
        self.chkLoop.setMinimumSize(QtCore.QSize(0, 22))
        self.chkLoop.setMaximumSize(QtCore.QSize(16777215, 22))
        self.chkLoop.setText("Loop")
        self.chkLoop.setObjectName("chkLoop")
        self.horizontalLayout.addWidget(self.chkLoop)
        self.spnPeriod = QtWidgets.QSpinBox(self.dockWidgetContents_2)
        self.spnPeriod.setMinimumSize(QtCore.QSize(0, 22))
        self.spnPeriod.setMaximumSize(QtCore.QSize(16777215, 22))
        self.spnPeriod.setToolTip("Period")
        self.spnPeriod.setStatusTip("Period")
        self.spnPeriod.setSuffix("ms")
        self.spnPeriod.setMinimum(10)
        self.spnPeriod.setMaximum(999999)
        self.spnPeriod.setProperty("value", 1000)
        self.spnPeriod.setObjectName("spnPeriod")
        self.horizontalLayout.addWidget(self.spnPeriod)
        self.btnSend = QtWidgets.QToolButton(self.dockWidgetContents_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnSend.sizePolicy().hasHeightForWidth())
        self.btnSend.setSizePolicy(sizePolicy)
        self.btnSend.setMinimumSize(QtCore.QSize(0, 22))
        self.btnSend.setMaximumSize(QtCore.QSize(16777215, 22))
        self.btnSend.setText(" Send ")
        self.btnSend.setObjectName("btnSend")
        self.horizontalLayout.addWidget(self.btnSend)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.txtEdtInput = QtWidgets.QTextEdit(self.dockWidgetContents_2)
        self.txtEdtInput.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.txtEdtInput.setFrameShadow(QtWidgets.QFrame.Plain)
        self.txtEdtInput.setLineWidth(0)
        self.txtEdtInput.setObjectName("txtEdtInput")
        self.verticalLayout.addWidget(self.txtEdtInput)
        self.verticalLayout.setStretch(1, 1)
        self.dockWidget_SendHex.setWidget(self.dockWidgetContents_2)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(2), self.dockWidget_SendHex)
        self.dockWidget_QuickSend = QtWidgets.QDockWidget(MainWindow)
        self.dockWidget_QuickSend.setContextMenuPolicy(QtCore.Qt.PreventContextMenu)
        self.dockWidget_QuickSend.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea|QtCore.Qt.RightDockWidgetArea)
        self.dockWidget_QuickSend.setWindowTitle("Quick Send")
        self.dockWidget_QuickSend.setObjectName("dockWidget_QuickSend")
        self.dockWidgetContents_3 = QtWidgets.QWidget()
        self.dockWidgetContents_3.setObjectName("dockWidgetContents_3")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.dockWidgetContents_3)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.quickSendTable = QtWidgets.QTableWidget(self.dockWidgetContents_3)
        font = QtGui.QFont()
        font.setFamily("Consolas")
        self.quickSendTable.setFont(font)
        self.quickSendTable.setEditTriggers(QtWidgets.QAbstractItemView.AllEditTriggers)
        self.quickSendTable.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.quickSendTable.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        self.quickSendTable.setHorizontalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        self.quickSendTable.setRowCount(10)
        self.quickSendTable.setColumnCount(2)
        self.quickSendTable.setObjectName("quickSendTable")
        self.quickSendTable.horizontalHeader().setVisible(False)
        self.quickSendTable.horizontalHeader().setMinimumSectionSize(16)
        self.quickSendTable.horizontalHeader().setStretchLastSection(True)
        self.quickSendTable.verticalHeader().setVisible(False)
        self.quickSendTable.verticalHeader().setDefaultSectionSize(16)
        self.quickSendTable.verticalHeader().setMinimumSectionSize(16)
        self.verticalLayout_3.addWidget(self.quickSendTable)
        self.dockWidget_QuickSend.setWidget(self.dockWidgetContents_3)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(2), self.dockWidget_QuickSend)
        self.toolBar = QtWidgets.QToolBar(MainWindow)
        self.toolBar.setMinimumSize(QtCore.QSize(0, 31))
        self.toolBar.setMaximumSize(QtCore.QSize(16777215, 31))
        self.toolBar.setContextMenuPolicy(QtCore.Qt.PreventContextMenu)
        self.toolBar.setWindowTitle("toolBar")
        self.toolBar.setMovable(False)
        self.toolBar.setAllowedAreas(QtCore.Qt.TopToolBarArea)
        self.toolBar.setFloatable(False)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
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
        self.actionAbout.setText("About UartVide")
        self.actionAbout.setIconText("About UartVide")
        self.actionAbout.setToolTip("About UartVide")
        self.actionAbout.setStatusTip("About UartVide")
        self.actionAbout.setObjectName("actionAbout")
        self.actionAbout_Qt = QtWidgets.QAction(MainWindow)
        self.actionAbout_Qt.setText("About Qt")
        self.actionAbout_Qt.setIconText("About Qt")
        self.actionAbout_Qt.setToolTip("About Qt")
        self.actionAbout_Qt.setStatusTip("About Qt")
        self.actionAbout_Qt.setObjectName("actionAbout_Qt")
        self.actionOpen_Cmd_File = QtWidgets.QAction(MainWindow)
        self.actionOpen_Cmd_File.setText("Open Quick Send File")
        self.actionOpen_Cmd_File.setIconText("Open Cmd File")
        self.actionOpen_Cmd_File.setToolTip("Load Quick Send Settings")
        self.actionOpen_Cmd_File.setStatusTip("Open Cmd File")
        self.actionOpen_Cmd_File.setObjectName("actionOpen_Cmd_File")
        self.actionQuick_Send_Panel = QtWidgets.QAction(MainWindow)
        self.actionQuick_Send_Panel.setCheckable(True)
        self.actionQuick_Send_Panel.setText("Quick Send Panel")
        self.actionQuick_Send_Panel.setIconText("Quick Send Panel")
        self.actionQuick_Send_Panel.setToolTip("Show or hide Quick Send Panel")
        self.actionQuick_Send_Panel.setStatusTip("Show or hide Quick Send Panel")
        self.actionQuick_Send_Panel.setObjectName("actionQuick_Send_Panel")

        self.retranslateUi(MainWindow)
        self.cmbBaudRate.setCurrentIndex(12)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        pass