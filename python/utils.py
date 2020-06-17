'''Helper functions used by multiple scripts'''

import numpy as np

# https://stackoverflow.com/questions/53401383/how-to-print-two-strings-large-text-side-by-side-in-python
def print_side_by_side(a, b, size=60, space=4):
  pstr = ''
  astr0 = str(a).split('\n')
  bstr0 = str(b).split('\n')
  for i in range(max(len(astr0), len(bstr0))):
    if len(astr0) > i:
      astr = astr0[i]
    else:
      astr = ''
    if len(bstr0) > i:
      bstr = bstr0[i]
    else:
      bstr = ''
    while astr or bstr:
      pstr += astr[:size].ljust(size) + " " * space + bstr[:size]
      astr = astr[size:]
      bstr = bstr[size:]
    pstr += '\n'
  return pstr

def is_int(x):
  try:
    int(x)
  except ValueError:
    return False
  return True

def x_0_100_cap(x):
  return int(max(min(round(x, 0), 100), 0))

def random_0_100_normal(mean, sd):
  return x_0_100_cap(np.random.normal(mean, sd))
