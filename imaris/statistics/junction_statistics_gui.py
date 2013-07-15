#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
GUI for Junction statistics calculations.
"""

import sys
import filament_parser
from ui_generic_in_out_opt import *


class JunctionsMainWindow(Ui_MainWindow):

    """Main Window for WingJ GUI."""

    def setup_window(self, window):
        """Customize the generic UI to our specific case."""
        super(JunctionsMainWindow, self).setupUi(window)
        window.setWindowTitle("Junction Statistics")
        self.label.setText("Junction Statistics")
        msg = "Input CSV File containing Filament points (Ctrl+O)"
        self.le_infile.setPlaceholderText(msg)
        self.cb_option.setText("Show a 3D plot of the calculated data.")
        window.addAction(self.sc_ctrl_w)
        window.addAction(self.sc_ctrl_q)
        QtCore.QObject.connect(self.pb_infile, QtCore.SIGNAL("clicked()"),
            self.selectInfile)
        QtCore.QObject.connect(self.pb_outfile, QtCore.SIGNAL("clicked()"),
            self.selectOutfile)
        QtCore.QObject.connect(self.bb_ok_cancel, QtCore.SIGNAL("rejected()"),
            window.close)
        QtCore.QObject.connect(self.bb_ok_cancel, QtCore.SIGNAL("accepted()"),
            self.run_calculations)
        QtCore.QObject.connect(self.sc_ctrl_w, QtCore.SIGNAL("triggered()"),
            window.close)
        QtCore.QObject.connect(self.sc_ctrl_q, QtCore.SIGNAL("triggered()"),
            window.close)
        QtCore.QObject.connect(self.sl_verbosity,
            QtCore.SIGNAL("valueChanged(int)"), self.sb_verbosity.setValue)
        QtCore.QMetaObject.connectSlotsByName(window)

    def selectInfile(self):
        self.le_infile.setText(QtGui.QFileDialog.getOpenFileName())
        # when the infile is changed, reset the outfile name:
        self.le_outfile.setText('')

    def selectOutfile(self):
        self.le_outfile.setText(QtGui.QFileDialog.getOpenFileName())

    def run_calculations(self):
        """Collect the settings and launch the calculation."""
        sys.argv = ['./filament_parser.py']
        infile = str(self.le_infile.text())
        sys.argv += ['-i', infile]
        outfile = str(self.le_outfile.text())
        sys.argv += ['-o', outfile]
        plot = None
        if (self.cb_option.checkState() == 2):
            plot = '--plot'
        if plot:
            sys.argv.append(plot)
        for _ in range(0, self.sl_verbosity.value()):
            sys.argv.append('-v')
        # print sys.argv
        filament_parser.main()


def main():
    """Set up the GUI window and show it."""
    app = QtGui.QApplication(sys.argv)
    main_window = QtGui.QMainWindow()
    gui = JunctionsMainWindow()
    gui.setup_window(main_window)
    main_window.show()
    return app.exec_()

if __name__ == "__main__":
    sys.exit(main())
