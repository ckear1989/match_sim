
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
      self.players = [Player() for i in range(30)]
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
    self.get_player_table()
    self.get_lineup()

  def __repr__(self):
    ps = 'team: {0} rating:{1}\n'.format(self.name, self.overall)
    ps += self.player_table.__str__()
    ps += '\n'
    return ps

  def __str__(self):
    return self.__repr__()

  def get_lineup(self):
    self.goalkeepers = [x for x in self.players if x.position in ['GK']]
    self.full_backs = [x for x in self.players if x.position in ['FB']]
    self.half_backs = [x for x in self.players if x.position in ['HB']]
    self.midfielders = [x for x in self.players if x.position in ['MI']]
    self.full_forwards = [x for x in self.players if x.position in ['FF']]
    self.half_forwards = [x for x in self.players if x.position in ['HF']]
    while len(self.goalkeepers) < 2:
     random.choice(self.players).position = 'GK'
    while len(self.full_backs) < 3:
     random.choice([x for x in self.players if x.position not in ['GK']]).position = 'FB'
     self.get_lineup()
    while len(self.half_backs) < 3:
     random.choice([x for x in self.players if x.position not in ['GK', 'FB']]).position = 'HB'
     self.get_lineup()
    while len(self.midfielders) < 2:
     random.choice([x for x in self.players if x.position not in ['GK', 'FB', 'HB']]).position = 'MI'
     self.get_lineup()
    while len(self.half_forwards) < 3:
     random.choice([x for x in self.players if x.position not in ['GK', 'FB', 'HB', 'HF']]).position = 'HF'
     self.get_lineup()
    while len(self.full_forwards) < 3:
     random.choice([x for x in self.players if x.position not in ['GK', 'FB', 'HB', 'HF']]).position = 'FF'
     self.get_lineup()
    self.defenders = self.full_backs + self.half_backs
    self.forwards = self.full_forwards + self.half_forwards
    self.lineup = {}
    player = random.choice(self.goalkeepers)
    player.lineup = 1
    self.lineup[1] = player
    for i in [2, 3, 4]:
      player = random.choice([x for x in self.full_backs if x not in self.lineup.values()])
      player.lineup = i
      self.lineup[i] = player
    for i in [5, 6, 7]:
      player = random.choice([x for x in self.half_backs if x not in self.lineup.values()])
      player.lineup = i
      self.lineup[i] = player
    for i in [8, 9]:
      player = random.choice([x for x in self.midfielders if x not in self.lineup.values()])
      player.lineup = i
      self.lineup[i] = player
    for i in [10, 11, 12]:
      player = random.choice([x for x in self.half_forwards if x not in self.lineup.values()])
      player.lineup = i
      self.lineup[i] = player
    for i in [13, 14, 15]:
      player = random.choice([x for x in self.full_forwards if x not in self.lineup.values()])
      player.lineup = i
      self.lineup[i] = player
    player = random.choice([x for x in self.goalkeepers if x not in self.lineup.values()])
    player.lineup = 16
    self.lineup[i] = player
    for i in [17, 18, 19, 20]:
      player = random.choice([x for x in self.players if x not in self.lineup.values()])
      player.lineup = i
      self.lineup[i] = player
    self.get_player_table()

  def get_player_table(self):
    x = PrettyTable()
    x.add_column('last name', [x.last_name for x in self.players])
    x.add_column('first name', [x.first_name for x in self.players])
    x.add_column('position', [x.position for x in self.players])
    x.add_column('lineup', [x.lineup for x in self.players])
    x.add_column('overall', [x.overall for x in self.players])
    x.add_column('passing', [x.passing for x in self.players])
    x.add_column('shooting', [x.shooting for x in self.players])
    x.add_column('fitness', [x.fitness for x in self.players])
    x.sortby = 'lineup'
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

if __name__=="__main__":
  team = Team('a', 'a')
  print(team)


