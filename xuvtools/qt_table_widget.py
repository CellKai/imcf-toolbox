# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'table_widget.ui'
#
# Created: Fri Mar  8 09:34:36 2013
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
        MainWindow.resize(650, 484)
        MainWindow.setMinimumSize(QtCore.QSize(650, 484))
        MainWindow.setWindowTitle(_fromUtf8("MainWindow"))
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setSizeConstraint(QtGui.QLayout.SetMinimumSize)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.tableWidget = QtGui.QTableWidget(self.centralwidget)
        self.tableWidget.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.tableWidget.setAlternatingRowColors(True)
        self.tableWidget.setRowCount(10)
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setObjectName(_fromUtf8("tableWidget"))
        self.gridLayout.addWidget(self.tableWidget, 1, 0, 1, 1)
        self.widget = QtGui.QWidget(self.centralwidget)
        self.widget.setEnabled(True)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy)
        self.widget.setMinimumSize(QtCore.QSize(80, 0))
        self.widget.setMaximumSize(QtCore.QSize(80, 16777215))
        self.widget.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.widget.setObjectName(_fromUtf8("widget"))
        self.formLayout = QtGui.QFormLayout(self.widget)
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setLabelAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.formLayout.setFormAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.formLayout.setMargin(0)
        self.formLayout.setHorizontalSpacing(6)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.pb_inc_h = QtGui.QPushButton(self.widget)
        self.pb_inc_h.setMinimumSize(QtCore.QSize(33, 0))
        self.pb_inc_h.setMaximumSize(QtCore.QSize(33, 16777215))
        self.pb_inc_h.setText(_fromUtf8("+"))
        self.pb_inc_h.setObjectName(_fromUtf8("pb_inc_h"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.pb_inc_h)
        self.sb_h = QtGui.QSpinBox(self.widget)
        self.sb_h.setMaximum(999)
        self.sb_h.setProperty("value", 2)
        self.sb_h.setObjectName(_fromUtf8("sb_h"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.sb_h)
        self.pb_dec_h = QtGui.QPushButton(self.widget)
        self.pb_dec_h.setMinimumSize(QtCore.QSize(33, 0))
        self.pb_dec_h.setMaximumSize(QtCore.QSize(33, 16777215))
        self.pb_dec_h.setText(_fromUtf8("-"))
        self.pb_dec_h.setObjectName(_fromUtf8("pb_dec_h"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.pb_dec_h)
        self.gridLayout.addWidget(self.widget, 1, 1, 1, 1)
        self.widget_2 = QtGui.QWidget(self.centralwidget)
        self.widget_2.setMinimumSize(QtCore.QSize(0, 33))
        self.widget_2.setMaximumSize(QtCore.QSize(200, 16777215))
        self.widget_2.setObjectName(_fromUtf8("widget_2"))
        self.gridLayout_2 = QtGui.QGridLayout(self.widget_2)
        self.gridLayout_2.setMargin(0)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.pb_dec_v = QtGui.QPushButton(self.widget_2)
        self.pb_dec_v.setMaximumSize(QtCore.QSize(33, 16777215))
        self.pb_dec_v.setText(_fromUtf8("-"))
        self.pb_dec_v.setObjectName(_fromUtf8("pb_dec_v"))
        self.gridLayout_2.addWidget(self.pb_dec_v, 0, 0, 1, 1)
        self.pb_inc_v = QtGui.QPushButton(self.widget_2)
        self.pb_inc_v.setMaximumSize(QtCore.QSize(33, 16777215))
        self.pb_inc_v.setText(_fromUtf8("+"))
        self.pb_inc_v.setObjectName(_fromUtf8("pb_inc_v"))
        self.gridLayout_2.addWidget(self.pb_inc_v, 0, 2, 1, 1)
        self.sb_v = QtGui.QSpinBox(self.widget_2)
        self.sb_v.setMaximumSize(QtCore.QSize(68, 16777215))
        self.sb_v.setProperty("value", 10)
        self.sb_v.setObjectName(_fromUtf8("sb_v"))
        self.gridLayout_2.addWidget(self.sb_v, 0, 1, 1, 1)
        self.gridLayout.addWidget(self.widget_2, 2, 0, 1, 1)
        self.cb_ordering = QtGui.QComboBox(self.centralwidget)
        self.cb_ordering.setObjectName(_fromUtf8("cb_ordering"))
        self.cb_ordering.addItem(_fromUtf8(""))
        self.cb_ordering.setItemText(0, _fromUtf8("column-wise from top to bottom, starting on the left side"))
        self.cb_ordering.addItem(_fromUtf8(""))
        self.cb_ordering.setItemText(1, _fromUtf8("column-wise from bottom to top, starting on the left side"))
        self.gridLayout.addWidget(self.cb_ordering, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        pass

