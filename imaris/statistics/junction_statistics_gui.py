#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
GUI for Junction statistics calculations.
"""

import sys
import argparse
import volpy as vp
from aux_gui import select_file
from aux import set_loglevel, check_filehandle
from ui_generic_in_out_opt import *


class JunctionsMainWindow(Ui_MainWindow):

    """Main Window for Junction Statistics GUI."""

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
            lambda elt=self.le_infile: select_file(elt))
        QtCore.QObject.connect(self.pb_outfile, QtCore.SIGNAL("clicked()"),
            lambda elt=self.le_outfile: select_file(elt))
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

    def preset_fields(self, values):
        """Preset field contents with supplied values."""
        if not values:
            return
        self.le_infile.setText(values[0])
        self.le_outfile.setText(values[1])

    def run_calculations(self):
        """Collect the settings and launch the calculation."""
        in_csv = str(self.le_infile.text())
        out_csv = check_filehandle(str(self.le_outfile.text()), 'w')
        set_loglevel(self.sl_verbosity.value())

        junction = vp.CellJunction(in_csv)
        junction.write_output(out_csv, in_csv)
        # reset the outfile's name
        self.le_outfile.setText('')
        if (self.cb_option.checkState() == 2):
            vp.plot3d_junction(junction, True, False)


def parse_arguments():
    """Parse commandline arguments for preset values."""
    argparser = argparse.ArgumentParser(description=__doc__)
    argparser.add_argument('-p', '--preset', required=False,
        help='Prefill fields with values in this list.')
    try:
        args = argparser.parse_args()
    except IOError as err:
        argparser.error(str(err))
    if args.preset != None:
        return args.preset.split(',')
    else:
        return None


def main():
    """Set up the GUI window and show it."""
    app = QtGui.QApplication(sys.argv)
    main_window = QtGui.QMainWindow()
    gui = JunctionsMainWindow()
    gui.setup_window(main_window)
    gui.preset_fields(parse_arguments())
    main_window.show()
    return app.exec_()

if __name__ == "__main__":
    sys.exit(main())
