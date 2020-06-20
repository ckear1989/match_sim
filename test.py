
import cProfile
import datetime
import pstats

from match_sim.event import Event
from match_sim.match import Match
from match_sim.team import Team
from match_sim.match_team import MatchTeam

def run_events(n):
  for i in range(n):
    match = Match(team_a, team_b, datetime.date(2020, 1, 1), True, False)
    event = Event(match, i)
    event.run(match)

def time_events(n, f_calls):
  cProfile.run('run_events({0})'.format(n), 'profile1.txt')
  p = pstats.Stats('profile1.txt')
  my_stats = p.strip_dirs().stats
  f_keys = [x for x in my_stats.keys() if x[2] in f_calls]
  f_vals = [my_stats[y] for y in f_keys]
  my_stats = {x[2]: y[0] for x, y in zip(f_keys, f_vals)}
  return my_stats

if __name__ == "__main__":

  team_a = MatchTeam(Team('a', 'a'))
  team_b = MatchTeam(Team('b', 'b'))
  functions0 = ['attack', 'recycle_posession']
  functions1 = ['posession_player_take_on', 'shooting_player_posession']
  print(time_events(10, functions0))
  print(time_events(100, functions0))
  print(time_events(10, functions1))
  print(time_events(100, functions1))

