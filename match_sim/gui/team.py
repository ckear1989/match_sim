
import time

import wx

from match_sim.cl.match_team import MatchTeam
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
    self.formation.injured_lineup(player.match.lineup)
    self.update_playing_positions()
    if self.control:
      print('playing', self.playing)
      print('subs', self.subs)
      print('off', self.off)
      print('playing lineups', self.formation.playing_lineups)
      print('off lineups', self.formation.off_lineups)
      print('injured lineups', self.formation.injured_lineups)
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
        event = MatchEvent(FORCED_SUB_EVENT, wx.ID_ANY)
        event.SetMyVal([self, player, reason])
        self.event_handler.ProcessEvent(event)
      else:
        self.auto_sub(player, preferred_position)
    self.update_playing_positions()

  def send_off_player(self, player):
    self.formation.remove_lineup(player.match.lineup)
    player.set_lineup(-1)
    self.update_playing_positions()
    if self.control:
      print('playing', self.playing)
      print('subs', self.subs)
      print('off', self.off)
      print('playing lineups', self.formation.playing_lineups)
      print('off lineups', self.formation.off_lineups)
      print('injured lineups', self.formation.injured_lineups)
    self.emit_send_off_event(player)

  def emit_send_off_event(self, player):
    if self.control is True:
      event = MatchEvent(PAUSE_EVENT, wx.ID_ANY)
      event.SetMyVal('{0} have lost {1} from their lineup.'.format(self.name, player))
      self.event_handler.ProcessEvent(event)

  def check_sub_made(self, player):
    self.update_playing_positions()
    if player in self.playing:
      return False
    return True
