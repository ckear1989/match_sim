
import datetime

import wx

from match_sim.cl.game import Game as ClGame
from match_sim.gui.template import TemplatePanel
from match_sim.gui.inbox import Inbox
from match_sim.gui.settings import Settings

class GamePanel(TemplatePanel):
  def __init__(self, parent, game):
    super().__init__(parent)
    self.game = game
    self.txt_output.AppendText(str(self.game))
    continue_button = wx.Button(self, label='Continue')
    continue_button.Bind(wx.EVT_BUTTON, self.on_continue)
    self.hbox2.Add(continue_button, 1, wx.LEFT | wx.BOTTOM, 5)
    inbox_button = wx.Button(self, label='Inbox[{0}]'.format(self.game.inbox.count))
    inbox_button.Bind(wx.EVT_BUTTON, self.GetParent().on_inbox)
    self.hbox2.Add(inbox_button, 1, wx.LEFT | wx.BOTTOM, 5)
    manage_button = wx.Button(self, label='Manage')
    manage_button.Bind(wx.EVT_BUTTON, self.GetParent().on_manage)
    self.hbox2.Add(manage_button, 1, wx.LEFT | wx.BOTTOM, 5)
    stats_button = wx.Button(self, label='Stats')
    stats_button.Bind(wx.EVT_BUTTON, self.GetParent().on_stats)
    self.hbox2.Add(stats_button, 1, wx.LEFT | wx.BOTTOM, 5)
    save_button = wx.Button(self, label='Save')
    save_button.Bind(wx.EVT_BUTTON, self.save_game)
    self.hbox2.Add(save_button, 1, wx.LEFT | wx.BOTTOM, 5)
    settings_button = wx.Button(self, label='Settings')
    settings_button.Bind(wx.EVT_BUTTON, self.get_settings)
    self.hbox2.Add(settings_button, 1, wx.LEFT | wx.BOTTOM, 5)
    self.SetSizer(self.main_sizer)

  def save_game(self, event):
    self.game.save()

  def get_settings(self, event):
    self.GetParent().on_settings(event)
    # self.game.settings.get_settings()

  def on_continue(self, event):
    self.game.pcontinue()
    self.insert_text(event)

  def insert_text(self, event):
    self.txt_output.Clear()
    self.txt_output.AppendText(str(self.game))

class Game(ClGame):
  def __init__(self, team, name):
    super().__init__(team, name)
    self.inbox = Inbox(self.teams[self.team])
    self.settings = Settings()

  def pcontinue(self):
    self.current_date += datetime.timedelta(1)
    self.process_teams_daily()
    self.process_fixtures_daily()
    self.update_next_fixture()
