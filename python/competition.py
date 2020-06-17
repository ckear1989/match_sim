
import random
import datetime
from prettytable import PrettyTable
from bracket import bracket
from itertools import permutations, combinations
import copy
from io import StringIO
import sys

import default
from team import Team
from utils import print_side_by_side

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
    self.get_stats_tables()

  def __repr__(self):
    if self.form in ['rr', 'drr']:
      return print_side_by_side(print_side_by_side(print_side_by_side(
        self.league_table,
        self.match_rating_table, 51),
        self.scorers_table, 100),
        self.assist_table, 136)
    elif self.form == 'cup':
      return print_side_by_side(print_side_by_side(print_side_by_side(
        self.bracket_p,
        self.match_rating_table, 50),
        self.scorers_table, 99),
        self.assist_table, 135)

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
    n_teams = len(self.teams.keys())
    n_rounds = (n_teams - 1) * 2
    games_per_round = int(n_teams / 2)
    sundays = get_sundays(self.start_date)[:n_rounds]
    self.fixtures = {}
    all_teams = list(self.teams.keys())
    matches = [list(x) for x in list(permutations(all_teams, 2))]
    for sunday in sundays:
      this_round = []
      current_round_teams = all_teams[:]
      while len(this_round) < games_per_round:
        match = list(random.sample(matches, 1)[0])
        if match[0] in current_round_teams:
          if match[1] in current_round_teams:
            this_round.append(match + [self.name])
            current_round_teams.remove(match[0])
            current_round_teams.remove(match[1])
            matches.remove(match)
      self.fixtures[sunday] = this_round

  def get_rr_fixtures(self):
    n_teams = len(self.teams.keys())
    n_rounds = n_teams - 1
    games_per_round = int(n_teams / 2)
    sundays = get_sundays(self.start_date)[:n_rounds]
    self.fixtures = {}
    all_teams = list(self.teams.keys())
    matches = [list(x) for x in list(combinations(all_teams, 2))]
    for sunday in sundays:
      this_round = []
      current_round_teams = all_teams[:]
      while len(this_round) < games_per_round:
        match = list(random.sample(matches, 1)[0])
        if match[0] in current_round_teams:
          if match[1] in current_round_teams:
            this_round.append(match + [self.name])
            current_round_teams.remove(match[0])
            current_round_teams.remove(match[1])
            matches.remove(match)
      self.fixtures[sunday] = this_round

  def schedule_replay(self, team_a, team_b, current_date):
    next_saturday = current_date + datetime.timedelta(6)
    if next_saturday in self.fixtures.keys():
      self.fixtures[next_saturday].append([team_a, team_b, '%s replay' % self.name])
    else:
      self.fixtures[next_saturday] = [[team_a, team_b, '%s replay' % self.name]]

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
    self.bracket_p = '{0} bracket\n'.format(self.name) + '\n'.join(self.bracket_p)
    if roundn is None:
      roundn = self.get_current_round()
    self.update_cup_fixtures(current_date, roundn)
    self.update_next_fixture(current_date)
    self.get_league_table()

  def update_cup_fixtures(self, current_date, roundn):
    nt = '-'*self.bracket.max
    pt = []
    sunday = get_sundays(self.start_date)[0]
    for around in self.bracket.rounds:
      if len(around) > 1:
        matchups = [[around[i], around[i+1]] for i in range(0, len(around), 2)]
        if len(matchups) > 0:
          self.fixtures[sunday] = [x + [self.name] for x in matchups]
      sunday = sunday + datetime.timedelta(7)

  def get_cup_fixtures(self):
    self.bracket = bracket.Bracket(list(self.teams.keys()))
    nt = '-'*self.bracket.max
    sunday = get_sundays(self.start_date)[0]
    # progress round 1 byes
    round1 = self.bracket.rounds[0]
    matchups = [[round1[i], round1[i+1]] for i in range(0, len(round1), 2)]
    for matchup in matchups:
      if matchup[0] == nt:
        self.bracket.update(2, matchup[1])
      elif matchup[1] == nt:
        self.bracket.update(2, matchup[0])
    sunday = get_sundays(self.start_date)[0]
    self.fixtures = {sunday: [x + [self.name] for x in matchups if nt not in x]}
    self.update_bracket(self.start_date)
    self.update_next_fixture(self.start_date)
    self.get_league_table()

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
    x.add_column('pd', [x.league_points_diff for x in self.teams.values()])
    x.add_column('points', [x.league_points for x in self.teams.values()])
    x.sortby = 'points'
    x.reversesort = True
    x.title = '%s table' % self.name
    self.league_table = x

  def get_players(self):
    self.players = [copy.deepcopy(player) for team in self.teams for player in self.teams[team].players]

  def get_stat_table(self, stat, sortby=None, n=10):
    if sortby is None:
      sortby = stat
    players = sorted([x for x in self.players if x.__dict__[sortby] > 0], key=lambda x: -x.__dict__[sortby])
    x = PrettyTable()
    x.add_column('player', players)
    x.add_column('team', [x.team for x in players])
    x.add_column(stat, [x.__dict__[stat] for x in players])
    x.title = '{0} top {1}'.format(self.name, stat)
    x = x.get_string(end=n)
    return(x)

  def get_stats_tables(self):
    self.scorers_table = self.get_stat_table('score', 'scoren')
    self.match_rating_table = self.get_stat_table('average_match_rating')
    self.overall_table = self.get_stat_table('overall')
    self.assist_table = self.get_stat_table('assists')

if __name__=="__main__":

  teams = {
    'a': Team('a', 'a'),
    'b': Team('b', 'b'),
    'c': Team('c', 'c'),
    'd': Team('d', 'd'),
    'e': Team('e', 'e')
  }
  # league1 = Competition('league div 1', 'drr', datetime.date(2020, 1, 1), teams)
  # print(league1)
  # league1 = Competition('league div 1', 'rr', datetime.date(2020, 1, 1), teams)
  # print(league1)
  cup1 = Competition('cup 1', 'cup', datetime.date(2020, 1, 1), teams)
  print(cup1)
  print(cup1.get_current_round())
  current_date = datetime.date(2020, 1, 5)
  cup1.update_bracket(current_date, 2, 'e')
  print(cup1.get_current_round())
  current_date = datetime.date(2020, 1, 12)
  cup1.update_bracket(current_date, 3, 'b')
  print(cup1.get_current_round())
  cup1.schedule_replay('a', 'e', current_date)
  print(cup1)
  current_date = datetime.date(2020, 1, 18)
  cup1.update_bracket(current_date, 3, 'a')
  print(cup1.get_current_round())
  current_date = datetime.date(2020, 1, 19)
  cup1.update_bracket(current_date, 4, 'b')
  print(cup1.get_current_round())
  print(cup1)

