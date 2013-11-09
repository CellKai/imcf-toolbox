#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
GUI for generating bitmaps from Imaris spots XML exports.
"""

import sys
from imaris_xml import StatisticsSpots
from numpy import savetxt
from log import set_loglevel
from misc import filehandle
from genui import fopen, fsave, GenericMainWindow
from genui.in_out_xysize_xysize import Ui_MainWindow, QtCore, QtGui


class SpotsToBitmapMainWindow(Ui_MainWindow, GenericMainWindow):

    """Main Window for Spots to Bitmap GUI."""

    def setup_window(self, window):
        """Customize the generic UI to our specific case."""
        super(SpotsToBitmapMainWindow, self).setupUi(window)
        self.set_defaults(window)
        window.setWindowTitle("Imaris Spots to Bitmap")
        self.label_1.setText("Spots To Bitmap Converter")
        self.group_1.setTitle("Input File")
        msg = "XML File containing Imaris spots export (Ctrl+O)"
        self.le_infile.setPlaceholderText(msg)
        ffilter = 'XML files (*.xml);;All files (*.*)'
        self.label_3.setText("Input size (in calibrated units)")
        self.group_2.setTitle("Output File")
        self.label_4.setText("Output size (in pixels)")
        self.sb_1.setValue(512)
        self.sb_2.setValue(512)
        # signal<->slot connections:
        conn = QtCore.QObject.connect
        conn(self.pb_infile, QtCore.SIGNAL("clicked()"),
             lambda elt=self.le_infile: fopen(elt, ffilter=ffilter))
        conn(self.pb_outfile, QtCore.SIGNAL("clicked()"),
             lambda elt=self.le_outfile: fsave(elt, directory=self.path))
        conn(self.le_infile,
             QtCore.SIGNAL("textChanged(QString)"), self._update_path)
        QtCore.QMetaObject.connectSlotsByName(window)

    def run_calculations(self):
        """Collect the settings and launch the calculation."""
        statusmsg = self.statusbar.showMessage
        button_ok = self.bb_ok_cancel.button(QtGui.QDialogButtonBox.Ok)
        button_ok.setEnabled(False)
        infile = str(self.le_infile.text())
        outfile = filehandle(str(self.le_outfile.text()), 'w')
        xmax = self.dsb_1.value()
        ymax = self.dsb_2.value()
        if (xmax + ymax) == 0:
            statusmsg('Input size required!')
            button_ok.setEnabled(True)
            return
        xtgt = self.sb_1.value()
        ytgt = self.sb_2.value()
        set_loglevel(self.sl_verbosity.value())

        statusmsg('Parsing XML file...')
        spots = StatisticsSpots(infile)
        spots.set_limits(xmax=xmax, ymax=ymax)
        statusmsg('Generating bitmap...')
        bitmap = spots.gen_bitmap((xtgt, ytgt), delta=50)
        statusmsg('Writing output file...')
        savetxt(outfile, bitmap, fmt='%i')
        statusmsg('Finished writing bitmap (%i x %i).' % (xtgt, ytgt))
        button_ok.setEnabled(True)


def main():
    """Set up the GUI window and show it."""
    app = QtGui.QApplication(sys.argv)
    main_window = QtGui.QMainWindow()
    gui = SpotsToBitmapMainWindow()
    gui.setup_window(main_window)
    main_window.show()
    return app.exec_()

if __name__ == "__main__":
    sys.exit(main())
