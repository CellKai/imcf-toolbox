#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module to set common default properties for PyQt windows.
"""

import genui
import os
from PyQt4 import QtGui, QtCore
from log import log


class GenericMainWindow(object):

    """Common methods and variables for main windows."""

    def __init__(self):
        """Prepare instance variables etc."""
        self.path = ''

    def _update_path(self, path):
        """Update the base directory for the file dialogs."""
        path = str(path)
        log.debug('GenericMainWindow._update_path(%s)' % path)
        if os.path.isdir(path):
            self.path = path
        else:
            self.path = os.path.dirname(path)

    def set_defaults(self, window):
        """Set some default values used in all derived GUIs."""
        self.preset_fields(genui.parse_presets())
        # NOTE I: there are many things that could potentially go wrong here,
        # but we don't try to catch them as they are important indicators that
        # something is missing in a derived subclass.
        # NOTE II: an instance of GenericMainWindow doesn't have the members
        # referenced herein, only an appropriately constructed subclass will,
        # so we disable the corresponding pylint message:
        # pylint: disable-msg=E1101
        window.addAction(self.sc_ctrl_w)
        window.addAction(self.sc_ctrl_q)
        conn = QtCore.QObject.connect
        conn(self.bb_ok_cancel, QtCore.SIGNAL("rejected()"), window.close)
        conn(self.bb_ok_cancel, QtCore.SIGNAL("accepted()"),
             self.run_calculations)
        conn(self.sc_ctrl_w, QtCore.SIGNAL("triggered()"), window.close)
        conn(self.sc_ctrl_q, QtCore.SIGNAL("triggered()"), window.close)
        conn(self.sl_verbosity, QtCore.SIGNAL("valueChanged(int)"),
             self.sb_verbosity.setValue)

    def preset_fields(self, val_dict):
        """Preset GUI elements with supplied values.

        This is a convenience method to allow for presetting contents of GUI
        elements e.g. to facilitate testing the behaviour from the
        commandline. Uses a dict that maps the names of the elements to their
        value, see parse_presets() below.

        Parameters
        ----------
        val_dict : dict
            The dictionary containing element names and their desired values.

        Example
        -------
        >>> presets = {'le_file_1': '/path/to/file', 'le_file_2': 'file2'}
        >>> window.preset_fields(presets) # doctest: +SKIP
        """
        # pylint: disable-msg=E1101
        if not val_dict:
            return
        types = (QtGui.QLineEdit,
                 QtGui.QDoubleSpinBox,
                 QtGui.QSpinBox)
        for name in val_dict.keys():
            elt = self.centralwidget.findChild(types, name)
            if elt:
                if type(elt) == QtGui.QLineEdit:
                    elt.setText(str(val_dict[name]))
                elif type(elt) == QtGui.QSpinBox:
                    elt.setValue(int(val_dict[name]))
                elif type(elt) == QtGui.QDoubleSpinBox:
                    elt.setValue(float(val_dict[name]))
                else:
                    log.error('Unrecognized widget type!')
            else:
                log.warn("Couldn't find GUI element '%s'" % name)
