# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'generic_in_out_xysize_xysize.ui'
#
# Created: Mon Nov 11 11:30:33 2013
#      by: PyQt4 UI code generator 4.10.3
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
        MainWindow.resize(590, 400)
        MainWindow.setWindowTitle(_fromUtf8("Generic Window Title"))
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.label_1 = QtGui.QLabel(self.centralwidget)
        self.label_1.setGeometry(QtCore.QRect(10, 10, 570, 37))
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_1.setFont(font)
        self.label_1.setText(_fromUtf8("Generic Description Text"))
        self.label_1.setObjectName(_fromUtf8("label_1"))
        self.bb_ok_cancel = QtGui.QDialogButtonBox(self.centralwidget)
        self.bb_ok_cancel.setGeometry(QtCore.QRect(400, 340, 176, 27))
        self.bb_ok_cancel.setToolTip(_fromUtf8(""))
        self.bb_ok_cancel.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.bb_ok_cancel.setObjectName(_fromUtf8("bb_ok_cancel"))
        self.sl_verbosity = QtGui.QSlider(self.centralwidget)
        self.sl_verbosity.setGeometry(QtCore.QRect(10, 310, 160, 29))
        self.sl_verbosity.setToolTip(_fromUtf8("Verbosity Level"))
        self.sl_verbosity.setMaximum(2)
        self.sl_verbosity.setOrientation(QtCore.Qt.Horizontal)
        self.sl_verbosity.setInvertedAppearance(False)
        self.sl_verbosity.setTickPosition(QtGui.QSlider.TicksBelow)
        self.sl_verbosity.setTickInterval(1)
        self.sl_verbosity.setObjectName(_fromUtf8("sl_verbosity"))
        self.label_2 = QtGui.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(180, 320, 155, 17))
        self.label_2.setText(_fromUtf8("Output Verbosity Level"))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.sb_verbosity = QtGui.QSpinBox(self.centralwidget)
        self.sb_verbosity.setGeometry(QtCore.QRect(350, 320, 13, 21))
        self.sb_verbosity.setFrame(False)
        self.sb_verbosity.setReadOnly(True)
        self.sb_verbosity.setButtonSymbols(QtGui.QAbstractSpinBox.NoButtons)
        self.sb_verbosity.setMaximum(2)
        self.sb_verbosity.setObjectName(_fromUtf8("sb_verbosity"))
        self.group_1 = QtGui.QGroupBox(self.centralwidget)
        self.group_1.setGeometry(QtCore.QRect(10, 60, 570, 100))
        self.group_1.setObjectName(_fromUtf8("group_1"))
        self.dsb_1 = QtGui.QDoubleSpinBox(self.group_1)
        self.dsb_1.setGeometry(QtCore.QRect(250, 70, 100, 27))
        self.dsb_1.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.dsb_1.setDecimals(3)
        self.dsb_1.setMaximum(9999.99)
        self.dsb_1.setObjectName(_fromUtf8("dsb_1"))
        self.dsb_2 = QtGui.QDoubleSpinBox(self.group_1)
        self.dsb_2.setGeometry(QtCore.QRect(360, 70, 100, 27))
        self.dsb_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.dsb_2.setDecimals(3)
        self.dsb_2.setMaximum(9999.99)
        self.dsb_2.setObjectName(_fromUtf8("dsb_2"))
        self.pb_infile = QtGui.QPushButton(self.group_1)
        self.pb_infile.setGeometry(QtCore.QRect(470, 30, 97, 27))
        self.pb_infile.setText(_fromUtf8("Browse"))
        self.pb_infile.setShortcut(_fromUtf8("Ctrl+O"))
        self.pb_infile.setObjectName(_fromUtf8("pb_infile"))
        self.le_infile = QtGui.QLineEdit(self.group_1)
        self.le_infile.setGeometry(QtCore.QRect(0, 30, 461, 27))
        self.le_infile.setText(_fromUtf8(""))
        self.le_infile.setPlaceholderText(_fromUtf8("Input File (Ctrl+O)"))
        self.le_infile.setObjectName(_fromUtf8("le_infile"))
        self.label_3 = QtGui.QLabel(self.group_1)
        self.label_3.setGeometry(QtCore.QRect(0, 70, 240, 30))
        self.label_3.setText(_fromUtf8("label_3"))
        self.label_3.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.group_2 = QtGui.QGroupBox(self.centralwidget)
        self.group_2.setGeometry(QtCore.QRect(10, 180, 570, 110))
        self.group_2.setObjectName(_fromUtf8("group_2"))
        self.pb_outfile = QtGui.QPushButton(self.group_2)
        self.pb_outfile.setGeometry(QtCore.QRect(470, 30, 97, 27))
        self.pb_outfile.setText(_fromUtf8("Browse"))
        self.pb_outfile.setShortcut(_fromUtf8("Ctrl+S"))
        self.pb_outfile.setObjectName(_fromUtf8("pb_outfile"))
        self.le_outfile = QtGui.QLineEdit(self.group_2)
        self.le_outfile.setGeometry(QtCore.QRect(0, 30, 461, 27))
        self.le_outfile.setText(_fromUtf8(""))
        self.le_outfile.setPlaceholderText(_fromUtf8("File to store results (Ctrl+S)"))
        self.le_outfile.setObjectName(_fromUtf8("le_outfile"))
        self.sb_1 = QtGui.QSpinBox(self.group_2)
        self.sb_1.setGeometry(QtCore.QRect(290, 70, 80, 27))
        self.sb_1.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.sb_1.setMaximum(99999)
        self.sb_1.setObjectName(_fromUtf8("sb_1"))
        self.sb_2 = QtGui.QSpinBox(self.group_2)
        self.sb_2.setGeometry(QtCore.QRect(380, 70, 80, 27))
        self.sb_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.sb_2.setMaximum(99999)
        self.sb_2.setObjectName(_fromUtf8("sb_2"))
        self.label_4 = QtGui.QLabel(self.group_2)
        self.label_4.setGeometry(QtCore.QRect(-1, 70, 281, 30))
        self.label_4.setText(_fromUtf8("label_4"))
        self.label_4.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_4.setObjectName(_fromUtf8("label_4"))
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
        QtCore.QObject.connect(self.bb_ok_cancel, QtCore.SIGNAL(_fromUtf8("rejected()")), MainWindow.close)
        QtCore.QObject.connect(self.sc_ctrl_w, QtCore.SIGNAL(_fromUtf8("triggered()")), MainWindow.close)
        QtCore.QObject.connect(self.sc_ctrl_q, QtCore.SIGNAL(_fromUtf8("triggered()")), MainWindow.close)
        QtCore.QObject.connect(self.sl_verbosity, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")), self.sb_verbosity.setValue)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        self.group_1.setTitle(_translate("MainWindow", "GroupBox", None))
        self.group_2.setTitle(_translate("MainWindow", "GroupBox", None))

