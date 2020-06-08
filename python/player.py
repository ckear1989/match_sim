
import numpy as np
import random

import default

def x_0_100_cap(x):
  return int(max(min(round(x, 0), 100), 0))

def random_0_100_normal(mean, sd):
  return x_0_100_cap(np.random.normal(mean, sd))

class Player():
  def __init__(self):
    self.first_name = random.choice(default.first_names)
    self.last_name = random.choice(default.last_names)
    self.defending = random_0_100_normal(80, 20)
    self.passing = random_0_100_normal(80, 20)
    self.shooting = random_0_100_normal(70, 20)
    self.fitness = random_0_100_normal(70, 20)
    self.get_overall()
    self.goals = 0
    self.points = 0
    self.score = 0
    self.position = random.choice(['GK', 'FB', 'HB', 'MI', 'HF', 'FF'])
    self.lineup = 0

  def __repr__(self):
    ps = '{0} {1}'.format(self.first_name[0], self.last_name)
    return ps

  def __str__(self):
    return self.__repr__()

  def get_overall(self):
    self.overall = int(round(np.mean([
      self.defending,
      self.passing,
      self.shooting,
      self.fitness
    ])))

  def update_score(self):
    self.score = (self.goals * 3) + self.points

