
from default import formations

class Formation():
  def __init__(self):
    self.nlist = formations[0]
    self.get_pos()
    self.get_pos_lineups()

  def __repr__(self):
    ps = '{0}\n'.format(self.nlist)
    ps += '{0}\n'.format(self.pos)
    return ps

  def __str__(self):
    return self.__repr__()

  def change(self):
    print(self)
    x = input('choose formation:\n{0}\n'.format('\t'.join(formations))).strip()
    if x in formations:
      self.nlist = x
      self.get_pos()
      self.get_pos_lineups()
    print(self)

  def get_pos(self):
    self.pos = [int(i) for i in self.nlist.split('-')]

  def get_pos_lineups(self):
    i = 2
    j = self.pos[0] + i
    self.full_back_lineups = range(i, j)
    i = j
    j = self.pos[1] + i
    self.half_back_lineups = range(i, j)
    i = j
    j = self.pos[2] + i
    self.midfielders_lineups = range(i, j)
    i = j
    j = self.pos[3] + i
    self.half_forward_lineups = range(i, j)
    i = j
    j = self.pos[4] + i
    self.full_forward_lineups = range(i, j)

