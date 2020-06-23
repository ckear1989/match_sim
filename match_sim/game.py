'''Season engine'''

import copy
import datetime
from progressbar import Counter, Timer, ProgressBar

from match import Match, Result
from season import Season

def process_league_match_result(match):
  '''Update team stats from match result.'''
  match.team_a.played += 1
  match.team_b.played += 1
  match.team_a.league_points_diff += (match.team_a.score.scoren - match.team_b.score.scoren)
  match.team_b.league_points_diff += (match.team_b.score.scoren - match.team_a.score.scoren)
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

class Game(Season):
  '''Season engine to store all game data'''
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
    for team in self.teams.keys():
      self.teams[team].update_postmatch_stats(compo)
      self.teams[team].reset_match_stats()
    self.update_league()
    self.update_cup()
    result = Result(match)
    if self.current_date in self.results.keys():
      self.results[self.current_date].append(result)
    else:
      self.results[self.current_date] = [result]

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

  def process(self, cmd):
    '''Call function based on user input cmd'''
    if cmd in ['sa', 'save']:
      self.save()
    elif cmd in ['se', 'settings']:
      self.settings.get_settings()
    elif cmd in ['st', 'stats']:
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
    elif cmd in ['i', 'inbox']:
      self.inbox.open()

if __name__ == "__main__":

  game = Game('Sharples', 'adam')
  game.cont()
