
import numpy as np
import random

import default

class Player():
  def __init__(self):
    self.first_name = random.choice(default.first_names)
    self.last_name = random.choice(default.last_names)
    self.overall = int(round(np.random.normal(50, 20), 0))

  def __repr__(self):
    ps = '{0} {1}\noverall:{2:d}'.format(self.first_name, self.last_name, self.overall)
    return ps

  def __str__(self):
    return self.__repr__

