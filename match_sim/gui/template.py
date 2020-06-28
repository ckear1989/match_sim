
import pathlib
path = pathlib.Path(__file__).parent.absolute()

import wx

import match_sim.default as default

class TemplateFrame(wx.Frame):
  def __init__(self):
    super().__init__(parent=None, title='Match Simulator 2020')
    self.sizer = wx.BoxSizer(wx.VERTICAL)
    self.SetSizer(self.sizer)
    self.SetSize((800, 600))
    self.Centre()

class TemplateButton(wx.Button):
  def __init__(self, parent, label):
    super().__init__(parent)
    # self.font = wx.SystemSettings.GetFont(wx.SYS_SYSTEM_FONT)
    # self.font.SetPointSize(15)
    # self.SetFont(self.font)
    png = wx.Image('{0}/../data/image/buttons/new0.png'.format(path), wx.BITMAP_TYPE_ANY)
    w = png.GetWidth() / 5
    h = png.GetHeight() / 5
    png = png.Scale(w, h)
    png = png.ConvertToBitmap()
    png.SetMask(wx.Mask())
    # print(png.GetMask())
    self.SetSize((w+10, h+10))
    self.SetBitmap(png)
    # print(self.GetSize())
    # print(png.GetSize())
    self.SetLabel(label)

class TemplatePanel(wx.Panel):
  def __init__(self, parent):
    super().__init__(parent)
    self.SetBackgroundColour('#4f5049')
    self.main_sizer = wx.BoxSizer(wx.VERTICAL)
    self.font = wx.SystemSettings.GetFont(wx.SYS_SYSTEM_FONT)
    self.font.SetPointSize(15)

    self.hbox1 = wx.BoxSizer()
    self.txt_output = wx.TextCtrl(self,
      style=wx.TE_MULTILINE|wx.BORDER_SUNKEN|wx.TE_READONLY|wx.TE_RICH2, size=(400,200))
    self.currently_showing = ''
    self.txt_output.AppendText(str(self.currently_showing))
    self.hbox1.Add(self.txt_output, proportion=1, flag=wx.EXPAND)
    self.main_sizer.Add(self.hbox1, proportion=2, flag=wx.ALL|wx.EXPAND, border=20)

    self.hbox2 = wx.BoxSizer(wx.HORIZONTAL)
    self.exit_button = TemplateButton(self, 'Exit')
    self.hbox3 = wx.BoxSizer(wx.HORIZONTAL)
    self.hbox4 = wx.BoxSizer()
    self.hbox4.Add(self.exit_button, proportion=0)
    self.hbox2.Add(self.hbox3, proportion=0, flag=wx.TOP|wx.BOTTOM|wx.LEFT, border=5)
    self.hbox2.Add(self.hbox4, proportion=0, flag=wx.TOP|wx.BOTTOM|wx.RIGHT, border=5)

    self.main_sizer.Add(self.hbox2, proportion=0)
    self.SetSizer(self.main_sizer)
    self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)

  def OnEraseBackground(self, evt):
    """
    https://www.blog.pythonlibrary.org/2010/03/18/wxpython-putting-a-background-image-on-a-panel/
    Add a picture to the background
    """
    # yanked from ColourDB.py
    dc = evt.GetDC()
            
    if not dc:
      dc = wx.ClientDC(self)
      rect = self.GetUpdateRegion().GetBox()
      dc.SetClippingRect(rect)
    dc.Clear()
    bmp = wx.Bitmap(default.gui_background)
    dc.DrawBitmap(bmp, 0, 0)

