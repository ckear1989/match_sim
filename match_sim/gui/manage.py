
from match_sim.gui.template import TemplatePanel, TemplateButton

import sys
import os
import pathlib
path = pathlib.Path(__file__).parent.absolute()

import wx

from match_sim.gui.graphics import PaintPanel, Colour
from match_sim.gui.training import TrainingPanel
import match_sim.cl.default as default

class MyTarget(wx.TextDropTarget):
 def __init__(self, obj):
  wx.TextDropTarget.__init__(self)
  self.object = obj

 def OnDropText(self, x, y, data):
  self.object.InsertItem(0, data)
  return True

class PlayerTarget(MyTarget):
  def __init__(self, obj, lineup, team):
    super().__init__(self)
    self.lineup = lineup
    self.team = team

  def OnDropText(self, x, y, data):
    player_n = int(data.split(' ')[0])
    if player_n > -1:
      for player in self.team:
        if player.match.lineup == self.lineup:
          player.set_lineup(player_n)
      text_n = ' '.join(data.split(' ')[1:])
      for player in self.team:
        if player.match.lineup == player_n:
          if str(player) == text_n:
            player.set_lineup(self.lineup)
    return True

class MatchPlayerTarget(MyTarget):
  def __init__(self, parent, lineup, team):
      MyTarget.__init__(self, parent.lineups[lineup])
      self.parent = parent
      self.lineup = lineup
      self.team = team

  def OnDropText(self, x, y, data):
    self.team.update_playing_positions()
    new_lineup = int(data.split(' ')[0])
    if self.lineup in self.team.formation.playing_lineups.keys():
      current_lineup = self.team.formation.playing_lineups[self.lineup]
      if current_lineup is None:
        print('target off')
        if new_lineup in self.team.formation.playing_lineups.values():
          print('dropped playing')
          self.team.formation.swap_playing_positions_off(new_lineup, current_lineup)
        elif new_lineup in self.team.formation.sub_lineups.values():
          print('dropped sub')
          return False
        elif new_lineup in self.team.formation.off_lineups:
          print('dropped off')
          return False
        else:
          print('target', self.lineup)
          print('target current', current_lineup)
          print('dropped', new_lineup)
          raise Exception('debug sub')
      elif current_lineup in self.team.formation.playing_lineups.values():
        print('target playing', current_lineup)
        if new_lineup in self.team.formation.playing_lineups.values():
          print('dropped playing', new_lineup)
          self.team.formation.swap_playing_positions(current_lineup, new_lineup)
        elif new_lineup in self.team.formation.sub_lineups.values():
          print('dropped sub', new_lineup)
          for player in self.team:
            if player.match.lineup == current_lineup:
              player_off = player
            elif player.match.lineup == new_lineup:
              player_on = player
          dlg = wx.MessageDialog(self.parent, '{0} coming off for {1}'.format(
              player_off, player_on), style=wx.OK|wx.CANCEL)
          resp = dlg.ShowModal()
          if resp == wx.ID_OK:
            self.team.sub_on_off(new_lineup, current_lineup)
            player_off.set_lineup(0)
        elif new_lineup in self.team.formation.off_lineups:
          print('dropped off', new_lineup)
          self.team.formation.swap_playing_positions_off(current_lineup, new_lineup)
        else:
          print('target', self.lineup)
          print('target current', current_lineup)
          print('dropped', new_lineup)
          raise Exception('debug sub')
      elif current_lineup in self.team.formation.sub_lineups.values():
        print('target sub', current_lineup)
        if new_lineup in self.team.formation.playing_lineups.values():
          print('dropped playing', new_lineup)
          for player in self.team:
            if player.match.lineup == current_lineup:
              player_on = player
            elif player.match.lineup == new_lineup:
              player_off = player
          dlg = wx.MessageDialog(self.parent, '{0} coming off for {1}'.format(
            player_off, player_on), style=wx.OK|wx.CANCEL)
          resp = dlg.ShowModal()
          if resp == wx.ID_OK:
            self.team.sub_on_off(current_lineup, new_lineup)
            player_off.set_lineup(0)
        elif new_lineup in self.team.formation.sub_lineups.values():
          print('dropped sub', new_lineup)
          return False
        elif new_lineup in self.team.formation.off_lineups:
          print('dropped off', new_lineup)
          return False
        else:
          print('target', self.lineup)
          print('target current', current_lineup)
          print('dropped', new_lineup)
          raise Exception('debug sub')
    elif self.lineup in self.team.formation.sub_lineups.keys():
      current_lineup = self.team.formation.sub_lineups[self.lineup]
      if current_lineup is not None:
        print('target sub', current_lineup)
        if new_lineup in self.team.formation.playing_lineups.values():
          print('dropped playing', new_lineup)
          for player in self.team:
            if player.match.lineup == current_lineup:
              player_on = player
            elif player.match.lineup == new_lineup:
              player_off = player
          dlg = wx.MessageDialog(self.parent, '{0} coming off for {1}'.format(
            player_off, player_on), style=wx.OK|wx.CANCEL)
          resp = dlg.ShowModal()
          if resp == wx.ID_OK:
            self.team.sub_on_off(current_lineup, new_lineup)
            player_off.set_lineup(0)
        elif new_lineup in self.team.formation.sub_lineups.values():
          print('dropped sub', new_lineup)
          return False
        elif new_lineup in self.team.formation.off_lineups:
          print('dropped off', new_lineup)
          return False
        else:
          print('target', self.lineup)
          print('target current', current_lineup)
          print('dropped', new_lineup)
          raise Exception('debug sub')
      else:
        print('target none')
        return False
    else:
      print('target', self.lineup)
      print('dropped', new_lineup)
      raise Exception('debug sub')  
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
  def __init__(self, parent, team, home=True, x0=None, y0=None):
    self.team = team
    self.home = home
    super().__init__(parent, x0, y0)
    colour = Colour()
    font = wx.Font(18, wx.DECORATIVE, wx.BOLD, wx.NORMAL)
    label_size = wx.Size(200, 28)
    self.test_button.Destroy()
    self.training_button = TemplateButton(self, 'Training')
    self.training_button.Bind(wx.EVT_BUTTON, self.on_training)
    self.hbox3.Add(self.training_button)
    # self.lineups = {}
    self.vbox1 = wx.BoxSizer(wx.VERTICAL)
    self.label1 = wx.StaticText(self, label='Starting Lineup:', size=label_size)
    self.label1.SetFont(font)
    self.label1.SetForegroundColour(colour.BL)
    self.label1.SetBackgroundColour(colour.LIME)
    self.vbox1.Add(self.label1, proportion=0)
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
    self.reserves = wx.ListCtrl(self, -1, style=wx.LC_LIST|wx.LC_SORT_ASCENDING, size=wx.Size(50, 280))
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
    self.free_taker_left = wx.ComboBox(self, choices=[str(x) for x in self.team])
    self.free_taker_left.SetStringSelection(str(self.team.free_taker_left))
    self.free_taker_left.Bind(wx.EVT_COMBOBOX, self.update_free_taker)
    self.free_taker_right = wx.ComboBox(self, choices=[str(x) for x in self.team])
    self.free_taker_right.SetStringSelection(str(self.team.free_taker_right))
    self.free_taker_right.Bind(wx.EVT_COMBOBOX, self.update_free_taker)
    self.free_taker_long = wx.ComboBox(self, choices=[str(x) for x in self.team])
    self.free_taker_long.SetStringSelection(str(self.team.free_taker_long))
    self.free_taker_long.Bind(wx.EVT_COMBOBOX, self.update_free_taker)
    label = wx.StaticText(self, label='Left free kicks:', size=label_size)
    label.SetFont(font)
    label.SetForegroundColour(colour.BL)
    label.SetBackgroundColour(colour.LIME)
    self.vbox3.Add(label, proportion=0)
    self.vbox3.Add(self.free_taker_left)
    label = wx.StaticText(self, label='Right free kicks:', size=label_size)
    label.SetFont(font)
    label.SetForegroundColour(colour.BL)
    label.SetBackgroundColour(colour.LIME)
    self.vbox3.Add(label, proportion=0)
    self.vbox3.Add(self.free_taker_right)
    label = wx.StaticText(self, label='Long free kicks:', size=label_size)
    label.SetFont(font)
    label.SetForegroundColour(colour.BL)
    label.SetBackgroundColour(colour.LIME)
    self.vbox3.Add(label, proportion=0)
    self.vbox3.Add(self.free_taker_long)
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

  def update_free_taker(self, event):
    self.team.update_free_taker(self.free_taker_left.GetValue(), 'left')
    self.team.update_free_taker(self.free_taker_right.GetValue(), 'right')
    self.team.update_free_taker(self.free_taker_long.GetValue(), 'long')
    self.refresh()
    pass

  def update_lists(self):
    for i in range(1, 22):
      self.lineups[i].ClearAll()
    self.reserves.ClearAll()
    for player in self.team:
      if player.match.lineup > 0:
        self.lineups[player.match.lineup].InsertItem(0, '{0} {1}'.format(player.match.lineup, player))
      else:
        self.reserves.InsertItem(0, '{0} {1}'.format(player.match.lineup, player))

  def Draw(self, dc):
    dc.Clear() # make sure you clear the bitmap!
    bmp = wx.Bitmap(default.gui_background)
    dc.DrawBitmap(bmp, 0, 0)
    self.draw_lineup(dc)

  def refresh(self):
    self.update_lists()
    self.team.update_playing_positions()
    self.UpdateDrawing()

  def draw_lineup(self, dc):
    self.draw_pitch(dc, self.team.name)
    for player in self.team.playing + self.team.subs:
      if player.match.lineup in self.team.formation.goalkeeper_lineups.values():
        colour_p = self.team.colour.goalkeeper_p
        colour_s = self.team.colour.goalkeeper_s
      else:
        colour_p = self.team.colour.home_p
        colour_s = self.team.colour.home_s
      x, y = self.team.formation.get_coords(player.match.lineup)
      self.draw_player(player, dc, x=x, y=y, x0=self.x0, y0=self.y0,
        colour_p=colour_p, colour_s=colour_s)
    self.draw_manager(self.team.manager, dc, x=380, y=340, x0=self.x0, y0=self.y0)

class MatchManagePanel(ManagePanel):
  def __init__(self, parent, team, home=True, x0=None, y0=None):
    super().__init__(parent, team, home, x0, y0)
    colour = Colour()
    font = wx.Font(12, wx.DECORATIVE, wx.BOLD, wx.NORMAL)
    self.training_button.Destroy()
    self.vbox3.Clear(True)
    self.txt_output = wx.StaticText(self, size=wx.Size(200, (28*4)), style=wx.ST_NO_AUTORESIZE)
    self.txt_output.SetFont(font)
    self.txt_output.SetBackgroundColour(colour.LIME)
    self.vbox1.Add(self.txt_output)
    self.exit_button.SetLabel('Continue')
    self.label1.SetLabel('Playing:')
    for i in range(1, 16):
      self.targets[i] = MatchPlayerTarget(self, i, self.team)
      self.lineups[i].SetDropTarget(self.targets[i])
    for i in range(16, 22):
      self.targets[i] = MatchPlayerTarget(self, i, self.team)
      self.lineups[i].SetDropTarget(self.targets[i])

  def make_a_sub(self, event):
    text = event.GetText()
    print(text)
    text_n = int(text.split(' ')[0])
    src = wx.DropSource(self.lineups[text_n])
    tobj = wx.TextDataObject(text)
    src.SetData(tobj)
    src.DoDragDrop(True)
    self.refresh()

  def update_lists(self):
    for i in range(1, 22):
      self.lineups[i].ClearAll()
      if i in self.team.formation.playing_lineups:
        current_lineup = self.team.formation.playing_lineups[i]
      else:
        current_lineup = self.team.formation.sub_lineups[i]
      players = [p for p in self.team if p.match.lineup == current_lineup]
      if len(players) > 0:
        player = players[0]
        self.lineups[i].InsertItem(0, '{0} {1}'.format(player.match.lineup, player))

  def draw_lineup(self, dc):
    self.draw_pitch(dc, self.team.name)
    off_count = 0
    for player in self.team.playing + self.team.subs + self.team.off:
      if player.match.lineup in self.team.formation.goalkeeper_lineups.values():
        colour_p = self.team.colour.goalkeeper_p
        colour_s = self.team.colour.goalkeeper_s
      else:
        colour_p = self.team.colour.home_p
        colour_s = self.team.colour.home_s
      if player.match.lineup < 1:
        off_count += 1
      x, y = self.team.formation.get_coords(player.match.lineup, off_count)
      self.draw_player_match(player, dc, x=x, y=y, x0=self.x0, y0=self.y0,
        colour_p=colour_p, colour_s=colour_s)
    self.draw_manager(self.team.manager, dc, x=380, y=340, x0=self.x0, y0=self.y0)

if __name__ == "__main__":

  app = wx.App(False)
  frame = DefaultFrame()
  panel = ManagePanel(frame)
  frame.sizer.Add(panel, 1, wx.EXPAND)
  frame.SetSizer(self.sizer)
  app.MainLoop()
