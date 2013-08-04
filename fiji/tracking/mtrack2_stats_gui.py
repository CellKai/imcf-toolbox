#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
GUI for statistics calculations from MTrack2 tracklists.
"""

import sys
from genui import fopen, fsave, GenericMainWindow
from genui.in_out_opt import Ui_MainWindow, QtCore, QtGui
from mtrack2_stats import gen_stats


class MTrack2MainWindow(Ui_MainWindow, GenericMainWindow):

    """Main Window for MTrack2 GUI."""

    def setup_window(self, window):
        """Customize the generic UI to our specific case."""
        super(MTrack2MainWindow, self).setupUi(window)
        self.set_defaults(window)
        window.setWindowTitle("MTrack2 statistics")
        self.label.setText("MTrack2 results analyzer")
        txt = "Input TXT File containing MTrack2 results (Ctrl+O)"
        self.le_infile.setPlaceholderText(txt)
        self.cb_option.setText("Write column labels into CSV file.")
        # self.cb_option.setDisabled(True)
        ffilter = 'Text files (*.txt);;All files (*.*)'
        QtCore.QObject.connect(self.pb_infile, QtCore.SIGNAL("clicked()"),
            lambda elt=self.le_infile: fopen(elt, ffilter=ffilter))
        QtCore.QObject.connect(self.pb_outfile, QtCore.SIGNAL("clicked()"),
            lambda elt=self.le_outfile: fsave(elt, directory=self.path))
        QtCore.QObject.connect(self.le_infile,
            QtCore.SIGNAL("textChanged(QString)"), self._update_path)
        QtCore.QMetaObject.connectSlotsByName(window)

    def run_calculations(self):
        """Collect the settings and launch the calculation."""
        statusmsg = self.statusbar.showMessage
        button_ok = self.bb_ok_cancel.button(QtGui.QDialogButtonBox.Ok)
        button_ok.setEnabled(False)
        infile = str(self.le_infile.text())
        outfile = str(self.le_outfile.text())
        label = False
        if (self.cb_option.checkState() == 2):
            label = True
        verbosity = self.sl_verbosity.value()
        statusmsg('Analyzing MTrack2 results...')
        gen_stats(f_in=infile, f_out=outfile, label=label,
            deltas=[1, 5], verbosity=verbosity)
        statusmsg('Finished creating statistics.')
        button_ok.setEnabled(True)


def main():
    """Set up the GUI window and show it."""
    app = QtGui.QApplication(sys.argv)
    main_window = QtGui.QMainWindow()
    gui = MTrack2MainWindow()
    gui.setup_window(main_window)
    main_window.show()
    return app.exec_()

if __name__ == "__main__":
    sys.exit(main())
