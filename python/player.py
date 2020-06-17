
import numpy as np
import random
import names

import default
from injury import Injury
from suspension import Suspension

def x_0_100_cap(x):
  return int(max(min(round(x, 0), 100), 0))

def random_0_100_normal(mean, sd):
  return x_0_100_cap(np.random.normal(mean, sd))

class Player():
  def __init__(self, team=None):
    self.first_name = names.get_first_name(gender='male')
    self.last_name = names.get_last_name()
    self.team = team
    self.defending = random_0_100_normal(80, 20)
    self.passing = random_0_100_normal(80, 20)
    self.shooting = random_0_100_normal(70, 20)
    self.fitness = random_0_100_normal(70, 20)
    self.condition = float(min(self.fitness, random_0_100_normal(70, 20)))
    self.get_overall()
    self.goals = 0
    self.points = 0
    self.scoren = 0
    self.score = ''
    self.assists = 0
    self.position = random.choice(['GK', 'FB', 'HB', 'MI', 'HF', 'FF'])
    self.lineup = 0
    self.minutes = 0
    self.match_rating = 5.0
    self.average_match_rating = 5.0
    self.match_ratings = []
    self.cards = []
    self.injury = Injury()
    self.suspension = Suspension()

  def __repr__(self):
    ps = '{0} {1}'.format(self.first_name[0], self.last_name)
    return ps

  def __str__(self):
    return self.__repr__()

  def __lt__(self, other):
    return(self.__repr__() < other.__repr__())

  def get_overall(self):
    self.overall = int(round(np.mean([
      self.defending,
      self.passing,
      self.shooting,
      self.fitness
    ])))

  def reset_match_stats(self):
    self.goals = 0
    self.points = 0
    self.update_score()
    self.minutes = 0
    self.assists = 0
    self.match_rating = 0.5
    self.cards = []

  def update_score(self):
    self.scoren = (self.goals * 3) + self.points
    self.score = '{0}-{1} ({2})'.format(self.goals, self.points, self.scoren)
    if len(self.match_ratings) > 0:
      self.average_match_rating = round(np.mean(self.match_ratings), 2)

  def gain_injury(self, current_date):
    self.injury.gain(current_date)

  def check_injury(self, current_date):
    if self.injury.return_date is not None:
      if self.injury.return_date <= current_date:
        self.reset_injury()

  def reset_injury(self):
    self.injury.reset()

  def gain_suspension(self, status, current_date):
    self.suspension.gain(status, current_date)

  def check_suspension(self, current_date):
    if self.suspension.return_date is not None:
      if self.suspension.return_date <= current_date:
        self.reset_suspension()

  def reset_suspension(self):
    self.suspension.reset()

  def assist(self):
    self.match_rating += 0.2
    self.assists += 1

  def turnover(self):
   self.match_rating += 0.5

  def save_goal(self):
   self.match_rating += 1.5

  def score_point(self):
   self.points += 1
   self.match_rating += 0.5
   self.update_score()

  def score_goal(self):
   self.goals += 1
   self.match_rating += 1.0
   self.update_score()

if __name__=="__main__":

  player = Player('a')
  print(player)

  # test injuries
  import datetime
  current_date = datetime.date(2020, 1, 1)
  for i in range(100):
    player.gain_injury(current_date)
    print(player.injury)

