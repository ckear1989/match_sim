
import pathlib
path = pathlib.Path(__file__).parent.absolute()

import wx

class TemplatePanel(wx.Panel):
  def __init__(self, parent):
    super().__init__(parent)
    self.SetBackgroundColour('#4f5049')
    self.main_sizer = wx.BoxSizer(wx.VERTICAL)

    self.hbox1 = wx.BoxSizer()
    self.txt_output = wx.TextCtrl(self,
      style=wx.TE_MULTILINE|wx.BORDER_SUNKEN|wx.TE_READONLY|wx.TE_RICH2, size=(400,200))
    self.currently_showing = ''
    self.txt_output.AppendText(str(self.currently_showing))
    self.hbox1.Add(self.txt_output, proportion=1, flag=wx.EXPAND)
    self.main_sizer.Add(self.hbox1, proportion=2, flag=wx.ALL|wx.EXPAND, border=20)

    self.hbox2 = wx.BoxSizer(wx.HORIZONTAL)
    self.exit_button = wx.Button(self, label='Exit')
    self.hbox2.Add(self.exit_button, 1, wx.RIGHT|wx.BOTTOM, 5)

    self.main_sizer.Add(self.hbox2, proportion=0, flag=wx.RIGHT|wx.BOTTOM, border=10)
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
    bmp = wx.Bitmap('{0}/../data/image/puma-40-20-artificial-grass-2.jpg'.format(path))
    dc.DrawBitmap(bmp, 0, 0)

