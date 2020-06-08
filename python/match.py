
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
  def __init__(self, team_a, team_b, date, silent):
    self.team_a = MatchTeam(team_a)
    self.team_b = MatchTeam(team_b)
    self.date = date
    self.silent = silent
    self.time = 0
    self.stopclock_time = stopclock(self.time)
    self.first_half_length = 35 * 60e3
    self.second_half_length = 35 * 60e3
    if self.silent is True:
      self.progressbar = progressbar.ProgressBar(maxval=70*60e3, \
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

  def play_half(self, end_time, time_step, tane=time_until_next_event()):
    self.throw_in()
    while self.time < end_time:
      self.time += 1
      self.stopclock_time = stopclock(self.time)
      if self.time % 1e3 == 0:
        printc(self.stopclock_time)
      if self.time % 60e3 == 0:
        if self.silent is True:
          self.progressbar.update(self.time)
        else:
          print(self.stopclock_time)
      if self.time == (tane*1e3):
        self.event()
        tune = time_until_next_event()
        tane += tune
      time.sleep(time_step)
      if self.silent is False:
        if keyboard.is_pressed('space') is True:
          self.pause()

  def pause(self):
    if self.silent is False:
      x = input('{0}\n'.format('\t'.join(['(l)ineup', '(c)ontinue', '(e)xit']))).strip()
      if x in ['l', 'lineup']:
        self.team_a.lineup_change()
      elif x in ['c', 'continue']:
        pass
      elif x in ['e', 'exit']:
        exit()
      else:
        self.pause()

  def play(self, time_step=0):
    self.team_a.lineup_check()
    self.team_b.lineup_check()
    self.pause()
    if self.silent is True:
      self.progressbar.start()
      stdout = sys.stdout
      f = open(os.devnull, 'w')
      sys.stdout = f
    self.play_half(self.first_half_length, time_step)
    self.half_time()
    second_half_end = self.first_half_length + self.second_half_length
    second_half_tane = (self.first_half_length*1e-3) + time_until_next_event()
    self.play_half(second_half_end, time_step, tane=second_half_tane)
    self.full_time()
    if self.silent is True:
      sys.stdout = stdout
      self.progressbar.finish()

  def get_scorers(self):
    team_a_scorers = sorted(self.team_a, key=lambda x: -x.score)
    team_b_scorers = sorted(self.team_b, key=lambda x: -x.score)
    for player in [x for x in team_a_scorers if x.score > 0]:
      print('{0} {1}-{2} ({3})'.format(player, player.goals, player.points, player.score))
    for player in [x for x in team_b_scorers if x.score > 0]:
      print('{0} {1}-{2} ({3})'.format(player, player.goals, player.points, player.score))

  def half_time(self, time_step=1):
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
      self.team_a.chance()
    else:
      self.team_b.chance()
    print(self.get_score())

  def get_score(self):
    return 'Score is now {0} {1}-{2} ({3}) {4} {5}-{6} ({7})'.format(
      self.team_a.name, self.team_a.goals, self.team_a.points, self.team_a.score,
      self.team_b.name, self.team_b.goals, self.team_b.points, self.team_b.score
    )

if __name__ == "__main__":

  team_a = Team('a', 'a')
  team_b = Team('b', 'b')
  match = Match(team_a, team_b, datetime.date(2020, 1, 1), False)
  match.play()
  match = Match(team_a, team_b, datetime.date(2020, 1, 1), True)
  match.play()

