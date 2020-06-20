'''Season engine'''

import time
import random
import datetime
import calendar
import copy
import pyfiglet
from prettytable import PrettyTable
import dill as pickle
from progressbar import Counter, Timer, ProgressBar
import concurrent.futures
import pathlib
path = pathlib.Path(__file__).parent.absolute()

import default
from utils import timed_future_progress_bar
from team import Team
from match_team import MatchTeam
from match import Match
from training import Training
from competition import Competition
from settings import Settings

def relegation(league):
  '''Get bottom of league team based on league points and point difference'''
  min_league_points = min([x.league_points for x in league.teams.values()])
  league_rel = [x for x in league.teams.values() if x.league_points == min_league_points]
  min_league_pd = min([x.league_points_diff for x in league_rel])
  league_rel = random.sample([x for x in league_rel if x.league_points_diff == min_league_pd], 1)
  return random.sample(league_rel, 1)[0].name

def promotion(league):
  '''Get top of league team based on league points and point difference'''
  max_league_points = max([x.league_points for x in league.teams.values()])
  league_pro = [x for x in league.teams.values() if x.league_points == max_league_points]
  max_league_pd = max([x.league_points_diff for x in league_pro])
  league_pro = random.sample([x for x in league_pro if x.league_points_diff == max_league_pd], 1)
  return random.sample(league_pro, 1)[0].name

def process_league_match_result(match):
  '''Update team stats from match result.'''
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

class Season():
  '''Season engine to store all game data'''
  def __init__(self, team_name, manager_name):
    random.seed(team_name)
    self.team = team_name
    self.manager = manager_name
    self.save_file = '{0}/data/games/{1}_{2}_{3}.dat'.format(
      path, self.team, self.manager, datetime.datetime.today().strftime('%Y%m%d'))
    self.start_date = datetime.date(2020, 1, 1)
    self.current_date = self.start_date
    self.year = self.start_date.year
    self.competitions = {}
    self.team_league = None
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
    '''User friendly representation of season in current state'''
    print_string = '{0}\n'.format(self.upcoming_events)
    print_string += '{0}\n'.format(self.teams[self.team])
    if self.next_team_fixture is not None:
      if 'league' in self.next_team_fixture[2]:
        print_string += '{0}\n'.format(self.team_league)
      elif 'cup' in self.next_team_fixture[2]:
        print_string += '{0}\n'.format(self.competitions['cup'])
    else:
      print_string += '{0}\n'.format(self.competitions['cup'])
    return print_string

  def get_upcoming_events(self):
    '''Create pretty table of events from previous day to week in advance'''
    G = "\033[0;32;40m" # Green
    N = "\033[0m" # Reset
    dates = [self.current_date + datetime.timedelta(i) for i in range(-1, 7)]
    weekdays = [calendar.day_name[x.weekday()] for x in dates]
    fixtures = [self.fixtures[x] if x in self.fixtures.keys() else None for x in dates]
    fixtures = ['\n'.join(['{0} {1} v {2}'.format(x[i][2], x[i][0], x[i][1]) for
      i in range(len(x))]) if x else ' ' for x in fixtures]
    results = [self.results[x] if x in self.results.keys() else None for x in dates]
    results = ['\n'.join([x[i].__repr__() for i in range(len(x))]) if x else ' ' for x in results]
    training = [self.teams[self.team].training.fixtures[x] if x in
      self.teams[self.team].training.fixtures.keys() else ' ' for x in dates]
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
    '''Refresh stats for leagues'''
    self.competitions['league1'].get_league_table()
    self.competitions['league1'].get_stats_tables()
    self.competitions['league2'].get_league_table()
    self.competitions['league2'].get_stats_tables()
    self.competitions['league3'].get_league_table()
    self.competitions['league3'].get_stats_tables()
    self.competitions['league4'].get_league_table()
    self.competitions['league4'].get_stats_tables()

  def update_cup(self):
    '''Refresh stats for cup'''
    self.competitions['cup'].update_bracket(self.current_date)
    self.competitions['cup'].get_stats_tables()

  def update_next_fixture(self):
    '''Refresh data on upcoming fixtures'''
    self.get_fixtures()
    remaining_fixtures = [x for x in self.fixtures if x > self.current_date]
    remaining_team_fixtures = [x for x in remaining_fixtures if
      any(self.team in y for y in self.fixtures[x])]
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
    upcoming_training = [x for x in self.teams[self.team].training.fixtures.keys() if
      x > self.current_date]
    if len(upcoming_training) > 0:
      self.next_training_date = min(upcoming_training)
    self.get_upcoming_events()

  def banner(self):
    '''Create ascii art banner from season data.  Print banner'''
    banner = pyfiglet.figlet_format('Season {0}\n{1}\n{2}\n'.format(
      self.year, self.manager, self.team))
    print(banner)

  def banner_end(self):
    '''Create ascii art banner from end of season data.  Print banner'''
    league_winners = promotion(self.team_league)
    current_round = self.competitions['cup'].get_current_round()
    cup_winners = self.competitions['cup'].bracket.rounds[current_round-1][0]
    banner = pyfiglet.figlet_format(
      'Season {0}\n{1}\n{2}\n{3} winners:\n{4}\nCup winners:\n{5}\n'.format(
      self.year, self.manager, self.team, self.team_league.name, league_winners, cup_winners))
    print(banner)

  def end(self):
    '''End of season (no remaining fixtures).  Print summary.  Setup next year.'''
    self.banner_end()
    self.year += 1
    self.promotion_relegation()
    self.reset_players()
    for comp in self.competitions:
      for team in self.competitions[comp].teams:
        self.competitions[comp].teams[team].reset_match_stats()
        self.competitions[comp].teams[team].reset_wld()
    for team in self.teams:
      self.teams[team].reset_match_stats()
      self.teams[team].reset_wld()
    self.get_fixtures()
    self.update_next_fixture()
    self.update_league()
    self.update_cup()

  def progress_get_teams(self):
    '''Create teams from random data.  Instantiate competitions'''
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

  def get_teams(self):
    print('creating teams...')
    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as pool:
      future = pool.submit(self.progress_get_teams)
      timed_future_progress_bar(future, 4)

  def reset_players(self):
    '''Reset stats of all players in all competitions'''
    for comp in self.competitions:
      for player in self.competitions[comp].players:
        player.reset_match_stats()

  def progress_init_competitions(self, teams1, teams2, teams3, teams4):
    '''Create 4 leagues and cup.'''
    self.competitions['league1'] = Competition('league1', 'rr',
      datetime.date(self.year, 1, 1), {x:self.teams[x] for x in self.teams if x in teams1})
    self.competitions['league2'] = Competition('league2', 'rr',
      datetime.date(self.year, 1, 1), {x:self.teams[x] for x in self.teams if x in teams2})
    self.competitions['league3'] = Competition('league3', 'rr',
      datetime.date(self.year, 1, 1), {x:self.teams[x] for x in self.teams if x in teams3})
    self.competitions['league4'] = Competition('league4', 'rr',
      datetime.date(self.year, 1, 1), {x:self.teams[x] for x in self.teams if x in teams4})
    for league in self.competitions.values():
      if self.team in league.teams.keys():
        self.team_league = league
    last_league_fixture_date = max([x.last_fixture_date for x in self.competitions.values()])
    self.competitions['cup'] = Competition('cup', 'cup',
      last_league_fixture_date + datetime.timedelta(1), self.teams)

  def init_competitions(self, teams1, teams2, teams3, teams4):
    print('creating competitions...')
    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as pool:
      future = pool.submit(self.progress_init_competitions, teams1, teams2, teams3, teams4)
      timed_future_progress_bar(future, 2)

  def promotion_relegation(self):
    '''Determine teams to move up or down.  Change lists of team names'''
    teams1 = list(self.competitions['league1'].teams.keys())
    teams2 = list(self.competitions['league2'].teams.keys())
    teams3 = list(self.competitions['league3'].teams.keys())
    teams4 = list(self.competitions['league4'].teams.keys())
    rel1 = relegation(self.competitions['league1'])
    rel2 = relegation(self.competitions['league2'])
    rel3 = relegation(self.competitions['league3'])
    pro2 = promotion(self.competitions['league2'])
    pro3 = promotion(self.competitions['league3'])
    pro4 = promotion(self.competitions['league4'])
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
    '''Create season fixtures from individual competitions'''
    self.fixtures = {}
    for comp in self.competitions:
      for f in self.competitions[comp].fixtures.keys():
        if f in self.fixtures.keys():
          self.fixtures[f] = self.fixtures[f] + self.competitions[comp].fixtures[f]
        else:
          self.fixtures[f] = self.competitions[comp].fixtures[f]
    # sort so user team match is last of day
    for adate in self.fixtures:
      self.fixtures[adate].sort(key=lambda x: self.team in x)

  def save(self):
    '''Save pickle version of season that can be loaded later'''
    def blocking_job():
      with open(self.save_file, 'wb') as f:
        pickle.dump(self, f)
    print('saving game...')
    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as pool:
      future = pool.submit(blocking_job)
      timed_future_progress_bar(future, 4)

  def cont(self):
    '''Continue season.  Wait on user input'''
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

  def process_cup_match_result(self, match, compo):
    '''Update team stats from match result.  Progress bracket.'''
    current_round = compo.get_current_round()
    if match.team_a.score > match.team_b.score:
      compo.update_bracket(self.current_date, (current_round+1), match.team_a.name)
    elif match.team_a.score < match.team_b.score:
      compo.update_bracket(self.current_date, (current_round+1), match.team_b.name)
    else:
      compo.schedule_replay(match.team_a.name, match.team_b.name, self.current_date)

  def process_match_result(self, match, comp):
    '''Update player and team stats postmatch'''
    compo = [x for x in self.competitions.values() if x.name in comp]
    if len(compo) != 1:
      raise Exception('problem with competition {0}'.format(comp))
    compo = compo[0]
    if compo.form in ['rr', 'drr']:
      process_league_match_result(match)
    elif compo.form == 'cup':
      self.process_cup_match_result(match, compo)
    self.teams[match.team_a.name] = copy.deepcopy(match.team_a)
    self.teams[match.team_b.name] = copy.deepcopy(match.team_b)
    compo.teams[match.team_a.name] = copy.deepcopy(match.team_a)
    compo.teams[match.team_b.name] = copy.deepcopy(match.team_b)
    i = 0
    for team in compo.teams.keys():
      for player in compo.teams[team]:
        compo.players[i].update_postmatch_stats(player)
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
    '''Create or append team training schedule'''
    options = ['(n)ew schedule', '(a)ppend schedule']
    cmd = input('choose option:\n%s\n' % '\t'.join(options))
    if cmd in ['n', 'new schedule']:
      self.teams[self.team].training.get_schedule(self.current_date)
    elif cmd in ['a', 'append schedule']:
      self.teams[self.team].training.append_schedule()
    self.get_upcoming_events()

  def skip(self):
    '''Ask user to skip until end of season'''
    sk = input('{0} days until next fixture\nSkip? (y)es (n)o\n'.format(
      self.days_until_next_fixture))
    if sk in ['y', 'yes']:
      self.current_date += (datetime.timedelta(self.days_until_next_fixture - 2))
      self.update_next_fixture()

  def manage_team(self):
    '''Manage user controlled team'''
    self.teams[self.team].manage()

  def process_teams_daily(self):
    '''Age team.  Call method to age players'''
    for team in self.teams:
      if self.current_date in self.teams[team].training.fixtures:
        self.teams[team].train(self.current_date)
      self.process_players_daily(team)
      self.teams[team].get_overall()

  def process_players_daily(self, team):
    '''Age players after one day of season'''
    for player in self.teams[team]:
      player.process_daily(self.current_date)

  def process_fixtures_daily(self):
    '''Get today\'s fixtures.  Iteratively play eatch game.'''
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
    '''Determine match arguments.  Play match.'''
    silent = False
    time_step = 1/self.settings.match_speed
    if self.settings.match_speed == 70:
      time_step = 0
    if self.team not in match_t:
      silent = True
      time_step = 0
    extra_time_required = False
    if 'replay' in match_t[2]:
      extra_time_required = True
    match = Match(self.teams[match_t[0]], self.teams[match_t[1]],
      self.current_date, silent, extra_time_required)
    match.play(time_step)
    self.process_match_result(match, match_t[2])
    self.update_next_fixture()

  def get_player_stats(self):
    '''Ask user for team and player.  Print player'''
    options = [x for x in self.teams]
    cmd0 = input('choose team:\n{0}\n'.format(options + ['(c)ontinue']))
    if cmd0 not in ['c', '(c)ontinue']:
      if cmd0 in self.teams.keys():
        options = ['{0}, {1}'.format(x.last_name, x.first_name) for x in self.teams[cmd0]]
        cmd1 = input('choose player:\n{0}\n'.format(options + ['(c)ontinue']))
        if cmd1 not in ['c', '(c)ontinue']:
          for x in self.teams[cmd0]:
            if x.last_name == cmd1.split(',')[0].strip():
              if x.first_name == cmd1.split(',')[1].strip():
                print(x)
        else:
          return
    else:
      return
    self.get_player_stats()

  def get_team_stats(self):
    '''Ask user for team.  Print team'''
    options = [x for x in self.teams]
    cmd = input('choose team:\n{0}\n'.format(options + ['(c)ontinue']))
    if cmd not in ['c', '(c)ontinue']:
      if cmd in self.teams.keys():
        print(self.teams[cmd])
    else:
      return
    self.get_team_stats()

  def get_competition_stats(self):
    '''Ask user for competition.  Print competition'''
    options = [x for x in self.competitions]
    cmd = input('choose competition:\n{0}\n'.format(options + ['(c)ontinue']))
    if cmd not in ['c', '(c)ontinue']:
      if cmd in self.competitions.keys():
        print(self.competitions[cmd])
    else:
      return
    self.get_competition_stats()

  def stats(self):
    '''Ask user which type of stats.  Call sub method'''
    options = ['(p)layers', '(t)eams', '(c)ompetitions']
    cmd = input('choose option:\n%s\n' % ' '.join(options))
    if cmd in ['p', 'players']:
      self.get_player_stats()
    if cmd in ['t', 'teams']:
      self.get_team_stats()
    elif cmd in ['c', 'competitions']:
      self.get_competition_stats()

  def process(self, cmd):
    '''Call function based on user input cmd'''
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

if __name__ == "__main__":

  season = Season('Sharples', 'adam')
  season.cont()
