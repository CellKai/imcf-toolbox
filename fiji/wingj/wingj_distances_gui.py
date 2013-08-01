#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
GUI for WingJ distance calculations.
"""

import sys
import argparse
from log import log
from misc import set_loglevel
from genui import select_file, select_directory
from genui.in2_spin import Ui_MainWindow, QtCore, QtGui
from volpy.imagej import read_csv_com, WingJStructure


class WingJMainWindow(Ui_MainWindow):

    """Main Window for WingJ GUI."""

    def __init__(self):
        self.path = ''

    def setup_window(self, window):
        """Customize the generic UI to our specific case."""
        super(WingJMainWindow, self).setupUi(window)
        window.setWindowTitle("WingJ Distances")
        self.label.setText("WingJ Distances")
        msg = 'Directory containing WingJ structure files.'
        self.le_infile.setPlaceholderText(msg)
        msg = 'ImageJ CSV export with "center of mass" measurements.'
        self.le_infile_2.setPlaceholderText(msg)
        self.label_3.setText("Pixel size to calibrate WingJ data")
        window.addAction(self.sc_ctrl_w)
        window.addAction(self.sc_ctrl_q)
        QtCore.QObject.connect(self.pb_infile, QtCore.SIGNAL("clicked()"),
            lambda elt=self.le_infile: select_directory(elt, dirsonly=False))
        ffilter = 'Comma-separated Values (*.csv);;' + \
            'Text files (*.txt);;All files (*.*)'
        QtCore.QObject.connect(self.pb_infile_2, QtCore.SIGNAL("clicked()"),
            lambda elt=self.le_infile_2: \
                select_file(elt, ffilter=ffilter, directory=self.path))
        QtCore.QObject.connect(self.bb_ok_cancel, QtCore.SIGNAL("rejected()"),
            window.close)
        QtCore.QObject.connect(self.bb_ok_cancel, QtCore.SIGNAL("accepted()"),
            self.run_calculations)
        QtCore.QObject.connect(self.sc_ctrl_w, QtCore.SIGNAL("triggered()"),
            window.close)
        QtCore.QObject.connect(self.sc_ctrl_q, QtCore.SIGNAL("triggered()"),
            window.close)
        QtCore.QObject.connect(self.le_infile,
            QtCore.SIGNAL("textChanged(QString)"), self._update_wjdir)
        QtCore.QObject.connect(self.sl_verbosity,
            QtCore.SIGNAL("valueChanged(int)"), self.sb_verbosity.setValue)
        QtCore.QMetaObject.connectSlotsByName(window)

    def _update_wjdir(self, path):
        """Update the base directory where to find the WingJ files."""
        self.path = path

    def preset_fields(self, values):
        """Preset field contents with supplied values."""
        if not values:
            return
        self.le_infile.setText(values[0])
        self.le_infile_2.setText(values[1])

    def run_calculations(self):
        """Collect the settings and launch the calculation."""
        directory = str(self.le_infile.text())
        in_ijroi = str(self.le_infile_2.text())
        calib = self.sb_double.value()
        set_loglevel(self.sl_verbosity.value())

        log.warn('Calculating distances to WingJ structures...')
        wingj = WingJStructure(directory, calib)
        coords = read_csv_com(in_ijroi)
        coords *= calib
        wingj.min_dist_csv_export(coords, directory)
        log.warn('Finished.')


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
