
import random
import numpy as np

import default
from player import Player

class Team():
  def __init__(self, name, manager, players=None):
    self.name = name
    self.manager = manager
    if players is None:
      random.seed(name)
      self.players = [Player() for i in range(14)]
    else:
      self.players = players
    self.overall = self.get_overall()

  def __repr__(self):
    ps = 'team: {0} rating:{1}\n'.format(self.name, self.overall)
    ps += '\n'.join([p.__repr__() for p in self.players])
    ps += '\n'
    return ps

  def __str__(self):
    return self.__repr__()

  def get_overall(self):
    return round(np.mean([p.overall for p in self.players]), 2)

