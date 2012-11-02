#!/usr/bin/python

import os
import wx
from wx_filechooser import FileChooser

app = wx.PySimpleApp()

fcd = FileChooser()
file1 = fcd.get_path()
print os.path.dirname(file1)
print os.path.basename(file1)
