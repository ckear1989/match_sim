
import pytest

from match_sim.tests.test_events import team_a

def test_team(team_a):
  assert len(team_a) == 30
  assert len(team_a.playing) == 15
  team_a.send_off_player(team_a.playing[0])
  assert len(team_a) == 30
  assert len(team_a.playing) == 14

