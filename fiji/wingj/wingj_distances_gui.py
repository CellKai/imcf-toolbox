#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
GUI for WingJ distance calculations.
"""

import sys
from log import log, set_loglevel
from genui import fopen, diropen, GenericMainWindow
from genui.in2_spin import Ui_MainWindow, QtCore, QtGui
from volpy.imagej import read_csv_com, WingJStructure


class WingJMainWindow(Ui_MainWindow, GenericMainWindow):

    """Main Window for WingJ GUI."""

    def setup_window(self, window):
        """Customize the generic UI to our specific case."""
        super(WingJMainWindow, self).setupUi(window)
        self.set_defaults(window)
        window.setWindowTitle("WingJ Distances")
        self.label.setText("WingJ Distances")
        msg = 'Directory containing WingJ structure files.'
        self.le_path_1.setPlaceholderText(msg)
        msg = 'ImageJ CSV export with "center of mass" measurements.'
        self.le_path_2.setPlaceholderText(msg)
        self.label_3.setText("Pixel size to calibrate WingJ data")
        QtCore.QObject.connect(self.pb_path_1, QtCore.SIGNAL("clicked()"),
            lambda elt=self.le_path_1: diropen(elt, dirsonly=False))
        ffilter = 'Comma-separated Values (*.csv);;' + \
            'Text files (*.txt);;All files (*.*)'
        QtCore.QObject.connect(self.pb_path_2, QtCore.SIGNAL("clicked()"),
            lambda elt=self.le_path_2: \
                fopen(elt, ffilter=ffilter, directory=self.path))
        QtCore.QObject.connect(self.le_path_1,
            QtCore.SIGNAL("textChanged(QString)"), self._update_path)
        QtCore.QMetaObject.connectSlotsByName(window)

    def run_calculations(self):
        """Collect the settings and launch the calculation."""
        directory = str(self.le_path_1.text())
        in_ijroi = str(self.le_path_2.text())
        calib = self.sb_double.value()
        set_loglevel(self.sl_verbosity.value())

        log.warn('Calculating distances to WingJ structures...')
        wingj = WingJStructure(directory, calib)
        coords = read_csv_com(in_ijroi)
        coords *= calib
        wingj.min_dist_csv_export(coords, directory)
        log.warn('Finished.')


def main():
    """Set up the GUI window and show it."""
    app = QtGui.QApplication(sys.argv)
    main_window = QtGui.QMainWindow()
    gui = WingJMainWindow()
    gui.setup_window(main_window)
    main_window.show()
    return app.exec_()

if __name__ == "__main__":
    sys.exit(main())
