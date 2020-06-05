
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
    self.score =  0

  def __repr__(self):
    ps = 'team: {0} rating:{1}\n'.format(self.name, self.overall)
    ps += '\n'.join([p.__repr__() for p in self.players])
    ps += '\n'
    return ps

  def __str__(self):
    return self.__repr__()

  def get_overall(self):
    return round(np.mean([p.overall for p in self.players]), 2)

  def chance(self):
    posession_player = random.choice(self.players)
    shooting_player = random.choice([x for x in self.players if x!= posession_player])
    print('Team {0} has a chance with {1} on the ball.'.format(self.name, posession_player), end='')
    if random.random() < (posession_player.passing/100):
      print('He passes the ball to {0}.'.format(shooting_player), end='')
      if random.random() < (shooting_player.shooting/100):
        self.score += 1
        print('And he scores.', end='')
      else:
        print('But he misses.', end='')
    else:
        print('But he loses posession with the kick.', end='')
