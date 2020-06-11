
import default
from team import Team
from match import Match
from training import Training
from competition import Competition

import datetime
import random
import dill as pickle
import copy
from prettytable import PrettyTable

class Season():
  def __init__(self, team_name, manager_name):
    random.seed(team_name)
    self.team = team_name
    self.manager = manager_name
    self.save_file = '../data/games/%s_%s_%s.dat' % (self.team, self.manager, datetime.datetime.today().strftime('%Y%m%d'))
    self.start_date = datetime.date(2020, 1, 1)
    self.current_date = self.start_date
    self.year = self.start_date.year
    self.get_teams()
    self.get_fixtures()
    self.results = {}
    self.teams[self.team].training = Training(self.current_date)
    self.update_next_fixture()
    self.update_league()
    self.update_cup()
    self.get_upcoming_events()

  def __repr__(self):
    ps = 'current date: {0}\nnext match date: {1}\n'.format(self.current_date, self.next_fixture_date)
    ps += 'current team status: {0}\nnext fixture opponent:{1}\n'.format(self.teams[self.team], self.teams[self.next_fixture_opponent])
    ps += 'upcoming events:\n{0}\n'.format(self.upcoming_events)
    ps += 'league table:\n{0}\n'.format(self.league1.league_table)
    ps += 'league scorers table:\n{0}\n'.format(self.league1.scorers_table)
    ps += 'cup bracket:\n{0}\n'.format(self.cup.bracket_p)
    ps += 'cup scorers table:\n{0}\n'.format(self.cup.scorers_table)
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

  def update_league(self):
    self.league1.get_league_table()
    self.league1.get_scorers_table()

  def update_cup(self):
    self.cup.get_scorers_table()
    self.cup.update_bracket(self.current_date)

  def update_next_fixture(self):
    self.next_fixture_date = min([x for x in self.fixtures.keys() if x > self.current_date])
    self.last_fixture_date = max([x for x in self.fixtures.keys() if x > self.current_date])
    self.days_until_next_fixture = (self.next_fixture_date - self.current_date).days
    self.next_fixture = self.fixtures[self.next_fixture_date]
    self.next_fixture_opponent = self.next_fixture[0]
    if self.next_fixture_opponent == self.team:
      self.next_fixture_opponent = self.next_fixture[1]
    self.next_training_date = None
    upcoming_training = [x for x in self.teams[self.team].training.fixtures.keys() if x > self.current_date]
    if len(upcoming_training) > 0:
      self.next_training_date = min(upcoming_training)

  def end(self):
    self.reset_players()
    for team in self.league1.teams.keys():
      self.league1.teams[team].reset_match_stats()
      self.league1.teams[team].reset_wld()
    for team in self.cup.teams.keys():
      self.cup.teams[team].reset_match_stats()
      self.cup.teams[team].reset_wld()
    self.year += 1
    self.get_fixtures()

  def get_teams(self):
    self.teams = {}
    for team in default.poss_teams:
      if team == self.team:
        self.teams[team] = Team(team, self.manager)
      else:
        self.teams[team] = Team(team, 'jim')
        self.teams[team].training = Training(self.current_date, [0, 2, 4], ['fi', 'pa', 'sh'])

  def reset_players(self):
    for player in self.league1.players:
      player.reset_match_stats()
    for player in self.cup.players:
      player.reset_match_stats()

  def get_fixtures(self):
    self.league1 = Competition('league div 1', 'rr', datetime.date(self.year, 1, 1), self.teams)
    self.cup = Competition('cup', 'cup', self.league1.last_fixture_date + datetime.timedelta(1), self.teams)
    self.fixtures = {**self.league1.fixtures, **self.cup.fixtures}

  def save(self):
    with open(self.save_file, 'wb') as f:
      pickle.dump(self, f)

  def cont(self):
    options = ['(c)ontinue', '(t)raining', '(s)ave', '(e)xit']
    cmd = ''
    while cmd not in ['exit', 'e']:
      print(self)
      if self.days_until_next_fixture > 9:
        self.skip()
      cmd = input('choose option:\n%s\n' % ' '.join(options))
      self.process(cmd)

  def process_match_result(self, match, comp):
    if 'league' in comp:
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
      self.league1.teams[match.team_a.name] = copy.deepcopy(match.team_a)
      self.league1.teams[match.team_b.name] = copy.deepcopy(match.team_b)
      i = 0
      for team in self.league1.teams.keys():
        for player in self.league1.teams[team]:
          self.league1.players[i].points += player.points
          self.league1.players[i].goals += player.goals
          self.league1.players[i].score += player.score
          i += 1
        self.teams[team].reset_match_stats()
        self.league1.teams[team].reset_match_stats()
    elif 'cup' in comp:
      # TODO cup progression detect round
      if match.team_a.score > match.team_b.score:
        self.cup.update_bracket(self.current_date, 3, match.team_a.name)
      elif match.team_a.score < match.team_b.score:
        self.cup.update_bracket(self.current_date, 3, match.team_a.name)
      else:
        # TODO cup draws
        pass
      self.teams[match.team_a.name] = copy.deepcopy(match.team_a)
      self.teams[match.team_b.name] = copy.deepcopy(match.team_b)
      self.cup.teams[match.team_a.name] = copy.deepcopy(match.team_a)
      self.cup.teams[match.team_b.name] = copy.deepcopy(match.team_b)
      i = 0
      for team in self.cup.teams.keys():
        for player in self.cup.teams[team]:
          self.cup.players[i].points += player.points
          self.cup.players[i].goals += player.goals
          self.cup.players[i].score += player.score
          i += 1
        self.teams[team].reset_match_stats()
        self.cup.teams[team].reset_match_stats()
    self.results[self.current_date] = match

  def training(self):
    options = ['(n)ew schedule', '(a)ppend schedule']
    cmd = input('choose option:\n%s\n' % '\t'.join(options))
    if cmd in ['n', 'new schedule']:
      self.teams[self.team].training.get_schedule(self.current_date)
    elif cmd in ['a', 'append schedule']:
      self.teams[self.team].training.append_schedule()

  def skip(self):
    sk = input('{0} days until next fixture\nSkip? (y) (n)\n'.format(self.days_until_next_fixture))
    if sk in ['y', 'yes']:
      self.current_date += (datetime.timedelta(self.days_until_next_fixture - 2))
      self.get_upcoming_events()

  def process(self, cmd):
    if cmd in ['s', 'save']:
      self.save()
    if cmd in ['t', 'training']:
      self.teams[self.team].training.get_schedule()
    if cmd in ['c', 'continue']:
      self.current_date += datetime.timedelta(1)
      for team in self.teams:
        if self.current_date in self.teams[team].training.fixtures:
          self.teams[team].train(self.teams[team].training.fixtures[self.current_date])
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
        self.process_match_result(next_match, next_match_t[2])
      if self.last_fixture_date == self.current_date:
        self.end()
    self.update_next_fixture()
    self.update_league()
    self.update_cup()
    self.get_upcoming_events()

if __name__=="__main__":

  season = Season('a', 'adam')
  season.cont()

