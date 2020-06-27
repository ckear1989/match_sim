
from match_sim.gui.template import TemplatePanel, TemplateButton

import sys
import os
import pathlib
path = pathlib.Path(__file__).parent.absolute()

# import pygame
import wx

class ManagePanel(TemplatePanel):
  def __init__(self, parent):
    super().__init__(parent)
    lineup_button = TemplateButton(self, 'Lineup')
    lineup_button.Bind(wx.EVT_BUTTON, self.on_lineup)
    self.hbox3.Add(lineup_button)
    formation_button = TemplateButton(self, 'Formation')
    formation_button.Bind(wx.EVT_BUTTON, self.on_tactics)
    self.hbox3.Add(formation_button)
    tactics_button = TemplateButton(self, 'Tactics')
    tactics_button.Bind(wx.EVT_BUTTON, self.on_tactics)
    self.hbox3.Add(tactics_button)
    training_button = TemplateButton(self, 'Training')
    training_button.Bind(wx.EVT_BUTTON, self.on_training)
    self.hbox3.Add(training_button)
    self.SetSizer(self.main_sizer)

  def on_lineup(self, event):
    self.GetParent().on_lineup(LineupPanel)

  def on_formation(self, event):
    self.GetParent().on_formation(FormationPanel)

  def on_tactics(self, event):
    self.GetParent().on_tactics(TacticsPanel)

  def on_training(self, event):
    self.GetParent().on_training(TrainingPanel)

class LineupPanel(TemplatePanel):
  def __init__(self, parent):
    super().__init__(parent)
    self.txt_output.Destroy()
    self.team = self.GetParent().game.teams[self.GetParent().game.team]
    self.starting = wx.ListBox(self)
    self.subs = wx.ListBox(self)
    self.reserves = wx.ListBox(self)
    self.hbox1.Add(self.starting)
    self.hbox1.Add(self.subs)
    self.hbox1.Add(self.reserves)
    self.txt_output = wx.TextCtrl(self,
      style=wx.TE_MULTILINE|wx.BORDER_SUNKEN|wx.TE_READONLY|wx.TE_RICH2, size=(400,200))
    self.currently_showing = ''
    self.txt_output.AppendText(str(self.currently_showing))
    self.refresh()
    self.hbox1.Add(self.txt_output, proportion=1, flag=wx.EXPAND)
    start_to_sub_button = TemplateButton(self, 'Move to subs')
    start_to_sub_button.Bind(wx.EVT_BUTTON, self.start_to_sub)
    sub_to_start_button = TemplateButton(self, 'Move to starting')
    sub_to_start_button.Bind(wx.EVT_BUTTON, self.sub_to_start)
    sub_to_res_button = TemplateButton(self, 'Move to reserves')
    sub_to_res_button.Bind(wx.EVT_BUTTON, self.sub_to_res)
    res_to_sub_button = TemplateButton(self, 'Move to subs')
    res_to_sub_button.Bind(wx.EVT_BUTTON, self.res_to_sub)
    self.hbox3.Add(start_to_sub_button, proportion=0)
    self.hbox3.Add(sub_to_start_button, proportion=0)
    self.hbox3.Add(sub_to_res_button, proportion=0)
    self.hbox3.Add(res_to_sub_button, proportion=0)
 
  def refresh(self):
    self.get_starting()
    self.get_subs()
    self.get_reserves()
    if self.starting.GetCount() > 0:
      self.starting.SetSelection(0)
    if self.subs.GetCount() > 0:
      self.subs.SetSelection(0)
    if self.reserves.GetCount() > 0:
      self.reserves.SetSelection(0)
    self.team.formation.get_ascii()
    self.team.formation.update_ascii(self.team)
    self.txt_output.Clear()
    self.txt_output.AppendText(str(self.team.formation))

  def start_to_sub(self, event):
    if self.starting.GetCount() > 0:
      p0 = self.starting.GetString(self.starting.GetSelection())
      self.lineups = [x.match.lineup for x in self.team]
      available_slots = [x for x in range(16, 22) if x not in self.lineups]
      if len(available_slots) > 0:
        slot = available_slots[0]
        player = next(x for x in self.team if str(x)==p0)
        player.match.lineup = slot
        self.refresh()

  def sub_to_start(self, event):
    if self.subs.GetCount() > 0:
      p0 = self.subs.GetString(self.subs.GetSelection())
      self.lineups = [x.match.lineup for x in self.team]
      available_slots = [x for x in range(1, 16) if x not in self.lineups]
      if len(available_slots) > 0:
        slot = available_slots[0]
        player = next(x for x in self.team if str(x)==p0)
        player.match.lineup = slot
        self.refresh()

  def sub_to_res(self, event):
    if self.subs.GetCount() > 0:
      p0 = self.subs.GetString(self.subs.GetSelection())
      slot = 0
      player = next(x for x in self.team if str(x)==p0)
      player.match.lineup = slot
      self.refresh()

  def res_to_sub(self, event):
    if self.reserves.GetCount() > 0:
      p0 = self.reserves.GetString(self.reserves.GetSelection())
      self.lineups = [x.match.lineup for x in self.team]
      available_slots = [x for x in range(16, 22) if x not in self.lineups]
      if len(available_slots) > 0:
        slot = available_slots[0]
        player = next(x for x in self.team if str(x)==p0)
        player.match.lineup = slot
        self.refresh()

  def get_starting(self):
    self.starting.Set([str(x) for x in self.team if x.match.lineup in range(1, 16)])

  def get_subs(self):
    self.subs.Set([str(x) for x in self.team if x.match.lineup in range(16, 22)])

  def get_reserves(self):
    self.reserves.Set([str(x) for x in self.team if x.match.lineup not in range(1, 22)])

class FormationPanel(TemplatePanel):
  def __init__(self, parent):
    super().__init__(parent)

class TacticsPanel(TemplatePanel):
  def __init__(self, parent):
    super().__init__(parent)

class TrainingPanel(TemplatePanel):
  def __init__(self, parent):
    super().__init__(parent)

class wxSDLWindow(wx.Frame):
  def __init__(self, parent, id, title = 'SDL window', **options):
    options['style'] = wx.DEFAULT_FRAME_STYLE | wx.TRANSPARENT_WINDOW
    wx.Frame.__init__(*(self, parent, id, title), **options)

    self._initialized = 0
    self._resized = 0
    self._surface = None
    self.__needsDrawing = 1

    self.Bind(wx.EVT_IDLE, self.OnIdle)
    
  def OnIdle(self, ev):
    if not self._initialized or self._resized:
      if not self._initialized:
        # get the handle
        hwnd = self.GetHandle()

        os.environ['SDL_WINDOWID'] = str(hwnd)
        if sys.platform == 'win32':
          os.environ['SDL_VIDEODRIVER'] = 'windib'

        pygame.init()

        self.Bind(wx.EVT_SIZE, self.OnSize)
        self._initialized = 1
    else:
      self._resized = 0

    x,y = self.GetSize()
    self._surface = pygame.display.set_mode((x,y))

    if self.__needsDrawing:
      self.draw()

  def OnPaint(self, ev):
    self.__needsDrawing = 1

  def OnSize(self, ev):
    self._resized = 1
    ev.Skip()

  def draw(self):
    raise NotImplementedError('please define a .draw() method!')

  def getSurface(self):
    return self._surface

class CircleWindow(wxSDLWindow):
  "draw a circle in a wxPython / PyGame window"
  def draw(self):
    surface = self.getSurface()
    if surface is not None:
      topcolor = 5
      bottomcolor = 100

      print('debug1')
      pygame.draw.circle(surface, (250,0,0), (100,100), 50)
      print('debug2')
      pygame.display.flip()
      print('debug3')

def pygametest():
  app = wx.App()
  sizeT = (640,480)
  w = CircleWindow(None, -1, size = sizeT)
  w.Show(1)
  app.MainLoop()

if __name__ == "__main__":
  pygametest()

