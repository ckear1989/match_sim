
from match_sim.reporting.inbox import Inbox as ClInbox

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
    self.currently_showing = self.game.inbox.msg
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
    self.game.inbox.get_read()
    self.txt_output.Clear()
    self.txt_output.AppendText(self.game.inbox.msg)

  def on_unread(self, event):
    self.game.inbox.get_unread()
    self.txt_output.Clear()
    self.txt_output.AppendText(self.game.inbox.msg)

  def on_next(self, event):
    self.game.inbox.get_next()
    self.txt_output.Clear()
    self.txt_output.AppendText(self.game.inbox.msg)

class Inbox(ClInbox):
  def __init__(self, team):
    super().__init__(team)
    self.current_folder = self.messages['unread']
    self.msg = str(self.current_folder) + '\n' + str(self.messages['read'])
    self.index = -1

  def get_read(self):
    self.index = -1
    self.current_folder = self.messages['read']
    self.msg = str(self.current_folder)
    if len(self.current_folder) == 0:
      self.msg = 'No more read emails'

  def get_unread(self):
    self.index = -1
    self.current_folder = self.messages['unread']
    self.msg = str(self.current_folder)
    if len(self.current_folder) == 0:
      self.msg = 'No more unread emails'

  def get_next(self):
    if self.current_folder == self.messages['unread']:
      if len(self.current_folder) > 0:
        self.msg = self.messages['unread'].pop(0)
        self.messages['read'].append(self.msg)
        self.update_count()
      else:
        self.msg = 'No unread emails'
    else:
      self.index += 1
      if len(self.current_folder) > self.index:
        self.msg = self.current_folder[self.index]
      else:
        self.msg = 'No more read emails'
