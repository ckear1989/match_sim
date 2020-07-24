
import wx

from match_sim.gui.template import TemplatePanel
from match_sim.gui.utils import ptable_to_grid

class StatsPanel(TemplatePanel):
  def __init__(self, parent):
    super().__init__(parent)
    self.txt_output.Destroy()
    self.game = self.GetParent().game
    self.comps = wx.ComboBox(self, choices=[x for x in self.game.competitions.keys()])
    self.comps.SetSelection(0)
    comp = self.comps.GetStringSelection()
    self.teams = wx.ComboBox(self, choices=[x for x in self.game.competitions[comp].teams])
    self.teams.SetSelection(0)
    team = self.teams.GetStringSelection()
    self.players = wx.ComboBox(self, choices=[str(x) for x in self.game.teams[team]])
    self.players.SetSelection(0)
    self.vbox1 = wx.BoxSizer(wx.VERTICAL)
    self.vbox2 = wx.BoxSizer(wx.VERTICAL)
    self.hbox1.Add(self.vbox1, flag=wx.ALL, border=5)
    self.hbox1.Add(self.vbox2, proportion=1, flag=wx.ALL, border=5)
    self.vbox1.Add(self.comps, proportion=1)
    self.vbox1.Add(self.teams, proportion=1)
    self.vbox1.Add(self.players, proportion=1)
    self.comps.Bind(wx.EVT_COMBOBOX, self.show_comp)
    self.teams.Bind(wx.EVT_COMBOBOX, self.show_team)
    self.players.Bind(wx.EVT_COMBOBOX, self.show_player)
    self.table = ptable_to_grid(self, self.game.competitions[self.comps.GetStringSelection()].league_table)
    self.vbox2.Add(self.table, proportion=0, flag=wx.ALL, border=5)

  def show_comp(self, event):
    self.refresh(event)
    self.table = ptable_to_grid(self, self.game.competitions[self.comps.GetStringSelection()].league_table)
    self.vbox2.Add(self.table, proportion=0, flag=wx.ALL, border=5)
    self.Layout()
    self.Update()

  def show_team(self, event):
    self.refresh(event)
    self.table = ptable_to_grid(self, self.game.teams[self.teams.GetStringSelection()].player_table, sort_col='lineup')
    self.vbox2.Add(self.table, proportion=0, flag=wx.ALL, border=5)
    self.Layout()
    self.Update()

  def show_player(self, event):
    self.refresh(event)
    player = [x for x in self.game.teams[self.teams.GetStringSelection()] if str(x) == self.players.GetStringSelection()][0]
    player.get_table()
    self.table = ptable_to_grid(self, player.table)
    self.vbox2.Add(self.table, proportion=0, flag=wx.ALL, border=5)
    self.Layout()
    self.Update()

  def refresh(self, event):
    self.table.Destroy()
    self.update_selections()

  def update_selections(self):
    comp = self.comps.GetStringSelection()
    team = self.teams.GetStringSelection()
    player = self.players.GetStringSelection()
    if team not in self.game.competitions[comp].teams:
      self.teams.Destroy()
      self.teams = wx.ComboBox(self, choices=[x for x in self.game.competitions[comp].teams])
      self.teams.SetSelection(0)
      self.vbox1.Add(self.teams, proportion=0)
      self.teams.Bind(wx.EVT_COMBOBOX, self.show_team)
      team = self.teams.GetStringSelection()
    if player not in [str(x) for x in self.game.teams[team]]:
      self.players.Destroy()
      self.players = wx.ComboBox(self, choices=[str(x) for x in self.game.teams[team]])
      self.vbox1.Add(self.players, proportion=0)
      self.players.SetSelection(0)
      self.players.Bind(wx.EVT_COMBOBOX, self.show_player)

