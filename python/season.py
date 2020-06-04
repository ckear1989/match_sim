
from team import Team
from match import Match
import default

import datetime
import random
import pickle

class Season():
  def __init__(self, team):
    self.team = team
    self.opponents = [t for t in default.poss_teams if t != self.team.name]
    self.save_file = '../data/games/%s_%s.dat' % (self.team.name, self.team.manager)
    self.start_date = datetime.date(2020, 1, 1)
    self.current_date = self.start_date
    self.start_year = self.start_date.year
    random.seed()
    self.teams = self.get_teams()
    self.fixtures = self.get_fixtures()

  def get_teams(self):
    teams = {}
    for opponent in self.opponents:
      teams[opponent] = Team(opponent, 'jim')
    return teams

  def get_fixtures(self):
    sundays = []
    for i in range(366):
      new_date = self.start_date + datetime.timedelta(i)
      if new_date.year == self.start_year:
        if new_date.weekday() == 6:
          sundays.append(new_date)
    matchups = []
    for opponent in self.opponents:
      for venue in ['home', 'away']:
        matchups.append((opponent, venue))
    fixtures = {}
    for i in range(len(matchups)):
      sunday = sundays[i]
      matchup = random.choice(matchups)
      fixtures[sunday] = {'opponent': matchup[0], 'venue': matchup[1]}
      matchups.remove(matchup)
    return fixtures

  def save(self):
    with open(self.save_file, 'wb') as f:
      pickle.dump(self, f)

  def load(self):
    return pickle.load(self.save_file)

  def cont(self):
    cmd = ''
    while cmd not in ['exit', 'e']:
      cmd = input('choose option:\n%s\n' % '\t'.join(['continue', 'training', 'save', 'exit']))
      self.process(cmd)

  def process(self, cmd):
    if cmd in ['c', 'continue']:
      next_f = min(self.fixtures.keys())
      next_f = self.fixtures[next_f]
      print(next_f)
      print(self.team)
      print(self.teams)
      next_match = Match(self.team, self.teams[next_f['opponent']])
      next_match.play()

if __name__=="__main__":

  team = Team('team_a', 'bob')
  season = Season(team)
  print(season.fixtures)
  season.cont()

