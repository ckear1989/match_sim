
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
    self.hbox1.Add(self.vbox2, flag=wx.ALL, border=5)
    self.vbox1.Add(self.comps, proportion=0)
    self.vbox1.Add(self.teams, proportion=0)
    self.vbox1.Add(self.players, proportion=0)
    self.get_tables()
    self.Bind(wx.EVT_COMBOBOX, self.refresh)

  def refresh(self, event):
    self.comp_table.Destroy()
    self.team_table.Destroy()
    # self.player_table.Destroy()
    self.update_selections()
    self.get_tables()

  def update_selections(self):
    comp = self.comps.GetStringSelection()
    team = self.teams.GetStringSelection()
    player = self.players.GetStringSelection()
    if team not in self.game.competitions[comp].teams:
      self.teams.Destroy()
      self.teams = wx.ComboBox(self, choices=[x for x in self.game.competitions[comp].teams])
      self.teams.SetSelection(0)
      self.vbox1.Add(self.teams, proportion=0)
      team = self.teams.GetStringSelection()
    if player not in [str(x) for x in self.game.teams[team]]:
      self.players.Destroy()
      self.players = wx.ComboBox(self, choices=[str(x) for x in self.game.teams[team]])
      self.vbox1.Add(self.players, proportion=0)
      self.players.SetSelection(0)

  def get_tables(self):
    self.comp_table = ptable_to_grid(self, self.game.competitions[self.comps.GetStringSelection()].league_table)
    self.team_table = ptable_to_grid(self, self.game.teams[self.teams.GetStringSelection()].player_table)
    # player_table = ptable_to_grid(self, )
    self.vbox2.Add(self.comp_table, flag=wx.ALL, border=5)
    self.vbox2.Add(self.team_table, flag=wx.ALL, border=5)
    self.Layout()

