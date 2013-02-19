#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from qt_open_file import *

class My_UI_Window(Ui_MainWindow):
    def setupUi(self, MainWindow):
        super(My_UI_Window, self).setupUi(MainWindow)
        MainWindow.setWindowTitle("SUBCLASS")
        self.label.setText('blabla')

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = My_UI_Window()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
