
import random
import datetime
from prettytable import PrettyTable

import default
from team import Team
import copy

def get_sundays(start_date):
  sundays = []
  year = start_date.year
  for i in range(366):
    adate = start_date + datetime.timedelta(i)
    if adate.year == year:
      if adate.weekday() == 6:
        sundays.append(adate)
  return sundays

class Competition():
  def __init__(self, name, form, start_date, teams):
    random.seed()
    self.name = name
    self.form = form
    self.start_date = start_date
    self.year = self.start_date.year
    self.teams = copy.deepcopy(teams)
    self.get_players()
    self.get_fixtures()
    self.update_next_fixture(self.start_date)

  def __repr__(self):
    ps = '{0}\n'.format(self.fixtures)
    ps += '{0}\n'.format(self.next_fixture_date)
    ps += '{0}\n'.format(self.last_fixture_date)
    ps += '{0}\n'.format(self.league_table)
    ps += '{0}\n'.format(self.scorers_table)
    return ps

  def __str__(self):
    return self.__repr__()

  def update_next_fixture(self, current_date):
    self.next_fixture_date = min([x for x in self.fixtures.keys() if x > current_date])
    self.last_fixture_date = max([x for x in self.fixtures.keys() if x > current_date])
    self.days_until_next_fixture = (self.next_fixture_date - current_date).days
    self.next_fixture = self.fixtures[self.next_fixture_date]

  def get_drr_fixtures(self):
    sundays = get_sundays(self.start_date)
    matchups = []
    for team_a in self.teams:
      for team_b in self.teams:
        if team_a != team_b:
          matchups.append((team_a, team_b))
    self.fixtures = {}
    sundays = sundays[:len(matchups)]
    for sunday in sundays:
      matchup = random.choice(matchups)
      self.fixtures[sunday] = matchup + [self.name]
      matchups.remove(matchup)

  def get_rr_fixtures(self):
    sundays = get_sundays(self.start_date)
    matchups = []
    for team_a in self.teams:
      for team_b in self.teams:
        if team_a < team_b:
          matchups.append([team_a, team_b])
    self.fixtures = {}
    sundays = sundays[:len(matchups)]
    for sunday in sundays:
      matchup = random.choice(matchups)
      rm = random.sample(matchup, 2)
      self.fixtures[sunday] = rm + [self.name]
      matchups.remove(matchup)

  def get_cup_fixtures(self):
    self.get_rr_fixtures()

  def get_fixtures(self):
    if self.form == 'rr':
      self.get_rr_fixtures()
    elif self.form == 'drr':
      self.get_drr_fixtures()
    elif self.form == 'cup':
      self.get_cup_fixtures()

  def get_league_table(self):
    x = PrettyTable()
    x.add_column('team', [x.name for x in self.teams.values()])
    x.add_column('played', [x.played for x in self.teams.values()])
    x.add_column('win', [x.league_win for x in self.teams.values()])
    x.add_column('loss', [x.league_loss for x in self.teams.values()])
    x.add_column('draw', [x.league_draw for x in self.teams.values()])
    x.add_column('points', [x.league_points for x in self.teams.values()])
    x.sortby = 'points'
    x.reversesort = True
    self.league_table = x

  def get_players(self):
    self.players = [copy.deepcopy(player) for team in self.teams for player in self.teams[team].players]

  def get_scorers_table(self):
    scorers = [x for x in self.players if x.score > 0]
    x = PrettyTable()
    x.add_column('player', scorers)
    x.add_column('team', [x.team for x in scorers])
    x.add_column('rscore', [x.score for x in scorers])
    x.add_column('score', ['{0}-{1} ({2})'.format(x.goals, x.points, x.score) for x in scorers])
    x.sortby = 'rscore'
    x.title = '%s top scorers' % self.name
    x.reversesort = True
    x = x.get_string(fields=['player', 'team', 'score'], end=10)
    self.scorers_table = x

if __name__=="__main__":

  league1 = Competition('league div 1', 'rr', datetime.date(2020, 1, 2), [Team('a', 'a'), Team('b', 'b')])
  print(league1)
  league1.update_next_fixture(datetime.date(2020, 1, 9))
  print(league1)

