
import numpy as np
import random

import default

def random_0_100_normal(mean, sd):
  return int(max(min(round(np.random.normal(mean, sd), 0), 100), 0))

class Player():
  def __init__(self):
    self.first_name = random.choice(default.first_names)
    self.last_name = random.choice(default.last_names)
    self.passing = random_0_100_normal(80, 20)
    self.shooting = random_0_100_normal(70, 20)
    self.fitness = random_0_100_normal(70, 20)
    self.overall = int(round(np.mean([
      self.passing,
      self.shooting,
      self.fitness
    ])))
    self.goals = 0
    self.points = 0
    self.score = 0
    self.position = random.choice(['GK', 'FB', 'HB', 'MI', 'HF', 'FF'])

  def __repr__(self):
    # ps = '{0} {1}\noverall:{2:d}'.format(self.first_name, self.last_name, self.overall)
    ps = '{0} {1}'.format(self.first_name[0], self.last_name)
    return ps

  def __str__(self):
    return self.__repr__()

  def update_score(self):
    self.score = (self.goals * 3) + self.points

