
import random

class Event():
  def __init__(self, match):
    self.match = match
    a_tot = match.team_a.overall
    b_tot = match.team_b.overall
    p_team_a_chance = a_tot / (a_tot+b_tot)
    p_team_a_posession = match.team_a.posession / (match.team_a.posession + match.team_b.posession)
    p_team_a_chance = p_team_a_chance * p_team_a_posession
    if random.random() < p_team_a_chance:
      self.attackers = match.team_a
      self.defenders = match.team_b
    else:
      self.attackers = match.team_b
      self.defenders = match.team_a
    self.posession_player = self.attackers.choose_player(0.01, 0.2, 0.4)
    self.shooting_player = self.attackers.choose_player(0.01, 0.1, 0.3)
    self.defending_player = self.defenders.choose_player(0.1, 0.7, 0.15)
    while self.shooting_player == self.posession_player:
      self.shooting_player = self.attackers.choose_player(0.01, 0.1, 0.3)

  def run(self):
    print(self.match.stopclock_time, end=' ')
    attack_propensity = self.attackers.attacking / (self.attackers.attacking+self.attackers.defending)
    print('Team {0} has posession with {1} on the ball.'.format(self.attackers.name, self.posession_player), end='')
    p0 = random.random()
    if p0 < attack_propensity:
      self.attack()
    else:
      print('He cycles back to retain posession.')

  def attack(self):
      print('He looks forward to attack.'.format(self.attackers.name, self.posession_player), end='')
      p0 = random.random()
      if p0 < (self.posession_player.passing/100):
        self.shooting_player_posession()
      elif p0 < 0.99:
        print('But he loses posession with the kick.', end='')
      else:
        self.foul(self.posession_player)
      self.shooting_player.update_score()
      self.attackers.update_score()
      print(self.match.get_score())

  def shooting_player_goal_attempt(self):
      p0 = random.random()
      if p0 < (self.shooting_player.shooting/100):
        self.shooting_player.goals += 1
        print('And he scores.', end='')
      else:
        print('But he misses.', end='')

  def shooting_player_point_attempt(self):
      p0 = random.random()
      if p0 < (self.shooting_player.shooting/100):
        self.shooting_player.points += 1
        print('And he scores.', end='')
      else:
        print('But he misses.', end='')

  def shooting_player_posession(self):
    print('He passes the ball to {0}.'.format(self.shooting_player), end='')
    p0 = random.random()
    if p0 < ((self.defending_player.defending-30)/100):
      print('But {0} wins the ball back for {1}.'.format(self.defending_player, self.defending_player.team))
    elif p0 < 0.8:
      print('He shoots for a point.', end='')
      self.shooting_player_point_attempt()
    elif p0 < 0.98:
      print('He shoots for a goal.', end='')
      self.shooting_player_goal_attempt()
    else:
      self.foul(self.shooting_player)

  def free_kick(self):
    shooting_player = self.attackers.choose_player(0.01, 0.1, 0.3)
    print('{0} steps up to take the free kick.'.format(self.shooting_player), end='')
    self.shooting_player_point_attempt()

  def foul(self, attacker):
    print('But he is fouled by {0}.'.format(self.defending_player), end='')
    p0 = random.random()
    if p0 < 0.2:
      print('{0} receives a yellow card.'.format(self.defending_player), end='')
      self.defending_player.cards.append('y')
      if self.defending_player.cards.count('y') == 2:
        self.defending_player.cards.append('r')
        print('And it\'s his second yellow.  He is sent off by the referee.', end='')
        self.defending_player.gain_suspension('yellow', self.match.date)
        self.defenders.playing.remove(self.defending_player)
      p1 = random.random()
      if p1 < 0.2:
        attacker.gain_injury(self.match.date)
        self.attackers.forced_substitution(attacker)
    elif p0 < 0.25:
      print('{0} receives a red card.'.format(self.defending_player), end='')
      self.defending_player.cards.append('r')
      self.defending_player.gain_suspension('red', self.match.date)
      self.defenders.playing.remove(self.defending_player)
      if self.defending_player.position == 'GK':
        player_off = random.choice(self.defenders.playing)
        self.defenders.forced_substitution(player_off, 'GK',
          '{0} has been sent off. {1} is being substituted to bring on a GK'.format(self.defending_player, player_off))
      p2 = random.random()
      if p2 < 0.5:
        attacker.gain_injury(self.match.date)
        self.attackers.forced_substitution(attacker)
    self.free_kick()

if __name__ == "__main__":

  import datetime

  from match import Match
  from team import Team

  team_a = Team('a', 'a', control=True)
  team_b = Team('b', 'b', control=False)
  match = Match(team_a, team_b, datetime.date(2020, 1, 1), silent=False)
  random.seed(123) # team_a forced sub
  random.seed(1234) # team_b auto sub
  event = Event(match)
  event.run()

