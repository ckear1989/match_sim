
import time

import wx

import match_sim.cl.default as default
from match_sim.cl.match import Match as ClMatch, time_until_next_event, stopclock, printc
from match_sim.gui.event import Event, MATCH_EVENT_CUSTOM, REFRESH_EVENT_CUSTOM, MatchEvent
from match_sim.gui.graphics import PaintPanel, Colour
from match_sim.gui.manage import ManagePanel, MatchManagePanel
from match_sim.gui.settings import MatchSettings
from match_sim.gui.template import TemplateButton
from match_sim.reporting.match_report import MatchReport

STOPCLOCK_EVENT = wx.NewEventType()
STOPCLOCK_EVENT_CUSTOM = wx.PyEventBinder(STOPCLOCK_EVENT, 1)
PAUSE_EVENT = wx.NewEventType()
PAUSE_EVENT_CUSTOM = wx.PyEventBinder(PAUSE_EVENT, 1)
FORCED_SUB_EVENT = wx.NewEventType()
FORCED_SUB_EVENT_CUSTOM = wx.PyEventBinder(FORCED_SUB_EVENT, 1)

class MatchPanel(PaintPanel):
  def __init__(self, parent, match, logs, x0=600, y0=None):
    self.match = match
    self.logs = logs
    super().__init__(parent, x0, y0)
    colour = Colour()
    self.exit_button.Destroy()
    font = wx.Font(16, wx.ROMAN, wx.ITALIC, wx.NORMAL) 
    self.game = self.GetParent().game
    self.verbosity = 5
    self.home = True
    if self.game.team == self.match.team_b.name:
      self.home = False
    self.test_button.Destroy()
    self.play_button = TemplateButton(self, 'Play')
    self.play_button.Bind(wx.EVT_BUTTON, self.on_play)
    self.hbox3.Add(self.play_button)
    self.pause_button = TemplateButton(self, 'Choose Lineup')
    self.pause_button.Bind(wx.EVT_BUTTON, self.emit_pause_event)
    self.hbox3.Add(self.pause_button)
    self.vbox1 = wx.BoxSizer(wx.VERTICAL)
    self.hbox1.Add(self.vbox1)
    self.hbox5 = wx.BoxSizer(wx.HORIZONTAL)
    self.hbox1.Add(self.hbox5)
    self.stopclock = wx.StaticText(self, size=wx.Size(68, 28), style=wx.ST_NO_AUTORESIZE)
    self.stopclock.SetLabel('00:00')
    self.stopclock.SetBackgroundColour(colour.BL)
    self.stopclock.SetForegroundColour(colour.WH)
    self.stopclock.SetFont(font)
    self.scoreboard_str()
    self.scoreboard_h.SetFont(font)
    self.scoreboard_a.SetFont(font)
    self.scoreboard_h.SetBackgroundColour(self.match.team_a.colour.home_p)
    self.scoreboard_a.SetBackgroundColour(self.match.team_b.colour.away_p)
    self.scoreboard_h.SetForegroundColour(self.match.team_a.colour.home_s)
    self.scoreboard_a.SetForegroundColour(self.match.team_b.colour.away_s)
    self.vbox1.Add(self.stopclock)
    self.vbox1.Add((481, 28))
    self.hbox5.Add(self.scoreboard_h)
    self.hbox5.Add((102, 28))
    self.hbox5.Add(self.scoreboard_a)
    self.txt_output = wx.StaticText(self, size=wx.Size(420, (28*4)), style=wx.ST_NO_AUTORESIZE)
    self.txt_output.SetBackgroundColour(colour.LIME)
    self.txt_output.SetFont(font)
    self.vbox1.Add(self.txt_output, flag=wx.ALL, border=5)
    self.txt_output_long = wx.TextCtrl(self, size=wx.Size(420, (28*8)), style=wx.TE_WORDWRAP|wx.TE_READONLY|wx.TE_MULTILINE)
    font = wx.Font(8, wx.ROMAN, wx.ITALIC, wx.NORMAL)
    self.txt_output_long.SetFont(font)
    self.vbox1.Add(self.txt_output_long, flag=wx.ALL, border=5)
    self.Bind(MATCH_EVENT_CUSTOM, self.on_match_event)
    self.Bind(STOPCLOCK_EVENT_CUSTOM, self.on_stopclock)
    self.Bind(PAUSE_EVENT_CUSTOM, self.on_pause)
    self.Bind(FORCED_SUB_EVENT_CUSTOM, self.on_forced_sub)
    self.Bind(REFRESH_EVENT_CUSTOM, self.refresh)

  def refresh(self, event):
    self.UpdateDrawing()

  def scoreboard_str(self):
    ps = str(self.match)
    ps = ps.split(')')
    try:
      self.scoreboard_h.SetLabel(ps[0] + ')')
      self.scoreboard_a.SetLabel(ps[1].strip() + ')')
      self.scoreboard_h.Show()
      self.scoreboard_a.Show()
    except AttributeError:
      self.scoreboard_h = wx.StaticText(self, size=wx.Size(338, 27), style=wx.ST_NO_AUTORESIZE)
      self.scoreboard_a = wx.StaticText(self, size=wx.Size(338, 27), style=wx.ST_NO_AUTORESIZE)
      self.scoreboard_str()

  def draw_lineup(self, dc):
    self.draw_pitch(dc, x0=500, y0=50, header_border=True)
    off_count = 0
    print('playing', self.match.team_a.playing)
    print('subs', self.match.team_a.subs)
    print('off', self.match.team_a.off)
    for player in self.match.team_a.playing + self.match.team_a.subs + self.match.team_a.off:
      if player.match.lineup in self.match.team_a.formation.goalkeeper_lineups:
        colour_p = self.match.team_a.colour.goalkeeper_p
        colour_s = self.match.team_a.colour.goalkeeper_s
      else:
        colour_p = self.match.team_a.colour.home_p
        colour_s = self.match.team_a.colour.home_s
      if player.match.lineup < 1:
        off_count += 1
      x, y = self.match.team_a.formation.get_coords(player.match.lineup, off_count)
      self.draw_player_match(player, dc, x=x, y=y, x0=500, y0=50,
        colour_p=colour_p, colour_s=colour_s)
    self.draw_manager(self.match.team_a.manager, dc, x=380, y=340, x0=500, y0=50)
    self.draw_pitch(dc, x0=940, y0=50, header_border=True)
    off_count = 0
    for player in self.match.team_b.playing + self.match.team_b.subs + self.match.team_b.off:
      if player.match.lineup in self.match.team_b.formation.goalkeeper_lineups:
        colour_p = self.match.team_b.colour.goalkeeper_p
        colour_s = self.match.team_b.colour.goalkeeper_s
      else:
        colour_p = self.match.team_b.colour.away_p
        colour_s = self.match.team_b.colour.away_s
      if player.match.lineup < 1:
        off_count += 1
      x, y = self.match.team_b.formation.get_coords(player.match.lineup, off_count)
      self.draw_player_match(player, dc, x=x, y=y, x0=940, y0=50,
        colour_p=colour_p, colour_s=colour_s)
    self.draw_manager(self.match.team_b.manager, dc, x=380, y=340, x0=940, y0=50)

  def Draw(self, dc):
    self.match.team_a.update_playing_positions()
    self.match.team_b.update_playing_positions()
    dc.Clear() # make sure you clear the bitmap!
    bmp = wx.Bitmap(default.gui_background)
    dc.DrawBitmap(bmp, 0, 0)
    self.draw_lineup(dc)
    self.scoreboard_str()
    wx.Yield()

  def emit_pause_event(self, msg=None):
    event = MatchEvent(PAUSE_EVENT, self.GetId())
    event.SetMyVal(msg)
    self.GetEventHandler().ProcessEvent(event)

  def on_pause(self, event):
    print('pause')
    self.pause_button.Hide()
    if self.match.time == 0:
      self.match.set_status('pre-match')
      self.GetParent().on_match_manage(ManagePanel, self.home)
    else:
      self.match.set_status('paused')
      if isinstance(event.GetMyVal(), str):
        time.sleep(0.5)
        self.txt_output.SetLabel(event.GetMyVal())
        self.Update()
      time.sleep(0.5)
      self.Update()
      wx.Yield()
      self.GetParent().on_match_manage(MatchManagePanel, self.home)
      if isinstance(event.GetMyVal(), str):
        self.GetParent().match_manage_panel.txt_output.SetLabel(event.GetMyVal())
    while self.match.status in ['pre-match', 'paused']:
      wx.Yield()
    self.game.teams[self.game.team].update_playing_positions()

  def on_forced_sub(self, event):
    print('forced sub')
    self.pause_button.Hide()
    self.match.set_status('forced-sub')
    team = event.GetMyVal()[0]
    player = event.GetMyVal()[1]
    reason = event.GetMyVal()[2]
    self.txt_output.SetLabel(
      '{0} have lost a player through injury. {1}'.format(team.name, reason))
    wx.Yield()
    time.sleep(0.5)
    self.GetParent().on_match_manage(MatchManagePanel, self.home)
    self.GetParent().match_manage_panel.txt_output.SetLabel(
      '{0} have lost a player through injury. {1}'.format(team.name, reason))
    while team.check_sub_made(player) is False:
      self.GetParent().match_manage_panel.exit_button.Hide()
      wx.Yield()
    self.GetParent().match_manage_panel.exit_button.Show()
    self.txt_output.SetLabel('')
    self.match.set_status('paused')

  def on_play(self, event):
    print('play')
    if self.match.status in ['pre-match']:
      self.pause_button.SetLabel('Pause')
      self.pause_button.Show()
      self.play_button.SetLabel('Continue')
      self.match.update_event_handler(self.GetEventHandler())
      self.match.team_a.update_event_handler(self.GetEventHandler())
      self.match.team_b.update_event_handler(self.GetEventHandler())
      for ts in self.match.play(self.match.settings.time_step):
        pass
    if self.match.status in ['finished']:
      self.play_button.Hide()
      self.pause_button.Hide()
      self.match.team_a.update_event_handler()
      self.match.team_b.update_event_handler()
      print('debug')
      self.game.process_match_result(self.match, self.match.comp_name)
      self.game.update_next_fixture()
      self.game.inbox.add_match_message(self.match)
      self.on_exit_match(event)
    self.match.set_status('playing')
    self.pause_button.SetLabel('Pause')
    self.pause_button.Show()

  def on_stopclock(self, event):
    self.stopclock.SetLabel(event.GetMyVal())
    for log in self.logs:
      if self.match.time in log.keys():
        self.txt_output_long.AppendText(log[self.match.time] + '\n')
    self.Update()
    wx.Yield()

  def on_match_event(self, event):
    ps = event.GetMyVal()
    vb = event.GetVerbosity()
    if vb == 0:
      self.txt_output_long.AppendText(ps + '\n')
    if 0 < vb <= self.verbosity:
      if len(ps) > 6:
        self.txt_output.SetLabel(ps)
        self.Update()
        wx.Yield()
        time.sleep(0.5)
    self.txt_output.SetLabel('')

  def on_exit_match(self, event):
    print('exit')
    if self.match.status in ['finished']:
      self.GetParent().exit_match(event)

class Match(ClMatch):
  def __init__(self, team_a, team_b, current_date, silent, extra_time_required, comp_name, event_handler, time_step):
    super().__init__(team_a, team_b, current_date, silent, extra_time_required)
    self.comp_name = comp_name
    self.event_handler = event_handler
    self.set_status('pre-match')
    self.at = 0
    self.first_half_length = 35 * 60
    self.second_half_length = 35 * 60
    self.settings = MatchSettings(time_step)
    self.report = MatchReport()

  def get_score(self, ts=True, sc=True):
    '''Get user friendly string of match score'''
    ps = ''
    if ts is True:
      ps += "' " + '{0} '.format(int(self.stopclock_time[:2]) + 1).rjust(2)
    if sc is True:
      ps += '{0} {1} {2} {3}'.format(
      self.team_a.name, self.team_a.score,
      self.team_b.name, self.team_b.score
    )
    return ps.strip()

  def append_report(self, ps):
    self.report[self.time] = ps

  def set_status(self, status):
    self.status = status

  def update_event_handler(self, event_handler=None):
    self.event_handler = event_handler

  def half_time(self):
    '''Reset added time back to 35 minutes.  Update scorer data.  Let user manage team'''
    event = Event(self, self.event_handler)
    event.half_time()
    self.at = 0
    self.time = self.first_half_length
    self.stopclock_time = stopclock(self.time)
    self.print_stopclock()
    wx.Yield()
    self.emit_pause_event('Half Time')
    yield 'half time'

  def full_time(self):
    '''Update scorer stats.  Print final result'''
    event = Event(self, self.event_handler)
    event.full_time()
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
    self.update_team_condition()
    self.set_status('playing')
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
    self.set_status('finished')

  def play_half(self, end_time, time_step, tane=time_until_next_event()):
    '''Run through 35 minutes of events.  Print clock and messages if needed'''
    yield 'throw in'
    if self.time == 0:
      self.throw_in()
    if (self.time == 35 * 60) and (self.at == 0):
      self.throw_in()
    while self.time < (end_time + self.at):
      if self.status == 'playing':
        self.time += 1
        if self.time % 1 == 0:
          self.stopclock_time = stopclock(self.time)
          self.print_stopclock()
        if self.time % 60 == 0:
          yield '1 minute'
          self.update_team_condition()
        if self.time % (34 * 60) == 0:
          self.at = self.added_time()
        if self.time == tane:
          self.event()
          tune = time_until_next_event()
          tane += tune
        if time_step > 0:
          time.sleep(time_step)
      else:
        wx.Yield()

  def GetId(self):
    return wx.ID_ANY

  def print_stopclock(self):
    if self.silent is not True:
      event = MatchEvent(STOPCLOCK_EVENT, self.GetId())
      event.SetMyVal(self.stopclock_time)
      self.event_handler.ProcessEvent(event)

  def emit_pause_event(self, msg=None):
    if self.silent is not True:
      event = MatchEvent(PAUSE_EVENT, self.GetId())
      event.SetMyVal(msg)
      self.event_handler.ProcessEvent(event)
    else:
      self.set_status('playing')

  def event(self):
    '''Instatiate event.  Run it'''
    event = Event(self, self.event_handler)
    event.run(self)
    self.abandon()

  def throw_in(self):
    '''Call event throw in method.  Print if necessary'''
    event = Event(self, self.event_handler)
    event.throw_in()

  def added_time(self):
    '''Call event method'''
    event = Event(self, self.event_handler)
    at = event.added_time()
    return at
