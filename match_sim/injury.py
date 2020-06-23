
import datetime
import random
import numpy as np

from default import body_parts

class Injury():
  def __init__(self):
    self.status = None
    self.part = None
    self.gain_date = None
    self.return_date = None

  def __repr__(self):
    if self.status is None:
      return ''
    else:
      ps = '{0} injured {1}.\nReturn date {2}.'.format(self.status, self.part, self.return_date)
      return ps

  def gain(self, current_date):
    self.gain_date = current_date
    self.part = random.choice(body_parts)
    p = random.random()
    if p < 0.8:
      self.status = 'Slightly'
      self.return_date = current_date + datetime.timedelta(np.random.gamma(7, 3))
    else:
      self.status = 'Severely'
      self.return_date = current_date + datetime.timedelta(np.random.gamma(20, 8))

  def reset(self):
    self.__init__()

