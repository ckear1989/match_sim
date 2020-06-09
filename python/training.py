
import default
from player import x_0_100_cap, random_0_100_normal

import datetime
import calendar

def options_from_list(alist):
  x = [xi for xi in alist if len(xi) > 2]
  x = ['({0}){1}'.format(xi[:2], xi[2:]) for xi in x]
  return x

class Training():
  def __init__(self, start_date, dow=None, fs=None):
    self.schedule = {}
    self.fixtures = {}
    self.start_date = start_date
    if dow is not None:
      if fs is not None:
        for i in range(len(dow)):
          self.schedule[dow[i]] = fs[i]
        self.get_fixtures()

  def __repr__(self):
    ps = '\n'.join(['{0}:{1}'.format(
      calendar.day_name[x[0]], x[1]) for x in self.schedule.items()])
    return ps

  def __str__(self):
    return self.__repr__()

  def get_schedule(self):
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
    year = self.start_date.year
    for i in range(366):
      adate = self.start_date + datetime.timedelta(i)
      if adate.year == year:
        for s in self.schedule:
          if adate.weekday() == s:
            self.fixtures[adate] = self.schedule[s]

  def train(self, ateam, focus):
    for x in ateam:
      if focus in ['de', 'defending']:
        x.defending = x_0_100_cap(x.defending + random_0_100_normal(5, 1))
        x.passing = x_0_100_cap(x.passing - random_0_100_normal(2, 1))
        x.shooting = x_0_100_cap(x.shooting - random_0_100_normal(2, 1))
        x.fitness = x_0_100_cap(x.fitness - random_0_100_normal(2, 1))
      if focus in ['pa', 'passing']:
        x.passing = x_0_100_cap(x.passing + random_0_100_normal(5, 1))
        x.defending = x_0_100_cap(x.defending - random_0_100_normal(2, 1))
        x.shooting = x_0_100_cap(x.shooting - random_0_100_normal(2, 1))
        x.fitness = x_0_100_cap(x.fitness - random_0_100_normal(2, 1))
      elif focus in ['sh', 'shooting']:
        x.shooting = x_0_100_cap(x.shooting + random_0_100_normal(5, 1))
        x.defending = x_0_100_cap(x.defending - random_0_100_normal(2, 1))
        x.passing = x_0_100_cap(x.passing - random_0_100_normal(2, 1))
        x.fitness = x_0_100_cap(x.fitness - random_0_100_normal(2, 1))
      elif focus in ['fi', 'fitness']:
        x.fitness = x_0_100_cap(x.fitness + random_0_100_normal(5, 1))
        x.defending = x_0_100_cap(x.defending - random_0_100_normal(2, 1))
        x.passing = x_0_100_cap(x.passing - random_0_100_normal(2, 1))
        x.shooting = x_0_100_cap(x.shooting - random_0_100_normal(2, 1))
      x.get_overall()
    ateam.get_overall()

if __name__=="__main__":
  from team import Team
  team = Team('a', 'a')
  team.get_training_schedule(datetime.date(2020, 1, 1))
  print(team.training)
  print(team)
  team.train('passing')
  team.train('shooting')
  team.train('fitness')
  print(team)

