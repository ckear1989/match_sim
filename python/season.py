
from team import Team

import datetime
import random
import pickle

class Season():
  def __init__(self, team):
    self.team = team
    self.opponents = ['team_b']
    self.save_file = '../data/games/%s.dat' % self.team.name
    self.start_date = datetime.date(2020, 1, 1)
    self.current_date = self.start_date
    self.start_year = self.start_date.year
    random.seed()
    self.fixtures = self.get_fixtures()

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

if __name__=="__main__":

  team = Team('team_a')
  season = Season(team)
  print(season.fixtures)

