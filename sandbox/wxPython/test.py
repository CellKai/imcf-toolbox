#!/usr/bin/python

import wx
from wx_filechooser import FileChooser

app = wx.PySimpleApp()

fcd = FileChooser()
print fcd.get_path()
