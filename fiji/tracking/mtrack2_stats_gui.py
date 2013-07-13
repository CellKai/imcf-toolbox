#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from mtrack2_stats import gen_stats
from ui_generic_in_out_opt import *


class My_UI_Window(Ui_MainWindow):
    def setupUi(self, MainWindow):
        super(My_UI_Window, self).setupUi(MainWindow)
        MainWindow.setWindowTitle("MTrack2 statistics")
        self.label.setText("MTrack2 results analyzer")
        txt = "Input TXT File containing MTrack2 results (Ctrl+O)"
        self.le_infile.setPlaceholderText(txt)
        self.cb_option.setText("Write column labels into CSV file.")
        # self.cb_option.setDisabled(True)
        MainWindow.addAction(self.sc_ctrl_w)
        MainWindow.addAction(self.sc_ctrl_q)
        QtCore.QObject.connect(self.pb_infile,
            QtCore.SIGNAL("clicked()"), self.selectInfile)
        QtCore.QObject.connect(self.pb_outfile,
            QtCore.SIGNAL("clicked()"), self.selectOutfile)
        QtCore.QObject.connect(self.bb_ok_cancel,
            QtCore.SIGNAL("rejected()"), MainWindow.close)
        QtCore.QObject.connect(self.bb_ok_cancel,
            QtCore.SIGNAL("accepted()"), self.runTool)
        QtCore.QObject.connect(self.sc_ctrl_w,
            QtCore.SIGNAL("triggered()"), MainWindow.close)
        QtCore.QObject.connect(self.sc_ctrl_q,
            QtCore.SIGNAL("triggered()"), MainWindow.close)
        QtCore.QObject.connect(self.sl_verbosity,
            QtCore.SIGNAL("valueChanged(int)"), self.sb_verbosity.setValue)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def selectInfile(self):
        self.le_infile.setText(QtGui.QFileDialog.getOpenFileName())
        # when the infile is changed, reset the outfile name:
        self.le_outfile.setText('')

    def selectOutfile(self):
        self.le_outfile.setText(QtGui.QFileDialog.getOpenFileName())

    def runTool(self):
        infile = str(self.le_infile.text())
        outfile = str(self.le_outfile.text())
        label = False
        if (self.cb_option.checkState() == 2):
            label = True
        verbosity = self.sl_verbosity.value()
        gen_stats(f_in=infile, f_out=outfile, label=label,
            deltas=[1, 5], verbosity=verbosity)
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
