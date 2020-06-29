
from default import tactics, tactics_s

class Tactics():
  def __init__(self):
    self.tactics = tactics[0]
    self.get_s()

  def __repr__(self):
    ps = '{0}\n'.format(self.tactics)
    ps += '{0}\n'.format(self.s)
    return ps

  def __str__(self):
    return self.__repr__()

  def change(self, x=None):
    if x is None:
      x = input('choose tactics:\n{0}\n'.format(' '.join(tactics))).strip()
    if x in tactics:
      self.tactics = x
      self.get_s()

  def get_s(self):
    self.s = tactics_s[self.tactics]

