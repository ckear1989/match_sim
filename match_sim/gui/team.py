
from match_sim.match_team import MatchTeam
from match_sim.gui.graphics import TeamColours

class Team(MatchTeam):
  def __init__(self, name, manager, players=None, control=False):
    super().__init__(name, manager, players, control)
    self.colour = TeamColours()
