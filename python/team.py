
import random

import default

class Team():
  def __init__(self, name, manager, players=None):
    self.name = name
    self.manager = manager
    if players is None:
      self.players = {}
      random.seed(name)
      for i in range(14):
        self.players[i] = '%s %s' % (
          random.choice(default.first_names), random.choice(default.last_names)
        )
    else:
      self.players = players

