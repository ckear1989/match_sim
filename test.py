
import copy
import cProfile
import datetime
import pstats
import random

from match_sim.event import Event
from match_sim.match import Match
from match_sim.team import Team
from match_sim.match_team import MatchTeam

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

if __name__ == "__main__":

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

