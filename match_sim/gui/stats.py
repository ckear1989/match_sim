
import wx

class StatsPanel(wx.Panel):
  def __init__(self, parent):
    super().__init__(parent)
    self.SetBackgroundColour('#4f5049')
    main_sizer = wx.BoxSizer(wx.VERTICAL)

    hbox1 = wx.BoxSizer()
    self.txt_output = wx.TextCtrl(self,
      style=wx.TE_MULTILINE|wx.BORDER_SUNKEN|wx.TE_READONLY|wx.TE_RICH2, size=(400,200))
    self.currently_showing = ''
    self.txt_output.AppendText(str(self.currently_showing))
    hbox1.Add(self.txt_output, proportion=1, flag=wx.EXPAND)
    main_sizer.Add(hbox1, proportion=2, flag=wx.ALL|wx.EXPAND, border=20)

    hbox2 = wx.BoxSizer(wx.HORIZONTAL)
    self.exit_button = wx.Button(self, label='Exit')
    hbox2.Add(self.exit_button, 1, wx.LEFT | wx.BOTTOM, 5)

    main_sizer.Add(hbox2, proportion=0, flag=wx.LEFT|wx.BOTTOM, border=10)
    self.SetSizer(main_sizer)
