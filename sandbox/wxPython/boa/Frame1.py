#Boa:Frame:Frame1

import wx
import wx.lib.filebrowsebutton

def create(parent):
    return Frame1(parent)

[wxID_FRAME1, wxID_FRAME1FILEBROWSEBUTTON1, 
] = [wx.NewId() for _init_ctrls in range(2)]

class Frame1(wx.Frame):
    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Frame.__init__(self, id=wxID_FRAME1, name='', parent=prnt,
              pos=wx.Point(387, 269), size=wx.Size(400, 250),
              style=wx.DEFAULT_FRAME_STYLE,
              title='File Selection & Processing')
        self.SetClientSize(wx.Size(384, 212))
        self.SetBackgroundStyle(wx.BG_STYLE_SYSTEM)

        self.fileBrowseButton1 = wx.lib.filebrowsebutton.FileBrowseButton(buttonText='Browse',
              dialogTitle='Choose a file', fileMask='*.*',
              id=wxID_FRAME1FILEBROWSEBUTTON1, initialValue='',
              labelText='File Entry:', parent=self, pos=wx.Point(64, 56),
              size=wx.Size(296, 48), startDirectory='.', style=wx.TAB_TRAVERSAL,
              toolTip='Type filename or click browse to choose file')

    def __init__(self, parent):
        self._init_ctrls(parent)
