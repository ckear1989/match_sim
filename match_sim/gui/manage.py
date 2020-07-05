
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
  try:
    self.object.InsertItem(0, data)
  except:
    return False
  return True

class ManagePanel(PaintPanel):
  def __init__(self, parent, x0=600, y0=None):
    super().__init__(parent, x0, y0)
    colour = Colour()
    font = wx.Font(18, wx.DECORATIVE, wx.BOLD, wx.NORMAL)
    label_size = wx.Size(200, 50)
    self.test_button.Destroy()
    training_button = TemplateButton(self, 'Training')
    training_button.Bind(wx.EVT_BUTTON, self.on_training)
    self.hbox3.Add(training_button)
    self.team = self.GetParent().game.teams[self.GetParent().game.team]
    # self.lineups = {}
    self.vbox1 = wx.BoxSizer(wx.VERTICAL)
    label = wx.StaticText(self, label='Starting Lineup:', size=label_size)
    label.SetFont(font)
    label.SetForegroundColour(colour.BL)
    label.SetBackgroundColour(colour.LIME)
    self.vbox1.Add(label, proportion=1)
    self.hbox1.Add(self.vbox1, flag=wx.EXPAND)
    self.vbox2 = wx.BoxSizer(wx.VERTICAL)
    label = wx.StaticText(self, label='Substitutes:', size=label_size)
    label.SetFont(font)
    label.SetForegroundColour(colour.BL)
    label.SetBackgroundColour(colour.LIME)
    self.vbox2.Add(label, proportion=1)
    self.hbox1.Add(self.vbox2, flag=wx.EXPAND)
    self.vbox3 = wx.BoxSizer(wx.VERTICAL)
    label = wx.StaticText(self, label='Reserves:', size=label_size)
    label.SetFont(font)
    label.SetForegroundColour(colour.BL)
    label.SetBackgroundColour(colour.LIME)
    self.vbox3.Add(label, proportion=1)
    self.hbox1.Add(self.vbox3, flag=wx.EXPAND)
    self.starting = wx.ListCtrl(self, -1, style=wx.LC_LIST|wx.LC_SORT_ASCENDING)
    self.subs = wx.ListCtrl(self, -1, style=wx.LC_LIST|wx.LC_SORT_ASCENDING)
    self.reserves = wx.ListCtrl(self, -1, style=wx.LC_LIST|wx.LC_SORT_ASCENDING)
    self.update_lists()
    self.vbox1.Add(self.starting, proportion=1, flag=wx.EXPAND)
    self.vbox2.Add(self.subs, proportion=1, flag=wx.EXPAND)
    self.vbox3.Add(self.reserves, proportion=1, flag=wx.EXPAND)
    self.starting_t = MyTarget(self.starting)
    self.starting.SetDropTarget(self.starting_t)
    self.subs_t = MyTarget(self.subs)
    self.subs.SetDropTarget(self.subs_t)
    self.reserves_t = MyTarget(self.reserves)
    self.reserves.SetDropTarget(self.reserves_t)
    self.Bind(wx.EVT_LIST_BEGIN_DRAG, self.make_a_sub)

    self.formation = wx.ComboBox(self, choices=default.formations)
    self.formation.SetStringSelection(self.team.formation.nlist)
    self.formation.Bind(wx.EVT_COMBOBOX, self.update_formation)
    label = wx.StaticText(self, label='Choose Formation:', size=label_size)
    label.SetFont(font)
    label.SetForegroundColour(colour.BL)
    label.SetBackgroundColour(colour.LIME)
    self.vbox1.Add(label, proportion=1)
    self.vbox1.Add(self.formation)
    self.tactics = wx.ComboBox(self, choices=default.tactics)
    self.tactics.SetStringSelection(self.team.tactics.tactics)
    self.tactics.Bind(wx.EVT_COMBOBOX, self.update_tactics)
    label = wx.StaticText(self, label='Choose Tactics:', size=label_size)
    label.SetFont(font)
    label.SetForegroundColour(colour.BL)
    label.SetBackgroundColour(colour.LIME)
    self.vbox2.Add(label, proportion=1)
    self.vbox2.Add(self.tactics)
    self.refresh()

  def on_training(self, event):
    self.GetParent().on_training(TrainingPanel)

  def make_a_sub(self, event):
    text = event.GetText()
    text_p = int(text.split(' ')[0])
    text_n = ' '.join(text.split(' ')[1:])
    team_lineups = [p.match.lineup for p in self.team]
    for player in self.team:
      if player.match.lineup == text_p:
        if str(player) == text_n:
          this_player = player
          if text_n in range(1, 16):
            src = wx.DropSource(self.starting)
            available_pos = [x for x in range(16, 22) if x not in team_lineups]
            if len(available_pos) > 0:
              available_pos = available_pos[0]
            else:
              available_pos = 0
            this_player.set_lineup(available_pos)
            tobj = wx.TextDataObject(text)
            src.SetData(tobj)
            src.DoDragDrop(True)
            self.starting.DeleteItem(event.GetIndex())
          elif text_n in range(16, 22):
            src = wx.DropSource(self.subs)
            available_pos = [x for x in range(1, 16) if x not in team_lineups]
            if len(available_pos) > 0:
              available_pos = available_pos[0]
            else:
              available_pos = 0
            this_player.set_lineup(available_pos)
            tobj = wx.TextDataObject(text)
            src.SetData(tobj)
            src.DoDragDrop(True)
            self.subs.DeleteItem(event.GetIndex())
          else:
            src = wx.DropSource(self.reserves)
            available_pos = [x for x in range(1, 22) if x not in team_lineups]
            if len(available_pos) > 0:
              available_pos = available_pos[0]
            else:
              available_pos = 0
            this_player.set_lineup(available_pos)
            tobj = wx.TextDataObject(text)
            src.SetData(tobj)
            src.DoDragDrop(True)
            self.starting.DeleteItem(event.GetIndex())
    self.refresh()

  def update_lineups(self, event):
    for i in range(1, 22):
      pname = self.lineups[i].GetValue()
      players = [p for p in self.team if str(p) == pname]
      if len(players) > 0:
        player = players[0]
        player.update_lineup(i)
        self.lineups[i].SetSelection(self.lineups[i].GetSelection())
        self.lineups[i].SetStringSelection(str(player))
        players = [p for p in self.team if p.match.lineup == i]
        for player in players:
          if str(player) != pname:
            player.update_lineup(0)
    self.refresh()

  def update_formation(self, event):
    self.team.formation_change(self.formation.GetValue())
    self.refresh()

  def update_tactics(self, event):
    self.team.tactics_change(self.tactics.GetValue())
    self.refresh()

  def update_lists(self):
    self.starting.ClearAll()
    self.subs.ClearAll()
    self.reserves.ClearAll()
    for player in self.team:
      if player.match.lineup in range(1, 16):
        self.starting.InsertItem(0, '{0} {1}'.format(player.match.lineup, player))
      elif player.match.lineup in range(16, 22):
        self.subs.InsertItem(0, '{0} {1}'.format(player.match.lineup, player))
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
