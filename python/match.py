
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

def printc(x):
  print('{0}\r'.format(x), end='')

def stopclock(a):
  t = datetime.timedelta(milliseconds=a)
  s = t.seconds
  m = int(math.floor(s / 60))
  s = s - 60 * m
  return '%02d:%02d' % (m, s)

def time_until_next_event(mean=60, sd=10):
  return max(round(np.random.normal(mean, sd), 0), 1)

class Match():
  def __init__(self, team_a, team_b, date, silent, control=[]):
    self.team_a = MatchTeam(team_a)
    self.team_b = MatchTeam(team_b)
    self.date = date
    self.silent = silent
    self.control = control
    self.time = 0
    self.stopclock_time = stopclock(self.time)
    self.first_half_length = 35 * 60e3
    self.second_half_length = 35 * 60e3
    if self.silent is True:
      self.progressbar = progressbar.ProgressBar(maxval=80*60e3, \
        widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
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
    at = at * 60e3
    return at

  def play_half(self, end_time, time_step, tane=time_until_next_event()):
    self.throw_in()
    at = 0
    while self.time < (end_time + at):
      self.time += 1
      self.stopclock_time = stopclock(self.time)
      if self.time % 1e3 == 0:
        printc(self.stopclock_time)
        if keyboard.is_pressed('space') is True:
          self.pause()
      if self.time % 60e3 == 0:
        if self.silent is True:
          self.progressbar.update(self.time)
        else:
          print(self.stopclock_time)
        self.update_team_condition()
      if self.time % (34 * 60e3) == 0:
        at = self.added_time()
      if self.time == (tane*1e3):
        self.event()
        tune = time_until_next_event()
        tane += tune
      time.sleep(time_step)
    print('{0} And that\'s the end of the half'.format(self.stopclock_time))

  def lineup(self):
    if len(self.control) > 0:
      x = input('{0}\n'.format('\t'.join(['(l)ineup', '(c)ontinue', '(e)xit']))).strip()
      if x in ['l', 'lineup']:
        if 'a' in self.control:
          self.team_a.lineup_change()
        if 'b' in self.control:
          self.team_b.lineup_change()
      elif x in ['c', 'continue']:
        pass
      elif x in ['e', 'exit']:
        exit()
      else:
        self.lineup()

  def pause(self):
    if len(self.control) > 0:
      x = input('{0}\n'.format('\t'.join(['(m)anage', '(c)ontinue', '(e)xit']))).strip()
      if x in ['m', 'manage']:
        if 'a' in self.control:
          self.team_a.manage()
        if 'b' in self.control:
          self.team_b.manage()
      elif x in ['c', 'continue']:
        pass
      elif x in ['e', 'exit']:
        exit()
      else:
        self.pause()

  def banner(self):
    if self.silent is True:
      self.progressbar.start()
      self.stdout = sys.stdout
      f = open(os.devnull, 'w')
      sys.stdout = f
    banner = pyfiglet.figlet_format('{0} vs {1} {2}\n'.format(self.team_a.name, self.team_b.name, self.date))
    print(banner)

  def banner_end(self):
    banner = pyfiglet.figlet_format('{0} {1}\n'.format(self.get_score().replace('Score is now ', ''), self.date))
    print(banner)
    if self.silent is True:
      sys.stdout = self.stdout
      self.progressbar.finish()

  def play(self, time_step=0):
    self.banner()
    self.team_a.lineup_check()
    self.team_b.lineup_check()
    self.lineup()
    self.pause()
    self.team_a.update_positions()
    self.team_b.update_positions()
    self.play_half(self.first_half_length, time_step)
    self.half_time()
    second_half_end = self.first_half_length + self.second_half_length
    second_half_tane = (self.first_half_length*1e-3) + time_until_next_event()
    self.play_half(second_half_end, time_step, tane=second_half_tane)
    self.full_time()
    self.banner_end()

  def get_scorers(self):
    self.team_a.get_scorer_table()
    self.team_b.get_scorer_table()
    print(self.team_a.scorer_table)
    print(self.team_b.scorer_table)

  def half_time(self):
    self.time = 35 * 60e3
    self.first_half_length = 35 * 60e3
    self.stopclock_time = stopclock(self.time)
    self.get_scorers()
    self.pause()

  def full_time(self):
    self.get_scorers()
    print('Full time score is:\n{0}'.format(self.get_score().replace('Score is now ', '')))

  def event(self):
    print(self.stopclock_time, end=' ')
    a_tot = self.team_a.overall
    b_tot = self.team_b.overall
    p_team_a_chance = a_tot / (a_tot+b_tot)
    if random.random() < p_team_a_chance:
      self.team_a.chance(self.team_b)
    else:
      self.team_b.chance(self.team_a)
    print(self.get_score())

  def get_score(self):
    return 'Score is now {0} {1}-{2} ({3}) {4} {5}-{6} ({7})'.format(
      self.team_a.name, self.team_a.goals, self.team_a.points, self.team_a.score,
      self.team_b.name, self.team_b.goals, self.team_b.points, self.team_b.score
    )

if __name__ == "__main__":

  team_a = Team('a', 'a')
  team_b = Team('b', 'b')
  match = Match(team_a, team_b, datetime.date(2020, 1, 1), False, control='a')
  match.play()
  match = Match(team_a, team_b, datetime.date(2020, 1, 1), True)
  match.play()

