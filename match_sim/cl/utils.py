'''Helper functions used by multiple scripts'''

import datetime
import time
import numpy as np
from tqdm import tqdm

def print_side_by_side(a, b, space=4):
  '''https://stackoverflow.com/questions/53401383/how-to-print-
     two-strings-large-text-side-by-side-in-python
  '''
  pstr = ''
  astr0 = str(a).split('\n')
  bstr0 = str(b).split('\n')
  amax = max([len(x) for x in astr0])
  bmax = max([len(x) for x in bstr0])
  size = max(amax, bmax)
  if (amax + bmax) < 180:
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
  else:
    pstr += '{0}\n{1}'.format(str(a) , str(b))
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

def random_normal(mean, sd):
  return round(np.random.normal(mean, sd), 0)

def get_sundays(start_date):
  sundays = []
  year = start_date.year
  for i in range(366):
    adate = start_date + datetime.timedelta(i)
    if adate.year == year:
      if adate.weekday() == 6:
        sundays.append(adate)
  return sundays

def timed_future_progress_bar(future, expected_time, increments=10):
  """
  https://stackoverflow.com/questions/59013308/python-progress-
    bar-for-non-loop-function
  Display progress bar for expected_time seconds.
  Complete early if future completes.
  Wait for future if it doesn't complete in expected_time.
  """
  interval = expected_time / increments
  with tqdm(total=increments) as pbar:
    for i in range(increments - 1):
      if future.done():
        # finish the progress bar
        # not sure if there's a cleaner way to do this?
        pbar.update(increments - i)
        return
      else:
        time.sleep(interval)
        pbar.update()
    # if the future still hasn't completed, wait for it.
    future.result()
    pbar.update()

