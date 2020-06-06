
import default

import datetime

def options_from_list(alist):
  x = [xi for xi in alist if len(xi) > 2]
  x = ['({0}){1}'.format(xi[:2], xi[2:]) for xi in x]
  return x

class Training():
  def __init__(self, start_date):
    self.schedule = []
    self.focus = []
    self.fixtures = {}
    self.start_date = start_date

  def __repr__(self):
    ps = '{0} {1} {2}'.format(self.schedule, self.focus, self.fixtures)
    return ps

  def __str__(self):
    return self.__repr__()

  def get_schedule(self):
    poss_days = options_from_list(default.dow.keys())
    dow = input('choose day of week to train:\n%s\n' % poss_days)
    if dow in default.dow.keys():
      if default.dow[dow] not in self.schedule:
        self.schedule.append(default.dow[dow])
    self.get_focus()
    self.get_fixtures()

  def get_focus(self):
    while len(self.schedule) > len(self.focus):
      dow = self.schedule[len(self.focus)]
      dow = [x for x in default.dow.keys() if default.dow[x] == dow][0]
      poss_focus = options_from_list(default.focus)
      focus = input('choose training focus for {0}:\n{1}\n'.format(dow, poss_focus))
      if focus in default.focus:
        self.focus.append(focus)

  def get_fixtures(self):
    year = self.start_date.year
    for i in range(366):
      adate = self.start_date + datetime.timedelta(i)
      if adate.year == year:
        for s in self.schedule:
          if adate.weekday() == s:
            self.fixtures[adate] = self.focus[self.schedule.index(s)]

if __name__=="__main__":
  t = Training(datetime.date(2020, 1, 1))
  t.get_schedule()
  t.get_schedule()
  t
  print(t)

