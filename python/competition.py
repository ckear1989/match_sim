
import random
import datetime

import default

def get_sundays(start_date):
  sundays = []
  year = start_date.year
  for i in range(366):
    adate = start_date + datetime.timedelta(i)
    if adate.year == year:
      if adate.weekday() == 6:
        sundays.append(adate)
  return sundays

class Competition():
  def __init__(self, name, form, start_date):
    random.seed()
    self.name = name
    self.form = form
    self.start_date = start_date
    self.year = self.start_date.year
    self.teams = default.poss_teams
    self.get_fixtures()
    self.update_next_fixture(self.start_date)

  def __repr__(self):
    ps = '{0}\n'.format(self.fixtures)
    ps += '{0}\n'.format(self.next_fixture_date)
    ps += '{0}\n'.format(self.last_fixture_date)
    return ps

  def __str__(self):
    return self.__repr__()

  def update_next_fixture(self, current_date):
    self.next_fixture_date = min([x for x in self.fixtures.keys() if x > current_date])
    self.last_fixture_date = max([x for x in self.fixtures.keys() if x > current_date])
    self.days_until_next_fixture = (self.next_fixture_date - current_date).days
    self.next_fixture = self.fixtures[self.next_fixture_date]

  def get_drr_fixtures(self):
    sundays = get_sundays(self.start_date)
    matchups = []
    for team_a in self.teams:
      for team_b in self.teams:
        if team_a != team_b:
          matchups.append((team_a, team_b))
    self.fixtures = {}
    sundays = sundays[:len(matchups)]
    for sunday in sundays:
      matchup = random.choice(matchups)
      self.fixtures[sunday] = matchup + [self.name]
      matchups.remove(matchup)

  def get_rr_fixtures(self):
    sundays = get_sundays(self.start_date)
    matchups = []
    for team_a in self.teams:
      for team_b in self.teams:
        if team_a < team_b:
          matchups.append([team_a, team_b])
    self.fixtures = {}
    sundays = sundays[:len(matchups)]
    for sunday in sundays:
      matchup = random.choice(matchups)
      rm = random.sample(matchup, 2)
      self.fixtures[sunday] = rm + [self.name]
      matchups.remove(matchup)

  def get_cup_fixtures(self):
    self.get_rr_fixtures()

  def get_fixtures(self):
    if self.form == 'rr':
      self.get_rr_fixtures()
    elif self.form == 'drr':
      self.get_drr_fixtures()
    elif self.form == 'cup':
      self.get_cup_fixtures()

if __name__=="__main__":

  league1 = Competition('league div 1', 'rr', datetime.date(2020, 1, 2))
  print(league1)
  league1.update_next_fixture(datetime.date(2020, 1, 9))
  print(league1)

