'''Season engine'''

import random
import datetime
import calendar
import names
import pyfiglet
from prettytable import PrettyTable
import dill as pickle
import concurrent.futures

import default
from utils import timed_future_progress_bar, print_side_by_side
from match_team import MatchTeam
from training import Training
from competition import Competition
from reporting.inbox import Inbox
from settings import Settings

class Season():
  '''Season engine to store all game data'''
  def __init__(self, team_name, manager_name):
    random.seed(team_name)
    self.team = team_name
    self.manager = manager_name
    self.save_file = '{0}{1}_{2}_{3}.dat'.format(
      default.save_dir, self.team, self.manager, datetime.datetime.today().strftime('%Y%m%d'))
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
    self.inbox = Inbox(self.teams[self.team])

  def __repr__(self):
    '''User friendly representation of season in current state'''
    return print_side_by_side(self.upcoming_events, self.teams[self.team])

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

  def relegation(self, league):
    '''Get bottom of league team based on league points and point difference'''
    league_teams = {x: self.teams[x] for x in league.teams}
    min_league_points = min([x.league_points for x in league_teams.values()])
    league_rel = [x for x in league_teams.values() if x.league_points == min_league_points]
    min_league_pd = min([x.league_points_diff for x in league_rel])
    league_rel = random.sample([x for x in league_rel if x.league_points_diff == min_league_pd], 1)
    return random.sample(league_rel, 1)[0].name
  
  def promotion(self, league):
    '''Get top of league team based on league points and point difference'''
    league_teams = {x: self.teams[x] for x in league.teams}
    max_league_points = max([x.league_points for x in league_teams.values()])
    league_pro = [x for x in league_teams.values() if x.league_points == max_league_points]
    max_league_pd = max([x.league_points_diff for x in league_pro])
    league_pro = random.sample([x for x in league_pro if x.league_points_diff == max_league_pd], 1)
    return random.sample(league_pro, 1)[0].name

  def update_league(self):
    '''Refresh stats for leagues'''
    league1_teams = self.competitions['league1'].teams
    league2_teams = self.competitions['league2'].teams
    league3_teams = self.competitions['league3'].teams
    league4_teams = self.competitions['league4'].teams
    self.competitions['league1'].get_league_table(self.teams)
    self.competitions['league1'].get_stats_tables(self.teams)
    self.competitions['league2'].get_league_table(self.teams)
    self.competitions['league2'].get_stats_tables(self.teams)
    self.competitions['league3'].get_league_table(self.teams)
    self.competitions['league3'].get_stats_tables(self.teams)
    self.competitions['league4'].get_league_table(self.teams)
    self.competitions['league4'].get_stats_tables(self.teams)

  def update_cup(self):
    '''Refresh stats for cup'''
    cup_teams = self.competitions['cup'].teams
    self.competitions['cup'].update_bracket(self.current_date)
    self.competitions['cup'].get_stats_tables(self.teams)

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
    league_winners = self.promotion(self.team_league)
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
    for team in self.teams:
      self.teams[team].reset_season_stats()
    self.get_fixtures()
    self.update_next_fixture()
    self.update_league()
    self.update_cup()

  def progress_get_teams(self):
    '''Create teams from random data.  Instantiate competitions'''
    self.teams = {}
    for team in default.poss_teams:
      if team == self.team:
        self.teams[team] = MatchTeam(team, self.manager, control=True)
      else:
        self.teams[team] = MatchTeam(team, names.get_full_name())
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
    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as pool:
      future = pool.submit(self.progress_get_teams)
      timed_future_progress_bar(future, 4)

  def progress_init_competitions(self, teams1, teams2, teams3, teams4):
    '''Create 4 leagues and cup.'''
    self.competitions['league1'] = Competition('league1', 'rr',
      datetime.date(self.year, 1, 1), {x: self.teams[x] for x in teams1})
    self.competitions['league2'] = Competition('league2', 'rr',
      datetime.date(self.year, 1, 1), {x: self.teams[x] for x in teams2})
    self.competitions['league3'] = Competition('league3', 'rr',
      datetime.date(self.year, 1, 1), {x: self.teams[x] for x in teams3})
    self.competitions['league4'] = Competition('league4', 'rr',
      datetime.date(self.year, 1, 1), {x: self.teams[x] for x in teams4})
    for league in self.competitions.values():
      if self.team in league.teams:
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
    teams1 = self.competitions['league1'].teams[:]
    teams2 = self.competitions['league2'].teams[:]
    teams3 = self.competitions['league3'].teams[:]
    teams4 = self.competitions['league4'].teams[:]
    rel1 = self.relegation(self.competitions['league1'])
    rel2 = self.relegation(self.competitions['league2'])
    rel3 = self.relegation(self.competitions['league3'])
    pro2 = self.promotion(self.competitions['league2'])
    pro3 = self.promotion(self.competitions['league3'])
    pro4 = self.promotion(self.competitions['league4'])
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
    cmd = ''
    while cmd not in ['exit', 'e']:
      options = ['(c)ontinue', '(i)nbox[{}]'.format(self.inbox.count), '(m)anage',
        '(t)raining', '(st)ats', '(sa)ve', '(se)ttings', '(e)xit']
      print(self)
      if self.next_fixture_date is None:
        self.end()
      if self.days_until_next_fixture > 9:
        self.skip()
      cmd = input('choose option:\n%s\n' % ' '.join(options))
      self.process(cmd)
      if self.settings.autosave is True:
        self.save()

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

if __name__ == "__main__":

  season = Season('Sharples', 'adam')
  season.cont()
