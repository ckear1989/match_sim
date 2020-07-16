
from match_sim.cl.default import formations, formations_ascii

class Formation():
  def __init__(self):
    self.nlist = formations[0]
    self.get_pos()
    self.playing_lineups = {i: i for i in range(1, 16)}
    self.sub_lineups = {i: i for i in range(16, 22)}
    self.goalkeeper_lineups = {}
    self.full_back_lineups = {}
    self.half_back_lineups = {}
    self.midfielder_lineups = {}
    self.half_forward_lineups = {}
    self.full_forward_lineups = {}
    self.off_lineups = {}
    self.get_pos_lineups()
    self.get_ascii()

  def __repr__(self):
    ps = '{0}\n'.format(self.nlist)
    ps += '{0}\n'.format(self.pos)
    ps += '{0}\n'.format(self.ascii)
    return ps

  def __str__(self):
    return self.__repr__()

  def post_match_reset(self, team):
    self.playing_lineups = {i: i for i in range(1, 16)}
    self.sub_lineups = {i: i for i in range(16, 22)}
    self.goalkeeper_lineups = {}
    self.full_back_lineups = {}
    self.half_back_lineups = {}
    self.midfielder_lineups = {}
    self.half_forward_lineups = {}
    self.full_forward_lineups = {}
    self.off_lineups = {}
    self.change(team, self.nlist)

  def change(self, team, x=None):
    if x is None:
      x = input('choose formation:\n{0}\n'.format(', '.join(sorted(formations)))).strip()
    if x in formations:
      self.nlist = x
      self.get_pos()
      self.get_pos_lineups()
      self.get_ascii()
      self.update_ascii(team)

  def remove_lineup(self, lineup):
    for i in self.playing_lineups:
      if self.playing_lineups[i] == lineup:
        playing_lineup = i
    self.off_lineups[lineup] = playing_lineup
    for x in self.playing_lineups:
      if self.playing_lineups[x] == lineup:
        self.playing_lineups[x] = None
    self.get_pos_lineups()

  def get_pos(self):
    self.pos = [int(i) for i in self.nlist.split('-')]

  def get_pos_lineups(self):
    # dict where key is starting lineup, value is current lineup
    self.goalkeeper_lineups[1] = self.playing_lineups[1]
    i = 2
    j = self.pos[0] + i
    for x in range(i, j):
      self.full_back_lineups[x] = self.playing_lineups[x]
    i = j
    j = self.pos[1] + i
    for x in range(i, j):
      self.half_back_lineups[x] = self.playing_lineups[x]
    i = j
    j = self.pos[2] + i
    for x in range(i, j):
      self.midfielder_lineups[x] = self.playing_lineups[x]
    i = j
    j = self.pos[3] + i
    for x in range(i, j):
      self.half_forward_lineups[x] = self.playing_lineups[x]
    i = j
    j = self.pos[4] + i
    for x in range(i, j):
      self.full_forward_lineups[x] = self.playing_lineups[x]

  def sub_on_off(self, on, off):
    for x in self.playing_lineups:
      if self.playing_lineups[x] == off:
        self.playing_lineups[x] = on
        self.sub_lineups[on] = None
        self.get_pos_lineups()
        return True

  def which_lineups(self, x, key=False):
    if key is False:
      if x in self.goalkeeper_lineups.values():
        return self.goalkeeper_lineups
      elif x in self.full_back_lineups.values():
        return self.full_back_lineups
      elif x in self.half_back_lineups.values():
        return self.half_back_lineups
      elif x in self.midfielder_lineups.values():
        return self.midfielder_lineups
      elif x in self.half_forward_lineups.values():
        return self.half_forward_lineups
      elif x in self.full_forward_lineups.values():
        return self.full_forward_lineups
    else:
      if x in self.goalkeeper_lineups.keys():
        return self.goalkeeper_lineups
      elif x in self.full_back_lineups.keys():
        return self.full_back_lineups
      elif x in self.half_back_lineups.keys():
        return self.half_back_lineups
      elif x in self.midfielder_lineups.keys():
        return self.midfielder_lineups
      elif x in self.half_forward_lineups.keys():
        return self.half_forward_lineups
      elif x in self.full_forward_lineups.keys():
        return self.full_forward_lineups

  def swap_playing_positions(self, x, y):
    x_lineups = self.which_lineups(x)
    y_lineups = self.which_lineups(y)
    # might be the same so use this verbose method
    for i in x_lineups:
      if x_lineups[i] == x:
        x_key = i
    for i in y_lineups:
      if y_lineups[i] == y:
        y_key = i
    x_lineups[x_key] = y
    y_lineups[y_key] = x
    self.playing_lineups[x_key] = y
    self.playing_lineups[y_key] = x

  def swap_playing_positions_off(self, on_lineup, off_lineup):
    on_lineups = self.which_lineups(on_lineup)
    off_lineups = self.which_lineups(off_lineup)
    # might be the same so use this verbose method
    for i in on_lineups:
      if on_lineups[i] == on_lineup:
        on_key = i
    for i in off_lineups:
      if off_lineups[i] == off_lineup:
        off_key = i
    on_lineups[on_key] = None
    off_lineups[off_key] = on_lineup

  def get_preferred_position(self, lineup):
    if lineup in [1, 16]:
      p = 'GK'
    elif lineup in self.full_back_lineups.values():
      p = 'FB'
    elif lineup in [17]:
      p = 'FB'
    elif lineup in self.half_back_lineups.values():
      p = 'HB'
    elif lineup in [18]:
      p = 'HB'
    elif lineup in self.midfielder_lineups.values():
      p = 'MI'
    elif lineup in [19]:
      p = 'MI'
    elif lineup in self.half_forward_lineups.values():
      p = 'HF'
    elif lineup in [20]:
      p = 'HF'
    elif lineup in self.full_forward_lineups.values():
      p = 'FF'
    elif lineup in [21]:
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

  def get_coords(self, i, off_count=None):
    if i in self.goalkeeper_lineups.values():
      x, y =  (170, 540)
    elif i in self.full_back_lineups.values():
      y = 480
      width = (340 / (len(self.full_back_lineups) + 1))
      j = list(self.full_back_lineups.values()).index(i) + 1
      x = (340 - (j*width))
    elif i in self.half_back_lineups.values():
      y = 380
      width = (340 / (len(self.half_back_lineups) + 1))
      j = list(self.half_back_lineups.values()).index(i) + 1
      x = (340 - (j*width))
    elif i in self.midfielder_lineups.values():
      y = 280
      width = (340 / (len(self.midfielder_lineups) + 1))
      j = list(self.midfielder_lineups.values()).index(i) + 1
      x = (340 - (j*width))
    elif i in self.half_forward_lineups.values():
      y = 180
      width = (340 / (len(self.half_forward_lineups) + 1))
      j = list(self.half_forward_lineups.values()).index(i) + 1
      x = (340 - (j*width))
    elif i in self.full_forward_lineups.values():
      y = 80
      width = (340 / (len(self.full_forward_lineups) + 1))
      j = list(self.full_forward_lineups.values()).index(i) + 1
      x = (340 - (j*width))
    elif i < 1:
      x = 380
      y = 290 + (off_count + 1) * 50
    else:
      x = 380
      y = 290 - ((21 - i) * 50)
    return x, y
