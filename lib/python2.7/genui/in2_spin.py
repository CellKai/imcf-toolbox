# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'generic_in2_spin.ui'
#
# Created: Sat Aug  3 10:08:22 2013
#      by: PyQt4 UI code generator 4.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(590, 298)
        MainWindow.setWindowTitle(_fromUtf8("Generic Window Title"))
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 10, 356, 37))
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label.setFont(font)
        self.label.setText(_fromUtf8("Generic Description Text"))
        self.label.setObjectName(_fromUtf8("label"))
        self.pb_path_1 = QtGui.QPushButton(self.centralwidget)
        self.pb_path_1.setGeometry(QtCore.QRect(480, 60, 97, 27))
        self.pb_path_1.setText(_fromUtf8("Browse"))
        self.pb_path_1.setShortcut(_fromUtf8("Ctrl+O"))
        self.pb_path_1.setObjectName(_fromUtf8("pb_path_1"))
        self.le_path_1 = QtGui.QLineEdit(self.centralwidget)
        self.le_path_1.setGeometry(QtCore.QRect(10, 60, 461, 27))
        self.le_path_1.setText(_fromUtf8(""))
        self.le_path_1.setPlaceholderText(_fromUtf8("Input File (Ctrl+O)"))
        self.le_path_1.setObjectName(_fromUtf8("le_path_1"))
        self.bb_ok_cancel = QtGui.QDialogButtonBox(self.centralwidget)
        self.bb_ok_cancel.setGeometry(QtCore.QRect(400, 230, 176, 27))
        self.bb_ok_cancel.setToolTip(_fromUtf8(""))
        self.bb_ok_cancel.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.bb_ok_cancel.setObjectName(_fromUtf8("bb_ok_cancel"))
        self.sl_verbosity = QtGui.QSlider(self.centralwidget)
        self.sl_verbosity.setGeometry(QtCore.QRect(10, 180, 160, 29))
        self.sl_verbosity.setToolTip(_fromUtf8("Verbosity Level"))
        self.sl_verbosity.setMaximum(2)
        self.sl_verbosity.setOrientation(QtCore.Qt.Horizontal)
        self.sl_verbosity.setInvertedAppearance(False)
        self.sl_verbosity.setTickPosition(QtGui.QSlider.TicksBelow)
        self.sl_verbosity.setTickInterval(1)
        self.sl_verbosity.setObjectName(_fromUtf8("sl_verbosity"))
        self.label_2 = QtGui.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(180, 190, 155, 17))
        self.label_2.setText(_fromUtf8("Output Verbosity Level"))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.sb_verbosity = QtGui.QSpinBox(self.centralwidget)
        self.sb_verbosity.setGeometry(QtCore.QRect(350, 190, 13, 21))
        self.sb_verbosity.setFrame(False)
        self.sb_verbosity.setReadOnly(True)
        self.sb_verbosity.setButtonSymbols(QtGui.QAbstractSpinBox.NoButtons)
        self.sb_verbosity.setMaximum(2)
        self.sb_verbosity.setObjectName(_fromUtf8("sb_verbosity"))
        self.le_path_2 = QtGui.QLineEdit(self.centralwidget)
        self.le_path_2.setGeometry(QtCore.QRect(10, 100, 461, 27))
        self.le_path_2.setText(_fromUtf8(""))
        self.le_path_2.setPlaceholderText(_fromUtf8("Input File (Ctrl+O)"))
        self.le_path_2.setObjectName(_fromUtf8("le_path_2"))
        self.pb_path_2 = QtGui.QPushButton(self.centralwidget)
        self.pb_path_2.setGeometry(QtCore.QRect(480, 100, 97, 27))
        self.pb_path_2.setText(_fromUtf8("Browse"))
        self.pb_path_2.setShortcut(_fromUtf8("Ctrl+O"))
        self.pb_path_2.setObjectName(_fromUtf8("pb_path_2"))
        self.sb_double = QtGui.QDoubleSpinBox(self.centralwidget)
        self.sb_double.setGeometry(QtCore.QRect(10, 140, 62, 27))
        self.sb_double.setMaximum(9999.99)
        self.sb_double.setSingleStep(0.1)
        self.sb_double.setProperty("value", 1.0)
        self.sb_double.setObjectName(_fromUtf8("sb_double"))
        self.label_3 = QtGui.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(80, 150, 361, 17))
        self.label_3.setText(_fromUtf8("Spinbox Label"))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.sc_ctrl_w = QtGui.QAction(MainWindow)
        self.sc_ctrl_w.setText(_fromUtf8("Ctrl+W"))
        self.sc_ctrl_w.setShortcut(_fromUtf8("Ctrl+W"))
        self.sc_ctrl_w.setObjectName(_fromUtf8("sc_ctrl_w"))
        self.sc_ctrl_q = QtGui.QAction(MainWindow)
        self.sc_ctrl_q.setText(_fromUtf8("Ctrl+Q"))
        self.sc_ctrl_q.setShortcut(_fromUtf8("Ctrl+Q"))
        self.sc_ctrl_q.setObjectName(_fromUtf8("sc_ctrl_q"))

        self.retranslateUi(MainWindow)
        QtCore.QObject.connect(self.pb_path_1, QtCore.SIGNAL(_fromUtf8("clicked()")), self.le_path_1.update)
        QtCore.QObject.connect(self.bb_ok_cancel, QtCore.SIGNAL(_fromUtf8("rejected()")), MainWindow.close)
        QtCore.QObject.connect(self.sc_ctrl_w, QtCore.SIGNAL(_fromUtf8("triggered()")), MainWindow.close)
        QtCore.QObject.connect(self.sc_ctrl_q, QtCore.SIGNAL(_fromUtf8("triggered()")), MainWindow.close)
        QtCore.QObject.connect(self.sl_verbosity, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")), self.sb_verbosity.setValue)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        pass

