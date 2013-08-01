#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Helper functions for PyQt related stuff.
"""

from PyQt4 import QtGui


def select_file(element, cap=None, directory='', ffilter=''):
    """Show file open dialog and update an element's text with the result.

    Provides a callback function for usage with "Browse" buttons or similar in
    a PyQt GUI. It displays the system's file selection dialog and lets the
    user select an existing file for opening it later on.

    Its purpose is the elimination of separate callback functions for each
    slot, resulting in many more or less identical code segments. To use it
    with Qt's connect() method, a lambda function must be used there, e.g.

    >>> connect(btn, sig, lambda elt=self.line_edit: select_file(elt))
    """
    if cap is None:
        cap='Open File'
    element.setText(QtGui.QFileDialog.getOpenFileName(
        caption=cap, directory=directory, filter=ffilter))


def select_file_save(element, cap=None, ffilter=''):
    """Show file save dialog and update an element's text with the result.

    Provides a callback function for usage with "Browse" buttons or similar in
    a PyQt GUI. It displays the system's file selection dialog and lets the
    user choose a non-existing file to be used as the target for storing some
    data.

    Its purpose is the elimination of separate callback functions for each
    slot, resulting in many more or less identical code segments. To use it
    with Qt's connect() method, a lambda function must be used there, e.g.

    >>> connect(btn, sig, lambda elt=self.line_edit: select_file(elt))
    """
    if cap is None:
        cap='Save As'
    element.setText(QtGui.QFileDialog.getSaveFileName(
        caption=cap, filter=ffilter))


def select_directory(element, cap=None, directory='', dirsonly=True):
    """Show directory dialog and update an element's text with the result.

    Provides a callback function for usage with "Browse" buttons or similar in
    a PyQt GUI. It displays the system's file selection dialog and lets the
    user choose an existing directory.

    Its purpose is the elimination of separate callback functions for each
    slot, resulting in many more or less identical code segments. To use it
    with Qt's connect() method, a lambda function must be used there, e.g.

    >>> connect(btn, sig, lambda elt=self.line_edit: select_file(elt))
    """
    if cap is None:
        cap='Select Directory'
    # TODO: this has no effect on Linux, test it on Windows and decide whether
    # to keep or discard it:
    if dirsonly:
        options = QtGui.QFileDialog.ShowDirsOnly
        element.setText(QtGui.QFileDialog.getExistingDirectory(
            caption=cap, directory=directory, options=options))
    else:
        element.setText(QtGui.QFileDialog.getExistingDirectory(
            caption=cap, directory=directory))
