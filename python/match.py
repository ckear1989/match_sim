
import datetime
import random
import time
import math
import numpy as np

from team import Team

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
  def __init__(self, team_a, team_b, date):
    self.team_a = team_a
    self.team_b = team_b
    self.date = date
    self.time = 0
    self.stopclock_time = stopclock(self.time)
    self.team_a_score = 0
    self.team_b_score = 0
    self.first_half_length = 35 * 60e3
    self.second_half_length = 35 * 60e3
    random.seed()

  def __repr__(self):
    return self.__str__()

  def __str__(self):
    ps = '{0} {1} {2} {3}'.format(self.team_a.name, self.team_a_score, self.team_b.name, self.team_b_score)
    return ps

  def play_half(self, end_time, time_step, tane=time_until_next_event()):
    while self.time <= end_time:
      self.time += 1
      if self.time % 1e3 == 0:
        self.stopclock_time = stopclock(self.time)
        printc(self.stopclock_time)
      # if self.time % (tane*1e3) == 0:
      if self.time == (tane*1e3):
        self.event()
        tune = time_until_next_event()
        tane += tune
      time.sleep(time_step)

  def play(self, time_step=1e-4):
    self.play_half(self.first_half_length, time_step)
    self.half_time()
    second_half_end = self.first_half_length + self.second_half_length
    second_half_tane = (self.first_half_length*1e-3) + time_until_next_event()
    self.play_half(second_half_end, time_step, tane=second_half_tane)
    self.full_time()

  def half_time(self, time_step=1):
    time.sleep(time_step)

  def full_time(self):
    self.half_time()

  def event(self):
    if random.random() < 0.5:
      self.team_a_score += 1
      print('{0} Team {1} scores'.format(self.stopclock_time, self.team_a.name))
    else:
      self.team_b_score += 1
      print('{0} Team {1} scores'.format(self.stopclock_time, self.team_b.name))
    self.print_score()

  def print_score(self):
      print('{0} Score is now {1} {2} {3} {4}'.format(self.stopclock_time, self.team_a.name, self.team_a_score, self.team_b.name, self.team_b_score))

if __name__ == "__main__":

  team_a = Team('a', 'a')
  team_b = Team('b', 'b')
  print(team_a)
  match = Match(team_a, team_b, datetime.date(2020,1,1))
  match.play(0)

