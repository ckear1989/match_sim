
import wx

from match_sim.event import Event as ClEvent

MATCH_EVENT = wx.NewEventType()
MATCH_EVENT_CUSTOM = wx.PyEventBinder(MATCH_EVENT, 1)
REFRESH_EVENT = wx.NewEventType()
REFRESH_EVENT_CUSTOM = wx.PyEventBinder(REFRESH_EVENT, 1)

class MatchEvent(wx.PyCommandEvent):
  def __init__(self, evtType, id):
    wx.PyCommandEvent.__init__(self, evtType, id)
    myVal = None

  def SetMyVal(self, val):
    self.myVal = val

  def GetMyVal(self):
    return self.myVal

class EventPl(list):
  def __init__(self, event_handler):
    super().__init__()
    self.event_handler = event_handler

  def append(self, astr):
    self.emit_match_event(astr)

  def emit_match_event(self, astr):
    event = MatchEvent(MATCH_EVENT, wx.ID_ANY)
    event.SetMyVal(astr)
    self.event_handler.ProcessEvent(event)

class Event(ClEvent):
  def __init__(self, amatch, event_handler):
    super().__init__(amatch)
    self.event_handler = event_handler
    self.pl = EventPl(self.event_handler)
    self.match = amatch

  def full_time(self):
    '''Update scorer stats.  Print final result'''
    self.pl.append('Full time score is:\n{0}'.format(self.match.get_score().replace('Score is now ', '')))

  def half_time(self):
    self.pl.append('And that\'s the end of the half')

  def emit_refresh_event(self):
    event = MatchEvent(REFRESH_EVENT, wx.ID_ANY)
    self.event_handler.ProcessEvent(event)

  def run(self, amatch):
    '''Print string collected from method.  Printed if match is not silent'''
    old_score = self.match.get_score()[:]
    super().run(amatch)
    new_score = self.match.get_score()[:]
    if new_score != old_score:
      self.emit_refresh_event()
