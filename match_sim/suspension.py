
import datetime

from default import suspensions

class Suspension():
  def __init__(self):
    self.status = None
    self.return_date = None
    self.gain_date = None

  def __repr__(self):
    if self.status is None:
      return ''
    else:
      ps = '{0} suspension.\nReturn date {1}.'.format(self.status, self.return_date)
      return ps

  def gain(self, status, current_date):
    self.status = status
    self.gain_date = current_date
    self.return_date = current_date + datetime.timedelta(suspensions[status])

  def reset(self):
    self.__init__()

