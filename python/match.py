
import datetime
import random
import time
import math
import copy
import sys
import os
import progressbar
import numpy as np
import keyboard
import pyfiglet

from team import Team
from match_team import MatchTeam
from event import Event

def printc(x):
  print('{0}\r'.format(x), end='')

def stopclock(a):
  t = datetime.timedelta(seconds=a)
  s = t.seconds
  m, s = divmod(s, 60)
  # m = int(math.floor(s / 60))
  # s = s - 60 * m
  return '%02d:%02d' % (m, s)

def time_until_next_event(mean=60, sd=10):
  return max(round(np.random.normal(mean, sd), 0), 1)

class Match():
  def __init__(self, team_a, team_b, date, silent, extra_time_required):
    self.team_a = MatchTeam(team_a)
    self.team_b = MatchTeam(team_b)
    self.date = date
    self.silent = silent
    self.extra_time_required = extra_time_required
    self.time = 0
    self.stopclock_time = stopclock(self.time*1e-0)
    self.first_half_length = 35 * 60e0
    self.second_half_length = 35 * 60e0
    self.get_progressbar(80*60e0)
    random.seed()

  def __repr__(self):
    ps = '{0} {1} {2} {3}'.format(self.team_a.name, self.team_a.score, self.team_b.name, self.team_b.score)
    return ps

  def __str__(self):
    return self.__repr__()

  def throw_in(self):
    if random.random() < 0.5:
      posession_player = random.choice(self.team_a)
      team = self.team_a.name
    else:
      posession_player = random.choice(self.team_b)
      team = self.team_b.name
    print('{0} The referee throws the ball in.{1} wins posession for {2}'.format(self.stopclock_time, posession_player, team))

  def update_team_condition(self):
    for x in self.team_a.playing + self.team_b.playing:
      x.minutes += 1
      x.condition = max((x.condition - 0.8), 0)
      x.get_overall()
    self.team_a.get_overall()
    self.team_b.get_overall()

  def added_time(self):
    at = random.choice(range(1, 7))
    print('{0} {1} minutes added time indicated by the linesman.'.format(self.stopclock_time, at))
    at = float(at)
    at += np.random.normal(0.5, 0.1)
    at = at * 60e0
    return at

  def play_half(self, end_time, time_step, tane=time_until_next_event()):
    self.throw_in()
    at = 0
    while self.time < (end_time + at):
      self.time += 1
      if self.time % 1e0 == 0:
        self.stopclock_time = stopclock(self.time*1e-0)
        printc(self.stopclock_time)
        if keyboard.is_pressed('space') is True:
          self.pause()
      if self.time % 60e0 == 0:
        if self.silent is True:
          self.progressbar.update(self.time)
        else:
          print(self.stopclock_time)
        self.update_team_condition()
      if self.time % (34 * 60e0) == 0:
        at = self.added_time()
      if self.time == (tane*1e0):
        self.event()
        tune = time_until_next_event()
        tane += tune
      if time_step > 0:
        time.sleep(time_step)
    print('{0} And that\'s the end of the half'.format(self.stopclock_time))

  def abandon(self):
    n_team_a = len(self.team_a.playing)
    n_team_b = len(self.team_b.playing)
    if (n_team_a < 11) or (n_team_b < 11):
      self.team_a.reset_match_stats()
      self.team_b.reset_match_stats()
      if n_team_a < 11:
        self.team_b.points = 1
      if n_team_b < 11:
        self.team_a.points = 1
      self.time = 80*60e0

  def lineup(self):
    self.team_a.lineup_check()
    self.team_b.lineup_check()
    self.team_a.lineup_change()
    self.team_b.lineup_change()

  def pause(self):
    self.team_a.manage()
    self.team_b.manage()

  def banner(self):
    banner = pyfiglet.figlet_format('{0} vs {1} {2}\n'.format(self.team_a.name, self.team_b.name, self.date))
    print(banner)

  def banner_end(self):
    banner = pyfiglet.figlet_format('{0} {1}\n'.format(self.get_score().replace('Score is now ', ''), self.date))
    print(banner)

  def end_progressbar(self):
    if self.silent is True:
      sys.stdout = self.stdout
      self.progressbar.finish()

  def shootout(self):
    p0 = random.random()
    if p0 < 0.5:
      print('{0} wins the shootout.'.format(self.team_a.name))
      self.team_a.score += 1
    else:
      print('{0} wins the shootout.'.format(self.team_b.name))
      self.team_b.score += 1

  def get_progressbar(self, end_time):
    if self.silent is True:
      self.progressbar = progressbar.ProgressBar(maxval=end_time, \
        widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
      self.progressbar.start()
      self.stdout = sys.stdout
      f = open(os.devnull, 'w')
      sys.stdout = f

  def extra_time(self, time_step):
    if self.extra_time_required is True:
      if self.team_a.score == self.team_b.score:
        print('The match is going to extra time.')
        self.get_progressbar(100*60e0)
        self.half_time()
        self.time = 70 * 60e0
        self.stopclock_time = stopclock(self.time*1e0)
        tane = (self.time*1e-0) + time_until_next_event()
        self.play_half(self.time + (10*60e0), time_step, tane=tane)
        self.half_time()
        self.time = (70 * 60e0) + (10*60e1)
        tane = (self.time*1e-0) + time_until_next_event()
        self.play_hailf(self.time + (10*60e0), time_step, tane=tane)
        self.full_time()
        if self.team_a.score == self.team_b.score:
          self.shootout()

  def play(self, time_step=0):
    self.banner()
    self.lineup()
    self.pause()
    self.play_half(self.first_half_length, time_step)
    self.half_time()
    second_half_end = self.first_half_length + self.second_half_length
    second_half_tane = (self.first_half_length*1e-0) + time_until_next_event()
    self.play_half(second_half_end, time_step, tane=second_half_tane)
    self.full_time()
    self.extra_time(time_step)
    self.banner_end()
    self.end_progressbar()

  def get_scorers(self):
    self.team_a.get_scorer_table()
    self.team_b.get_scorer_table()
    print(self.team_a.scorer_table)
    print(self.team_b.scorer_table)

  def half_time(self):
    self.time = 35 * 60e0
    self.first_half_length = 35 * 60e0
    self.stopclock_time = stopclock(self.time*1e-0)
    self.get_scorers()
    self.pause()

  def full_time(self):
    self.get_scorers()
    print('Full time score is:\n{0}'.format(self.get_score().replace('Score is now ', '')))

  def event(self):
    event = Event(self)
    event.run()

  def get_score(self):
    return 'Score is now {0} {1}-{2} ({3}) {4} {5}-{6} ({7})'.format(
      self.team_a.name, self.team_a.goals, self.team_a.points, self.team_a.score,
      self.team_b.name, self.team_b.goals, self.team_b.points, self.team_b.score
    )

if __name__ == "__main__":

  import cProfile
  import pstats
  team_a = Team('a', 'a')
  team_b = Team('b', 'b')
  match = Match(team_a, team_b, datetime.date(2020, 1, 1), True, False)
  cProfile.run('match.play();print(match)', 'profile4.txt')
  p0 = pstats.Stats('profile0.txt')
  p0.strip_dirs().sort_stats('time').print_stats(20)
  p1 = pstats.Stats('profile1.txt')
  p1.strip_dirs().sort_stats('time').print_stats(20)
  p2 = pstats.Stats('profile2.txt')
  p2.strip_dirs().sort_stats('time').print_stats(20)
  p3 = pstats.Stats('profile3.txt')
  p3.strip_dirs().sort_stats('time').print_stats(20)
  p4 = pstats.Stats('profile4.txt')
  p4.strip_dirs().sort_stats('time').print_stats(20)
  # match.play()
  # match = Match(team_a, team_b, datetime.date(2020, 1, 1), True, False)
  # match.play()

