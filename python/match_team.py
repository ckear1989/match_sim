
from team import Team

import copy
import random

def is_int(x):
  try:
    int(x)
  except:
     return False
  return True

class MatchTeam(Team):
  def __init__(self, team):
    self.__dict__ = copy.deepcopy(team.__dict__)

  def lineup_check(self):
    lineups = [x.lineup for x in self]
    for i in range(1, 21):
      if lineups.count(i) == 1:
        continue
      elif lineups.count(i) == 0:
        print('No player assigned to number %s' % i)
      elif lineups.count(i) > 1:
        print('{0} players assigned to number {1}'.format(lineups.count(i), i))
      self.lineup_change()

  def lineup_change(self, l_a=None, l_b=None):
    print(self)
    if l_b is None:
      l_b = input('player to assign new lineup number (last, first):')
    if ',' in l_b:
      f = l_b.split(',')[1].strip()
      l = l_b.split(',')[0].strip()
    else:
      return None
    players = [x for x in self if (x.first_name == f) and (x.last_name == l)]
    if len(players) > 0:
      player = players[0]
      if l_a is None:
        l_a = input('lineup number to change {0} to:'.format(player))
        if is_int(l_a):
          l_a = int(l_a)
        else:
          return None
      player.lineup = l_a
    self.get_player_table()
    self.lineup_check()
    print(self)

  def choose_player(self, p0, p1, p2):
    p = random.random()
    if p < p0:
      player = random.choice(self.goalkeepers)
    elif p < (p0+p1):
      player = random.choice(self.defenders)
    elif p < (p0+p1+p2):
      player = random.choice(self.midfielders)
    else:
      player = random.choice(self.forwards)
    return player

  def chance(self, opp):
    posession_player = self.choose_player(0.01, 0.2, 0.4)
    shooting_player = self.choose_player(0.01, 0.1, 0.3)
    defending_player = opp.choose_player(0.1, 0.7, 0.15)
    print('Team {0} has a chance with {1} on the ball.'.format(self.name, posession_player), end='')
    if random.random() < (posession_player.passing/100):
      print('He passes the ball to {0}.'.format(shooting_player), end='')
      if random.random() < ((defending_player.defending-30)/100):
        print('But {0} wins the ball back for {1}.'.format(defending_player, opp.name))
      elif random.random() < 0.8:
        print('He shoots for a point.', end='')
        if random.random() < (shooting_player.shooting/100):
          shooting_player.points += 1
          print('And he scores.', end='')
        else:
          print('But he misses.', end='')
      else:
        print('He shoots for a goal.', end='')
        if random.random() < (shooting_player.shooting/100):
          shooting_player.goals += 1
          print('And he scores.', end='')
        else:
          print('But he misses.', end='')
    else:
        print('But he loses posession with the kick.', end='')
    shooting_player.update_score()
    self.update_score()

if __name__=="__main__":
  team = Team('a', 'a')
  mteam = MatchTeam(team)
  mteam.lineup_change()
  mteam.lineup_change(1, 'Driscoll, Simon')
  mteam.lineup_change(40, 'Driscoll, Simon')

