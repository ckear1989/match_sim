'''Match playing engine'''

import datetime
import random
import time
import sys
import os
import numpy as np
import keyboard
import pyfiglet

from team import Team
from match_team import MatchTeam
from event import Event

def printc(x):
  '''Print and clear'''
  print('{0}\r'.format(x), end='')

def stopclock(a):
  '''Format seconds to mm:ss string'''
  t = datetime.timedelta(seconds=a)
  s = t.seconds
  m, s = divmod(s, 60)
  return '%02d:%02d' % (m, s)

def time_until_next_event(mean=60, sd=10):
  '''Stochastic number of seconds until next event'''
  return max(round(np.random.normal(mean, sd), 0), 1)

class Result():
  '''Strip down match object'''
  def __init__(self, amatch):
    self.team_a_name = amatch.team_a.name
    self.team_b_name = amatch.team_b.name
    self.team_a_score = amatch.team_a.score
    self.team_b_score = amatch.team_b.score

  def __repr__(self):
    '''User friendly scoreboard of match to represent object'''
    ps = '{0} {1} {2} {3}'.format(
      self.team_a_name, self.team_a_score, self.team_b_name, self.team_b_score
    )
    return ps

class Match():
  '''Match playing engine'''
  def __init__(self, team_home, team_away, date, silent, extra_time_required):
    self.team_a = team_home
    self.team_b = team_away
    self.date = date
    self.silent = silent
    self.extra_time_required = extra_time_required
    self.time = 0
    self.stopclock_time = stopclock(self.time)
    self.first_half_length = 35 * 60
    self.second_half_length = 35 * 60

  def __repr__(self):
    '''User friendly scoreboard of match to represent object'''
    ps = '{0} {1} {2} {3}'.format(
      self.team_a.name, self.team_a.score, self.team_b.name, self.team_b.score
    )
    return ps

  def print_event_list(self, pl):
    '''Print each line in list.  Pause appropriately.'''
    if self.silent is not True:
      for ps in pl:
        print(ps, end='')
      print()

  def throw_in(self):
    '''Call event throw in method.  Print if necessary'''
    event = Event(self)
    event.throw_in()
    self.print_event_list(event.pl)

  def update_team_condition(self):
    '''Age team by one minute'''
    for x in self.team_a.playing + self.team_b.playing:
      x.age_match_minute()
    self.team_a.get_overall()
    self.team_b.get_overall()

  def added_time(self):
    '''Call event method'''
    event = Event(self)
    at = event.added_time()
    self.print_event_list(event.pl)
    at = random.choice(range(1, 7))
    return at

  def play_half(self, end_time, time_step, tane=time_until_next_event()):
    '''Run through 35 minutes of events.  Print clock and messages if needed'''
    self.throw_in()
    at = 0
    while self.time < (end_time + at):
      self.time += 1
      if self.time % 1 == 0:
        self.stopclock_time = stopclock(self.time)
        if self.silent is not True:
          printc(self.stopclock_time)
        if keyboard.is_pressed('space') is True:
          self.pause()
      if self.time % 60 == 0:
        if self.silent is not True:
          print(self.stopclock_time)
        self.update_team_condition()
      if self.time % (34 * 60) == 0:
        at = self.added_time()
      if self.time == tane:
        self.event()
        tune = time_until_next_event()
        tane += tune
      if time_step > 0:
        time.sleep(time_step)
    if self.silent is not True:
      print('{0} And that\'s the end of the half'.format(self.stopclock_time))

  def abandon(self):
    '''Determine if team has too few players.  Award victory to opponent'''
    n_team_a = len(self.team_a.playing)
    n_team_b = len(self.team_b.playing)
    if (n_team_a < 11) or (n_team_b < 11):
      self.team_a.reset_match_stats()
      self.team_b.reset_match_stats()
      if n_team_a < 11:
        self.team_b.points = 1
      if n_team_b < 11:
        self.team_a.points = 1
      self.time = 80*60

  def lineup(self):
    '''Check lineups prior to match start.  Give user chance to change before match starts'''
    self.team_a.auto_lineup()
    self.team_b.auto_lineup()

  def pause(self):
    '''Pause match.  Give user chance to manage team'''
    self.team_a.manage()
    self.team_b.manage()

  def banner(self):
    '''Create beginning of match ascii banner.  Print it'''
    banner = pyfiglet.figlet_format('{0} vs {1} {2}\n'.format(
      self.team_a.name, self.team_b.name, self.date))
    if self.silent is not True:
      print(banner)

  def banner_end(self):
    '''Create end of match ascii banner.  Print it'''
    banner = pyfiglet.figlet_format('{0} {1}\n'.format(
      self.get_score().replace('Score is now ', ''), self.date))
    if self.silent is not True:
      print(banner)

  def shootout(self):
    '''Coin toss to determine winner'''
    p0 = random.random()
    if p0 < 0.5:
      if self.silent is not True:
        print('{0} wins the shootout.'.format(self.team_a.name))
      self.team_a.score += 1
    else:
      if self.silent is not True:
        print('{0} wins the shootout.'.format(self.team_b.name))
      self.team_b.score += 1

  def extra_time(self, time_step):
    '''Determine if extra time is needed.Play 2x10 minute periods of events'''
    if self.extra_time_required is True:
      if self.team_a.score == self.team_b.score:
        print('The match is going to extra time.')
        self.half_time()
        self.time = 70 * 60
        self.stopclock_time = stopclock(self.time)
        tane = (self.time) + time_until_next_event()
        self.play_half(self.time + (10*60), time_step, tane=tane)
        self.half_time()
        self.time = (70 * 60) + (10*60)
        tane = (self.time) + time_until_next_event()
        self.play_half(self.time + (10*60), time_step, tane=tane)
        self.full_time()
        if self.team_a.score == self.team_b.score:
          self.shootout()

  def play(self, time_step=0):
    '''Play through various stages of matches.  Update timekeeping.'''
    self.banner()
    self.lineup()
    self.pause()
    self.play_half(self.first_half_length, time_step)
    self.half_time()
    second_half_end = self.first_half_length + self.second_half_length
    second_half_tane = (self.first_half_length) + time_until_next_event()
    self.play_half(second_half_end, time_step, tane=second_half_tane)
    self.full_time()
    self.extra_time(time_step)
    self.banner_end()

  def get_scorers(self):
    '''Call team methods to collate scorer data.  Print tables.'''
    self.team_a.get_scorer_table()
    self.team_b.get_scorer_table()
    if self.silent is not True:
      print(self.team_a.scorer_table)
      print(self.team_b.scorer_table)

  def half_time(self):
    '''Reset added time back to 35 minutes.  Update scorer data.  Let user manage team'''
    self.time = 35 * 60
    self.first_half_length = 35 * 60
    self.stopclock_time = stopclock(self.time)
    self.get_scorers()
    self.pause()

  def full_time(self):
    '''Update scorer stats.  Print final result'''
    self.get_scorers()
    if self.silent is not True:
      print('Full time score is:\n{0}'.format(self.get_score().replace('Score is now ', '')))

  def event(self):
    '''Instatiate event.  Run it'''
    event = Event(self)
    event.run(self)
    self.print_event_list(event.pl)
    self.abandon()

  def get_score(self):
    '''Get user friendly string of match score'''
    return 'Score is now {0} {1} {2} {3})'.format(
      self.team_a.name, self.team_a.score,
      self.team_b.name, self.team_b.score
    )

if __name__ == "__main__":

  team_a = MatchTeam(Team('a', 'a'))
  team_b = MatchTeam(Team('b', 'b'))
  match = Match(team_a, team_b, datetime.date(2020, 1, 1), True, False)
  # match.play(0.1)
  # match = Match(team_a, team_b, datetime.date(2020, 1, 1), True, False)
  # match.play()
  import cProfile
  import pstats
  cProfile.run('match.play()', 'profile1.txt')
  p = pstats.Stats('profile1.txt').sort_stats('tottime').reverse_order()
  p.print_stats()
