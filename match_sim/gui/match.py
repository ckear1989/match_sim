
import wx

import match_sim.default as default
from match_sim.gui.graphics import PaintPanel, Colour
from match_sim.gui.template import TemplateButton
from match_sim.cl.match import Match as ClMatch

class MatchPanel(PaintPanel):
  def __init__(self, parent, match, x0=600, y0=None):
    self.match = match
    super().__init__(parent, x0, y0)
    self.game = self.GetParent().game
    self.test_button.Destroy()
    play_button = TemplateButton(self, 'Play')
    play_button.Bind(wx.EVT_BUTTON, self.on_play)
    self.hbox3.Add(play_button)
    pause_button = TemplateButton(self, 'Pause')
    pause_button.Bind(wx.EVT_BUTTON, self.on_pause)
    self.hbox3.Add(pause_button)
    self.team = self.GetParent().game.teams[self.GetParent().game.team]
    self.lineups = {}
    self.vbox1 = wx.BoxSizer(wx.VERTICAL)
    self.vbox1.Add((1, 400))
    self.hbox1.Add(self.vbox1)
    self.vbox2 = wx.BoxSizer(wx.VERTICAL)
    self.vbox2.Add((1, 400))
    self.hbox1.Add(self.vbox2)
    self.InitUI()
    self.dc = wx.ClientDC(self)
    self.refresh()

  def draw_lineup(self):
    self.dc = wx.ClientDC(self)
    self.draw_pitch(self.dc, self.team.name)
    for i in range(1, 22):
      players = [p for p in self.team if p.match.lineup == i]
      if len(players) > 0:
        player = players[0]
        x, y = self.team.formation.get_coords(i)
        self.draw_player(player, self.dc, x=x, y=y) 

  def refresh(self):
    self.draw_lineup()

  def on_pause(self, event):
    print('debug5')
    print(self.match)
    self.refresh()

  def on_play(self, event):
    print(self.match)
    self.refresh()
    import time
    time.sleep(2)
    self.GetParent().exit_match(event)

class Match(ClMatch):
  def __init__(self, team_a, team_b, current_date, silent, extra_time_required):
    super().__init__(team_a, team_b, current_date, silent, extra_time_required)
    self.status = 'pre-match'

  def play(self, time_step=0):
    pass

  def print_event_list(self, pl):
    '''Print each line in list.  Pause appropriately.'''
    if self.silent is not True:
      for ps in pl:
        print(ps, end='')
      print()

