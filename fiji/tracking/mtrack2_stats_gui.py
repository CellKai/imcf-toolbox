#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import mtrack2_stats
from generic_in_out_opt import *

class My_UI_Window(Ui_MainWindow):
    def setupUi(self, MainWindow):
        super(My_UI_Window, self).setupUi(MainWindow)
        MainWindow.setWindowTitle("MTrack2 statistics")
        self.label.setText("MTrack2 results analyzer")
        self.le_infile.setPlaceholderText("Input CSV File containing MTrack2 results (Ctrl+O)")
        self.cb_plot.setText("Combine tracks.")
        self.cb_plot.setDisabled(True)
        MainWindow.addAction(self.sc_ctrl_w)
        MainWindow.addAction(self.sc_ctrl_q)
        QtCore.QObject.connect(self.pb_infile, QtCore.SIGNAL("clicked()"), self.selectInfile)
        QtCore.QObject.connect(self.pb_outfile, QtCore.SIGNAL("clicked()"), self.selectOutfile)
        QtCore.QObject.connect(self.bb_ok_cancel, QtCore.SIGNAL("rejected()"), MainWindow.close)
        QtCore.QObject.connect(self.bb_ok_cancel, QtCore.SIGNAL("accepted()"), self.runTool)
        QtCore.QObject.connect(self.sc_ctrl_w, QtCore.SIGNAL("triggered()"), MainWindow.close)
        QtCore.QObject.connect(self.sc_ctrl_q, QtCore.SIGNAL("triggered()"), MainWindow.close)
        QtCore.QObject.connect(self.sl_verbosity, QtCore.SIGNAL("valueChanged(int)"), self.sb_verbosity.setValue)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def selectInfile(self):
        self.le_infile.setText(QtGui.QFileDialog.getOpenFileName())
        # when the infile is changed, reset the outfile name:
        self.le_outfile.setText('')

    def selectOutfile(self):
        self.le_outfile.setText(QtGui.QFileDialog.getOpenFileName())

    def runTool(self):
        sys.argv = ['./mtrack2_stats.py']
        infile = str(self.le_infile.text())
        sys.argv += ['-i', infile]
        outfile = str(self.le_outfile.text())
        sys.argv += ['-o', outfile]
        for inc_verbosity in range(0, self.sl_verbosity.value()):
            sys.argv.append('-v')
        # print sys.argv
        mtrack2_stats.main()
        # TODO: should we exit after the work's done? -> ask user!
        # sys.exit()


if __name__ == "__main__":
    # instantiate a QApplication object
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = My_UI_Window()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
