#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from qt_table_widget import *

class My_UI_Window(Ui_MainWindow):
    def setupUi(self, MainWindow):
        super(My_UI_Window, self).setupUi(MainWindow)
        MainWindow.setWindowTitle("Grid Aligner")
        QtCore.QObject.connect(self.sb_h, QtCore.SIGNAL("valueChanged(int)"), self.set_cols)
        QtCore.QObject.connect(self.sb_v, QtCore.SIGNAL("valueChanged(int)"), self.set_rows)
        QtCore.QObject.connect(self.pb_inc_h, QtCore.SIGNAL("clicked()"), self.inc_cols)
        QtCore.QObject.connect(self.pb_dec_h, QtCore.SIGNAL("clicked()"), self.dec_cols)
        QtCore.QObject.connect(self.pb_inc_v, QtCore.SIGNAL("clicked()"), self.inc_rows)
        QtCore.QObject.connect(self.pb_dec_v, QtCore.SIGNAL("clicked()"), self.dec_rows)
        # QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def inc_cols(self):
        self.tableWidget.insertColumn(0)
        self.sb_h.setValue(self.tableWidget.columnCount())

    def dec_cols(self):
        self.tableWidget.removeColumn(0)
        self.sb_h.setValue(self.tableWidget.columnCount())

    def set_cols(self, val):
        delta = val - self.tableWidget.columnCount()
        # print delta
        for i in range(delta):
            self.tableWidget.insertColumn(0)
        for i in range(delta * -1):
            self.tableWidget.removeColumn(0)

    def inc_rows(self):
        self.tableWidget.insertRow(0)
        self.sb_v.setValue(self.tableWidget.rowCount())

    def dec_rows(self):
        self.tableWidget.removeRow(0)
        self.sb_v.setValue(self.tableWidget.rowCount())

    def set_rows(self, val):
        delta = val - self.tableWidget.rowCount()
        # print delta
        for i in range(delta):
            self.tableWidget.insertRow(0)
        for i in range(delta * -1):
            self.tableWidget.removeRow(0)


if __name__ == "__main__":
    # instantiate a QApplication object
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = My_UI_Window()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())



