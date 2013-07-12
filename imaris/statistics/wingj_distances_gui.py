#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
GUI for WingJ distance calculations.
"""

import sys
from wingj_distances import wingj_dist_to_surfaces
from ui_generic_in4_out3_spin import *

def select_file(element):
    """Show file dialog and update an elements text with the result.

    This is a callback function for usage with "Browse" buttons or similar in a
    PyQt GUI. It displays the system's file selection dialog and updates the
    supplied GUI element with the result. To use it with Qt's connect() method,
    a lambda function must be used there, e.g.

    >>> connect(btn, sig, lambda elt=self.line_edit: select_file(elt))

    The main purpose of this is to eliminate the need for implementing a
    separate callback function for each slot, resulting in many more or less
    identical code segments.
    """
    element.setText(QtGui.QFileDialog.getOpenFileName())


class My_UI_Window(Ui_MainWindow):
    """Main Window for WingJ GUI."""
    def setupUi(self, MainWindow):
        """Customize the generic UI to our specific case."""
        super(My_UI_Window, self).setupUi(MainWindow)
        MainWindow.setWindowTitle("WingJ Distances")
        self.label.setText("WingJ Distances")
        msg = 'WingJ structure file for the %s.'
        self.le_infile.setPlaceholderText(msg % 'A-P separation')
        self.le_infile_2.setPlaceholderText(msg % 'V-D separation')
        self.le_infile_3.setPlaceholderText(msg % 'contour line')
        msg = 'Imaris XML export having a "Position" sheet.'
        self.le_infile_4.setPlaceholderText(msg)
        self.label_3.setText("Pixel size to calibrate WingJ data")
        msg = 'Output CSV file for distances to %s line.'
        self.le_outfile.setPlaceholderText(msg % 'A-P')
        self.le_outfile_2.setPlaceholderText(msg % 'V-D')
        self.le_outfile_3.setPlaceholderText(msg % 'contour')
        MainWindow.addAction(self.sc_ctrl_w)
        MainWindow.addAction(self.sc_ctrl_q)
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
        QtCore.QObject.connect(self.bb_ok_cancel, QtCore.SIGNAL("rejected()"), MainWindow.close)
        QtCore.QObject.connect(self.bb_ok_cancel, QtCore.SIGNAL("accepted()"), self.runTool)
        QtCore.QObject.connect(self.sc_ctrl_w, QtCore.SIGNAL("triggered()"), MainWindow.close)
        QtCore.QObject.connect(self.sc_ctrl_q, QtCore.SIGNAL("triggered()"), MainWindow.close)
        QtCore.QObject.connect(self.sl_verbosity, QtCore.SIGNAL("valueChanged(int)"), self.sb_verbosity.setValue)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def runTool(self):
        """Collect the settings and launch the calculation."""
        in_ap = str(self.le_infile.text())
        in_vd = str(self.le_infile_2.text())
        in_cnt = str(self.le_infile_3.text())
        in_xml = str(self.le_infile_4.text())
        out_ap = str(self.le_outfile.text())
        out_vd = str(self.le_outfile_2.text())
        out_cnt = str(self.le_outfile_3.text())
        # TODO: set loglevel from verbosity value:
        # verbosity = self.sl_verbosity.value()
        # FIXME: pixelsize is missing!
        wingj_dist_to_surfaces(in_ap, in_vd, in_cnt, in_xml,
            out_ap, out_vd, out_cnt)


if __name__ == "__main__":
    # instantiate a QApplication object
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = My_UI_Window()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
