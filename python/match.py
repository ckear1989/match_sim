
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

  def throw_in(self):
    if random.random() < 0.5:
      posession_player = random.choice(self.team_a.players)
      team = self.team_a.name
    else:
      posession_player = random.choice(self.team_b.players)
      team = self.team_b.name
    print('{0} The referee throws the ball in.  {1} wins posession for {2}'.format(self.stopclock_time, posession_player, team))

  def play_half(self, end_time, time_step, tane=time_until_next_event()):
    while self.time <= end_time:
      self.time += 1
      self.stopclock_time = stopclock(self.time)
      if self.time % 1e3 == 0:
        printc(self.stopclock_time)
      if self.time % 60e3 == 0:
        printc(self.stopclock_time)
      if self.time == (tane*1e3):
        self.event()
        tune = time_until_next_event()
        tane += tune
      time.sleep(time_step)

  def play(self, time_step=0):
    self.throw_in()
    self.play_half(self.first_half_length, time_step)
    self.half_time()
    second_half_end = self.first_half_length + self.second_half_length
    second_half_tane = (self.first_half_length*1e-3) + time_until_next_event()
    self.throw_in()
    self.play_half(second_half_end, time_step, tane=second_half_tane)
    self.full_time()

  def half_time(self, time_step=1):
    for player in self.team_a.players:
      print('{0} {1}'.format(player, player.score))
    for player in self.team_b.players:
      print('{0} {1}'.format(player, player.score))
    time.sleep(time_step)

  def full_time(self):
    self.half_time()
    self.team_a.played += 1
    self.team_b.played += 1
    if self.team_a.score > self.team_b.score:
      self.team_a.points += 2
    elif self.team_a.score < self.team_b.score:
      self.team_b.points += 2
    else:
      self.team_a.points += 1
      self.team_b.points += 1

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
    return 'Score is now {0} {1} {2} {3}'.format(
      self.team_a.name, self.team_a.score, self.team_b.name, self.team_b.score)

if __name__ == "__main__":

  team_a = Team('a', 'a')
  team_b = Team('b', 'b')
  match = Match(team_a, team_b, datetime.date(2020, 1, 1))
  match.play(0)

