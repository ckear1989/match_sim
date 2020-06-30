
import datetime

import wx
import wx.grid

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
    self.txt_output.Destroy()
    self.vbox1 = wx.BoxSizer(wx.VERTICAL)
    self.vbox2 = wx.BoxSizer(wx.VERTICAL)
    self.hbox1.Add(self.vbox1, flag=wx.ALL, border=5)
    self.hbox1.Add(self.vbox2, flag=wx.ALL, border=5)
    self.create_tables()
    continue_button = TemplateButton(self, 'Continue')
    continue_button.Bind(wx.EVT_BUTTON, self.on_continue)
    self.hbox3.Add(continue_button, proportion=0)
    inbox_button = TemplateButton(self, 'Inbox[{0}]'.format(self.game.inbox.count))
    inbox_button.Bind(wx.EVT_BUTTON, self.on_inbox)
    self.hbox3.Add(inbox_button, proportion=0)
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

  def ptable_to_grid(self, atable):
    x = wx.grid.Grid(self)
    rows = atable._rows
    cols = atable._field_names
    x.CreateGrid(len(rows), len(cols))
    i = 0
    j = 0
    G = "\033[0;32;40m" # Green
    N = "\033[0m" # Reset
    for col in cols:
      x.SetColLabelValue(j, str(col))
      j += 1
    i = 0
    for arow in rows:
      j = 0
      for acol in arow:
        x.SetCellValue(i, j, str(acol).replace(G, '').replace(N, ''))
        x.SetReadOnly(i, j)
        j += 1
      i += 1
    x.HideRowLabels()
    return x

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
    self.refresh(event)

  def create_tables(self):
    self.events = self.ptable_to_grid(self.game.upcoming_events)
    self.vbox1.Add(self.events, flag=wx.ALL, border=5)
    self.league_table = self.ptable_to_grid(self.game.team_league.league_table)
    self.vbox1.Add(self.league_table, flag=wx.ALL, border=5)
    self.team = self.ptable_to_grid(self.game.teams[self.game.team].player_table)
    self.team.DeleteCols(5, 5)
    self.team.DeleteCols(8, 2)
    self.vbox2.Add(self.team, flag=wx.ALL, border=5)
    self.Layout()

  def refresh(self, event):
    # self.events.SetTable(self.ptable_to_grid(self.game.upcoming_events))
    # self.league_table.SetTable(self.ptable_to_grid(self.game.team_league.league_table))
    # self.team.SetTable(self.ptable_to_grid(self.game.teams[self.game.team].player_table))
    self.events.Destroy()
    self.league_table.Destroy()
    self.team.Destroy()
    self.create_tables()

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
