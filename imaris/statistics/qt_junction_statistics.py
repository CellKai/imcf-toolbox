# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'junction_statistics.ui'
#
# Created: Tue Feb 19 11:50:53 2013
#      by: PyQt4 UI code generator 4.8.5
#
# WARNING! All changes made in this file will be lost!

import sys
import filament_parser
from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(590, 400)
        MainWindow.setWindowTitle(_fromUtf8("Junction Statistics"))

        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 10, 265, 37))
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label.setFont(font)
        self.label.setText(_fromUtf8("Junction Statistics"))
        self.label.setObjectName(_fromUtf8("label"))

        self.pb_infile = QtGui.QPushButton(self.centralwidget)
        self.pb_infile.setGeometry(QtCore.QRect(480, 60, 97, 27))
        self.pb_infile.setText(_fromUtf8("Browse"))
        self.pb_infile.setShortcut(_fromUtf8("Ctrl+O"))
        self.pb_infile.setFlat(False)
        self.pb_infile.setObjectName(_fromUtf8("pb_infile"))

        self.le_infile = QtGui.QLineEdit(self.centralwidget)
        self.le_infile.setGeometry(QtCore.QRect(10, 60, 461, 27))
        self.le_infile.setText(_fromUtf8(""))
        self.le_infile.setPlaceholderText(_fromUtf8("Input CSV File containing Filament points (Ctrl+O)"))
        self.le_infile.setObjectName(_fromUtf8("le_infile"))

        self.pb_outfile = QtGui.QPushButton(self.centralwidget)
        self.pb_outfile.setGeometry(QtCore.QRect(480, 210, 97, 27))
        self.pb_outfile.setText(_fromUtf8("Browse"))
        self.pb_outfile.setShortcut(_fromUtf8("Ctrl+S"))
        self.pb_outfile.setObjectName(_fromUtf8("pb_outfile"))

        self.le_outfile = QtGui.QLineEdit(self.centralwidget)
        self.le_outfile.setGeometry(QtCore.QRect(10, 210, 461, 27))
        self.le_outfile.setText(_fromUtf8(""))
        self.le_outfile.setFrame(True)
        self.le_outfile.setPlaceholderText(_fromUtf8("File to store results (Ctrl+S)"))
        self.le_outfile.setObjectName(_fromUtf8("le_outfile"))

        self.bb_ok_cancel = QtGui.QDialogButtonBox(self.centralwidget)
        self.bb_ok_cancel.setGeometry(QtCore.QRect(400, 340, 176, 27))
        self.bb_ok_cancel.setToolTip(_fromUtf8(""))
        self.bb_ok_cancel.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.bb_ok_cancel.setObjectName(_fromUtf8("bb_ok_cancel"))

        self.cb_plot = QtGui.QCheckBox(self.centralwidget)
        self.cb_plot.setGeometry(QtCore.QRect(10, 100, 282, 22))
        self.cb_plot.setText(_fromUtf8("Show a 3D plot of the calculated data."))
        self.cb_plot.setShortcut(_fromUtf8("Ctrl+P"))
        self.cb_plot.setChecked(True)
        self.cb_plot.setObjectName(_fromUtf8("cb_plot"))

        self.sl_verbosity = QtGui.QSlider(self.centralwidget)
        self.sl_verbosity.setGeometry(QtCore.QRect(10, 270, 160, 29))
        self.sl_verbosity.setToolTip(_fromUtf8("Verbosity Level"))
        self.sl_verbosity.setMaximum(2)
        self.sl_verbosity.setOrientation(QtCore.Qt.Horizontal)
        self.sl_verbosity.setInvertedAppearance(False)
        self.sl_verbosity.setTickPosition(QtGui.QSlider.TicksBelow)
        self.sl_verbosity.setTickInterval(1)
        self.sl_verbosity.setObjectName(_fromUtf8("sl_verbosity"))

        self.label_2 = QtGui.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(180, 280, 155, 17))
        self.label_2.setText(_fromUtf8("Output Verbosity Level"))
        self.label_2.setObjectName(_fromUtf8("label_2"))

        self.sb_verbosity = QtGui.QSpinBox(self.centralwidget)
        self.sb_verbosity.setGeometry(QtCore.QRect(350, 280, 13, 21))
        self.sb_verbosity.setFrame(False)
        self.sb_verbosity.setReadOnly(True)
        self.sb_verbosity.setButtonSymbols(QtGui.QAbstractSpinBox.NoButtons)
        self.sb_verbosity.setMaximum(2)
        self.sb_verbosity.setObjectName(_fromUtf8("sb_verbosity"))

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

        MainWindow.addAction(self.sc_ctrl_w)
        MainWindow.addAction(self.sc_ctrl_q)

        self.retranslateUi(MainWindow)

        QtCore.QObject.connect(self.pb_infile, QtCore.SIGNAL(_fromUtf8("clicked()")), self.selectInfile)
        QtCore.QObject.connect(self.pb_outfile, QtCore.SIGNAL(_fromUtf8("clicked()")), self.selectOutfile)
        QtCore.QObject.connect(self.bb_ok_cancel, QtCore.SIGNAL(_fromUtf8("rejected()")), MainWindow.close)
        QtCore.QObject.connect(self.bb_ok_cancel, QtCore.SIGNAL(_fromUtf8("accepted()")), self.runTool)
        QtCore.QObject.connect(self.sc_ctrl_w, QtCore.SIGNAL(_fromUtf8("triggered()")), MainWindow.close)
        QtCore.QObject.connect(self.sc_ctrl_q, QtCore.SIGNAL(_fromUtf8("triggered()")), MainWindow.close)
        QtCore.QObject.connect(self.sl_verbosity, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")), self.sb_verbosity.setValue)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        pass

    def selectInfile(self):
        self.le_infile.setText(QtGui.QFileDialog.getOpenFileName())
        # when the infile is changed, reset the outfile name:
        self.le_outfile.setText('')

    def selectOutfile(self):
        self.le_outfile.setText(QtGui.QFileDialog.getOpenFileName())

    def runTool(self):
        sys.argv = ['./filament_parser.py']
        infile = str(self.le_infile.text())
        sys.argv += ['-i', infile]
        outfile = str(self.le_outfile.text())
        sys.argv += ['-o', outfile]
        plot = None
        if (self.cb_plot.checkState() == 2):
            plot = '--plot'
        if plot:
            sys.argv.append(plot)
        for inc_verbosity in range(0, self.sl_verbosity.value()):
            sys.argv.append('-v')
        # print sys.argv
        filament_parser.main()
