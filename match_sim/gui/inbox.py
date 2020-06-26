
import wx

from match_sim.gui.template import TemplatePanel
from match_sim.reporting.inbox import Inbox as ClInbox

class InboxPanel(TemplatePanel):
  def __init__(self, parent, game):
    super().__init__(parent)
    self.game = game
    self.currently_showing = self.game.inbox.msg
    self.txt_output.AppendText(str(self.currently_showing))
    read_button = wx.Button(self, label='Read')
    read_button.Bind(wx.EVT_BUTTON, self.on_read)
    self.hbox2.Add(read_button, 1, wx.LEFT | wx.BOTTOM, 5)
    unread_button = wx.Button(self, label='Unread')
    unread_button.Bind(wx.EVT_BUTTON, self.on_unread)
    self.hbox2.Add(unread_button, 1, wx.LEFT | wx.BOTTOM, 5)
    next_button = wx.Button(self, label='Next')
    next_button.Bind(wx.EVT_BUTTON, self.on_next)
    self.hbox2.Add(next_button, 1, wx.LEFT | wx.BOTTOM, 5)
    self.SetSizer(self.main_sizer)

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
