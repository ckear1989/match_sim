
import default
from team import Team
from match_team import MatchTeam
from match import Match
from training import Training
from competition import Competition
from settings import Settings

import pyfiglet
from prettytable import PrettyTable
import datetime
import calendar
import random
import dill as pickle
import copy
from progressbar import Counter, Timer, ProgressBar
import time

# https://stackoverflow.com/questions/53401383/how-to-print-two-strings-large-text-side-by-side-in-python
def print_side_by_side(a, b, size=60, space=4):
  pstr = ''
  astr0 = str(a).split('\n')
  bstr0 = str(b).split('\n')
  for i in range(max(len(astr0), len(bstr0))):
    if len(astr0) > i:
      astr = astr0[i]
    else:
      astr = ''
    if len(bstr0) > i:
      bstr = bstr0[i]
    else:
      bstr = ''
    while astr or bstr:
      pstr += astr[:size].ljust(size) + " " * space + bstr[:size]
      astr = astr[size:]
      bstr = bstr[size:]
    pstr += '\n'
  return pstr

def relegation(league):
  min_league_points = min([x.league_points for x in league.teams.values()])
  league_rel = [x for x in league.teams.values() if x.league_points == min_league_points]
  min_league_pd = min([x.league_points_diff for x in league_rel])
  league_rel = random.sample([x for x in league_rel if x.league_points_diff == min_league_pd], 1)
  return random.sample(league_rel, 1)[0].name

def promotion(league):
  max_league_points = max([x.league_points for x in league.teams.values()])
  league_pro = [x for x in league.teams.values() if x.league_points == max_league_points]
  max_league_pd = max([x.league_points_diff for x in league_pro])
  league_pro = random.sample([x for x in league_pro if x.league_points_diff == max_league_pd], 1)
  return random.sample(league_pro, 1)[0].name

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
    self.settings = Settings()

  def __repr__(self):
    ps = '{0}\n'.format(self.upcoming_events)
    ps += '{0}\n'.format(self.teams[self.team])
    if self.next_team_fixture is not None:
      if 'league' in self.next_team_fixture[2]:
        ps += print_side_by_side(self.team_league.league_table, self.team_league.scorers_table)
      elif 'cup' in self.next_team_fixture[2]:
        ps += print_side_by_side(self.cup.bracket_p, self.cup.scorers_table)
    else:
      ps += print_side_by_side(self.cup.bracket_p, self.cup.scorers_table)
    return ps

  def get_upcoming_events(self):
    #Color
    R = "\033[0;31;40m" #RED
    G = "\033[0;32;40m" # GREEN
    Y = "\033[0;33;40m" # Yellow
    B = "\033[0;34;40m" # Blue
    N = "\033[0m" # Reset
    dates = [self.current_date + datetime.timedelta(i) for i in range(-1, 7)]
    weekdays =[calendar.day_name[x.weekday()] for x in dates]
    fixtures = [self.fixtures[x] if x in self.fixtures.keys() else None for x in dates]
    fixtures = ['\n'.join(['{0} {1} v {2}'.format(x[i][2], x[i][0], x[i][1]) for i in range(len(x))]) if x else ' ' for x in fixtures]
    results = [self.results[x] if x in self.results.keys() else None for x in dates]
    results = ['\n'.join([x[i].__repr__() for i in range(len(x))]) if x else ' ' for x in results]
    training = [self.teams[self.team].training.fixtures[x] if x in self.teams[self.team].training.fixtures.keys() else ' ' for x in dates]
    training = ['defending' if x == 'de' else x for x in training]
    training = ['passing' if x == 'pa' else x for x in training]
    training = ['shooting' if x == 'sh' else x for x in training]
    training = ['fitness' if x == 'fi' else x for x in training]
    i = list(range(-1, 7))
    today = dates.index(self.current_date)
    dates = [G+str(x)+N if x == self.current_date else str(x) for x in dates]
    weekdays[today] = '{0}{1}{2}'.format(G, weekdays[today], N)
    fixtures[today] = '{0}{1}{2}'.format(G, fixtures[today], N)
    results[today] = '{0}{1}{2}'.format(G, results[today], N)
    training[today] = '{0}{1}{2}'.format(G, training[today], N)
    x = PrettyTable()
    x.add_column('i', i)
    x.add_column('date', dates)
    x.add_column('weekday', weekdays)
    x.add_column('fixtures', fixtures)
    x.add_column('results', results)
    x.add_column('training', training)
    x.sortby = 'i'
    x.title = '{0} upcoming events'.format(self.current_date)
    self.upcoming_events = x

  def update_league(self):
    self.league1.get_league_table()
    self.league1.get_scorers_table()
    self.league2.get_league_table()
    self.league2.get_scorers_table()
    self.league3.get_league_table()
    self.league3.get_scorers_table()
    self.league4.get_league_table()
    self.league4.get_scorers_table()

  def update_cup(self):
    self.cup.get_scorers_table()
    self.cup.update_bracket(self.current_date)

  def update_next_fixture(self):
    self.get_fixtures()
    remaining_fixtures = [x for x in self.fixtures.keys() if x > self.current_date]
    remaining_team_fixtures = [x for x in remaining_fixtures if any(self.team in y for y in self.fixtures[x])]
    self.next_fixture_date = None
    self.last_fixture_date = None
    self.days_until_next_fixture = None
    self.next_fixture = None
    self.next_team_fixture_date = None
    self.last_team_fixture_date = None
    self.days_until_next_team_fixture = None
    self.next_team_fixture = None
    self.next_team_fixture_opponent = None
    if len(remaining_fixtures) > 0:
      self.next_fixture_date = min(remaining_fixtures)
      self.last_fixture_date = max(remaining_fixtures)
      self.days_until_next_fixture = (self.next_fixture_date - self.current_date).days
      self.next_fixture = self.fixtures[self.next_fixture_date]
      if len(remaining_team_fixtures) > 0:
        self.next_team_fixture_date = min(remaining_team_fixtures)
        self.last_team_fixture_date = max(remaining_team_fixtures)
        self.days_until_next_team_fixture = (self.next_team_fixture_date - self.current_date).days
        next_team_fixture = self.fixtures[self.next_team_fixture_date]
        for f in next_team_fixture:
          if self.team in f:
            self.next_team_fixture = f
        self.next_team_fixture_opponent = self.next_team_fixture[0]
        if self.next_team_fixture_opponent == self.team:
          self.next_team_fixture_opponent = self.next_team_fixture[1]
    self.next_training_date = None
    upcoming_training = [x for x in self.teams[self.team].training.fixtures.keys() if x > self.current_date]
    if len(upcoming_training) > 0:
      self.next_training_date = min(upcoming_training)
    self.get_upcoming_events()

  def banner(self):
    banner = pyfiglet.figlet_format('Season {0}\n{1}\n{2}\n'.format(self.year, self.manager, self.team))
    print(banner)

  def banner_end(self):
    league_winners = promotion(self.team_league)
    current_round = self.cup.get_current_round()
    cup_winners = self.cup.bracket.rounds[current_round-1][0]
    banner = pyfiglet.figlet_format('Season {0}\n{1}\n{2}\n{3} winners:\n{4}\nCup winners:\n{5}\n'.format(
      self.year, self.manager, self.team, self.team_league.name, league_winners, cup_winners))
    print(banner)

  def end(self):
    self.banner_end()
    self.year += 1
    self.promotion_relegation()
    self.reset_players()
    for team in self.teams.keys():
      self.teams[team].reset_match_stats()
      self.teams[team].reset_wld()
    for team in self.league1.teams.keys():
      self.league1.teams[team].reset_match_stats()
      self.league1.teams[team].reset_wld()
    for team in self.league2.teams.keys():
      self.league2.teams[team].reset_match_stats()
      self.league2.teams[team].reset_wld()
    for team in self.league3.teams.keys():
      self.league3.teams[team].reset_match_stats()
      self.league3.teams[team].reset_wld()
    for team in self.league4.teams.keys():
      self.league4.teams[team].reset_match_stats()
      self.league4.teams[team].reset_wld()
    for team in self.cup.teams.keys():
      self.cup.teams[team].reset_match_stats()
      self.cup.teams[team].reset_wld()
    self.get_fixtures()
    self.update_next_fixture()
    self.update_league()
    self.update_cup()

  def get_teams(self):
    self.teams = {}
    for team in default.poss_teams:
      if team == self.team:
        self.teams[team] = MatchTeam(Team(team, self.manager, control=True))
      else:
        self.teams[team] = MatchTeam(Team(team, 'jim'))
        self.teams[team].training = Training(self.current_date, [0, 2, 4], ['fi', 'pa', 'sh'])
    n_teams = len(self.teams.keys())
    poss_teams = random.sample(self.teams.keys(), n_teams)
    teams_per_div = int(n_teams / 4)
    teams1 = poss_teams[:teams_per_div]
    teams2 = poss_teams[teams_per_div:teams_per_div+4]
    teams3 = poss_teams[teams_per_div+4:teams_per_div+8]
    teams4 = poss_teams[teams_per_div+8:]
    self.init_competitions(teams1, teams2, teams3, teams4)

  def reset_players(self):
    for player in self.league1.players:
      player.reset_match_stats()
    for player in self.cup.players:
      player.reset_match_stats()

  def init_competitions(self, teams1, teams2, teams3, teams4):
    self.league1 = Competition('league1', 'rr', datetime.date(self.year, 1, 1), {x:self.teams[x] for x in self.teams if x in teams1})
    self.league2 = Competition('league2', 'rr', datetime.date(self.year, 1, 1), {x:self.teams[x] for x in self.teams if x in teams2})
    self.league3 = Competition('league3', 'rr', datetime.date(self.year, 1, 1), {x:self.teams[x] for x in self.teams if x in teams3})
    self.league4 = Competition('league4', 'rr', datetime.date(self.year, 1, 1), {x:self.teams[x] for x in self.teams if x in teams4})
    if self.team in self.league1.teams.keys():
      self.team_league = self.league1
    elif self.team in self.league2.teams.keys():
      self.team_league = self.league2
    elif self.team in self.league3.teams.keys():
      self.team_league = self.league3
    elif self.team in self.league4.teams.keys():
      self.team_league = self.league4
    last_league_fixture_date = max([
      self.league1.last_fixture_date,
      self.league2.last_fixture_date,
      self.league3.last_fixture_date,
      self.league4.last_fixture_date
    ])
    self.cup = Competition('cup', 'cup', last_league_fixture_date + datetime.timedelta(1), self.teams)

  def promotion_relegation(self):
    teams1 = list(self.league1.teams.keys())
    teams2 = list(self.league2.teams.keys())
    teams3 = list(self.league3.teams.keys())
    teams4 = list(self.league4.teams.keys())
    rel1 = relegation(self.league1)
    rel2 = relegation(self.league2)
    rel3 = relegation(self.league3)
    pro2 = promotion(self.league2)
    pro3 = promotion(self.league3)
    pro4 = promotion(self.league4)
    teams1.remove(rel1)
    teams1.append(pro2)
    teams2.remove(pro2)
    teams2.remove(rel2)
    teams2.append(rel1)
    teams2.append(pro3)
    teams3.remove(pro3)
    teams3.remove(rel3)
    teams3.append(rel2)
    teams3.append(pro4)
    teams4.remove(pro4)
    teams4.append(rel3)
    self.init_competitions(teams1, teams2, teams3, teams4)

  def get_fixtures(self):
    self.fixtures = {
      **self.league1.fixtures,
      **self.cup.fixtures
    }
    for f in self.league2.fixtures.keys():
      if f in self.fixtures.keys():
        self.fixtures[f] = self.fixtures[f] + self.league2.fixtures[f]
    for f in self.league3.fixtures.keys():
      if f in self.fixtures.keys():
        self.fixtures[f] = self.fixtures[f] + self.league3.fixtures[f]
    for f in self.league4.fixtures.keys():
      if f in self.fixtures.keys():
        self.fixtures[f] = self.fixtures[f] + self.league4.fixtures[f]
    for adate in self.fixtures.keys():
      self.fixtures[adate].sort(key=lambda x: self.team in x)

  def save(self):
    widgets = ['Saving game...', Timer()]
    pbar = ProgressBar(widgets=widgets)
    for i in pbar([0]):
      with open(self.save_file, 'wb') as f:
        pickle.dump(self, f)

  def cont(self):
    self.banner()
    options = ['(c)ontinue', '(m)anage', '(t)raining', '(st)ats', '(sa)ve', '(se)ttings', '(e)xit']
    cmd = ''
    while cmd not in ['exit', 'e']:
      print(self)
      if self.next_fixture_date is None:
        self.end()
      if self.days_until_next_fixture > 9:
        self.skip()
      cmd = input('choose option:\n%s\n' % ' '.join(options))
      self.process(cmd)
      if self.settings.autosave is True:
        self.save()

  def process_match_result(self, match, comp):
    compo = [x for x in [self.league1, self.league2, self.league3, self.league4, self.cup] if x.name in comp]
    if len(compo) != 1:
      raise Exception('problem with competition {0}'.format(comp))
    else:
      compo = compo[0]
    if compo.form in ['rr', 'drr']:
      match.team_a.played += 1
      match.team_b.played += 1
      match.team_a.league_points_diff += (match.team_a.points - match.team_b.points)
      match.team_b.league_points_diff += (match.team_b.points - match.team_a.points)
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
    elif compo.form == 'cup':
      current_round = compo.get_current_round()
      if match.team_a.score > match.team_b.score:
        compo.update_bracket(self.current_date, (current_round+1), match.team_a.name)
      elif match.team_a.score < match.team_b.score:
        compo.update_bracket(self.current_date, (current_round+1), match.team_b.name)
      else:
        compo.schedule_replay(match.team_a.name, match.team_b.name, self.current_date)
    self.teams[match.team_a.name] = copy.deepcopy(match.team_a)
    self.teams[match.team_b.name] = copy.deepcopy(match.team_b)
    compo.teams[match.team_a.name] = copy.deepcopy(match.team_a)
    compo.teams[match.team_b.name] = copy.deepcopy(match.team_b)
    i = 0
    for team in compo.teams.keys():
      for player in compo.teams[team]:
        compo.players[i].points += player.points
        compo.players[i].goals += player.goals
        compo.players[i].score += player.score
        i += 1
      self.teams[team].reset_match_stats()
      compo.teams[team].reset_match_stats()
    self.update_league()
    self.update_cup()
    if self.current_date in self.results.keys():
      self.results[self.current_date].append(match)
    else:
      self.results[self.current_date] = [match]

  def training(self):
    options = ['(n)ew schedule', '(a)ppend schedule']
    cmd = input('choose option:\n%s\n' % '\t'.join(options))
    if cmd in ['n', 'new schedule']:
      self.teams[self.team].training.get_schedule(self.current_date)
    elif cmd in ['a', 'append schedule']:
      self.teams[self.team].training.append_schedule()
    self.get_upcoming_events()

  def skip(self):
    sk = input('{0} days until next fixture\nSkip? (y)es (n)o\n'.format(self.days_until_next_fixture))
    if sk in ['y', 'yes']:
      self.current_date += (datetime.timedelta(self.days_until_next_fixture - 2))
      self.update_next_fixture()

  def manage_team(self):
    self.teams[self.team].manage()

  def process_teams_daily(self):
    for team in self.teams:
      if self.current_date in self.teams[team].training.fixtures:
        self.teams[team].train(self.teams[team].training.fixtures[self.current_date])
      self.process_players_daily(team)
      self.teams[team].get_overall()

  def process_players_daily(self, team):
    for player in self.teams[team]:
      player.check_injury(self.current_date)
      player.check_suspension(self.current_date)
      player.condition = min((player.condition + 5), player.fitness)
      player.get_overall()

  def process_fixtures_daily(self):
    if self.current_date == self.next_fixture_date:
      fixtures = self.fixtures[self.current_date]
      if len(fixtures) > 1:
        if self.team in fixtures[-1]:
          widgets = ['Processed: ', Counter(), ' matches (', Timer(), ')']
          pbar = ProgressBar(widgets=widgets)
          for match_t in pbar(fixtures[:-1]):
            self.process_match_tuple(match_t)
          time.sleep(0.1)
          next_match_t = fixtures[-1]
          self.process_match_tuple(next_match_t)
        else:
          for match_t in fixtures:
            self.process_match_tuple(match_t)
      else:
        for match_t in fixtures:
          self.process_match_tuple(match_t)

  def process_match_tuple(self, match_t):
    silent = False
    if self.team not in match_t:
      silent = True
    extra_time_required = False
    if 'replay' in match_t[2]:
      extra_time_required = True
    match = Match(self.teams[match_t[0]], self.teams[match_t[1]], self.current_date, silent, extra_time_required)
    match.play()
    self.process_match_result(match, match_t[2])
    self.update_next_fixture()

  def stats(self):
    pass

  def process(self, cmd):
    if cmd in ['sa', 'save']:
      self.save()
    if cmd in ['se', 'settings']:
      self.settings.get_settings()
    if cmd in ['st', 'stats']:
      self.stats()
    elif cmd in ['m', 'manage']:
      self.manage_team()
    elif cmd in ['t', 'training']:
      self.teams[self.team].training.get_schedule()
    elif cmd in ['c', 'continue']:
      self.current_date += datetime.timedelta(1)
      self.process_teams_daily()
      self.process_fixtures_daily()
      self.update_next_fixture()

if __name__=="__main__":

  season = Season('a', 'adam')
  season.cont()

