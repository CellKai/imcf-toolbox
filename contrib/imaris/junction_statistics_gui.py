#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
GUI for Junction statistics calculations.
"""

# FIXME: needs to be adjusted to new filaments structure (p3d+edges)

import sys
import volpy as vp
import volpy.plot as plot
from log import set_loglevel
from misc import filehandle
from genui import fopen, fsave, GenericMainWindow
from genui.in_out_opt import Ui_MainWindow, QtCore, QtGui


class JunctionsMainWindow(Ui_MainWindow, GenericMainWindow):

    """Main Window for Junction Statistics GUI."""

    def setup_window(self, window):
        """Customize the generic UI to our specific case."""
        super(JunctionsMainWindow, self).setupUi(window)
        self.set_defaults(window)
        window.setWindowTitle("Junction Statistics")
        self.label.setText("Junction Statistics")
        msg = "Input CSV File containing Filament points (Ctrl+O)"
        self.le_infile.setPlaceholderText(msg)
        self.cb_option.setText("Show a 3D plot of the calculated data.")
        ffilter = 'Comma-separated Values (*.csv);;All files (*.*)'
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
        in_csv = str(self.le_infile.text())
        out_csv = filehandle(str(self.le_outfile.text()), 'w')
        set_loglevel(self.sl_verbosity.value())

        statusmsg('Parsing junction files...')
        junction = vp.CellJunction(in_csv)
        statusmsg('Writing output files...')
        junction.write_output(out_csv, in_csv)
        if (self.cb_option.checkState() == 2):
            statusmsg('Showing plot...')
            plot.junction(junction, True, False)
        statusmsg('Finished.')
        button_ok.setEnabled(True)


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
