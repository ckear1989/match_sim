
import pytest
import copy
import datetime
import random

from match_sim.cl.event import Event
from match_sim.cl.match import Match
from match_sim.cl.team import Team
from match_sim.cl.match_team import MatchTeam

@pytest.fixture
def team_a():
  return MatchTeam(Team('a', 'a'), 'a')

@pytest.fixture
def team_b():
  return MatchTeam(Team('b', 'b'), 'b')

@pytest.fixture
def match(team_a, team_b):
  return Match(team_a, team_b, datetime.date(2020, 1, 1), True, False)

def run_event(i, team_a, team_b, match):
  random.seed(i)
  event = Event(match)
  event.run(match)

def test_event(team_a, team_b, match):
  run_event(123, team_a, team_b, match)
  run_event(123, team_a, team_b, match)

def test_event_posession(team_a, team_b, match):
  team_a.tactics_change('posession')
  team_b.tactics_change('posession')
  run_event(123, team_a, team_b, match)
  run_event(123, team_a, team_b, match)

def test_event_blanket(team_a, team_b, match):
  team_a.tactics_change('blanket')
  team_b.tactics_change('blanket')
  run_event(123, team_a, team_b, match)
  run_event(123, team_a, team_b, match)

def test_event_attacking(team_a, team_b, match):
  team_a.tactics_change('attacking')
  team_b.tactics_change('attacking')
  run_event(123, team_a, team_b, match)
  run_event(123, team_a, team_b, match)

def test_event_gung_ho(team_a, team_b, match):
  team_a.tactics_change('gung-ho')
  team_b.tactics_change('gung-ho')
  run_event(123, team_a, team_b, match)
  run_event(123, team_a, team_b, match)

def test_event_send_off(team_a, team_b):
  team_a.send_off_player(team_a.playing[0])
  team_b.send_off_player(team_b.playing[0])
  assert len(team_a.playing) == 14
  assert len(team_b.playing) == 14

def test_event_sub_1(team_a, team_b):
  team_a.auto_sub(team_a.playing[0])
  team_b.auto_sub(team_b.playing[0])
  assert len(team_a.playing) == 15
  assert len(team_b.playing) == 15
  assert team_a.subs_used == 1
  assert team_b.subs_used == 1

def test_event_sub_2(team_a, team_b):
  player_a = team_a.playing[0]
  player_b = team_b.playing[0]
  assert team_a.subs_used == 0
  assert team_b.subs_used == 0
  team_a.auto_sub(player_a)
  team_b.auto_sub(player_b)
  assert len(team_a.playing) == 15
  assert len(team_b.playing) == 15
  assert team_a.subs_used == 1
  assert team_b.subs_used == 1
  assert player_a not in team_a.playing
  assert player_b not in team_b.playing

