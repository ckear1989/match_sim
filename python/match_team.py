
from team import Team

import copy

class MatchTeam(Team):
  def __init__(self, team):
    self.__dict__ = copy.deepcopy(team.__dict__)

  def lineup_check(self):
    lineups = [x.lineup for x in self.players]
    for i in range(1, 21):
      if lineups.count(i) != 1:
        print('lineup problem with number %s' % i)
        self.lineup_change()

  def lineup_change(self, l_a=None, l_b=None):
    print(self)
    if l_a is None:
      l_a = int(input('lineup number to change:'))
    if l_b is None:
      l_b = input('player to assign lineup number {0} (last, first):'.format(l_a))
    f = l_b.split(',')[1].strip()
    l = l_b.split(',')[0].strip()
    players = [x for x in self.players if (x.first_name == f) and (x.last_name == l)]
    if len(players) > 0:
      player = players[0]
      player.lineup = l_a
    self.get_player_table()
    self.lineup_check()
    print(self)

if __name__=="__main__":
  team = Team('a', 'a')
  mteam = MatchTeam(team)
  mteam.lineup_change(1, 'Driscoll, Simon')
  mteam.lineup_change(40, 'Driscoll, Simon')

