
import time

import wx

from match_sim.match_team import MatchTeam
from match_sim.gui.match import MatchEvent, FORCED_SUB_EVENT, PAUSE_EVENT
from match_sim.gui.graphics import TeamColours

class Team(MatchTeam):
  def __init__(self, name, manager, players=None, control=False):
    super().__init__(name, manager, players, control)
    self.colour = TeamColours()
    self.update_event_handler()

  def update_event_handler(self, event_handler=None):
    self.event_handler = event_handler

  def forced_substitution(self, player, preferred_position=None, reason=None):
    '''Force user to make a sub'''
    subs_used = len([x for x in self.playing if x.match.lineup not in range(1, 16)])
    if subs_used > 4:
      self.playing.remove(player)
    else:
      if preferred_position is None:
        preferred_position = player.physical.position
      if reason is None:
        reason = '{0} {1} has {2} injured his {3} and needs to be substituted.'.format(
          player.physical.position, player, player.season.injury.status.lower(),
          player.season.injury.part)
      if self.control is True:
        event = MatchEvent(FORCED_SUB_EVENT, wx.ID_ANY)
        event.SetMyVal([self, player, reason])
        self.event_handler.ProcessEvent(event)
      else:
        self.auto_sub(player, preferred_position)

  def check_sub_made(self, player):
    self.update_playing_positions()
    if player in self.playing:
      return False
    return True
