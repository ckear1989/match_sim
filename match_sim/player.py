'''Create objects to represent people'''

import random
import names
import numpy as np

from injury import Injury
from suspension import Suspension
from utils import random_0_100_normal

class Score():
  '''Store data on score'''
  def __init__(self):
    self.goals = 0
    self.points = 0
    self.scoren = 0
    self.score = '0-0 (0)'

  def __repr__(self):
    '''User friendly representation of score'''
    return self.score

  def __lt__(self, other):
    '''Score less than other score'''
    return self.scoren < other.scoren

  def __gt__(self, other):
    '''Score more than other score'''
    return self.scoren > other.scoren

  def __eq__(self, other):
    '''Score equal to other score'''
    return self.scoren == other.scoren

  def score_point(self):
    '''Increment stat and update score'''
    self.points += 1
    self.update_score()

  def score_goal(self):
    '''Increment stat and update score'''
    self.goals += 1
    self.update_score()

  def update_score(self):
    '''Recalculate total score and reformat string representation'''
    self.scoren = (self.goals * 3) + self.points
    self.score = '{0}-{1} ({2})'.format(self.goals, self.points, self.scoren)

class MatchStats():
  '''Store data on match'''
  def __init__(self):
    self.score = Score()
    self.assists = 0
    self.lineup = 0
    self.minutes = 0
    self.rating = 0.0

  def reset_match_stats(self):
    '''Reset stats accrued during match'''
    self.score = Score()
    self.assists = 0
    self.minutes = 0
    self.rating = 0.0

  def age_match_minute(self):
    '''Increment minutes played'''
    self.minutes += 1
    self.rating = min(self.rating + 0.1, 10.0)

  def assist(self):
    '''Increment assist and improve rating'''
    self.rating += 0.5
    self.assists += 1

  def turnover(self):
    '''Improve rating after turning over opponent'''
    self.rating += 0.5

  def save_goal(self):
    '''Improve rating during match'''
    self.rating += 1.5

  def score_point(self):
    '''Increment score and improve rating during match'''
    self.score.score_point()
    self.rating += 1.0

  def score_goal(self):
    '''Increment score and improve rating during match'''
    self.score.score_goal()
    self.rating += 2.0

class PhysicalStats():
  '''Randomly generate ratings for physical attributes'''
  def __init__(self):
    self.position = random.choice(['GK', 'FB', 'HB', 'MI', 'HF', 'FF'])
    self.defending = random_0_100_normal(80, 20)
    self.passing = random_0_100_normal(80, 20)
    self.shooting = random_0_100_normal(70, 20)
    self.fitness = random_0_100_normal(70, 20)
    self.condition = float(min(self.fitness, random_0_100_normal(70, 20)))
    self.get_overall()

  def get_overall(self):
    '''Overall physical rating as average of certain attributes'''
    self.overall = int(round(np.mean([
      self.defending,
      self.passing,
      self.shooting,
      self.fitness
    ])))

  def condition_deteriorate(self, n):
    '''Decrement condition to represent tiring during match'''
    self.condition = max((self.condition-0.08), n)

  def condition_improve(self):
    '''Increment condition to represent resting period'''
    self.condition = min((self.condition + 5), self.fitness)

class SeasonStats():
  '''Store data to be updated over course of season'''
  def __init__(self):
    self.match_ratings = []
    self.cards = []
    self.injury = Injury()
    self.suspension = Suspension()
    self.update_match_rating()
    self.score = Score()
    self.assists = 0

  def gain_card(self, card):
    '''Add card to currently held cards'''
    self.cards.append(card)

  def update_match_rating(self):
    '''Recalculate average match rating'''
    self.average_match_rating = 0.0
    if len(self.match_ratings) > 0:
      self.average_match_rating = round(np.mean(self.match_ratings), 2)

  def gain_injury(self, date):
    '''Update injury class'''
    self.injury.gain(date)

  def check_injury(self, date):
    '''Compare current date with return date and reset if necessary'''
    if self.injury.return_date is not None:
      if self.injury.return_date <= date:
        self.reset_injury()

  def reset(self):
    self.match_rating = 0
    self.cards = []
    self.update_match_rating()
    self.score = Score()
    self.assists = 0

  def reset_injury(self):
    '''Clear injury'''
    self.injury.reset()

  def gain_suspension(self, status, date):
    '''Update suspension object'''
    self.suspension.gain(status, date)

  def check_suspension(self, date):
    '''Compare current date with return date and reset if necessary'''
    if self.suspension.return_date is not None:
      if self.suspension.return_date <= date:
        self.reset_suspension()

  def reset_suspension(self):
    '''Clear suspension'''
    self.suspension.reset()

class Player():
  '''Player object to represent player'''
  def __init__(self, team=None):
    self.first_name = names.get_first_name(gender='male')
    self.last_name = names.get_last_name()
    self.team = team
    self.match = MatchStats()
    self.physical = PhysicalStats()
    self.season = SeasonStats()
    self.league = SeasonStats()
    self.cup = SeasonStats()

  def __repr__(self):
    '''Return user friendly representation of player'''
    return '{0} {1}'.format(self.first_name[0], self.last_name)

  def __lt__(self, other):
    '''Assert player order for table sorting'''
    return self.__repr__() < other.__repr__()

  def update_lineup(self, i):
    self.match.lineup = i

  def update_postmatch_stats(self, comp):
    '''Copy match playing stats from one player to self'''
    if comp.form in ['rr', 'drr']:
      stats = self.league
    elif comp.form in ['cup']:
      stats = self.cup
    stats.score.points += self.match.score.points
    stats.score.goals += self.match.score.goals
    stats.assists += self.match.assists
    if self.match.minutes > 0:
      stats.match_ratings.append(self.match.rating)
    stats.update_match_rating()
    self.update_score()

  def save_goal(self):
    '''Improve rating during match'''
    self.match.save_goal()

  def gain_card(self, card):
    '''Add card to currently held cards'''
    self.season.gain_card(card)

  def assist(self):
    '''Tell sub class to do it\'s job'''
    self.match.assist()

  def turnover(self):
    '''Tell sub class to do it\'s job'''
    self.match.turnover()

  def update_score(self):
    '''Tell sub class to do it\'s job'''
    self.match.score.update_score()
    self.league.score.update_score()
    self.cup.score.update_score()

  def score_point(self):
    '''Tell sub class to do it\'s job'''
    self.match.score_point()

  def score_goal(self):
    '''Tell sub class to do it\'s job'''
    self.match.score_goal()

  def reset_match_stats(self):
    '''Set all match stats to start of match positions'''
    self.match.reset_match_stats()

  def reset_season_stats(self):
    '''Set all match stats to start of match positions'''
    self.season.reset()
    self.league.reset()
    self.cup.reset()

  def gain_injury(self, date):
    '''Tell sub class to do it\'s job'''
    self.season.gain_injury(date)

  def check_injury(self, date):
    '''Tell sub class to do it\'s job'''
    self.season.check_injury(date)

  def check_suspension(self, date):
    '''Tell sub class to do it\'s job'''
    self.season.check_suspension(date)

  def condition_improve(self):
    '''Tell sub class to do it\'s job'''
    self.physical.condition_improve()

  def get_overall(self):
    '''Tell sub class to do it\'s job'''
    self.physical.get_overall()

  def process_daily(self, date):
    '''Update player stats after aging a day'''
    self.check_injury(date)
    self.check_suspension(date)
    self.condition_improve()
    self.get_overall()

  def condition_deteriorate(self, n):
    '''Update player stats after playing a minute'''
    self.physical.condition_deteriorate(n)
    self.get_overall()

  def age_match_minute(self):
    '''Update player stats after playing a minute'''
    self.physical.condition_deteriorate(0.2)
    self.match.age_match_minute()
    self.get_overall()

  def gain_suspension(self, status, date):
    '''Update suspension object'''
    self.season.gain_suspension(status, date)

if __name__ == "__main__":

  player = Player('a')
  print(player)

  # test injuries
  import datetime
  current_date = datetime.date(2020, 1, 1)
  for i in range(100):
    player.gain_injury(current_date)
    print(player.season.injury)
