
from team import Team
from match import Match
import default

import datetime
import random
import pickle
import copy

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
    self.opponents = [t for t in default.poss_teams if t != self.team.name]
    self.save_file = '../data/games/%s_%s.dat' % (self.team.name, self.team.manager)
    self.start_date = datetime.date(2020, 1, 1)
    self.current_date = self.start_date
    self.year = self.start_date.year
    random.seed()
    self.teams = self.get_teams()
    self.fixtures = self.get_fixtures()
    self.results = copy.deepcopy(self.fixtures)
    self.update_next_fixture()

  def __str__(self):
    ps = 'current date: {0}\nnext match date: {1}\n'.format(self.current_date, self.next_fixture_date)
    ps += 'current team status: {0}\nnext fixture opponent:{1}\n'.format(self.team, self.next_fixture_opponent)
    return ps

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
    for opponent in self.opponents:
      teams[opponent] = Team(opponent, 'jim')
    return teams

  def get_fixtures(self):
    sundays = get_sundays(self.year)
    matchups = []
    for opponent in self.opponents:
      for venue in ['home', 'away']:
        matchups.append((opponent, venue))
    fixtures = {}
    sundays = sundays[:len(matchups)]
    for sunday in sundays:
      matchup = random.choice(matchups)
      if matchup[1] == 'home':
        fixtures[sunday] = Match(self.team, self.teams[matchup[0]], sunday)
      else:
        fixtures[sunday] = Match(self.teams[matchup[0]], self.team, sunday)
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
    if cmd in ['c', 'continue']:
      self.current_date += datetime.timedelta(1)
      print(self)
      if self.current_date == self.next_fixture_date:
        next_match = self.fixtures.pop(self.next_fixture_date)
        next_match.play()
        self.results[self.next_fixture_date] = next_match
        print(self.fixtures)
        print(self.results)
        self.update_next_fixture()
      if self.fixtures == {}:
        self.end()

if __name__=="__main__":

  team = Team('team_a', 'bob')
  season = Season(team)
  season.cont()

