#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
GUI for WingJ distance calculations.
"""

import sys
import argparse
from log import log
from misc import set_loglevel
from genui import select_file
from genui.in4_out3_spin import Ui_MainWindow, QtCore, QtGui
from wingj_distances import wingj_dist_to_surfaces


class WingJMainWindow(Ui_MainWindow):

    """Main Window for WingJ GUI."""

    def setup_window(self, window):
        """Customize the generic UI to our specific case."""
        super(WingJMainWindow, self).setupUi(window)
        window.setWindowTitle("WingJ Distances")
        self.label.setText("WingJ Distances")
        msg = 'WingJ structure file for the %s.'
        self.le_infile.setPlaceholderText(msg % 'A-P separation')
        self.le_infile_2.setPlaceholderText(msg % 'V-D separation')
        self.le_infile_3.setPlaceholderText(msg % 'contour line')
        msg = 'ImageJ CSV export with "center of mass" measurements.'
        self.le_infile_4.setPlaceholderText(msg)
        self.label_3.setText("Pixel size to calibrate WingJ data")
        msg = 'Output CSV file for distances to %s line.'
        self.le_outfile.setPlaceholderText(msg % 'A-P')
        self.le_outfile_2.setPlaceholderText(msg % 'V-D')
        self.le_outfile_3.setPlaceholderText(msg % 'contour')
        window.addAction(self.sc_ctrl_w)
        window.addAction(self.sc_ctrl_q)
        QtCore.QObject.connect(self.pb_infile, QtCore.SIGNAL("clicked()"),
            lambda elt=self.le_infile: select_file(elt))
        QtCore.QObject.connect(self.pb_infile_2, QtCore.SIGNAL("clicked()"),
            lambda elt=self.le_infile_2: select_file(elt))
        QtCore.QObject.connect(self.pb_infile_3, QtCore.SIGNAL("clicked()"),
            lambda elt=self.le_infile_3: select_file(elt))
        QtCore.QObject.connect(self.pb_infile_4, QtCore.SIGNAL("clicked()"),
            lambda elt=self.le_infile_4: select_file(elt))
        QtCore.QObject.connect(self.pb_outfile, QtCore.SIGNAL("clicked()"),
            lambda elt=self.le_outfile: select_file(elt))
        QtCore.QObject.connect(self.pb_outfile_2, QtCore.SIGNAL("clicked()"),
            lambda elt=self.le_outfile_2: select_file(elt))
        QtCore.QObject.connect(self.pb_outfile_3, QtCore.SIGNAL("clicked()"),
            lambda elt=self.le_outfile_3: select_file(elt))
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
        self.le_infile_2.setText(values[1])
        self.le_infile_3.setText(values[2])
        self.le_infile_4.setText(values[3])
        self.le_outfile.setText(values[4])
        self.le_outfile_2.setText(values[5])
        self.le_outfile_3.setText(values[6])

    def run_calculations(self):
        """Collect the settings and launch the calculation."""
        in_ap = str(self.le_infile.text())
        in_vd = str(self.le_infile_2.text())
        in_cnt = str(self.le_infile_3.text())
        in_ijroi = str(self.le_infile_4.text())
        out_ap = str(self.le_outfile.text())
        out_vd = str(self.le_outfile_2.text())
        out_cnt = str(self.le_outfile_3.text())
        px_size = self.sb_double.value()
        set_loglevel(self.sl_verbosity.value())
        wingj_dist_to_surfaces(
            (in_ap, in_vd, in_cnt),
            (out_ap, out_vd, out_cnt),
            px_size, None, in_ijroi)


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
    gui = WingJMainWindow()
    gui.setup_window(main_window)
    gui.preset_fields(parse_arguments())
    main_window.show()
    return app.exec_()

if __name__ == "__main__":
    sys.exit(main())
