#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Helper functions for PyQt related stuff.
"""

from PyQt4 import QtGui

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
