#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from qt_table_widget import *

class My_UI_Window(Ui_MainWindow):
    def setupUi(self, MainWindow):
        super(My_UI_Window, self).setupUi(MainWindow)
        MainWindow.setWindowTitle("Grid Aligner")
        # self.label.setText("Grid Aligner")
        QtCore.QObject.connect(self.pb_plus, QtCore.SIGNAL("clicked()"), self.tableWidget.insertColumn)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)


if __name__ == "__main__":
    # instantiate a QApplication object
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = My_UI_Window()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())



