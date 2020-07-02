
import time

import wx

import match_sim.default as default
from match_sim.gui.graphics import PaintPanel, Colour
from match_sim.gui.template import TemplateButton
from match_sim.cl.match import Match as ClMatch, time_until_next_event, stopclock, printc

MATCH_EVENT = wx.NewEventType()
MATCH_EVENT_CUSTOM = wx.PyEventBinder(MATCH_EVENT, 1)
STOPCLOCK_EVENT = wx.NewEventType()
STOPCLOCK_EVENT_CUSTOM = wx.PyEventBinder(STOPCLOCK_EVENT, 1)

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
    font = wx.Font(16, wx.ROMAN, wx.ITALIC, wx.NORMAL) 
    self.match = self.GetParent().match
    self.game = self.GetParent().game
    self.test_button.Destroy()
    self.exit_button.Bind(wx.EVT_BUTTON, self.on_exit_match)
    play_button = TemplateButton(self, 'Play')
    play_button.Bind(wx.EVT_BUTTON, self.on_play)
    self.hbox3.Add(play_button)
    pause_button = TemplateButton(self, 'Pause')
    pause_button.Bind(wx.EVT_BUTTON, self.on_pause)
    self.hbox3.Add(pause_button)
    self.vbox1 = wx.BoxSizer(wx.VERTICAL)
    self.hbox1.Add(self.vbox1)
    self.vbox2 = wx.BoxSizer(wx.VERTICAL)
    self.hbox1.Add(self.vbox2)
    self.stopclock = wx.StaticText(self)
    self.stopclock.SetLabel('00:00')
    self.stopclock.SetFont(font)
    self.scoreboard = wx.StaticText(self, size=wx.Size(400, 100), style=wx.ST_NO_AUTORESIZE)
    self.scoreboard.SetLabel(str(self.match))
    self.scoreboard.SetFont(font)
    self.hbox5 = wx.BoxSizer(wx.HORIZONTAL)
    self.hbox5.Add(self.stopclock)
    self.hbox5.Add(self.scoreboard)
    self.vbox1.Add(self.hbox5)
    self.txt_output = wx.StaticText(self, size = wx.Size(400, 500), style=wx.ST_NO_AUTORESIZE)
    self.txt_output.SetFont(font)
    self.vbox1.Add(self.txt_output)
    self.refresh()
    self.Bind(MATCH_EVENT_CUSTOM, self.on_match_event)
    self.Bind(STOPCLOCK_EVENT_CUSTOM, self.on_stopclock)

  def draw_lineup(self):
    dc = wx.ClientDC(self)
    self.draw_pitch(dc, self.match.team_a.name, x0=460)
    for i in range(1, 22):
      players = [p for p in self.match.team_a if p.match.lineup == i]
      if len(players) > 0:
        player = players[0]
        x, y = self.match.team_a.formation.get_coords(i)
        self.draw_player_score(player, dc, x=x, y=y, x0=460,
          colour_p=self.match.team_a.colour.home_p, colour_s=self.match.team_a.colour.home_s)
    self.draw_pitch(dc, self.match.team_b.name, x0=900)
    for i in range(1, 22):
      players = [p for p in self.match.team_b if p.match.lineup == i]
      if len(players) > 0:
        player = players[0]
        x, y = self.match.team_b.formation.get_coords(i)
        self.draw_player_score(player, dc, x=x, y=y, x0=900,
          colour_p=self.match.team_a.colour.home_p, colour_s=self.match.team_a.colour.away_s)

  def refresh(self):
    self.draw_lineup()
    self.scoreboard.SetLabel(str(self.match))

  def on_pause(self, event):
    print('pause')
    self.refresh()

  def on_play(self, event):
    print('play')
    if self.match.status in ['pre-match']:
      self.refresh()
      self.match.update_event_handler(self.GetEventHandler())
      for ts in self.match.play():
        pass
      self.game.process_match_result(self.match, self.match.comp_name)
      self.game.update_next_fixture()

  def on_stopclock(self, event):
    self.stopclock.SetLabel(event.GetMyVal())
    wx.Yield()

  def on_match_event(self, event):
    for ps in event.GetMyVal():
      if len(ps) > 5:
        self.txt_output.SetLabel(ps)
        wx.Yield()
        time.sleep(0.5)
    self.refresh()

  def on_exit_match(self, event):
    print('exit')
    if self.match.status in ['finished']:
      self.GetParent().exit_match(event)

class Match(ClMatch):
  def __init__(self, team_a, team_b, current_date, silent, extra_time_required, comp_name, event_handler):
    super().__init__(team_a, team_b, current_date, silent, extra_time_required)
    self.comp_name = comp_name
    self.event_handler = event_handler
    self.status = 'pre-match'

  def update_event_handler(self, event_handler):
    self.event_handler = event_handler

  def half_time(self):
    '''Reset added time back to 35 minutes.  Update scorer data.  Let user manage team'''
    self.time = 35 * 60
    self.first_half_length = 35 * 60
    self.stopclock_time = stopclock(self.time)
    yield 'half time'

  def full_time(self):
    '''Update scorer stats.  Print final result'''
    self.print_event_list('Full time score is:\n{0}'.format(self.get_score().replace('Score is now ', '')))
    yield 'full time'

  def extra_time(self, time_step):
    '''Determine if extra time is needed.Play 2x10 minute periods of events'''
    if self.extra_time_required is True:
      if self.team_a.score == self.team_b.score:
        self.print_event_list('The match is going to extra time.')
        for ps in self.half_time():
          yield ps
        self.time = 70 * 60
        self.stopclock_time = stopclock(self.time)
        tane = (self.time) + time_until_next_event()
        for ps in self.play_half(self.time + (10*60), time_step, tane=tane):
          yield ps
        for ps in self.half_time():
          yield ps
        self.time = (70 * 60) + (10*60)
        tane = (self.time) + time_until_next_event()
        for ps in self.play_half(self.time + (10*60), time_step, tane=tane):
          yield ps
        for ps in self.full_time():
          yield ps
        if self.team_a.score == self.team_b.score:
          for ps in self.shootout():
            yield ps
    yield 'extra time'

  def shootout(self):
    '''Coin toss to determine winner'''
    p0 = random.random()
    if p0 < 0.5:
      self.print_event_list('{0} wins the shootout.'.format(self.team_a.name))
      self.team_a.score.scoren += 1
    else:
      self.print_event_list('{0} wins the shootout.'.format(self.team_b.name))
      self.team_b.score.scoren += 1
    yield 'shootout'

  def play(self, time_step=0):
    '''Play through various stages of matches.  Update timekeeping.'''
    yield 'pre match'
    self.status = 'playing'
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
    self.status = 'finished'

  def play_half(self, end_time, time_step, tane=time_until_next_event()):
    '''Run through 35 minutes of events.  Print clock and messages if needed'''
    yield 'throw in'
    self.throw_in()
    at = 0
    while self.time < (end_time + at):
      self.time += 1
      if self.time % 1 == 0:
        self.stopclock_time = stopclock(self.time)
        yield '1 second'
        self.print_stopclock()
      if self.time % 60 == 0:
        yield '1 minute'
        self.update_team_condition()
      if self.time % (34 * 60) == 0:
        at = self.added_time()
      if self.time == tane:
        self.event()
        tune = time_until_next_event()
        tane += tune
      if time_step > 0:
        print(time_step)
        time.sleep(time_step)
    self.print_event_list(['{0} And that\'s the end of the half'.format(self.stopclock_time)])

  def GetId(self):
    return wx.ID_ANY

  def print_stopclock(self):
    '''Print each line in list.  Pause appropriately.'''
    if self.silent is not True:
      event = MatchEvent(STOPCLOCK_EVENT, self.GetId())
      event.SetMyVal(self.stopclock_time)
      self.event_handler.ProcessEvent(event)

  def print_event_list(self, pl):
    '''Print each line in list.  Pause appropriately.'''
    if self.silent is not True:
      event = MatchEvent(MATCH_EVENT, self.GetId())
      event.SetMyVal(pl)
      self.event_handler.ProcessEvent(event)

