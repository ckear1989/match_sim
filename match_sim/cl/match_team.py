'''Methods for manipulating team for management and matches'''

import random
import time

from match_sim.cl.utils import is_int
from match_sim.cl.team import Team
from match_sim.cl.formation import Formation
from match_sim.cl.tactics import Tactics

class MatchTeam(Team):
  '''Contain all data on team and players'''
  def __init__(self, name, manager, players=None, control=False):
    super().__init__(name, manager, players, control)
    self.formation = Formation()
    self.tactics = Tactics()
    self.auto_lineup()
    self.stats_update()
    self.free_taker_right = sorted([x for x in self], reverse=True,
      key=lambda x: x.physical.right+x.physical.shooting)[0]
    self.free_taker_left = sorted([x for x in self], reverse=True,
      key=lambda x: x.physical.left+x.physical.shooting)[0]
    self.free_taker_long = sorted([x for x in [self.free_taker_right,
      self.free_taker_left]], reverse=True, key=lambda x: x.physical.shooting)[0]

  def update_playing_positions(self):
    '''Update team positions based on lineup and formation'''
    self.formation.get_pos_lineups()
    self.goalkeepers = [x for x in self.playing if x.match.lineup in
      self.formation.goalkeeper_lineups]
    self.full_backs = [x for x in self.playing if x.match.lineup in
      self.formation.full_back_lineups]
    self.half_backs = [x for x in self.playing if x.match.lineup in
      self.formation.half_back_lineups]
    self.midfielders = [x for x in self.playing if x.match.lineup in
      self.formation.midfielder_lineups]
    self.half_forwards = [x for x in self.playing if x.match.lineup in
      self.formation.half_forward_lineups]
    self.full_forwards = [x for x in self.playing if x.match.lineup in
      self.formation.full_forward_lineups]
    self.defenders = self.full_backs + self.half_backs
    self.forwards = self.full_forwards + self.half_forwards
    self.off = [x for x in self if ((x.match.lineup < 1) and (x.match.minutes > 0))]
    self.get_player_table()

  def update_free_taker(self, pstring, side):
    player = [x for x in self if str(x) == pstring][0]
    if side == 'left':
      self.free_taker_left = player
    elif side == 'right':
      self.free_taker_right = player
    elif side == 'long':
      self.free_taker_long = player

  def lineup_change(self, l_a=None, l_b=None):
    '''Ask user to change lineup.  Continue is only escape'''
    if self.control is True:
      print('set pre-match lineup')
      time.sleep(0.5)
      print(self)
      if l_b is None:
        l_b = input('(c)ontinue or\nplayer to assign new lineup number (last, first):\n')
      if l_b in ['c', 'continue']:
        return
      if ',' in l_b:
        f = l_b.split(',')[1].strip()
        l = l_b.split(',')[0].strip()
      else:
        cmd = input('(c)ontinue ?\n')
        if cmd not in ['c', 'continue']:
          self.lineup_change()
        return
      players = [x for x in self if (x.first_name == f) and (x.last_name == l)]
      if len(players) > 0:
        player = players[0]
        if l_a is None:
          l_a = input('(c)ontinue or\nlineup number to change {0} to:'.format(player))
          if l_a in ['c', 'continue']:
            return
          if is_int(l_a):
            l_a = int(l_a)
          else:
            cmd = input('(c)ontinue ?\n')
            if cmd not in ['c', 'continue']:
              self.lineup_change()
            return
        player.match.lineup = l_a
      self.update_playing_positions()
      print(self)
      cmd = input('(c)ontinue ?\n')
      if cmd not in ['c', 'continue']:
        self.lineup_change()
      return True

  def formation_change(self, x=None):
    '''Call formation method'''
    self.formation.change(self, x)
    self.update_playing_positions()

  def tactics_change(self, x=None):
    '''Call tactics method. Update team stats'''
    self.tactics.change(x)
    self.stats_update()

  def stats_update(self):
    '''Copy chosen tactic attributes'''
    self.attacking = self.tactics.s['attacking']
    self.posession = self.tactics.s['posession']
    self.defending = self.tactics.s['defending']
    self.update_playing_positions()

  def manage(self):
    '''Ask user to manage team.  Control is only escape'''
    if self.control is True:
      x = ''
      while x not in ['c', 'continue']:
        x = input('{0}\n'.format('\t'.join(['(l)ineup', '(s)ubstitute', '(f)ormation',
          '(t)actics', '(c)ontinue']))).strip()
        if x in ['l', 'lineup']:
          if len([x for x in self if x.match.minutes > 0]) > 0:
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
    '''Force user to make a sub'''
    subs_used = len([x for x in self.playing if x.match.lineup not in range(1, 16)])
    if subs_used > 4:
      self.playing.remove(player)
      player.set_lineup(0)
    else:
      if preferred_position is None:
        preferred_position = player.physical.position
      if reason is None:
        reason = '{0} {1} has {2} injured his {3} and needs to be substituted.'.format(
          player.physical.position, player, player.season.injury.status.lower(),
          player.season.injury.part)
      if self.control is True:
        sub_made = False
        while sub_made is not True:
          if self.control is True:
            print(reason)
          sub_made = self.substitute(l_a=player)
      else:
        self.auto_sub(player, preferred_position)
    self.update_playing_positions()

  def auto_lineup(self):
    '''Set team lineup for non-controlled team.  Force changes only when necessary'''
    self.formation.post_match_reset(self)
    self.eligible = [p for p in self if (p.season.injury.status is None) and (p.season.suspension.status is None)]
    for x in self:
      x.match.lineup = -1
      if x in self.eligible:
        x.match.lineup = 0
    for i in range(1, 22):
      preferred_position = self.formation.get_preferred_position(i)
      player_on = [x for x in self.eligible if x.physical.position == preferred_position and
        x.match.lineup not in range(1, 22)]
      if len(player_on) > 0:
        player_on = sorted(player_on, key=lambda x: -x.physical.condition)[0]
        player_on.match.lineup = i
      else:
        player_on = [x for x in self.eligible if x.match.lineup not in range(1, 22)]
        if len(player_on) > 0:
          player_on = sorted(player_on, key=lambda x: -x.physical.condition)[0]
          player_on.match.lineup = i
        else:
          raise Exception('team {0} unable to fill lineup number {1}\n{2}'.format(
            self.name, i, self))
    self.playing = [p for p in self.eligible if p.match.lineup in range(1, 16)]
    self.subs = [p for p in self.eligible if p.match.lineup in range(16, 22)]
    self.update_playing_positions()

  def send_off_player(self, player):
    self.formation.playing_lineups.remove(player.match.lineup)
    player.update_lineup(-1)
    self.playing.remove(player)

  def auto_sub(self, player, preferred_position=None):
    '''For non-controlled teams choose sub'''
    if preferred_position is None:
      preferred_position = player.position
    player_on = [x for x in self.subs if x.physical.position == player.physical.position]
    if len(player_on) > 0:
      self.substitute(player, sorted(player_on, key=lambda x: -x.physical.condition)[0])
    else:
      self.substitute(player, sorted(self.subs, key=lambda x: -x.physical.condition)[0])
    self.update_playing_positions()

  def substitute(self, l_a=None, l_b=None):
    '''Determine if sub can be made.  Ask user for players to switch.  Execute switch'''
    subs_used = len([x for x in self.playing if x.match.lineup not in range(1, 16)])
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
          return
        players = [x for x in self.subs if (x.first_name == f) and (x.last_name == l)]
        if len(players) > 0:
          player_on = players[0]
        else:
          print('Player "{0}" not found in substitutes. \
                 Please check player is numbered 16-21.'.format(l_b))
          return
      else:
        player_on = l_b
      if l_a is None:
        l_a = input('substitute player coming off {(last, first):')
        if ',' in l_a:
          f = l_a.split(',')[1].strip()
          l = l_a.split(',')[0].strip()
        else:
          print('No comma detected in "{0}". Please use (last, first) format'.format(l_a))
          return
        players = [x for x in self.playing if (x.first_name == f) and (x.last_name == l)]
        if len(players) > 0:
          player_off = players[0]
        else:
          print('Player "{0}" not found in currently playing. Please check \
            player is currently on.'.format(l_a))
          return
      else:
        player_off = l_a
      if self.control is True:
        print('{0} is coming on for {1}.'.format(player_on, player_off))
      self.playing.remove(player_off)
      self.subs.remove(player_on)
      self.playing.append(player_on)
      self.formation.ammend_pos_lineups(player_off.match.lineup, player_on.match.lineup)
      player_off.set_lineup(0)
      self.update_playing_positions()
      if self.control is True:
        print(self)
      return True
    print('{0} substitutes already used'.format(subs_used))
    return

  def condition_deteriorate(self, n):
    for x in self.players:
      x.condition_deteriorate(n)
    self.get_overall()

  def choose_player(self, p0, p1, p2):
    '''Randomly choose player from position bucket.'''
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

  def choose_free_taker(self):
    if ((self.free_taker_right in self.playing) and
      (self.free_taker_left in self.playing)):
      return random.choice([self.free_taker_right, self.free_taker_left])
    elif ((self.free_taker_right in self.playing) and
      (self.free_taker_left not in self.playing)):
      return random.choice([self.free_taker_right, self.choose_player(0.05, 0.1, 0.2)])
    elif ((self.free_taker_right not in self.playing) and
      (self.free_taker_left in self.playing)):
      return random.choice([self.free_taker_left, self.choose_player(0.05, 0.1, 0.2)])
    else:
      return self.choose_player(0.05, 0.1, 0.2)

  def choose_free_taker_45(self):
    if (self.free_taker_long in self.playing):
      return self.free_taker_long
    elif (self.free_taker_right in self.playing):
      return self.free_taker_right
    elif (self.free_taker_left in self.playing):
      return self.free_taker_left
    else:
      return self.choose_player(0.05, 0.1, 0.2)

  def reset_match_stats(self):
    '''Clear all scores etc. for beginning of next match'''
    super().reset_match_stats()
    self.formation.get_pos_lineups()

if __name__ == "__main__":
  mteam = MatchTeam('a', 'a', control=True)
  mteam.manage()
