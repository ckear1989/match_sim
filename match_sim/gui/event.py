
import random

import wx

from match_sim.cl.event import Event as ClEvent
from match_sim.reporting import match_message as msg

MATCH_EVENT = wx.NewEventType()
MATCH_EVENT_CUSTOM = wx.PyEventBinder(MATCH_EVENT, 1)
REFRESH_EVENT = wx.NewEventType()
REFRESH_EVENT_CUSTOM = wx.PyEventBinder(REFRESH_EVENT, 1)

class MatchEvent(wx.PyCommandEvent):
  def __init__(self, evtType, id):
    wx.PyCommandEvent.__init__(self, evtType, id)
    myVal = None
    verbosity = None

  def SetMyVal(self, val):
    self.myVal = val

  def GetMyVal(self):
    return self.myVal

  def SetVerbosity(self, val):
    self.verbosity = val

  def GetVerbosity(self):
    return self.verbosity

class EventPl(list):
  def __init__(self, event_handler, amatch):
    super().__init__()
    self.event_handler = event_handler
    self.match = amatch

  def append(self, astr, vb=5):
    self.emit_match_event(astr, vb)
    if vb == 0:
      self.match.append_report(astr)

  def emit_match_event(self, astr, vb=5):
    event = MatchEvent(MATCH_EVENT, wx.ID_ANY)
    event.SetMyVal(astr)
    event.SetVerbosity(vb)
    self.event_handler.ProcessEvent(event)

class Event(ClEvent):
  def __init__(self, amatch, event_handler):
    super().__init__(amatch)
    self.event_handler = event_handler
    self.pl = EventPl(self.event_handler, amatch)
    self.match = amatch

  def full_time(self):
    '''Update scorer stats.  Print final result'''
    self.pl.append(random.choice(msg.full_time).format(self.match.get_score().replace('Score is now ', '')), 1)
    self.pl.append('FT {0}'.format(self.match.get_score(ts=False)), vb=0)

  def half_time(self):
    self.pl.append(random.choice(msg.half_time), 1)
    self.pl.append('HT {0}'.format(self.match.get_score(ts=False)), vb=0)

  def emit_refresh_event(self):
    event = MatchEvent(REFRESH_EVENT, wx.ID_ANY)
    self.event_handler.ProcessEvent(event)

  def run(self, amatch):
    '''Print string collected from method.  Printed if match is not silent'''
    old_score = self.match.get_score()[:]
    super().run(amatch)
    new_score = self.match.get_score()[:]
    if new_score != old_score:
      self.emit_refresh_event()

  def shooting_player_point_attempt(self, shooting_player=None, assisting_player=None):
    '''Point attempt made.  Score or wide determined'''
    if shooting_player is None:
      shooting_player = self.shooting_player
    if assisting_player is None:
      assisting_player = self.posession_player
    p0 = random.random()
    if p0 < (shooting_player.physical.shooting*1.2/100):
      shooting_player.score_point()
      assisting_player.assist()
      shooting_player.update_score()
      self.attackers.update_score()
      self.pl.append(random.choice(msg.he_scores_point), 5)
      self.pl.append('{0} {1} point'.format(self.match.get_score(), shooting_player), vb=0)
    elif p0 < 0.97:
      self.pl.append(random.choice(msg.he_misses_point), 5)
    else:
      self.pl.append(random.choice(msg.he_wins_45), 5)
      self.free_kick_45()

  def free_kick_45(self):
    shooting_player = self.attackers.choose_free_taker_45()
    self.pl.append(random.choice(msg.he_takes_45).format(shooting_player))
    p0 = random.random()
    if p0 < 0.7:
      shooting_player.score_point()
      shooting_player.update_score()
      self.attackers.update_score()
      self.pl.append(random.choice(he_scores_45))
      self.pl.append('{0} {1} point'.format(self.match.get_score(), shooting_player), vb=0)
    else:
      self.pl.append(random.choice(msg.he_misses_45))

  def shooting_player_goal_attempt(self, shooting_player=None, assisting_player=None):
    '''Point attempt made.  Score or wide or goalkeeper save determined'''
    if shooting_player is None:
      shooting_player = self.shooting_player
    if assisting_player is None:
      assisting_player = self.posession_player
    p0 = random.random()
    if p0 < (self.shooting_player.physical.shooting/100):
      shooting_player.score_goal()
      assisting_player.assist()
      shooting_player.update_score()
      self.attackers.update_score()
      self.pl.append(random.choice(msg.he_scores_goal))
      self.pl.append('{0} {1} goal'.format(self.match.get_score(), shooting_player), vb=0)
    elif p0 < 0.95:
      self.pl.append(random.choice(msg.goalkeeper_saves_goal))
      self.goalkeeper.save_goal()
    else:
      self.pl.append(random.choice(msg.he_misses_goal))

  def foul(self, attacker):
    '''Foul event happens.  Card determined.  Injury determined.  Free kick given'''
    self.pl.append(random.choice(msg.fouled_by).format(self.defending_player), 5)
    p0 = random.random()
    if p0 < 0.2:
      self.defending_player.gain_card('y')
      self.pl.append(random.choice(msg.yellow_for).format(self.defending_player), 5)
      self.pl.append('{0} {1} {2} yellow'.format(self.match.get_score(sc=False), self.defenders.name, self.defending_player), vb=0)
      if self.defending_player.season.cards.count('y') == 2:
        self.defending_player.gain_card('r')
        self.defending_player.gain_suspension('yellow', self.date)
        self.defenders.send_off_player(self.defending_player)
        self.pl.append(random.choice(msg.second_yellow), 5)
        self.pl.append('{0} {1} {2} second yellow'.format(self.match.get_score(sc=False), self.defenders.name, self.defending_player), vb=0)
        self.emit_refresh_event()
      p1 = random.random()
      if p1 < 0.2:
        attacker.gain_injury(self.date)
        self.pl.append('{0} {1} {2} injury'.format(self.match.get_score(sc=False), self.attackers.name, attacker), vb=0)
        self.emit_refresh_event()
        self.attackers.forced_substitution(attacker)
    elif p0 < 0.25:
      self.defending_player.gain_card('r')
      self.defending_player.gain_suspension('red', self.date)
      self.defenders.send_off_player(self.defending_player)
      self.pl.append(random.choice(msg.red).format(self.defending_player), 5)
      self.pl.append('{0} {1} {2} red'.format(self.match.get_score(sc=False), self.defenders.name, self.defending_player), vb=0)
      self.emit_refresh_event()
      if self.defending_player.physical.position == 'GK':
        player_off = random.choice(self.defenders.playing)
        self.defenders.forced_substitution(player_off, 'GK',
          '{0} has been sent off. {1} is being substituted to bring on a GK'.format(
           self.defending_player, player_off))
      p2 = random.random()
      if p2 < 0.5:
        attacker.gain_injury(self.date)
        self.pl.append('{0} {1} {2} injury'.format(self.match.get_score(sc=False), self.attackers.name, attacker), vb=0)
        self.emit_refresh_event()
        self.attackers.forced_substitution(attacker)
    self.free_kick(attacker)

