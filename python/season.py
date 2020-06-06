
import default
from team import Team
from match import Match
from training import Training

import datetime
import random
import pickle
import copy
from prettytable import PrettyTable

def get_sundays(year):
  sundays = []
  adate = datetime.date(year, 1, 1)
  for i in range(366):
    adate += datetime.timedelta(1)
    if adate.year == year:
      if adate.weekday() == 6:
        sundays.append(adate)
  return sundays

class Season():
  def __init__(self, team):
    self.team = team
    self.save_file = '../data/games/%s_%s.dat' % (self.team.name, self.team.manager)
    self.start_date = datetime.date(2020, 1, 1)
    self.current_date = self.start_date
    self.year = self.start_date.year
    random.seed()
    self.teams = self.get_teams()
    self.fixtures = self.get_fixtures()
    self.results = copy.deepcopy(self.fixtures)
    self.update_next_fixture()
    self.get_league_table()
    self.training = None

  def __repr__(self):
    ps = 'current date: {0}\nnext match date: {1}\n'.format(self.current_date, self.next_fixture_date)
    ps += 'current team status: {0}\nnext fixture opponent:{1}\n'.format(self.team, self.next_fixture_opponent)
    return ps

  def __str__(self):
    return self.__repr__()

  def get_league_table(self):
    x = PrettyTable()
    x.add_column('team', [x.name for x in self.teams.values()])
    x.add_column('played', [x.played for x in self.teams.values()])
    x.add_column('win', [x.league_win for x in self.teams.values()])
    x.add_column('loss', [x.league_loss for x in self.teams.values()])
    x.add_column('draw', [x.league_draw for x in self.teams.values()])
    x.add_column('points', [x.league_points for x in self.teams.values()])
    self.league_table = x

  def update_league_table(self):
    self.get_league_table()

  def update_next_fixture(self):
    self.next_fixture_date = min(self.fixtures.keys())
    self.next_fixture = self.fixtures[self.next_fixture_date]
    next_fixture_opponent = self.next_fixture.team_a.name
    if next_fixture_opponent == self.team.name:
      next_fixture_opponent = self.next_fixture.team_b.name
    self.next_fixture_opponent = copy.deepcopy(self.teams[next_fixture_opponent])

  def end(self):
    self.year += 1
    self.fixtures = self.get_fixtures()

  def get_teams(self):
    teams = {}
    for team in default.poss_teams:
      teams[team] = Team(team, 'jim')
    return teams

  def get_fixtures(self):
    sundays = get_sundays(self.year)
    matchups = []
    for team_a in self.teams.keys():
      for team_b in self.teams.keys():
        if team_a != team_b:
          matchups.append((team_a, team_b))
    fixtures = {}
    sundays = sundays[:len(matchups)]
    for sunday in sundays:
      matchup = random.choice(matchups)
      fixtures[sunday] = Match(self.teams[matchup[0]], self.teams[matchup[1]], sunday)
      matchups.remove(matchup)
    return fixtures

  def save(self):
    with open(self.save_file, 'wb') as f:
      pickle.dump(self, f)

  def load(self):
    return pickle.load(self.save_file)

  def cont(self):
    options = ['(c)ontinue', '(t)raining', '(s)ave', '(e)xit']
    cmd = ''
    while cmd not in ['exit', 'e']:
      cmd = input('choose option:\n%s\n' % '\t'.join(options))
      self.process(cmd)

  def process(self, cmd):
    if cmd in ['s', 'save']:
      self.save()
    if cmd in ['t', 'training']:
      if self.training is None:
        self.training = Training(self.current_date)
      print('current training schedule\n{0}\n'.format(self.training))
      self.training.get_schedule()
      print('new training schedule\n{0}\n'.format(self.training))
    if cmd in ['c', 'continue']:
      self.current_date += datetime.timedelta(1)
      print(self)
      if self.current_date == self.next_fixture_date:
        next_match = self.fixtures.pop(self.next_fixture_date)
        next_match.play()
        self.teams[next_match.team_a.name].played += 1
        self.teams[next_match.team_b.name].played += 1
        if next_match.team_a.score > next_match.team_b.score:
          self.teams[next_match.team_a.name].league_win += 1
          self.teams[next_match.team_b.name].league_loss += 1
          self.teams[next_match.team_a.name].league_points += 2
        elif next_match.team_a.score < next_match.team_b.score:
          self.teams[next_match.team_b.name].league_win += 1
          self.teams[next_match.team_a.name].league_loss += 1
          self.teams[next_match.team_b.name].league_points += 2
        else:
          self.teams[next_match.team_a.name].league_draw += 1
          self.teams[next_match.team_b.name].league_draw += 1
          self.teams[next_match.team_a.name].league_points += 1
          self.teams[next_match.team_b.name].league_points += 1
        self.results[self.next_fixture_date] = next_match
      if self.fixtures == {}:
        self.end()
      self.update_next_fixture()
      self.update_league_table()
      print(self.league_table)

if __name__=="__main__":

  team = Team('b', 'bob')
  season = Season(team)
  season.cont()

