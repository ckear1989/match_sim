
import keyboard
from match_sim.tests.test_events import team_a, team_b, match

def test_match(match):
  assert match.time == 0
  assert match.silent == True

def test_play_match(match):
  match.play()
