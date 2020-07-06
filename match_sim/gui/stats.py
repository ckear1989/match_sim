
import wx

from match_sim.gui.template import TemplatePanel

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
    self.hbox1.Add(self.vbox1)
    self.vbox1.Add(self.comps, proportion=0)
    self.vbox1.Add(self.teams, proportion=0)
    self.vbox1.Add(self.players, proportion=0)

