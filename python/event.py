'''Generate data for stochastic events'''

import random

class Event():
  '''Data generated for attacking event.  Stochastically evaluate event'''
  def __init__(self, amatch):
    self.stopclock_time = amatch.stopclock_time
    a_tot = amatch.team_a.overall
    b_tot = amatch.team_b.overall
    self.silent = amatch.silent
    self.date = amatch.date
    p_team_a_chance = a_tot / (a_tot+b_tot)
    p_team_a_posession = amatch.team_a.posession / amatch.team_b.posession
    p_team_a_chance = p_team_a_chance * p_team_a_posession
    if random.random() < p_team_a_chance:
      self.attackers = amatch.team_a
      self.defenders = amatch.team_b
    else:
      self.attackers = amatch.team_b
      self.defenders = amatch.team_a
    self.posession_player = self.attackers.choose_player(0.01, 0.2, 0.4)
    self.shooting_player = self.attackers.choose_player(0.01, 0.1, 0.3)
    self.defending_player = self.defenders.choose_player(0.1, 0.7, 0.15)
    self.goalkeeper = self.defenders.goalkeepers[0]
    while self.shooting_player == self.posession_player:
      self.shooting_player = self.attackers.choose_player(0.01, 0.1, 0.3)
    while self.goalkeeper == self.defending_player:
      self.defending_player = self.defenders.choose_player(0.1, 0.7, 0.15)
    self.pl = []

  def run(self, amatch):
    '''Print string collected from method.  Printed if match is not silent'''
    self.pl.append(self.stopclock_time + ' ')
    attack_propensity = min(1, (1.6 * self.attackers.attacking /
      (self.attackers.attacking+self.attackers.defending)))
    self.pl.append('{0} has posession with {1} on the ball.'.format(
      self.attackers.name, self.posession_player))
    p0 = random.random()
    if p0 < attack_propensity:
      self.attack(amatch)
    else:
      self.pl.append('He cycles back to retain posession.')
    if self.silent is not True:
      for x in self.pl:
        print(x, end='')
      print()
    self.attackers.update_playing_positions()
    self.defenders.update_playing_positions()

  def attack(self, amatch):
    '''Attackers have posession.  Pass or take on or foul given'''
    self.pl.append('He looks forward to attack.')
    p0 = random.random()
    if p0 < (0.33 * self.posession_player.physical.passing/100):
      self.posession_player_take_on()
    elif p0 < (0.66 * self.posession_player.physical.passing/100):
      self.shooting_player_posession()
    elif p0 < 0.98:
      self.pl.append('But he loses posession with the kick.')
    else:
      self.foul(self.posession_player)
    self.shooting_player.update_score()
    self.attackers.update_score()
    self.pl.append(amatch.get_score())

  def posession_player_take_on(self):
    '''Player takes on opponent with the ball.  Success or failure or foul determined'''
    self.pl.append('He takes the ball into the tackle against {0}.'.format(self.defending_player))
    p0 = random.random()
    if p0 < 0.4:
      self.pl.append('{0} gets past his man and looks to shoot.'.format(self.posession_player))
      p1 = random.random()
      if p1 < 0.8:
        self.pl.append('The kick goes high.')
        self.posession_player_point_attempt()
      else:
        self.pl.append('He\' bearing down on goal.')
        self.posession_player_goal_attempt()
    elif p0 < 0.8:
      self.pl.append('But {0} wins the ball back for {1}.'.format(
        self.defending_player, self.defending_player.team))
      self.defending_player.turnover()
    else:
      self.foul(self.posession_player)

  def posession_player_point_attempt(self):
    '''Point attempt made.  Pass correct parameter to method'''
    self.shooting_player_point_attempt(self.posession_player,
      self.attackers.choose_player(0.2, 0.4, 0.2))

  def posession_player_goal_attempt(self):
    '''Point attempt made.  Pass correct parameter to method'''
    self.shooting_player_goal_attempt(self.posession_player,
      self.attackers.choose_player(0.2, 0.4, 0.2))

  def shooting_player_goal_attempt(self, shooting_player=None, assisting_player=None):
    '''Point attempt made.  Score or wide or goalkeeper save determined'''
    if shooting_player is None:
      shooting_player = self.shooting_player
    if assisting_player is None:
      assisting_player = self.posession_player
    p0 = random.random()
    if p0 < (self.shooting_player.physical.shooting/100):
      shooting_player.score_goal()
      assisting_player.assist()
      self.pl.append('And he scores.')
    elif p0 < 0.95:
      self.pl.append('It\'s saved by the goalkeeper.')
      self.goalkeeper.save_goal()
    else:
      self.pl.append('But he misses.')

  def shooting_player_point_attempt(self, shooting_player=None, assisting_player=None):
    '''Point attempt made.  Score or wide determined'''
    if shooting_player is None:
      shooting_player = self.shooting_player
    if assisting_player is None:
      assisting_player = self.posession_player
    p0 = random.random()
    if p0 < (shooting_player.physical.shooting*1.2/100):
      self.pl.append('And he scores.')
      shooting_player.score_point()
      assisting_player.assist()
    else:
      self.pl.append('But he misses.')

  def shooting_player_posession(self):
    '''Shooting player receives ball.  Loses ball or shoots or fouled is determined'''
    self.pl.append('He passes the ball to {0}.'.format(self.shooting_player))
    p0 = random.random()
    if p0 < ((self.defending_player.physical.defending-30)/100):
      self.pl.append('But {0} wins the ball back for {1}.'.format(self.defending_player,
        self.defending_player.team))
      self.defending_player.turnover()
    elif p0 < 0.8:
      self.pl.append('He shoots for a point.')
      self.shooting_player_point_attempt()
    elif p0 < 0.98:
      self.pl.append('He shoots for a goal.')
      self.shooting_player_goal_attempt()
    else:
      self.foul(self.shooting_player)

  def free_kick(self, assister):
    '''Shooting player chosen.   Free kick or penalty decided.  Attempt method called'''
    shooting_player = self.attackers.choose_player(0.01, 0.1, 0.3)
    p0 = random.random()
    if p0 < 0.95:
      self.pl.append('{0} steps up to take the free kick.'.format(self.shooting_player))
      self.shooting_player_point_attempt(shooting_player, assister)
    else:
      self.pl.append('It\'s inside the box.  It will be a penalty.')
      self.pl.append('The penalty is to be taken by {0}.'.format(self.shooting_player))
      self.shooting_player_goal_attempt(shooting_player, assister)

  def foul(self, attacker):
    '''Foul event happens.  Card determined.  Injury determined.  Free kick given'''
    self.pl.append('But he is fouled by {0}.'.format(self.defending_player))
    p0 = random.random()
    if p0 < 0.2:
      self.pl.append('{0} receives a yellow card.'.format(self.defending_player))
      self.defending_player.gain_card('y')
      if self.defending_player.season.cards.count('y') == 2:
        self.defending_player.gain_card('r')
        self.pl.append('And it\'s his second yellow.  He is sent off by the referee.')
        self.defending_player.gain_suspension('yellow', self.date)
        self.defenders.playing.remove(self.defending_player)
      p1 = random.random()
      if p1 < 0.2:
        attacker.gain_injury(self.date)
        self.attackers.forced_substitution(attacker)
    elif p0 < 0.25:
      self.pl.append('{0} receives a red card.'.format(self.defending_player))
      self.defending_player.gain_card('r')
      self.defending_player.gain_suspension('red', self.date)
      self.defenders.playing.remove(self.defending_player)
      if self.defending_player.physical.position == 'GK':
        player_off = random.choice(self.defenders.playing)
        self.defenders.forced_substitution(player_off, 'GK',
          '{0} has been sent off. {1} is being substituted to bring on a GK'.format(
           self.defending_player, player_off))
      p2 = random.random()
      if p2 < 0.5:
        attacker.gain_injury(self.date)
        self.attackers.forced_substitution(attacker)
    self.free_kick(attacker)

if __name__ == "__main__":

  import datetime

  from match import Match
  from team import Team

  team_a = Team('a', 'a', control=True)
  team_b = Team('b', 'b', control=False)
  match = Match(team_a, team_b, datetime.date(2020, 1, 1), silent=False, extra_time_required=False)
  random.seed(123) # team_a forced sub
  random.seed(1234) # team_b auto sub
  event = Event(match)
  event.run(match)
