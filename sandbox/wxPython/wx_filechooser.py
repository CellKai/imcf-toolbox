#!/usr/bin/python

import wx
import os


class FileChooser(object):

    def __init__(self, title='', path='', wcd=''):
        self.title = 'Select file'
        self.wcd = 'All files (*.*)|*.*'
        self.path = os.getcwd()
        if title != '':
            self.title = title
        if wcd != '':
            self.wcd = wcd
        if path != '':
            self.path = path

    def get_path(self):
        self.dialog = wx.FileDialog(None, self.title, \
            self.path, '', self.wcd, wx.OPEN)
        if self.dialog.ShowModal() == wx.ID_OK:
            return self.dialog.GetPath()
        self.dialog.Destroy()
