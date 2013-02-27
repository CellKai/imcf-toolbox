#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from qt_table_widget import *

class My_UI_Window(Ui_MainWindow):
    def setupUi(self, MainWindow):
        super(My_UI_Window, self).setupUi(MainWindow)
        MainWindow.setWindowTitle("Grid Aligner")
        self.change_table_size()
        QtCore.QObject.connect(self.sb_h, QtCore.SIGNAL("valueChanged(int)"), self.set_cols)
        QtCore.QObject.connect(self.sb_v, QtCore.SIGNAL("valueChanged(int)"), self.set_rows)
        QtCore.QObject.connect(self.pb_inc_h, QtCore.SIGNAL("clicked()"), self.inc_cols)
        QtCore.QObject.connect(self.pb_dec_h, QtCore.SIGNAL("clicked()"), self.dec_cols)
        QtCore.QObject.connect(self.pb_inc_v, QtCore.SIGNAL("clicked()"), self.inc_rows)
        QtCore.QObject.connect(self.pb_dec_v, QtCore.SIGNAL("clicked()"), self.dec_rows)
        QtCore.QObject.connect(self.tableWidget, QtCore.SIGNAL("cellChanged(int, int)"), self.foo)
        # QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def foo(self, x, y):
        print x, y

    def inc_cols(self):
        self.tableWidget.insertColumn(0)
        self.change_table_size()

    def dec_cols(self):
        self.tableWidget.removeColumn(0)
        self.change_table_size()

    def set_cols(self, val):
        delta = val - self.tableWidget.columnCount()
        # print delta
        for i in range(delta):
            self.tableWidget.insertColumn(0)
        for i in range(delta * -1):
            self.tableWidget.removeColumn(0)
        self.change_table_size()

    def inc_rows(self):
        self.tableWidget.insertRow(0)
        self.change_table_size()

    def dec_rows(self):
        self.tableWidget.removeRow(0)
        self.change_table_size()

    def set_rows(self, val):
        delta = val - self.tableWidget.rowCount()
        # print delta
        for i in range(delta):
            self.tableWidget.insertRow(0)
        for i in range(delta * -1):
            self.tableWidget.removeRow(0)
        self.change_table_size()

    def set_cell_status(self, row, col):
        item = self.tableWidget.item(row, col)
        cols = self.tableWidget.columnCount()
        # print item
        if item is None:
            # print "not existing: %s %s" % (row, col)
            cell = QtGui.QTableWidgetItem("%s" % ((cols * row) + col))
            cell.setCheckState(QtCore.Qt.Checked)
            self.tableWidget.setItem(row, col, cell)
        else:
            # print row, col
            item.setText("%s" % ((cols * row) + col))

    def change_table_size(self):
        rows = self.tableWidget.rowCount()
        cols = self.tableWidget.columnCount()
        for r in range(rows):
            for c in range(cols):
                self.set_cell_status(r, c)

    def update_table(self):
        rows = self.tableWidget.rowCount()
        cols = self.tableWidget.columnCount()
        self.sb_v.setValue(rows)
        self.sb_v.setValue(rows)
        self.sb_h.setValue(cols)
        self.sb_h.setValue(cols)
        cur = 0
        for r in range(rows):
            for c in range(cols):
                item = self.tableWidget.item(r, c)
                curstat = item.checkState()
                item.setText("%s" % ((cols * r) + c))
                print "%s %s %s" % (r, c, curstat)
                # cell = QtGui.QTableWidgetItem("%s" % ((cols * r) + c))
                # cell.setCheckState(QtCore.Qt.Checked)
                # self.tableWidget.setItem(r, c, cell)


if __name__ == "__main__":
    # instantiate a QApplication object
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = My_UI_Window()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())



