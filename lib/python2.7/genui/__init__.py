#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Helper functions for PyQt related stuff.
"""

from genui.generic_window import GenericMainWindow

import argparse
from PyQt4 import QtGui


def parse_presets(input_string=None):
    """Parse commandline arguments for preset values.

    Check the commandline for a '--preset' argument and assemble a dict from
    the string found there. Each section of the preset-string has to have the
    form "gui_element_name=desired_value" (without the quotes), multiple
    sections can be appended by using a comma (,) as separator.

    The generated dictionary is intended for being used with
    GenericMainWindow.preset_fields().

    Returns
    -------
    presets : dict
        A dictionary of the key-value mappings parsed from the commandline.

    Example
    -------
    >>> preset_string = ['--preset',
    ...     'le_file_1=/path/to/file1,le_file_2=/other/path/for/file2']
    >>> parse_presets(preset_string)
    {'le_file_2': '/other/path/for/file2', 'le_file_1': '/path/to/file1'}
    """
    argparser = argparse.ArgumentParser(description=__doc__)
    argparser.add_argument('-p', '--preset', required=False,
        help='Prefill fields with values in this list.')
    try:
        args = argparser.parse_args(input_string)
    except IOError as err:
        argparser.error(str(err))
    if args.preset != None:
        presets = {}
        for item in args.preset.split(','):
            key, val = item.split('=')
            presets[key] = val
        return presets
    else:
        return None


def fopen(element, cap=None, directory='', ffilter=''):
    """Show file open dialog and update an element's text with the result.

    Provides a callback function for usage with "Browse" buttons or similar in
    a PyQt GUI. It displays the system's file selection dialog and lets the
    user select an existing file for opening it later on.

    Its purpose is the elimination of separate callback functions for each
    slot, resulting in many more or less identical code segments. To use it
    with Qt's connect() method, a lambda function must be used there, e.g.

    >>> connect(btn, sig, lambda elt=self.line_edit: fopen(elt))
    ... # doctest: +SKIP
    """
    if cap is None:
        cap = 'Open File'
    element.setText(QtGui.QFileDialog.getOpenFileName(
        caption=cap, directory=directory, filter=ffilter))


def fsave(element, cap=None, directory='', ffilter=''):
    """Show file save dialog and update an element's text with the result.

    Provides a callback function for usage with "Browse" buttons or similar in
    a PyQt GUI. It displays the system's file selection dialog and lets the
    user choose a non-existing file to be used as the target for storing some
    data.

    Its purpose is the elimination of separate callback functions for each
    slot, resulting in many more or less identical code segments. To use it
    with Qt's connect() method, a lambda function must be used there, e.g.

    >>> connect(btn, sig, lambda elt=self.line_edit: fsave(elt))
    ... # doctest: +SKIP
    """
    if cap is None:
        cap = 'Save As'
    element.setText(QtGui.QFileDialog.getSaveFileName(
        caption=cap, directory=directory, filter=ffilter))


def diropen(element, cap=None, directory='', dirsonly=True):
    """Show directory dialog and update an element's text with the result.

    Provides a callback function for usage with "Browse" buttons or similar in
    a PyQt GUI. It displays the system's file selection dialog and lets the
    user choose an existing directory.

    Its purpose is the elimination of separate callback functions for each
    slot, resulting in many more or less identical code segments. To use it
    with Qt's connect() method, a lambda function must be used there, e.g.

    >>> connect(btn, sig, lambda elt=self.line_edit: diropen(elt))
    ... # doctest: +SKIP
    """
    if cap is None:
        cap = 'Select Directory'
    # NOTE: dirsonly has no effect on Linux but it works on Windows
    if dirsonly:
        options = QtGui.QFileDialog.ShowDirsOnly
        element.setText(QtGui.QFileDialog.getExistingDirectory(
            caption=cap, directory=directory, options=options))
    else:
        element.setText(QtGui.QFileDialog.getExistingDirectory(
            caption=cap, directory=directory))


if __name__ == "__main__":
    print('Running doctest on file "%s".' % __file__)
    import doctest
    doctest.testmod()
