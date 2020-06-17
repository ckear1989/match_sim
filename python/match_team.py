
from team import Team
from formation import Formation
from tactics import Tactics

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
    self.tactics = Tactics()
    self.stats_update()
    self.get_lineup()
    self.lineup_check()
    self.update_playing_positions()

  def update_playing_positions(self):
    self.goalkeepers = [x for x in self.playing if x.lineup in self.formation.goalkeeper_lineups]
    self.full_backs = [x for x in self.playing if x.lineup in self.formation.full_back_lineups]
    self.half_backs = [x for x in self.playing if x.lineup in self.formation.half_back_lineups]
    self.midfielders = [x for x in self.playing if x.lineup in self.formation.midfielder_lineups]
    self.half_forwards = [x for x in self.playing if x.lineup in self.formation.half_forward_lineups]
    self.full_forwards = [x for x in self.playing if x.lineup in self.formation.full_forward_lineups]
    self.defenders = self.full_backs + self.half_backs
    self.forwards = self.full_forwards + self.half_forwards
    self.get_player_table()

  def lineup_check(self):
    lineups = [x.lineup for x in self]
    for i in range(1, 22):
      if lineups.count(i) == 1:
        p = [x for x in self if x.lineup == i][0]
        if p.injury.status is not None:
          print('{0} in number {1} has an injury.\n{2}'.format(p, i, p.injury))
        if p.suspension.status is not None:
          print('{0} in number {1} is suspended.\n{2}'.format(p, i, p.suspension))
        else:
          continue
      elif lineups.count(i) == 0:
        print('No player assigned to number %s' % i)
      elif lineups.count(i) > 1:
        print('{0} players assigned to number {1}'.format(lineups.count(i), i))
      if self.control is True:
        self.lineup_change()
      else:
        self.auto_lineup()
    self.update_playing_positions()
    self.formation.update_ascii(self)

  def lineup_change(self, l_a=None, l_b=None):
    if self.control is True:
      print('set pre-match lineup')
      time.sleep(0.3)
      print(self)
      if l_b is None:
        l_b = input('player to assign new lineup number (last, first):')
      if ',' in l_b:
        f = l_b.split(',')[1].strip()
        l = l_b.split(',')[0].strip()
      else:
        cmd = input('(c)ontinue\n')
        if cmd not in ['c', 'continue']:
          self.lineup_change()
        return None
      players = [x for x in self if (x.first_name == f) and (x.last_name == l)]
      if len(players) > 0:
        player = players[0]
        if l_a is None:
          l_a = input('lineup number to change {0} to:'.format(player))
          if is_int(l_a):
            l_a = int(l_a)
          else:
            cmd = input('(c)ontinue\n')
            if cmd not in ['c', 'continue']:
              self.lineup_change()
            return None
        player.lineup = l_a
      self.update_playing_positions()
      self.lineup_check()
      print(self)
      cmd = input('(c)ontinue\n')
      if cmd not in ['c', 'continue']:
        self.lineup_change()

  def formation_change(self):
    self.formation.change(self)
    self.update_playing_positions()

  def tactics_change(self):
    self.tactics.change()
    self.stats_update()
    self.update_playing_positions()

  def stats_update(self):
    self.attacking = self.tactics.s['attacking']
    self.posession = self.tactics.s['posession']
    self.defending = self.tactics.s['defending']
    self.update_playing_positions()

  def manage(self):
    if self.control is True:
      x = ''
      while x not in ['c', 'continue']:
        x = input('{0}\n'.format('\t'.join(['(l)ineup', '(s)ubstitute', '(f)ormation', '(t)actics', '(c)ontinue']))).strip()
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
          self.tactics_change()

  def forced_substitution(self, player, preferred_position=None, reason=None):
    subs_used = len([x for x in self.playing if x.lineup not in range(1, 16)])
    if subs_used > 4:
      self.playing.remove(player)
    else:
      if preferred_position is None:
        preferred_position = player.position
      if reason is None:
        reason = '{0} {1} has {2} injured his {3} and needs to be substituted.'.format(
          player.position, player, player.injury.status.lower(), player.injury.part)
      if self.control is True:
        sub_made = False
        while sub_made is not True:
          print(reason)
          sub_made = self.substitute(l_a=player)
      else:
        self.auto_sub(player, preferred_position)

  def auto_lineup(self):
    lineups = [x.lineup for x in self]
    for i in range(1, 22):
      if lineups.count(i) == 1:
        p = [x for x in self if x.lineup == i][0]
        if p.injury.status is not None:
          player_on = [x for x in self if x.position == p.position and x.lineup not in range(1, 22)]
          if len(player_on) > 0:
            random.choice(player_on).lineup = p.lineup
            p.lineup = 0
          else:
            player_on = [x for x in self if x.lineup not in range(1, 22)]
            if len(player_on) > 0:
              random.choice(player_on).lineup = p.lineup
              p.lineup = 0
            else:
              raise Exception('team {0} unable to fill lineup due to injury to {1}\n{2}'.format(self.name, p, self))
        if p.suspension.status is not None:
          player_on = [x for x in self if x.position == p.position and x.lineup not in range(1, 22)]
          if len(player_on) > 0:
            random.choice(player_on).lineup = p.lineup
            p.lineup = 0
          else:
            player_on = [x for x in self if x.lineup not in range(1, 22)]
            if len(player_on) > 0:
              random.choice(player_on).lineup = p.lineup
              p.lineup = 0
            else:
              raise Exception('team {0} unable to fill lineup due to suspension to {1}\n{2}'.format(self.name, p, self))
        else:
          continue
      elif lineups.count(i) == 0:
        preferred_position = self.formation.get_preferred_position(i)
        player_on = [x for x in self if x.position == preferred_position and x.lineup not in range(1, 22)]
        if len(player_on) > 0:
          player_on = random.choice(player_on)
          player_on.lineup = i
        else:
          player_on = [x for x in self if x.lineup not in range(1, 22)]
          if len(player_on) > 0:
            player_on = random.choice(player_on)
            player_on.lineup = i
          else:
            raise Exception('team {0} unable to fill lineup number {1}\n{2}'.format(self.name, i, self))
      elif lineups.count(i) > 1:
        while lineups.count(i) > 1:
          player_off = [x for x in self if x.lineup == i]
          player_off = random.choice(player_off)
          player_off.lineup = 0
          lineups = [x.lineup for x in self]
    self.update_playing_positions()

  def auto_sub(self, player, preferred_position=None):
    if preferred_position is None:
      preferred_position = player.position
    player_on = [x for x in self.subs if x.position == player.position]
    if len(player_on) > 0:
      self.substitute(player, random.choice(player_on))
    else:
      self.substitute(player, random.choice(self.subs))

  def substitute(self, l_a=None, l_b=None):
    subs_used = len([x for x in self.playing if x.lineup not in range(1, 16)])
    if subs_used < 5:
      if self.control is True:
        print(self)
      if l_b is None:
        l_b = input('substitute player coming on (last, first):')
        if ',' in l_b:
          f = l_b.split(',')[1].strip()
          l = l_b.split(',')[0].strip()
        else:
          print('No comma detected in "{0}". Please use (last, first) format'.format(l_b))
          return None
        players = [x for x in self.subs if (x.first_name == f) and (x.last_name == l)]
        if len(players) > 0:
          player_on = players[0]
        else:
          print('Player "{0}" not found in substitutes. Please check player is numbered 16-21.'.format(l_b))
          return None
      else:
        player_on = l_b
      if l_a is None:
        l_a = input('substitute player coming off {(last, first):')
        if ',' in l_a:
          f = l_a.split(',')[1].strip()
          l = l_a.split(',')[0].strip()
        else:
          print('No comma detected in "{0}". Please use (last, first) format'.format(l_a))
          return None
        players = [x for x in self.playing if (x.first_name == f) and (x.last_name == l)]
        if len(players) > 0:
          player_off = players[0]
        else:
          print('Player "{0}" not found in currently playing. Please check player is currently on.'.format(l_a))
          return None
      else:
        player_off = l_a
      print('{0} is coming on for {1}.'.format(player_on, player_off))
      self.playing.remove(player_off)
      self.subs.remove(player_on)
      self.playing.append(player_on)
      self.formation.ammend(player_off.lineup, player_on.lineup)
      self.update_playing_positions()
      if self.control is True:
        print(self)
      return True
    else:
      print('{0} substitutes already used'.format(subs_used))

  def choose_player(self, p0, p1, p2):
    try:
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
    except IndexError:
      return self.choose_player(p0, p1, p2)

if __name__=="__main__":
  team = Team('a', 'a', control=True)
  mteam = MatchTeam(team)
  mteam.manage()

