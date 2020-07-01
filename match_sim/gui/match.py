
import wx

import match_sim.default as default
from match_sim.gui.graphics import PaintPanel, Colour
from match_sim.gui.template import TemplateButton
from match_sim.cl.match import Match as ClMatch, time_until_next_event, stopclock, printc

myEVT_CUSTOM = wx.NewEventType()
EVT_CUSTOM = wx.PyEventBinder(myEVT_CUSTOM, 1)

class MatchEvent(wx.PyCommandEvent):
  def __init__(self, evtType, id):
    wx.PyCommandEvent.__init__(self, evtType, id)
    myVal = None

  def SetMyVal(self, val):
    self.myVal = val

  def GetMyVal(self):
    return self.myVal

class MatchPanel(PaintPanel):
  def __init__(self, parent, x0=600, y0=None):
    super().__init__(parent, x0, y0)
    self.match = self.GetParent().match
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
    self.txt_output = wx.TextCtrl(self,
      style=wx.TE_MULTILINE|wx.BORDER_SUNKEN|wx.TE_READONLY|wx.TE_RICH2, size=(400,200))
    self.hbox1.Add(self.txt_output)
    self.InitUI()
    self.dc = wx.ClientDC(self)
    self.refresh()
    self.Bind(EVT_CUSTOM, self.on_match_event)

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
    self.refresh()
    # import time
    # time.sleep(2)
    print('pause')

  def on_play(self, event):
    self.refresh()
    self.match.update_event_handler(self.GetEventHandler())
    for ts in self.match.play():
      wx.Yield()
      print(ts)
      import time
      time.sleep(0.1)
    # for ts in self.match.play_half(self.match.first_half_length, 0):
    #   wx.Yield()
    #   print(ts)
    #   self.refresh()
    #   import time
    #   time.sleep(1)
    # self.match.half_time()
    # second_half_end = self.match.first_half_length + self.match.second_half_length
    # second_half_tane = (self.match.first_half_length) + time_until_next_event()
    # for ts in self.match.play_half(second_half_end, 0, tane=second_half_tane):
    #   wx.Yield()
    #   print(ts)
    #   self.refresh()
    # self.match.full_time()
    # self.match.extra_time(0)

    self.game.process_match_result(self.match, self.match.comp_name)
    self.game.update_next_fixture()
    self.GetParent().exit_match(event)

  def on_match_event(self, event):
    wx.Yield()
    print(event.GetMyVal())
    self.txt_output.Clear()
    self.txt_output.AppendText(event.GetMyVal())
    self.refresh()
    self.Layout()
    import time
    time.sleep(0.1)

class Match(ClMatch):
  def __init__(self, team_a, team_b, current_date, silent, extra_time_required, comp_name, event_handler):
    super().__init__(team_a, team_b, current_date, silent, extra_time_required)
    self.comp_name = comp_name
    self.event_handler = event_handler

  def update_event_handler(self, event_handler):
    self.event_handler = event_handler

  def half_time(self):
    '''Reset added time back to 35 minutes.  Update scorer data.  Let user manage team'''
    self.time = 35 * 60
    self.first_half_length = 35 * 60
    self.stopclock_time = stopclock(self.time)
    yield 'half time'

  def play(self, time_step=0):
    '''Play through various stages of matches.  Update timekeeping.'''
    # self.banner()
    # self.lineup()
    # self.pause()
    yield 'pre match'
    for ts in self.play_half(self.first_half_length, time_step):
      yield ts
    for ts in self.half_time():
      yield ts
    second_half_end = self.first_half_length + self.second_half_length
    second_half_tane = (self.first_half_length) + time_until_next_event()
    for ts in self.play_half(second_half_end, time_step, tane=second_half_tane):
      yield ts
    for ts in self.full_time():
      yield ts
    for ts in self.extra_time(time_step):
      yield ts
    # self.banner_end()

  def play_half(self, end_time, time_step, tane=time_until_next_event()):
    '''Run through 35 minutes of events.  Print clock and messages if needed'''
    self.throw_in()
    yield 'throw in'
    at = 0
    while self.time < (end_time + at):
      self.time += 1
      if self.time % 1 == 0:
        self.stopclock_time = stopclock(self.time)
        if self.silent is not True:
          yield '1 second'
          pass
          # printc(self.stopclock_time)
      if self.time % 60 == 0:
        if self.silent is not True:
          yield '1 minute'
          pass
          # print(self.stopclock_time)
        self.update_team_condition()
      if self.time % (34 * 60) == 0:
        at = self.added_time()
      if self.time == tane:
        self.event()
        tune = time_until_next_event()
        tane += tune
      if time_step > 0:
        time.sleep(time_step)
      yield self.time
    if self.silent is not True:
      print('{0} And that\'s the end of the half'.format(self.stopclock_time))

  def GetId(self):
    return wx.ID_ANY

  def print_event_list(self, pl):
    '''Print each line in list.  Pause appropriately.'''
    if self.silent is not True:
      event = MatchEvent(myEVT_CUSTOM, self.GetId())
      event.SetMyVal(''.join(pl))
      self.event_handler.ProcessEvent(event)

