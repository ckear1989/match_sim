
import copy
import cProfile
import datetime
import pstats
import random

import matplotlib
import matplotlib.pyplot as plt
import numpy as np

from match_sim.event import Event
from match_sim.injury import Injury
from match_sim.match import Match
from match_sim.match_team import MatchTeam
from match_sim.suspension import Suspension
from match_sim.team import Team

def run_events(n):
  for i in range(n):
    random.seed(i)
    match = Match(copy.deepcopy(team_a), copy.deepcopy(team_b), datetime.date(2020, 1, 1), True, False)
    event = Event(match)
    event.run(match)

def time_events(n, f_calls, team_x, team_y):
  cProfile.run('run_events({0})'.format(n), 'profile1.txt')
  p = pstats.Stats('profile1.txt')
  my_stats = p.strip_dirs().stats
  f_keys = [x for x in my_stats.keys() if x[2] in f_calls]
  f_vals = [my_stats[y] for y in f_keys]
  my_stats = {x[2]: y[0]/n for x, y in zip(f_keys, f_vals)}
  return my_stats

def event_distribution_tactic_change():
  functions0 = ['attack', 'recycle_posession', 'defensive_setup']
  functions1 = ['branch0', 'branch1', 'branch2', 'branch3']
  team_a = MatchTeam(Team('a', 'a'))
  team_b = MatchTeam(Team('b', 'b'))
  print(time_events(200, functions0, team_a, team_b))
  print(time_events(200, functions1, team_a, team_b))
  team_a.tactics_change('posession')
  team_b.tactics_change('posession')
  print(time_events(200, functions0, team_a, team_b))
  print(time_events(200, functions1, team_a, team_b))
  team_a.tactics_change('blanket')
  team_b.tactics_change('blanket')
  print(time_events(200, functions0, team_a, team_b))
  print(time_events(200, functions1, team_a, team_b))
  team_a.tactics_change('attacking')
  team_b.tactics_change('attacking')
  print(time_events(200, functions0, team_a, team_b))
  print(time_events(200, functions1, team_a, team_b))
  team_a.tactics_change('gung-ho')
  team_b.tactics_change('gung-ho')
  print(time_events(200, functions0, team_a, team_b))
  print(time_events(200, functions1, team_a, team_b))

def plot_distribution(adict, title, ylabel, outfile):
  max_x = max([x for y in adict.values() for x in y])
  t = np.arange(0, max_x*2, 1)
  fig, ax = plt.subplots()
  for status in adict.keys():
    y = [adict[status].count(i) for i in t]
    y = [x if x > 0 else np.nan for x in y]
    # ax.plot(t, y, label=status)
    ax.bar(t, y, label=status)
  ax.set_ylabel(ylabel)
  ax.set_title(title)
  ax.legend()
  plt.savefig(outfile)

def injury_distribution(n):
  out_dict = {'Slightly': [], 'Severely': []}
  injury = Injury()
  for i in range(n):
    injury.gain(datetime.date(2020, 1, 1))
    out_dict[injury.status].append((injury.return_date - datetime.date(2020, 1, 1)).days)
  plot_distribution(out_dict, 'Injury length (days) by status', 'Count', 'injury.png')

def suspension_distribution(n):
  out_dict = {'red': [], 'yellow': []}
  suspension = Suspension()
  for i in range(n):
    suspension.gain('red', datetime.date(2020, 1, 1))
    out_dict[suspension.status].append((suspension.return_date - datetime.date(2020, 1, 1)).days)
  for i in range(n):
    suspension.gain('yellow', datetime.date(2020, 1, 1))
    out_dict[suspension.status].append((suspension.return_date - datetime.date(2020, 1, 1)).days)
  plot_distribution(out_dict, 'Suspension length (days) by status', 'Count', 'suspension.png')

if __name__ == "__main__":

  # event_distribution_tactic_change()
  # injury_distribution(50000)
  suspension_distribution(10)
