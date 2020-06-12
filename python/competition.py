
import random
import datetime
from prettytable import PrettyTable
from bracket import bracket

import default
from team import Team
import copy
from io import StringIO
import sys

def get_sundays(start_date):
  sundays = []
  year = start_date.year
  for i in range(366):
    adate = start_date + datetime.timedelta(i)
    if adate.year == year:
      if adate.weekday() == 6:
        sundays.append(adate)
  return sundays

# https://stackoverflow.com/questions/16571150/how-to-capture-stdout-output-from-a-python-function-call
class Capturing(list):
  def __enter__(self):
    self._stdout = sys.stdout
    sys.stdout = self._stringio = StringIO()
    return self
  def __exit__(self, *args):
    self.extend(self._stringio.getvalue().splitlines())
    del self._stringio    # free up some memory
    sys.stdout = self._stdout

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
    self.get_league_table()
    self.get_scorers_table()

  def __repr__(self):
    ps = '{0}\n'.format(self.fixtures)
    ps += '{0}\n'.format(self.next_fixture_date)
    ps += '{0}\n'.format(self.last_fixture_date)
    if 'league' in self.form:
      ps += '{0}\n'.format(self.league_table)
    if 'cup' in self.form:
      ps += '{0}\n'.format(self.bracket_p)
    ps += '{0}\n'.format(self.scorers_table)
    return ps

  def __str__(self):
    return self.__repr__()

  def update_next_fixture(self, current_date):
    remaining_fixtures = [x for x in self.fixtures.keys() if x > current_date]
    if len(remaining_fixtures) > 0:
      self.next_fixture_date = min([x for x in self.fixtures.keys() if x > current_date])
      self.last_fixture_date = max([x for x in self.fixtures.keys() if x > current_date])
      self.days_until_next_fixture = (self.next_fixture_date - current_date).days
      self.next_fixture = self.fixtures[self.next_fixture_date]
    else:
      self.next_fixture_date = None
      self.last_fixture_date = None
      self.days_until_next_fixture = None
      self.next_fixture = None

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

  def schedule_replay(self, team_a, team_b, current_date):
    self.fixtures[current_date + datetime.timedelta(6)] = [team_a, team_b, '%s replay' % self.name]

  def get_current_round(self):
    nt = '-'*self.bracket.max
    r = 1
    current_round = 1
    for around in self.bracket.rounds:
      if nt not in around:
        current_round = r
      r += 1
    return current_round

  def update_bracket(self, current_date, roundn=None, winner=None):
    if roundn is not None:
      if winner is not None:
        self.bracket.update(roundn, [winner])
    with Capturing() as self.bracket_p:
      self.bracket.show()
    self.bracket_p = '\n'.join(self.bracket_p)
    self.update_cup_fixtures(current_date)
    self.update_next_fixture(current_date)
    self.get_league_table()
    self.get_scorers_table()

  def update_cup_fixtures(self, current_date):
    nt = '-'*self.bracket.max
    pt = []
    sundays = get_sundays(current_date)
    matchups = []
    for around in self.bracket.rounds:
      if len(around) > 1:
        matchups = [[around[i], around[i+1]] for i in range(0, len(around), 2)]
        matchups = [m for m in matchups if nt not in m]
        matchups = [m for m in matchups if m + [self.name] not in self.fixtures.values()]
        if len(matchups) > 0:
          sundays = [x for x in sundays if x > current_date]
          sundays = [x for x in sundays if x not in self.fixtures.keys()]
          sundays = sundays[:len(matchups)]
          for sunday in sundays:
            matchup = random.choice(matchups)
            if matchup not in self.fixtures.values():
              self.fixtures[sunday] = matchup + [self.name]
            matchups.remove(matchup)

  def get_cup_fixtures(self):
    # /home/bort/.local/lib/python3.6/site-packages/bracket/bracket.py
    self.bracket = bracket.Bracket(list(self.teams.keys()))
    nt = '-'*self.bracket.max
    pt = []
    sundays = get_sundays(self.start_date)
    # progress round 1 byes
    round1 = self.bracket.rounds[0]
    matchups = [[round1[i], round1[i+1]] for i in range(0, len(round1), 2)]
    for matchup in matchups:
      if matchup[0] == nt:
        self.bracket.update(2, matchup[1])
      elif matchup[1] == nt:
        self.bracket.update(2, matchup[0])
    matchups = [m for m in matchups if nt not in m]
    self.fixtures = {}
    sundays = sundays[:len(matchups)]
    for sunday in sundays:
      matchup = random.choice(matchups)
      self.fixtures[sunday] = matchup + [self.name]
      matchups.remove(matchup)
    self.update_bracket(self.start_date)
    self.update_next_fixture(self.start_date)
    self.get_league_table()
    self.get_scorers_table()

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

  teams = {
    'a': Team('a', 'a'),
    'b': Team('b', 'b'),
    'c': Team('c', 'c'),
    'd': Team('d', 'd'),
    'e': Team('e', 'e')
  }
  league1 = Competition('league div 1', 'rr', datetime.date(2020, 1, 1), teams)
  print(league1)
  cup1 = Competition('cup 1', 'cup', datetime.date(2020, 1, 1), teams)
  print(cup1)
  print(cup1.get_current_round())
  current_date = datetime.date(2020, 1, 5)
  cup1.update_bracket(current_date, 2, 'e')
  print(cup1.get_current_round())
  current_date = datetime.date(2020, 1, 12)
  cup1.update_bracket(current_date, 3, 'b')
  print(cup1.get_current_round())
  current_date = datetime.date(2020, 1, 19)
  cup1.schedule_replay('a', 'e', current_date)
  print(cup1)
  cup1.update_bracket(current_date, 3, 'a')
  print(cup1.get_current_round())
  current_date = datetime.date(2020, 1, 26)
  cup1.update_bracket(current_date, 4, 'b')
  print(cup1.get_current_round())
  print(cup1)

