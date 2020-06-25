
import wx

class InboxPanel(wx.Panel):
  def __init__(self, parent, game):
    super().__init__(parent)
    self.game = game
    self.SetBackgroundColour('#4f5049')
    main_sizer = wx.BoxSizer(wx.VERTICAL)

    hbox1 = wx.BoxSizer()
    self.txt_output = wx.TextCtrl(self,
      style=wx.TE_MULTILINE|wx.BORDER_SUNKEN|wx.TE_READONLY|wx.TE_RICH2, size=(400,200))
    self.currently_showing = self.game.inbox.messages['unread']
    self.txt_output.AppendText(str(self.currently_showing))
    hbox1.Add(self.txt_output, proportion=1, flag=wx.EXPAND)
    main_sizer.Add(hbox1, proportion=2, flag=wx.ALL|wx.EXPAND, border=20)

    hbox2 = wx.BoxSizer(wx.HORIZONTAL)
    read_button = wx.Button(self, label='Read')
    read_button.Bind(wx.EVT_BUTTON, self.on_read)
    hbox2.Add(read_button, 1, wx.LEFT | wx.BOTTOM, 5)
    unread_button = wx.Button(self, label='Unread')
    unread_button.Bind(wx.EVT_BUTTON, self.on_unread)
    hbox2.Add(unread_button, 1, wx.LEFT | wx.BOTTOM, 5)
    next_button = wx.Button(self, label='Next')
    next_button.Bind(wx.EVT_BUTTON, self.on_next)
    hbox2.Add(next_button, 1, wx.LEFT | wx.BOTTOM, 5)
    self.exit_button = wx.Button(self, label='Exit')
    hbox2.Add(self.exit_button, 1, wx.LEFT | wx.BOTTOM, 5)

    main_sizer.Add(hbox2, proportion=0, flag=wx.LEFT|wx.BOTTOM, border=10)
    self.SetSizer(main_sizer)

  def on_read(self, event):
    self.currently_showing = self.game.inbox.messages['read']
    self.txt_output.Clear()
    self.txt_output.AppendText(str(self.currently_showing))

  def on_unread(self, event):
    self.currently_showing = self.game.inbox.messages['unread']
    self.txt_output.Clear()
    self.txt_output.AppendText(str(self.currently_showing))

  def on_next(self, event):
    self.txt_output.Clear()
    self.txt_output.AppendText(self.currently_showing[0])
    self.game.inbox.update_count()

