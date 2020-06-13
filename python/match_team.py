
from team import Team
from formation import Formation

import copy
import random
import time

def is_int(x):
  try:
    int(x)
  except:
     return False
  return True

class MatchTeam(Team):
  def __init__(self, team):
    self.__dict__ = copy.deepcopy(team.__dict__)
    self.playing = [x for x in self if x.lineup in range(1, 16)]
    self.subs = [x for x in self if x.lineup in range(16, 22)]
    self.formation = Formation()

  def update_positions(self):
    self.goalkeepers = [x for x in self.playing if x.position in ['GK']]
    self.full_backs = [x for x in self.playing if x.position in ['FB']]
    self.half_backs = [x for x in self.playing if x.position in ['HB']]
    self.midfielders = [x for x in self.playing if x.position in ['MI']]
    self.full_forwards = [x for x in self.playing if x.position in ['FF']]
    self.half_forwards = [x for x in self.playing if x.position in ['HF']]
    self.defenders = self.full_backs + self.half_backs
    self.forwards = self.full_forwards + self.half_forwards

  def update_playing_positions(self):
    self.goalkeepers = [x for x in self.playing if x.lineup == 1]
    self.full_backs = [x for x in self.playing if x.lineup in self.formation.full_back_lineups]
    self.half_backs = [x for x in self.playing if x.lineup in self.formation.half_back_lineups]
    self.midfielders = [x for x in self.playing if x.lineup in self.formation.midfielders_lineups]
    self.half_forwards = [x for x in self.playing if x.lineup in self.formation.half_forward_lineups]
    self.full_forwards = [x for x in self.playing if x.lineup in self.formation.full_forward_lineups]
    self.defenders = self.full_backs + self.half_backs
    self.forwards = self.full_forwards + self.half_forwards

  def lineup_check(self):
    lineups = [x.lineup for x in self]
    for i in range(1, 22):
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

  def formation_change(self):
    self.formation.change()
    self.update_playing_positions()

  def tactics(self):
    pass

  def manage(self):
    x = input('{0}\n'.format('\t'.join(['(l)ineup', '(s)ubstitute', '(f)ormation', '(t)actics']))).strip()
    if x in ['l', 'lineup']:
      if len([x for x in self if x.minutes > 0]) > 0:
        print('can\'t set up lineup during match!\r')
        time.sleep(1)
      else:
        self.lineup_change()
    if x in ['s', 'substitute']:
      self.substitute()
    elif x in ['f', 'formation']:
      self.formation_change()
    elif x in ['t', 'tactics']:
      self.tactics()

  def substitute(self, l_a=None, l_b=None):
    print(self)
    if l_b is None:
      l_b = input('substitute player coming on (last, first):')
    if ',' in l_b:
      f = l_b.split(',')[1].strip()
      l = l_b.split(',')[0].strip()
    else:
      return None
    players = [x for x in self.subs if (x.first_name == f) and (x.last_name == l)]
    if len(players) > 0:
      player_on = players[0]
      if l_a is None:
        l_a = input('substitute player coming off {(last, first):')
        if ',' in l_a:
          f = l_a.split(',')[1].strip()
          l = l_a.split(',')[0].strip()
        else:
          return None
        players = [x for x in self.playing if (x.first_name == f) and (x.last_name == l)]
        if len(players) > 0:
          player_off = players[0]
        else:
          return None
      self.playing.remove(player_off)
      self.subs.remove(player_on)
      self.playing.append(player_on)
    self.update_positions()
    self.get_player_table()
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

  def shooting_player_goal_attempt(self, shooting_player):
      p0 = random.random()
      if p0 < (shooting_player.shooting/100):
        shooting_player.goals += 1
        print('And he scores.', end='')
      else:
        print('But he misses.', end='')

  def shooting_player_point_attempt(self, shooting_player):
      p0 = random.random()
      if p0 < (shooting_player.shooting/100):
        shooting_player.points += 1
        print('And he scores.', end='')
      else:
        print('But he misses.', end='')

  def shooting_player_posession(self, shooting_player, defending_player):
    print('He passes the ball to {0}.'.format(shooting_player), end='')
    p0 = random.random()
    if p0 < ((defending_player.defending-30)/100):
      print('But {0} wins the ball back for {1}.'.format(defending_player, defending_player.team))
    elif p0 < 0.8:
      print('He shoots for a point.', end='')
      self.shooting_player_point_attempt(shooting_player)
    elif p0 < 0.98:
      print('He shoots for a goal.', end='')
      self.shooting_player_goal_attempt(shooting_player)
    else:
      self.foul(defending_player)

  def free_kick(self):
    shooting_player = self.choose_player(0.01, 0.1, 0.3)
    print('{0} steps up to take the free kick.'.format(shooting_player), end='')
    self.shooting_player_point_attempt(shooting_player)

  def foul(self, defender):
    print('But he is fouled by {0}.'.format(defender), end='')
    p0 = random.random()
    if p0 < 0.3:
      print('{0} receives a yellow card.'.format(defender), end='')
      defender.cards.append('y')
      if defender.cards.count('y') == 2:
        defender.cards.append('r')
        print('And it\'s his second yellow.  He is sent off by the referee.', end='')
        opp.playing.remove(defender)
    self.free_kick()

  def chance(self, opp):
    posession_player = self.choose_player(0.01, 0.2, 0.4)
    shooting_player = self.choose_player(0.01, 0.1, 0.3)
    while shooting_player == posession_player:
      shooting_player = self.choose_player(0.01, 0.1, 0.3)
    defending_player = opp.choose_player(0.1, 0.7, 0.15)
    print('Team {0} has a chance with {1} on the ball.'.format(self.name, posession_player), end='')
    p0 = random.random()
    if p0 < (posession_player.passing/100):
      self.shooting_player_posession(shooting_player, defending_player)
    elif p0 < 0.99:
      print('But he loses posession with the kick.', end='')
    else:
      self.foul(defending_player)
    shooting_player.update_score()
    self.update_score()

if __name__=="__main__":
  team = Team('a', 'a')
  mteam = MatchTeam(team)
  mteam.manage()

