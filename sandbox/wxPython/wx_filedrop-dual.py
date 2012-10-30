#!/usr/bin/python

# filedrop.py

import wx

class FileDrop(wx.FileDropTarget):
    def __init__(self, window):
        wx.FileDropTarget.__init__(self)
        self.window = window

    def OnDropFiles(self, x, y, filenames):

        for name in filenames:
            try:
                file = open(name, 'r')
                text = file.read()
                self.window.WriteText(text)
                file.close()
            except IOError, error:
                dlg = wx.MessageDialog(None, 'Error opening file\n' + str(error))
                dlg.ShowModal()
            except UnicodeDecodeError, error:
                dlg = wx.MessageDialog(None, 'Cannot open non ascii files\n' \
                    + str(error))
                dlg.ShowModal()

class DropFile(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, size = (450, 400))

        panel = wx.Panel(self)
        panel.SetBackgroundColour('#4f5049')

        vbox = wx.BoxSizer(wx.VERTICAL)

        self.text1 = wx.TextCtrl(panel, -1, style = wx.TE_MULTILINE)
        self.text2 = wx.TextCtrl(panel, -1, style = wx.TE_MULTILINE)

        vbox.Add(self.text1, 1, wx.EXPAND | wx.BOTTOM, 3)
        vbox.Add(self.text2, 1, wx.EXPAND | wx.TOP, 3)
        panel.SetSizer(vbox)

        dt1 = FileDrop(self.text1)
        dt2 = FileDrop(self.text2)
        self.text1.SetDropTarget(dt1)
        self.text2.SetDropTarget(dt2)
        self.Centre()
        self.Show(True)


app = wx.App()
DropFile(None, -1, 'filedrop.py')
app.MainLoop()
