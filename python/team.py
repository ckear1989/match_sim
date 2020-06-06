
import random
import numpy as np
from prettytable import PrettyTable

import default
from player import Player

class Team():
  def __init__(self, name, manager, players=None):
    self.name = name
    self.manager = manager
    if players is None:
      random.seed(name)
      self.players = [Player() for i in range(20)]
    else:
      self.players = players
    self.overall = self.get_overall()
    self.score =  0
    self.played = 0
    self.goals = 0
    self.points = 0
    self.league_win = 0
    self.league_loss = 0
    self.league_draw = 0
    self.league_points = 0
    self.goalkeepers = [x for x in self.players if x.position in ['GK']]
    self.defenders = [x for x in self.players if x.position in ['FB', 'HB']]
    self.midfielders = [x for x in self.players if x.position in ['MI']]
    self.forwards = [x for x in self.players if x.position in ['FF', 'HF']]
    self.get_player_table()

  def __repr__(self):
    ps = 'team: {0} rating:{1}\n'.format(self.name, self.overall)
    ps += self.player_table.__str__()
    ps += '\n'
    return ps

  def __str__(self):
    return self.__repr__()

  def get_player_table(self):
    x = PrettyTable()
    x.add_column('last name', [x.last_name for x in self.players])
    x.add_column('first name', [x.first_name for x in self.players])
    x.add_column('overall', [x.overall for x in self.players])
    self.player_table = x

  def get_overall(self):
    return round(np.mean([p.overall for p in self.players]), 2)

  def choose_player(self, p0, p1, p2):
    p = random.random()
    if p < p0:
      player = random.choice(self.goalkeepers)
    elif p < (p0+p1):
      player = random.choice(self.defenders)
    elif p < (p0+p1+p2):
      player = random.choice(self.midfielders)
    else:
      player = random.choice(self.forwards)
    return player

  def chance(self):
    posession_player = self.choose_player(0.01, 0.2, 0.4)
    shooting_player = self.choose_player(0.01, 0.1, 0.3)
    print('Team {0} has a chance with {1} on the ball.'.format(self.name, posession_player), end='')
    if random.random() < (posession_player.passing/100):
      print('He passes the ball to {0}.'.format(shooting_player), end='')
      if random.random() < 0.8:
        print('He shoots for a point.', end='')
        if random.random() < (shooting_player.shooting/100):
          shooting_player.points += 1
          print('And he scores.', end='')
        else:
          print('But he misses.', end='')
      else:
        print('He shoots for a goal.', end='')
        if random.random() < (shooting_player.shooting/100):
          shooting_player.goals += 1
          print('And he scores.', end='')
        else:
          print('But he misses.', end='')
    else:
        print('But he loses posession with the kick.', end='')
    shooting_player.update_score()
    self.update_score()

  def update_score(self):
    self.goals = sum([x.goals for x in self.players])
    self.points = sum([x.points for x in self.players])
    self.score = (self.goals * 3) + self.points

