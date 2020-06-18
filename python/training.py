'''Training for players and teams'''

import datetime
import calendar

import default
from utils import x_0_100_cap, random_0_100_normal

def options_from_list(alist):
  '''String format list'''
  x = [xi for xi in alist if len(xi) > 2]
  x = ['({0}){1}'.format(xi[:2], xi[2:]) for xi in x]
  return x

def train(ateam, focus):
  '''Alter team player attributes based on training focus.'''
  for x in ateam:
    if focus in ['de', 'defending']:
      x.physical.defending = x_0_100_cap(x.physical.defending + random_0_100_normal(5, 1))
      x.physical.passing = x_0_100_cap(x.physical.passing - random_0_100_normal(2, 1))
      x.physical.shooting = x_0_100_cap(x.physical.shooting - random_0_100_normal(2, 1))
      x.physical.fitness = x_0_100_cap(x.physical.fitness - random_0_100_normal(2, 1))
    if focus in ['pa', 'passing']:
      x.physical.passing = x_0_100_cap(x.physical.passing + random_0_100_normal(5, 1))
      x.physical.defending = x_0_100_cap(x.physical.defending - random_0_100_normal(2, 1))
      x.physical.shooting = x_0_100_cap(x.physical.shooting - random_0_100_normal(2, 1))
      x.physical.fitness = x_0_100_cap(x.physical.fitness - random_0_100_normal(2, 1))
    elif focus in ['sh', 'shooting']:
      x.physical.shooting = x_0_100_cap(x.physical.shooting + random_0_100_normal(5, 1))
      x.physical.defending = x_0_100_cap(x.physical.defending - random_0_100_normal(2, 1))
      x.physical.passing = x_0_100_cap(x.physical.passing - random_0_100_normal(2, 1))
      x.physical.fitness = x_0_100_cap(x.physical.fitness - random_0_100_normal(2, 1))
    elif focus in ['fi', 'fitness']:
      x.physical.fitness = x_0_100_cap(x.physical.fitness + random_0_100_normal(5, 1))
      x.physical.defending = x_0_100_cap(x.physical.defending - random_0_100_normal(2, 1))
      x.physical.passing = x_0_100_cap(x.physical.passing - random_0_100_normal(2, 1))
      x.physical.shooting = x_0_100_cap(x.physical.shooting - random_0_100_normal(2, 1))
    x.get_overall()
  ateam.get_overall()

class Training():
  '''Data on team training schedule. Methods to run training events'''
  def __init__(self, start_date, dow=None, fs=None):
    self.schedule = {}
    self.fixtures = {}
    self.start_date = start_date
    if dow is not None:
      if fs is not None:
        for i in enumerate(dow):
          self.schedule[dow[i]] = fs[i]
        self.get_fixtures()

  def __repr__(self):
    '''Day of week and focus formatted string'''
    ps = '\n'.join(['{0}:{1}'.format(
      calendar.day_name[x[0]], x[1]) for x in self.schedule.items()])
    return ps

  def get_schedule(self):
    '''Ask user for day of week to train on.  Pair with training focus'''
    poss_days = options_from_list(default.dow.keys())
    dow = input('choose day of week to train:\n%s\n' % poss_days)
    if dow in default.dow.keys():
      focus = None
      while focus not in default.focus:
        poss_focus = options_from_list(default.focus)
        focus = input('choose training focus for {0}:\n{1}\n'.format(dow, poss_focus))
      self.schedule[default.dow[dow]] = focus
      self.get_fixtures()
    else:
      print('sorry, {0} is not an option, try again'.format(dow))

  def get_fixtures(self):
    '''Iterate through year. Add training focus to schedule'''
    year = self.start_date.year
    for i in range(366):
      adate = self.start_date + datetime.timedelta(i)
      if adate.year == year:
        for s in self.schedule:
          if adate.weekday() == s:
            self.fixtures[adate] = self.schedule[s]

if __name__ == "__main__":
  from team import Team
  team = Team('a', 'a')
  team.get_training_schedule(datetime.date(2020, 1, 1))
  print(team.training)
  print(team)
  train(team, 'passing')
  train(team, 'shooting')
  train(team, 'fitness')
  print(team)
