
import datetime
import random
import time

from team import Team

def print0(a):
  print(a, end=' ')

class Match():
  def __init__(self, team_a, team_b, date):
    self.team_a = team_a
    self.team_b = team_b
    self.date = date
    self.time = 0
    self.team_a_score = 0
    self.team_b_score = 0
    random.seed()

  def __repr__(self):
    return self.__str__()

  def __str__(self):
    ps = '{0} {1} {2} {3}'.format(self.team_a.name, self.team_a_score, self.team_b.name, self.team_b_score)
    return ps

  def play(self, time_step=0.1):
    while self.time <= 35:
      self.time += 1
      print0(self.time)
      if self.time % 5 == 0:
        self.event()
      time.sleep(time_step)
      print()
    self.half_time()
    while self.time <= 70:
      self.time += 1
      print0(self.time)
      if self.time % 5 == 0:
        self.event()
      time.sleep(time_step)
      print()
    self.full_time()

  def half_time(self, time_step=1):
    time.sleep(time_step)

  def full_time(self):
    self.half_time()

  def event(self):
    if random.random() < 0.5:
      self.team_a_score += 1
      print0('Team {0} scores.'.format(self.team_a.name))
    else:
      self.team_b_score += 1
      print0('Team {0} scores.'.format(self.team_b.name))
    self.print_score()

  def print_score(self):
      print0('Score is now {0} {1} {2} {3}'.format(self.team_a.name, self.team_a_score, self.team_b.name, self.team_b_score))

if __name__ == "__main__":

  team_a = Team('a', 'a')
  team_b = Team('b', 'b')
  match = Match(team_a, team_b, datetime.date(2020,1,1))
  match.play()

