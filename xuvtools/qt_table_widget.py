# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'table_widget.ui'
#
# Created: Wed Feb 27 08:40:41 2013
#      by: PyQt4 UI code generator 4.8.5
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
        MainWindow.resize(538, 463)
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.tableWidget = QtGui.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(10, 10, 451, 351))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.tableWidget.sizePolicy().hasHeightForWidth())
        self.tableWidget.setSizePolicy(sizePolicy)
        self.tableWidget.setAutoFillBackground(False)
        self.tableWidget.setFrameShadow(QtGui.QFrame.Sunken)
        self.tableWidget.setGridStyle(QtCore.Qt.DashLine)
        self.tableWidget.setRowCount(3)
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setObjectName(_fromUtf8("tableWidget"))
        self.tableWidget.horizontalHeader().setDefaultSectionSize(30)
        self.tableWidget.horizontalHeader().setMinimumSectionSize(30)
        self.sb_x = QtGui.QSpinBox(self.centralwidget)
        self.sb_x.setGeometry(QtCore.QRect(470, 90, 59, 27))
        self.sb_x.setMaximum(999)
        self.sb_x.setProperty("value", 2)
        self.sb_x.setObjectName(_fromUtf8("sb_x"))
        self.pb_inc_h = QtGui.QPushButton(self.centralwidget)
        self.pb_inc_h.setGeometry(QtCore.QRect(490, 50, 40, 27))
        self.pb_inc_h.setText(_fromUtf8("+"))
        self.pb_inc_h.setObjectName(_fromUtf8("pb_inc_h"))
        self.pb_dec_h = QtGui.QPushButton(self.centralwidget)
        self.pb_dec_h.setGeometry(QtCore.QRect(490, 130, 40, 27))
        self.pb_dec_h.setText(_fromUtf8("-"))
        self.pb_dec_h.setObjectName(_fromUtf8("pb_dec_h"))
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QObject.connect(self.sb_x, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")), self.tableWidget.insertColumn)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        pass

