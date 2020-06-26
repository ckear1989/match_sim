
import datetime

import wx

from match_sim.cl.game import Game as ClGame
from match_sim.gui.template import TemplatePanel, TemplateButton
from match_sim.gui.inbox import Inbox
from match_sim.gui.settings import Settings

class GamePanel(TemplatePanel):
  def __init__(self, parent, game):
    super().__init__(parent)
    self.game = game
    self.txt_output.AppendText(str(self.game))
    continue_button = TemplateButton(self, 'Continue')
    continue_button.Bind(wx.EVT_BUTTON, self.on_continue)
    self.hbox3.Add(continue_button, proportion=0)
    inbox_button = TemplateButton(self, 'Inbox[{0}]'.format(self.game.inbox.count))
    inbox_button.Bind(wx.EVT_BUTTON, self.GetParent().on_inbox)
    self.hbox3.Add(inbox_button, proportion=0, )
    manage_button = TemplateButton(self, 'Manage')
    manage_button.Bind(wx.EVT_BUTTON, self.GetParent().on_manage)
    self.hbox3.Add(manage_button, proportion=0)
    stats_button = TemplateButton(self, 'Stats')
    stats_button.Bind(wx.EVT_BUTTON, self.GetParent().on_stats)
    self.hbox3.Add(stats_button, proportion=0)
    settings_button = TemplateButton(self, 'Settings')
    settings_button.Bind(wx.EVT_BUTTON, self.get_settings)
    self.hbox3.Add(settings_button, proportion=0)
    save_button = TemplateButton(self, 'Save')
    save_button.Bind(wx.EVT_BUTTON, self.save_game)
    self.hbox3.Add(save_button, proportion=0)
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
