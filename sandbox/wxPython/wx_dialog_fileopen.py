#!/usr/bin/python

import wx
import os

app = wx.PySimpleApp()

wildcard = 'PowerShell files (*.ps1)|*.ps1|' \
           'All files (*.*)|*.*'
print wildcard

dlg_fo = wx.FileDialog(None, 'Select input file', \
    os.getcwd(), '', wildcard, wx.OPEN)

if dlg_fo.ShowModal() == wx.ID_OK:
    print dlg_fo.GetPath()

dlg_fo.Destroy()
app.MainLoop()
