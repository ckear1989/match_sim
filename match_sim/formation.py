
from default import formations, formations_ascii

class Formation():
  def __init__(self):
    self.nlist = formations[0]
    self.get_pos()
    self.get_pos_lineups()
    self.get_ascii()

  def __repr__(self):
    ps = '{0}\n'.format(self.nlist)
    ps += '{0}\n'.format(self.pos)
    ps += '{0}\n'.format(self.ascii)
    return ps

  def __str__(self):
    return self.__repr__()

  def change(self, team):
    print(self)
    x = input('choose formation:\n{0}\n'.format(', '.join(sorted(formations)))).strip()
    if x in formations:
      self.nlist = x
      self.get_pos()
      self.get_pos_lineups()
      self.get_ascii()
      self.update_ascii(team)
    print(self)

  def get_pos(self):
    self.pos = [int(i) for i in self.nlist.split('-')]

  def get_pos_lineups(self):
    self.goalkeeper_lineups = [1]
    i = 2
    j = self.pos[0] + i
    self.full_back_lineups = list(range(i, j))
    i = j
    j = self.pos[1] + i
    self.half_back_lineups = list(range(i, j))
    i = j
    j = self.pos[2] + i
    self.midfielder_lineups = list(range(i, j))
    i = j
    j = self.pos[3] + i
    self.half_forward_lineups = list(range(i, j))
    i = j
    j = self.pos[4] + i
    self.full_forward_lineups = list(range(i, j))

  def ammend(self, off, on):
    if off in self.goalkeeper_lineups:
      self.goalkeeper_lineups.append(on)
    if off in self.full_back_lineups:
      self.full_back_lineups.append(on)
    if off in self.half_back_lineups:
      self.half_back_lineups.append(on)
    if off in self.midfielder_lineups:
      self.midfielder_lineups.append(on)
    if off in self.half_forward_lineups:
      self.half_forward_lineups.append(on)
    if off in self.full_forward_lineups:
      self.full_forward_lineups.append(on)

  def get_preferred_position(self, lineup):
    if lineup in self.goalkeeper_lineups + [16]:
      p = 'GK'
    elif lineup in self.full_back_lineups + [17]:
      p = 'FB'
    elif lineup in self.half_back_lineups + [18]:
      p = 'HB'
    elif lineup in self.midfielder_lineups + [19]:
      p = 'MI'
    elif lineup in self.half_forward_lineups + [20]:
      p = 'HF'
    elif lineup in self.full_forward_lineups + [21]:
      p = 'FF'
    return p

  def get_ascii(self):
    self.ascii = formations_ascii[self.nlist]

  def update_ascii(self, team):
    for i in range(16):
      p = [x for x in team if x.match.lineup == i]
      postr = '<-----P{:02d}----->'.format(i)
      plstr = str(p).center(15).replace('[', ' ').replace(']', ' ')
      self.ascii = self.ascii.replace(postr, plstr)

