'''Class to represent team'''

import random
import numpy as np
from prettytable import PrettyTable
import names

from match_sim.cl.player import Player, Score
from match_sim.cl.training import Training, train

class TeamIterator:
  '''https://thispointer.com/python-how-to-make-a-class-
     iterable-create-iterator-class-for-it/
  '''
  def __init__(self, ateam):
    # Team object reference
    self._team = ateam
    # member variable to keep track of current index
    self._index = 0

  def __next__(self):
    ''''Returns the next value from team object's lists '''
    if self._index < len(self._team.players):
      result = self._team.players[self._index]
      self._index += 1
      return result
    # End of Iteration
    raise StopIteration

class Team():
  '''Store data on team.  Container for players'''
  def __init__(self, name, manager, players=None, control=False):
    self.name = name
    self.manager = manager
    self.coach = names.get_full_name()
    if players is None:
      random.seed(name)
      self.players = [Player(name) for i in range(30)]
    else:
      self.players = players
    self.control = control
    self.get_overall()
    self.score = Score()
    self.played = 0
    self.league_win = 0
    self.league_loss = 0
    self.league_draw = 0
    self.league_points = 0
    self.league_points_diff = 0
    self.get_player_table()
    self.get_scorer_table()
    self.get_lineup()
    self.training = Training(None)

  def __repr__(self):
    '''Formatted player table represents team'''
    ps = self.player_table.__str__()
    return ps

  def __iter__(self):
    ''' Returns the Iterator object '''
    return TeamIterator(self)

  def __len__(self):
    '''Length for iterator'''
    return len(self.players)

  def __getitem__(self, i):
    '''Next player'''
    return self.players[i]

  def __add__(self, other):
    '''Add teams together.  Why not?'''
    return self.players + other.players

  def get_lineup(self):
    '''Get default lineup for team.  Change positions if necessary'''
    # TODO refactor
    self.goalkeepers = [x for x in self if x.physical.position in ['GK']]
    self.full_backs = [x for x in self if x.physical.position in ['FB']]
    self.half_backs = [x for x in self if x.physical.position in ['HB']]
    self.midfielders = [x for x in self if x.physical.position in ['MI']]
    self.full_forwards = [x for x in self if x.physical.position in ['FF']]
    self.half_forwards = [x for x in self if x.physical.position in ['HF']]
    while len(self.goalkeepers) < 2:
      random.choice(self).physical.position = 'GK'
      self.get_lineup()
    while len(self.goalkeepers) > 2:
      random.choice([x for x in self if x.physical.position == 'GK']).\
        physical.position = random.choice(['FB', 'HB', 'MI', 'HF', 'FF'])
      self.get_lineup()
    while len(self.full_backs) < 3:
      random.choice([x for x in self if x.physical.position not in ['GK']]).\
        physical.position = 'FB'
      self.get_lineup()
    while len(self.half_backs) < 3:
      random.choice([x for x in self if x.physical.position not in ['GK', 'FB']]).\
        physical.position = 'HB'
      self.get_lineup()
    while len(self.midfielders) < 2:
      random.choice([x for x in self if x.physical.position not in ['GK', 'FB', 'HB']]).\
       physical.position = 'MI'
      self.get_lineup()
    while len(self.half_forwards) < 3:
      random.choice([x for x in self if x.physical.position not in ['GK', 'FB', 'HB', 'HF']]).\
        physical.position = 'HF'
      self.get_lineup()
    while len(self.full_forwards) < 3:
      random.choice([x for x in self if x.physical.position not in ['GK', 'FB', 'HB', 'HF']]).\
        physical.position = 'FF'
      self.get_lineup()
    self.defenders = self.full_backs + self.half_backs
    self.forwards = self.full_forwards + self.half_forwards
    if 1 not in [x.match.lineup for x in self]:
      player = random.choice(self.goalkeepers)
      player.match.lineup = 1
    for i in [2, 3, 4]:
      if i not in [x.match.lineup for x in self]:
        player = random.choice([x for x in self.full_backs if x.match.lineup == 0])
        player.match.lineup = i
    for i in [5, 6, 7]:
      if i not in [x.match.lineup for x in self]:
        player = random.choice([x for x in self.half_backs if x.match.lineup == 0])
        player.match.lineup = i
    for i in [8, 9]:
      if i not in [x.match.lineup for x in self]:
        player = random.choice([x for x in self.midfielders if x.match.lineup == 0])
        player.match.lineup = i
    for i in [10, 11, 12]:
      if i not in [x.match.lineup for x in self]:
        player = random.choice([x for x in self.half_forwards if x.match.lineup == 0])
        player.match.lineup = i
    for i in [13, 14, 15]:
      if i not in [x.match.lineup for x in self]:
        player = random.choice([x for x in self.full_forwards if x.match.lineup == 0])
        player.match.lineup = i
    if 16 not in [x.match.lineup for x in self]:
      player = random.choice([x for x in self.goalkeepers if x.match.lineup == 0])
      player.match.lineup = 16
    for i in [17, 18, 19, 20, 21]:
      if i not in [x.match.lineup for x in self]:
        player = random.choice([x for x in self if x.match.lineup == 0])
        player.match.lineup = i
    self.get_player_table()

  def get_player_table(self):
    '''Table of all players with selected stats'''
    x = PrettyTable()
    x.add_column('last name', [x.last_name for x in self])
    x.add_column('first name', [x.first_name for x in self])
    x.add_column('position', [x.physical.position for x in self])
    x.add_column('lineup', [x.match.lineup for x in self])
    x.add_column('overall', [x.physical.overall for x in self])
    x.add_column('rating', [x.season.average_match_rating for x in self])
    x.add_column('defending', [x.physical.defending for x in self])
    x.add_column('passing', [x.physical.passing for x in self])
    x.add_column('shooting', [x.physical.shooting for x in self])
    x.add_column('fitness', [x.physical.fitness for x in self])
    x.add_column('condition', [x.physical.condition for x in self])
    x.add_column('injury', [x.season.injury for x in self])
    x.add_column('suspension', [x.season.suspension for x in self])
    x.add_column('minutes', [x.match.minutes for x in self])
    x.add_column('score', [x.match.score.score for x in self])
    x.sortby = 'lineup'
    x.title = '{0} {1} {2}'.format(self.name, self.manager, self.overall)
    x.float_format = '5.2'
    player_table_fields = ['last name', 'first name', 'position', 'lineup', 'condition', 'injury', 'suspension']
    self.player_table = x
    x.fields = player_table_fields

  def get_scorer_table(self):
    '''Subset to scorers.  Format table'''
    scorers = [i for i in sorted(self, key=lambda x:
      -x.match.score.scoren) if i.match.score.scoren > 0]
    x = PrettyTable()
    x.add_column('%s scorers' % self.name, scorers)
    x.add_column('score', [x.match.score.score for x in scorers])
    self.scorer_table = x

  def get_overall(self):
    '''Overall team rating based on player ratings'''
    self.overall = round(np.mean([p.physical.overall for p in self]), 2)
    self.get_player_table()

  def update_score(self):
    '''Sum player points and goals.'''
    self.score.goals = sum([x.match.score.goals for x in self])
    self.score.points = sum([x.match.score.points for x in self])
    self.score.update_score()

  def update_postmatch_stats(self, comp):
    '''Clear all scores etc. for beginning of next match'''
    for x in self:
      x.update_postmatch_stats(comp)
    self.get_player_table()

  def reset_match_stats(self):
    '''Clear all scores etc. for beginning of next match'''
    for x in self:
      x.reset_match_stats()
      x.update_score()
    self.update_score()

  def reset_season_stats(self):
    '''Clear all scores etc. for beginning of next match'''
    for x in self:
      x.reset_season_stats()
      x.update_score()
    self.update_score()
    self.reset_wld()

  def reset_wld(self):
    '''End of season reset stats for next season'''
    self.played = 0
    self.league_points = 0
    self.league_points_diff = 0
    self.league_win = 0
    self.league_loss = 0
    self.league_draw = 0

  def get_training_schedule(self, adate):
    '''Call training method to start new training'''
    self.training = Training(adate)
    self.append_training_schedule()

  def append_training_schedule(self):
    '''Add to existing training schedule'''
    self.training.get_schedule()

  def train(self, date):
    '''Call method to alter player stats'''
    if date in self.training.schedule.keys():
      focus = self.training.schedule[date]
      train(self, focus)

  def get_player_report(self, inbox, date):
    '''Clear all scores etc. for beginning of next match'''
    if self.control is True:
      for x in self:
        if x.season.injury.status is not None:
          if x.season.injury.gain_date == date:
            inbox.add_injury_message(x)
        if x.season.suspension.status is not None:
          if x.season.suspension.gain_date == date:
            inbox.add_suspension_message(x)

if __name__ == "__main__":
  team = Team('a', 'a')
  print(team)
