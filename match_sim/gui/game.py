
import datetime
import random

import dill as pickle
import names
import wx
import wx.grid

from match_sim.cl.game import Game as ClGame
import match_sim.cl.default as default
from match_sim.cl.training import Training
from match_sim.gui.graphics import Colour
from match_sim.gui.inbox import InboxPanel, Inbox
from match_sim.gui.manage import ManagePanel
from match_sim.gui.match import MatchPanel, Match
from match_sim.gui.stats import StatsPanel
from match_sim.gui.settings import SettingsPanel, Settings
from match_sim.gui.team import Team
from match_sim.gui.template import TemplatePanel, TemplateButton
from match_sim.gui.utils import ptable_to_grid

class GamePanel(TemplatePanel):
  def __init__(self, parent):
    super().__init__(parent)
    self.game = self.GetParent().game
    self.match_logs = {}
    self.txt_output.Destroy()
    self.vbox1 = wx.BoxSizer(wx.VERTICAL)
    self.vbox2 = wx.BoxSizer(wx.VERTICAL)
    self.hbox1.Add(self.vbox1, flag=wx.ALL, border=5)
    self.hbox1.Add(self.vbox2, flag=wx.ALL, border=5)
    self.create_tables()
    continue_button = TemplateButton(self, 'Continue')
    continue_button.Bind(wx.EVT_BUTTON, self.on_continue)
    self.hbox3.Add(continue_button, proportion=0)
    self.inbox_button = TemplateButton(self, 'Inbox[{0}]'.format(self.game.inbox.count))
    self.inbox_button.Bind(wx.EVT_BUTTON, self.on_inbox)
    self.hbox3.Add(self.inbox_button, proportion=0)
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
    self.game.current_date += datetime.timedelta(1)
    self.game.process_teams_daily()
    self.process_fixtures_daily()
    self.game.update_next_fixture()
    self.refresh(event)

  def create_tables(self):
    font = wx.Font(16, wx.ROMAN, wx.ITALIC, wx.NORMAL) 
    colour = Colour()
    label_size = wx.Size((200, 28))
    self.events = ptable_to_grid(self, self.game.upcoming_events)
    self.label1 = wx.StaticText(self, size=label_size)
    self.label1.SetFont(font)
    self.label1.SetForegroundColour(colour.BL)
    self.label1.SetBackgroundColour(colour.LIME)
    self.label1.SetLabel('Upcoming Events')
    self.label2 = wx.StaticText(self, size=label_size)
    self.label2.SetFont(font)
    self.label2.SetForegroundColour(colour.BL)
    self.label2.SetBackgroundColour(colour.LIME)
    self.label2.SetLabel('{0} Table'.format(self.game.team_league.name))
    self.label3 = wx.StaticText(self, size=label_size)
    self.label3.SetFont(font)
    self.label3.SetForegroundColour(colour.BL)
    self.label3.SetBackgroundColour(colour.LIME)
    self.label3.SetLabel('Team Status')
    self.vbox1.Add(self.label1, flag=wx.ALL, border=5)
    self.vbox1.Add(self.events, flag=wx.ALL, border=5)
    self.league_table = ptable_to_grid(self, self.game.team_league.league_table)
    self.vbox1.Add(self.label2, flag=wx.ALL, border=5)
    self.vbox1.Add(self.league_table, flag=wx.ALL, border=5)
    self.team = ptable_to_grid(self, self.game.teams[self.game.team].player_table)
    self.team.DeleteCols(5, 5)
    self.team.DeleteCols(8, 2)
    self.vbox2.Add(self.label3, flag=wx.ALL, border=5)
    self.vbox2.Add(self.team, flag=wx.ALL, border=5)
    self.Layout()

  def refresh(self, event):
    self.inbox_button.SetLabel('Inbox[{0}]'.format(self.game.inbox.count))
    self.events.Destroy()
    self.league_table.Destroy()
    self.team.Destroy()
    self.label1.Destroy()
    self.label2.Destroy()
    self.label3.Destroy()
    self.create_tables()

  def process_fixtures_daily(self):
    '''Get today\'s fixtures.  Iteratively play eatch game.'''
    if self.game.current_date == self.game.next_fixture_date:
      self.match_logs[self.game.current_date] = []
      fixtures = self.game.fixtures[self.game.current_date]
      if len(fixtures) > 1:
        if self.game.team in fixtures[-1]:
          self.progress = wx.ProgressDialog('Processing games', "please wait", parent=self, style=wx.PD_SMOOTH)
          for match_t in fixtures[:-1]:
            self.process_match_tuple(match_t)
          next_match_t = fixtures[-1]
          self.progress.Destroy()
          self.process_match_tuple(next_match_t)
        else:
          for match_t in fixtures:
            self.process_match_tuple(match_t)
      else:
        for match_t in fixtures:
          self.process_match_tuple(match_t)

  def process_match_tuple(self, match_t):
    '''Determine match arguments.  Play match.'''
    silent = False
    time_step = 1/self.game.settings.match_speed
    if self.game.settings.match_speed == 70:
      time_step = 0
    if self.game.team not in match_t:
      silent = True
      time_step = 0
    extra_time_required = False
    if 'replay' in match_t[2]:
      extra_time_required = True
    match = Match(self.game.teams[match_t[0]], self.game.teams[match_t[1]],
      self.game.current_date, silent, extra_time_required, match_t[2], self.GetEventHandler(), time_step)
    if silent is True:
      for ts in match.play(0):
        pass
      self.match_logs[self.game.current_date].append(match.report)
      self.game.process_match_result(match, match.comp_name)
      self.game.update_next_fixture()
    else:
      self.GetParent().on_match(MatchPanel, match, self.match_logs[self.game.current_date])
    self.game.inbox.add_match_message(match)

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

  def get_teams(self):
    '''Create teams from random data.  Instantiate competitions'''
    self.teams = {}
    for team in default.poss_teams:
      if team == self.team:
        self.teams[team] = Team(team, self.manager, control=True)
      else:
        self.teams[team] = Team(team, names.get_full_name())
        self.teams[team].training = Training(self.current_date, [0, 2, 4], ['fi', 'pa', 'sh'])
    n_teams = len(self.teams.keys())
    poss_teams = random.sample(self.teams.keys(), n_teams)
    teams_per_div = int(n_teams / 4)
    teams1 = poss_teams[:teams_per_div]
    teams2 = poss_teams[teams_per_div:(teams_per_div*2)]
    teams3 = poss_teams[(teams_per_div*2):(teams_per_div*3)]
    teams4 = poss_teams[(teams_per_div*3):]
    self.init_competitions(teams1, teams2, teams3, teams4)

  def save(self):
    with open(self.save_file, 'wb') as f:
      pickle.dump(self, f)
      # debug failed save
      # for key, value in self.__dict__.items():
      #   print(key)
      #   pickle.dump(value, f)
