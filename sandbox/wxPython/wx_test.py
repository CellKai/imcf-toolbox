#!/usr/bin/python

import wx
app = wx.App()

frame = wx.Frame(None, -1, 'window title', size=(250,250))
frame.Center()
frame.Show()
app.MainLoop()

