'''Create competition objects with fixture and player data '''

import random
import datetime
import copy
import sys
from itertools import permutations, combinations
from io import StringIO
from prettytable import PrettyTable
from bracket import bracket

from team import Team
from utils import print_side_by_side, get_sundays

class Capturing(list):
  '''https://stackoverflow.com/questions/16571150/
     how-to-capture-stdout-output-from-a-python-function-call
  '''
  def __enter__(self):
    self._stdout = sys.stdout
    sys.stdout = self._stringio = StringIO()
    return self
  def __exit__(self, *args):
    self.extend(self._stringio.getvalue().splitlines())
    del self._stringio    # free up some memory
    sys.stdout = self._stdout

class Competition():
  '''Create different competitions and generate fixtures'''
  def __init__(self, name, form, start_date, teams):
    random.seed()
    self.name = name
    self.form = form
    self.start_date = start_date
    self.year = self.start_date.year
    self.teams = [x for x in teams.keys()]
    self.bracket = bracket.Bracket(self.teams)
    with Capturing() as self.bracket_p:
      self.bracket.show()
    self.bracket_p = '{0} bracket\n'.format(self.name) + '\n'.join(self.bracket_p)
    self.fixtures = {}
    self.get_fixtures()
    self.update_next_fixture(self.start_date)
    self.get_league_table(teams)
    self.get_stats_tables(teams)

  def __repr__(self):
    '''Create user friendly string representation of league or cup'''
    if self.form in ['rr', 'drr']:
      return print_side_by_side(print_side_by_side(print_side_by_side(
        self.league_table,
        self.match_rating_table),
        self.scorers_table),
        self.assist_table)
    return print_side_by_side(print_side_by_side(print_side_by_side(
      self.bracket_p,
      self.match_rating_table),
      self.scorers_table),
      self.assist_table)

  def update_next_fixture(self, date):
    '''Store info on next and last fixtures'''
    remaining_fixtures = [x for x in self.fixtures if x > date]
    if len(remaining_fixtures) > 0:
      self.next_fixture_date = min([x for x in self.fixtures if x > date])
      self.last_fixture_date = max([x for x in self.fixtures if x > date])
      self.days_until_next_fixture = (self.next_fixture_date - date).days
      self.next_fixture = self.fixtures[self.next_fixture_date]
    else:
      self.next_fixture_date = None
      self.last_fixture_date = None
      self.days_until_next_fixture = None
      self.next_fixture = None

  def get_drr_fixtures(self):
    '''Round robin fixtures.  Each team plays each other twice'''
    n_teams = len(self.teams)
    n_rounds = (n_teams - 1) * 2
    games_per_round = int(n_teams / 2)
    sundays = get_sundays(self.start_date)[:n_rounds]
    all_teams = self.teams[:]
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
    '''ROund robin fixtures.  Each team plays each other once'''
    n_teams = len(self.teams)
    n_rounds = n_teams - 1
    games_per_round = int(n_teams / 2)
    sundays = get_sundays(self.start_date)[:n_rounds]
    all_teams = self.teams[:]
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

  def schedule_replay(self, team_a, team_b, date):
    '''Add fixture for 3 days from now for a replay'''
    next_saturday = date + datetime.timedelta(3)
    if next_saturday in self.fixtures.keys():
      self.fixtures[next_saturday].append([team_a, team_b, '%s replay' % self.name])
    else:
      self.fixtures[next_saturday] = [[team_a, team_b, '%s replay' % self.name]]

  def get_current_round(self):
    '''Determine which round in the cup is currently being played'''
    null_opponent = '-'*self.bracket.max
    iround = 1
    current_round = 1
    for around in self.bracket.rounds:
      if null_opponent not in around:
        current_round = iround
      iround += 1
    return current_round

  def update_bracket(self, date, roundn=None, winner=None):
    '''Progress bracket of winning team.  Recreate fixtures'''
    if roundn is not None:
      if winner is not None:
        self.bracket.update(roundn, [winner])
    with Capturing() as self.bracket_p:
      self.bracket.show()
    self.bracket_p = '{0} bracket\n'.format(self.name) + '\n'.join(self.bracket_p)
    if roundn is None:
      roundn = self.get_current_round()
    self.update_cup_fixtures()
    self.update_next_fixture(date)

  def update_cup_fixtures(self):
    '''Create fixtures from beginnin of bracket to latest tie'''
    sunday = get_sundays(self.start_date)[0]
    for around in self.bracket.rounds:
      if len(around) > 1:
        matchups = [[around[i], around[i+1]] for i in range(0, len(around), 2)]
        if len(matchups) > 0:
          self.fixtures[sunday] = [x + [self.name] for x in matchups]
      sunday = sunday + datetime.timedelta(7)

  def get_cup_fixtures(self):
    '''Create knockout fixtures from input teams'''
    null_opponent = '-'*self.bracket.max
    sunday = get_sundays(self.start_date)[0]
    # progress round 1 byes
    round1 = self.bracket.rounds[0]
    matchups = [[round1[i], round1[i+1]] for i in range(0, len(round1), 2)]
    for matchup in matchups:
      if matchup[0] == null_opponent:
        self.bracket.update(2, matchup[1])
      elif matchup[1] == null_opponent:
        self.bracket.update(2, matchup[0])
    sunday = get_sundays(self.start_date)[0]
    self.fixtures[sunday] = [x + [self.name] for x in matchups if null_opponent not in x]
    self.update_bracket(self.start_date)
    self.update_next_fixture(self.start_date)

  def get_fixtures(self):
    '''Decide and call which method will be used to generate fixtures'''
    if self.form == 'rr':
      self.get_rr_fixtures()
    elif self.form == 'drr':
      self.get_drr_fixtures()
    elif self.form == 'cup':
      self.get_cup_fixtures()

  def get_league_table(self, steams):
    '''Create prettytable for league stats'''
    myteams = {x: steams[x] for x in self.teams}
    x = PrettyTable()
    x.add_column('team', [x.name for x in myteams.values()])
    x.add_column('played', [x.played for x in myteams.values()])
    x.add_column('win', [x.league_win for x in myteams.values()])
    x.add_column('loss', [x.league_loss for x in myteams.values()])
    x.add_column('draw', [x.league_draw for x in myteams.values()])
    x.add_column('pd', [x.league_points_diff for x in myteams.values()])
    x.add_column('points', [x.league_points for x in myteams.values()])
    x.sortby = 'points'
    x.reversesort = True
    x.title = '%s table' % self.name
    self.league_table = x

  def get_stats_tables(self, steams, n=10):
    '''Create prettytable objects to print for user friendly stats'''
    myteams = {x: steams[x] for x in self.teams}
    myplayers = [myteams[x].players for x in self.teams]
    myplayers = [p for team in myplayers for p in team]
    if self.form in ['rr', 'drr']:
      players = sorted([x for x in myplayers if x.league.score.scoren > 0],
        key=lambda x: -x.league.score.scoren)
      x = PrettyTable()
      x.add_column('player', players)
      x.add_column('team', [x.team for x in players])
      x.add_column('score', [x.league.score.score for x in players])
      x.title = '{0} top {1}'.format(self.name, 'score')
      x = x.get_string(end=n)
      self.scorers_table = x

      players = sorted(myplayers, key=lambda x: -x.league.assists)
      x = PrettyTable()
      x.add_column('player', players)
      x.add_column('team', [x.team for x in players])
      x.add_column('assists', [x.league.assists for x in players])
      x.title = '{0} top {1}'.format(self.name, 'assists')
      x = x.get_string(end=n)
      self.assist_table = x

      players = sorted(myplayers, key=lambda x: -x.league.average_match_rating)
      x = PrettyTable()
      x.add_column('player', players)
      x.add_column('team', [x.team for x in players])
      x.add_column('average_match_rating', [x.league.average_match_rating for
        x in players])
      x.title = '{0} top {1}'.format(self.name, 'average_match_rating')
      x = x.get_string(end=n)
      self.match_rating_table = x

    elif self.form in ['cup']:
      players = sorted([x for x in myplayers if x.cup.score.scoren > 0],
        key=lambda x: -x.cup.score.scoren)
      x = PrettyTable()
      x.add_column('player', players)
      x.add_column('team', [x.team for x in players])
      x.add_column('score', [x.cup.score.score for x in players])
      x.title = '{0} top {1}'.format(self.name, 'score')
      x = x.get_string(end=n)
      self.scorers_table = x

      players = sorted(myplayers, key=lambda x: -x.cup.assists)
      x = PrettyTable()
      x.add_column('player', players)
      x.add_column('team', [x.team for x in players])
      x.add_column('assists', [x.cup.assists for x in players])
      x.title = '{0} top {1}'.format(self.name, 'assists')
      x = x.get_string(end=n)
      self.assist_table = x

      players = sorted(myplayers, key=lambda x: -x.cup.average_match_rating)
      x = PrettyTable()
      x.add_column('player', players)
      x.add_column('team', [x.team for x in players])
      x.add_column('average_match_rating', [x.cup.average_match_rating for
        x in players])
      x.title = '{0} top {1}'.format(self.name, 'average_match_rating')
      x = x.get_string(end=n)
      self.match_rating_table = x

    players = sorted(myplayers, key=lambda x: -x.physical.overall)
    x = PrettyTable()
    x.add_column('player', players)
    x.add_column('team', [x.team for x in players])
    x.add_column('overall', [x.physical.overall for x in players])
    x.title = '{0} top {1}'.format(self.name, 'overall')
    x = x.get_string(end=n)
    self.overall_table = x

if __name__ == "__main__":

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
