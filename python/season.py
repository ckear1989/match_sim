
import default
from team import Team
from match import Match
from training import Training

import datetime
import calendar
import random
import dill as pickle
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
  def __init__(self, team_name, manager_name):
    random.seed(team_name)
    self.team = team_name
    self.manager = manager_name
    self.save_file = '../data/games/%s_%s_%s.dat' % (self.team, self.manager, datetime.datetime.today().strftime('%Y%m%d'))
    self.start_date = datetime.date(2020, 1, 1)
    self.current_date = self.start_date
    self.year = self.start_date.year
    self.calendar = calendar.calendar(self.year)
    self.get_teams()
    self.get_fixtures()
    self.results = {}
    self.teams[self.team].training = Training(self.current_date)
    self.update_next_fixture()
    self.get_league_table()
    self.get_upcoming_events()

  def __repr__(self):
    ps = 'current date: {0}\nnext match date: {1}\n'.format(self.current_date, self.next_fixture_date)
    ps += 'current team status: {0}\nnext fixture opponent:{1}\n'.format(self.teams[self.team], self.teams[self.next_fixture_opponent])
    ps += 'upcoming events:\n{0}\n'.format(self.upcoming_events)
    ps += 'league table:\n{0}\n'.format(self.league_table)
    ps += 'current training schedule:\n{0}\n'.format(self.teams[self.team].training)
    return ps

  def __str__(self):
    return self.__repr__()

  def get_upcoming_events(self):
    ps = ''
    for i in range(5):
      adate = self.current_date + datetime.timedelta(i)
      events = []
      if adate in self.fixtures.keys():
        events += [self.fixtures[adate]]
      if adate in self.results.keys():
        events += [self.results[adate]]
      if adate in self.teams[self.team].training.fixtures.keys():
        events += [self.teams[self.team].training.fixtures[adate]]
      if events == []:
        events= ''
      ps += ('{0} {1}\n'.format(adate, events))
    self.upcoming_events = ps

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
    self.next_fixture_date = min([x for x in self.fixtures.keys() if x > self.current_date])
    self.next_fixture = self.fixtures[self.next_fixture_date]
    self.next_fixture_opponent = self.next_fixture[0]
    if self.next_fixture_opponent == self.team:
      self.next_fixture_opponent = self.next_fixture[1]
    self.next_training_date = None
    upcoming_training = [x for x in self.teams[self.team].training.fixtures.keys() if x > self.current_date]
    if len(upcoming_training) > 0:
      self.next_training_date = min(upcoming_training)

  def end(self):
    self.year += 1
    self.get_fixtures()

  def get_teams(self):
    self.teams = {}
    for team in default.poss_teams:
      if team == self.team:
        self.teams[team] = Team(team, self.manager)
      else:
        self.teams[team] = Team(team, 'jim')
        self.teams[team].training = Training(self.current_date, ['mo', 'we'], ['fi', 'pa'])

  def get_fixtures(self):
    sundays = get_sundays(self.year)
    matchups = []
    for team_a in self.teams.keys():
      for team_b in self.teams.keys():
        if team_a != team_b:
          matchups.append((team_a, team_b))
    self.fixtures = {}
    sundays = sundays[:len(matchups)]
    for sunday in sundays:
      matchup = random.choice(matchups)
      self.fixtures[sunday] = matchup
      matchups.remove(matchup)

  def save(self):
    with open(self.save_file, 'wb') as f:
      pickle.dump(self, f)

  def cont(self):
    options = ['(c)ontinue', '(t)raining', '(s)ave', '(e)xit']
    cmd = ''
    while cmd not in ['exit', 'e']:
      print(self)
      cmd = input('choose option:\n%s\n' % '\t'.join(options))
      self.process(cmd)

  def process_match_result(self, match):
    match.team_a.played += 1
    match.team_b.played += 1
    if match.team_a.score > match.team_b.score:
      match.team_a.league_win += 1
      match.team_b.league_loss += 1
      match.team_a.league_points += 2
    elif match.team_a.score < match.team_b.score:
      match.team_b.league_win += 1
      match.team_a.league_loss += 1
      match.team_b.league_points += 2
    else:
      match.team_a.league_draw += 1
      match.team_b.league_draw += 1
      match.team_a.league_points += 1
      match.team_b.league_points += 1
    self.teams[match.team_a.name] = copy.deepcopy(match.team_a)
    self.teams[match.team_b.name] = copy.deepcopy(match.team_b)
    for team in self.teams.keys():
      self.teams[team].reset_score()
    self.results[self.current_date] = match

  def training(self):
    options = ['(n)ew schedule', '(a)ppend schedule']
    cmd = input('choose option:\n%s\n' % '\t'.join(options))
    if cmd in ['n', 'new schedule']:
      self.teams[self.team].training.get_schedule(self.current_date)
    elif cmd in ['a', 'append schedule']:
      self.teams[self.team].training.append_schedule()

  def process(self, cmd):
    if cmd in ['s', 'save']:
      self.save()
    if cmd in ['t', 'training']:
      self.teams[self.team].training.get_schedule()
    if cmd in ['c', 'continue']:
      self.current_date += datetime.timedelta(1)
      for team in self.teams:
        for player in self.teams[team]:
          player.condition = min((player.condition + 10), player.fitness)
          player.get_overall()
        self.teams[team].get_overall()
      if self.current_date == self.next_fixture_date:
        next_match_t = self.fixtures[self.current_date]
        silent = True
        control = []
        if self.team in next_match_t:
          silent = False
          if self.team == next_match_t[0]:
            control = ['a']
          elif self.team == next_match_t[1]:
            control = ['b']
        next_match = Match(self.teams[next_match_t[0]], self.teams[next_match_t[1]], self.current_date, silent, control)
        next_match.play()
        self.process_match_result(next_match)
      elif self.current_date == self.next_training_date:
        self.teams[self.team].train(self.teams[self.team].training.fixtures[self.current_date])
      if self.fixtures == {}:
        self.end()
    self.update_next_fixture()
    self.update_league_table()
    self.get_upcoming_events()

if __name__=="__main__":

  season = Season('a', 'adam')
  season.cont()

