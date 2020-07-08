
from match_sim.gui.template import TemplatePanel, TemplateButton

import sys
import os
import pathlib
path = pathlib.Path(__file__).parent.absolute()

import wx

from match_sim.gui.graphics import PaintPanel, Colour
import match_sim.default as default

class MyTarget(wx.TextDropTarget):
 def __init__(self, obj):
  wx.TextDropTarget.__init__(self)
  self.object = obj

 def OnDropText(self, x, y, data):
  self.object.InsertItem(0, data)
  return True

class PlayerTarget(MyTarget):
  def __init__(self, obj, pos, team):
    super().__init__(self)
    self.pos = pos
    self.team = team

  def OnDropText(self, x, y, data):
    player_n = int(data.split(' ')[0])
    for player in self.team:
      if player.match.lineup == self.pos:
        player.set_lineup(player_n)
    text_n = ' '.join(data.split(' ')[1:])
    for player in self.team:
      if player.match.lineup == player_n:
        if str(player) == text_n:
          player.set_lineup(self.pos)
    return True

class MatchPlayerTarget(PlayerTarget):
  def OnDropText(self, x, y, data):
    new_lineup = int(data.split(' ')[0])
    new_name = ' '.join(data.split(' ')[1:])
    if (new_lineup in self.team.formation.playing_lineups) and (self.pos in self.team.formation.playing_lineups):
      return False
    if (new_lineup not in self.team.formation.playing_lineups) and (self.pos not in self.team.formation.playing_lineups):
      return False
    if self.pos in self.team.formation.playing_lineups:
      # dragged player coming on
      for player in self.team.playing:
        if player.match.lineup == self.pos:
          self.team.playing.remove(player)
          player.set_lineup(0)
      for player in self.team.subs:
        if player.match.lineup == new_lineup:
          if str(player) == new_name:
            self.team.playing.append(player)
            self.team.subs.remove(player)
      self.team.formation.ammend_pos_lineups(self.pos, new_lineup)
    else:
      # dragged player coming on
      for player in self.team.subs:
        if player.match.lineup == self.pos:
          self.team.playing.append(player)
          self.team.subs.remove(player)
      for player in self.team.playing:
        if player.match.lineup == new_lineup:
          if str(player) == new_name:
            self.team.playing.remove(player)
            player.set_lineup(0)
      self.team.formation.ammend_pos_lineups(new_lineup, self.pos)
    self.team.update_playing_positions()
    return True

class ReservesTarget(PlayerTarget):
  def OnDropText(self, x, y, data):
    player_n = int(data.split(' ')[0])
    text_n = ' '.join(data.split(' ')[1:])
    for player in self.team:
      if player.match.lineup == player_n:
        if player.match.lineup > -1:
          if str(player) == text_n:
            player.set_lineup(0)
    return True

class ManagePanel(PaintPanel):
  def __init__(self, parent, x0=None, y0=None):
    super().__init__(parent, x0, y0)
    colour = Colour()
    font = wx.Font(18, wx.DECORATIVE, wx.BOLD, wx.NORMAL)
    label_size = wx.Size(200, 50)
    self.test_button.Destroy()
    self.training_button = TemplateButton(self, 'Training')
    self.training_button.Bind(wx.EVT_BUTTON, self.on_training)
    self.hbox3.Add(self.training_button)
    self.team = self.GetParent().game.teams[self.GetParent().game.team]
    # self.lineups = {}
    self.vbox1 = wx.BoxSizer(wx.VERTICAL)
    label = wx.StaticText(self, label='Starting Lineup:', size=label_size)
    label.SetFont(font)
    label.SetForegroundColour(colour.BL)
    label.SetBackgroundColour(colour.LIME)
    self.vbox1.Add(label, proportion=0)
    self.hbox1.Add(self.vbox1, flag=wx.EXPAND)
    self.vbox2 = wx.BoxSizer(wx.VERTICAL)
    label = wx.StaticText(self, label='Substitutes:', size=label_size)
    label.SetFont(font)
    label.SetForegroundColour(colour.BL)
    label.SetBackgroundColour(colour.LIME)
    self.vbox2.Add(label, proportion=0)
    self.hbox1.Add(self.vbox2, flag=wx.EXPAND)
    self.vbox3 = wx.BoxSizer(wx.VERTICAL)
    label = wx.StaticText(self, label='Reserves:', size=label_size)
    label.SetFont(font)
    label.SetForegroundColour(colour.BL)
    label.SetBackgroundColour(colour.LIME)
    self.vbox3.Add(label, proportion=0)
    self.hbox1.Add(self.vbox3, flag=wx.EXPAND)
    self.lineups = {}
    self.targets = {}
    for i in range(1, 16):
      self.lineups[i] = wx.ListCtrl(self, -1, style=wx.LC_LIST, size=wx.Size(50, 28))
      self.targets[i] = PlayerTarget(self.lineups[i], i, self.team)
      self.lineups[i].SetDropTarget(self.targets[i])
      self.vbox1.Add(self.lineups[i], proportion=0, flag=wx.EXPAND)
    for i in range(16, 22):
      self.lineups[i] = wx.ListCtrl(self, -1, style=wx.LC_LIST, size=wx.Size(50, 28))
      self.targets[i] = PlayerTarget(self.lineups[i], i, self.team)
      self.lineups[i].SetDropTarget(self.targets[i])
      self.vbox2.Add(self.lineups[i], proportion=0, flag=wx.EXPAND)
    self.reserves = wx.ListCtrl(self, -1, style=wx.LC_LIST|wx.LC_SORT_ASCENDING)
    self.update_lists()
    self.vbox3.Add(self.reserves, proportion=1, flag=wx.EXPAND)
    self.reserves_t = ReservesTarget(self.reserves, 0, self.team)
    self.reserves.SetDropTarget(self.reserves_t)
    self.Bind(wx.EVT_LIST_BEGIN_DRAG, self.make_a_sub)
    self.formation = wx.ComboBox(self, choices=default.formations)
    self.formation.SetStringSelection(self.team.formation.nlist)
    self.formation.Bind(wx.EVT_COMBOBOX, self.update_formation)
    label = wx.StaticText(self, label='Choose Formation:', size=label_size)
    label.SetFont(font)
    label.SetForegroundColour(colour.BL)
    label.SetBackgroundColour(colour.LIME)
    self.vbox2.Add(label, proportion=0)
    self.vbox2.Add(self.formation)
    self.tactics = wx.ComboBox(self, choices=default.tactics)
    self.tactics.SetStringSelection(self.team.tactics.tactics)
    self.tactics.Bind(wx.EVT_COMBOBOX, self.update_tactics)
    label = wx.StaticText(self, label='Choose Tactics:', size=label_size)
    label.SetFont(font)
    label.SetForegroundColour(colour.BL)
    label.SetBackgroundColour(colour.LIME)
    self.vbox2.Add(label, proportion=0)
    self.vbox2.Add(self.tactics)
    self.refresh()

  def on_training(self, event):
    self.GetParent().on_training(TrainingPanel)

  def make_a_sub(self, event):
    text = event.GetText()
    text_n = int(text.split(' ')[0])
    if text_n > 0:
      src = wx.DropSource(self.lineups[text_n])
    else:
      src = wx.DropSource(self.reserves)
    tobj = wx.TextDataObject(text)
    src.SetData(tobj)
    src.DoDragDrop(True)
    self.refresh()

  def update_formation(self, event):
    self.team.formation_change(self.formation.GetValue())
    self.refresh()

  def update_tactics(self, event):
    self.team.tactics_change(self.tactics.GetValue())
    self.refresh()

  def update_lists(self):
    for i in range(1, 22):
      self.lineups[i].ClearAll()
    self.reserves.ClearAll()
    for player in self.team:
      if player.match.lineup > 0:
        self.lineups[player.match.lineup].InsertItem(0, '{0} {1}'.format(player.match.lineup, player))
      else:
        self.reserves.InsertItem(0, '{0} {1}'.format(player.match.lineup, player))

  def refresh(self):
    self.update_lists()
    self.team.update_playing_positions()
    self.draw_lineup()

  def draw_lineup(self):
    dc = wx.ClientDC(self)
    self.draw_pitch(dc, self.team.name)
    for i in range(1, 22):
      players = [p for p in self.team if p.match.lineup == i]
      if len(players) > 0:
        player = players[0]
        x, y = self.team.formation.get_coords(i)
        self.draw_player(player, dc, x=x, y=y, colour_p=self.team.colour.home_p, colour_s=self.team.colour.home_s) 

class MatchManagePanel(ManagePanel):
  def __init__(self, parent, x0=None, y0=None):
    super().__init__(parent, x0, y0)
    self.training_button.Destroy()
    self.vbox3.Clear(True)
    # self.hbox1.Remove(self.vbox3)
    self.txt_output = wx.StaticText(self)
    self.vbox3.Add(self.txt_output)
    self.exit_button.SetLabel('Continue')
    for i in range(1, 16):
      self.targets[i] = MatchPlayerTarget(self.lineups[i], i, self.team)
      self.lineups[i].SetDropTarget(self.targets[i])
    for i in range(16, 22):
      self.targets[i] = MatchPlayerTarget(self.lineups[i], i, self.team)
      self.lineups[i].SetDropTarget(self.targets[i])

  def make_a_sub(self, event):
    text = event.GetText()
    text_n = int(text.split(' ')[0])
    src = wx.DropSource(self.lineups[text_n])
    tobj = wx.TextDataObject(text)
    src.SetData(tobj)
    src.DoDragDrop(True)
    self.refresh()

  def update_lists(self):
    for i in range(1, 22):
      self.lineups[i].ClearAll()
    i = 0
    for j in self.team.formation.playing_lineups:
      i += 1
      for player in self.team.playing:
        if player.match.lineup == j:
          self.lineups[i].InsertItem(0, '{0} {1}'.format(player.match.lineup, player))
    for player in self.team.subs:
      if player.match.lineup > 0:
        self.lineups[player.match.lineup].InsertItem(0, '{0} {1}'.format(player.match.lineup, player))

class TrainingPanel(TemplatePanel):
  def __init__(self, parent):
    super().__init__(parent)

if __name__ == "__main__":

  app = wx.App(False)
  frame = DefaultFrame()
  panel = ManagePanel(frame)
  frame.sizer.Add(panel, 1, wx.EXPAND)
  frame.SetSizer(self.sizer)
  app.MainLoop()
