
import datetime

import wx

from match_sim.cl.game import Game as ClGame
from match_sim.gui.template import TemplatePanel, TemplateButton
from match_sim.gui.inbox import InboxPanel, Inbox
from match_sim.gui.manage import ManagePanel
from match_sim.gui.stats import StatsPanel
from match_sim.gui.settings import SettingsPanel, Settings

class GamePanel(TemplatePanel):
  def __init__(self, parent):
    super().__init__(parent)
    self.game = self.GetParent().game
    self.txt_output.AppendText(str(self.game))
    continue_button = TemplateButton(self, 'Continue')
    continue_button.Bind(wx.EVT_BUTTON, self.on_continue)
    self.hbox3.Add(continue_button, proportion=0)
    inbox_button = TemplateButton(self, 'Inbox[{0}]'.format(self.game.inbox.count))
    inbox_button.Bind(wx.EVT_BUTTON, self.on_inbox)
    self.hbox3.Add(inbox_button, proportion=0, )
    manage_button = TemplateButton(self, 'Manage')
    manage_button.Bind(wx.EVT_BUTTON, self.on_manage)
    self.hbox3.Add(manage_button, proportion=0)
    stats_button = TemplateButton(self, 'Stats')
    stats_button.Bind(wx.EVT_BUTTON, self.on_stats)
    self.hbox3.Add(stats_button, proportion=0)
    settings_button = TemplateButton(self, 'Settings')
    settings_button.Bind(wx.EVT_BUTTON, self.on_settings)
    self.hbox3.Add(settings_button, proportion=0)
    save_button = TemplateButton(self, 'Save')
    save_button.Bind(wx.EVT_BUTTON, self.save_game)
    self.hbox3.Add(save_button, proportion=0)
    self.SetSizer(self.main_sizer)

  def on_inbox(self, event):
    self.GetParent().on_inbox(InboxPanel)

  def on_manage(self, event):
    self.GetParent().on_manage(ManagePanel)

  def on_stats(self, event):
    self.GetParent().on_stats(StatsPanel)

  def on_settings(self, event):
    self.GetParent().on_settings(SettingsPanel)

  def save_game(self, event):
    self.game.save()

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
