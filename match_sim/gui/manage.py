
from match_sim.gui.template import TemplatePanel, TemplateButton

import sys
import os
import pathlib
path = pathlib.Path(__file__).parent.absolute()

import wx

from match_sim.gui.graphics import PaintPanel, Colour
import match_sim.default as default

class ManagePanel(TemplatePanel):
  def __init__(self, parent):
    super().__init__(parent)
    lineup_button = TemplateButton(self, 'Lineup')
    lineup_button.Bind(wx.EVT_BUTTON, self.on_lineup)
    self.hbox3.Add(lineup_button)
    training_button = TemplateButton(self, 'Training')
    training_button.Bind(wx.EVT_BUTTON, self.on_training)
    self.hbox3.Add(training_button)
    self.SetSizer(self.main_sizer)

  def on_lineup(self, event):
    self.GetParent().on_lineup(LineupPanel)

  def on_training(self, event):
    self.GetParent().on_training(TrainingPanel)

class LineupPanel(PaintPanel):
  def __init__(self, parent, x0=600, y0=None):
    super().__init__(parent, x0, y0)
    colour = Colour()
    font = wx.Font(18, wx.DECORATIVE, wx.BOLD, wx.NORMAL)
    label_size = wx.Size(200, 50)
    self.team = self.GetParent().game.teams[self.GetParent().game.team]
    self.lineups = {}
    self.vbox1 = wx.BoxSizer(wx.VERTICAL)
    label = wx.StaticText(self, label='Choose Starting Lineup:', size=label_size)
    label.SetFont(font)
    label.SetForegroundColour(colour.BL)
    label.SetBackgroundColour(colour.LIME)
    self.vbox1.Add(label, proportion=1)
    self.hbox1.Add(self.vbox1)
    self.vbox2 = wx.BoxSizer(wx.VERTICAL)
    label = wx.StaticText(self, label='Choose Substitutes:', size=label_size)
    label.SetFont(font)
    label.SetForegroundColour(colour.BL)
    label.SetBackgroundColour(colour.LIME)
    self.vbox2.Add(label, proportion=1)
    self.hbox1.Add(self.vbox2)
    for i in range(1, 16):
      self.lineups[i] = wx.ComboBox(self, choices=[str(x) for x in self.team] + [''])
      self.lineups[i].SetStringSelection([str(x) for x in self.team if x.match.lineup == i][0])
      self.lineups[i].Bind(wx.EVT_COMBOBOX, self.update_lineups)
      self.vbox1.Add(self.lineups[i], flag=wx.ALL, border=2)
    for i in range(16, 22):
      self.lineups[i] = wx.ComboBox(self, choices=[str(x) for x in self.team] + [''])
      self.lineups[i].SetStringSelection([str(x) for x in self.team if x.match.lineup == i][0])
      self.lineups[i].Bind(wx.EVT_COMBOBOX, self.update_lineups)
      self.vbox2.Add(self.lineups[i], flag=wx.ALL, border=2)
    self.formation = wx.ComboBox(self, choices=default.formations)
    self.formation.SetStringSelection(self.team.formation.nlist)
    self.formation.Bind(wx.EVT_COMBOBOX, self.update_formation)
    label = wx.StaticText(self, label='Choose Formation:', size=label_size)
    label.SetFont(font)
    label.SetForegroundColour(colour.BL)
    label.SetBackgroundColour(colour.LIME)
    self.vbox1.Add(label, proportion=1)
    self.vbox1.Add(self.formation)
    self.tactics = wx.ComboBox(self, choices=default.tactics)
    self.tactics.SetStringSelection(self.team.tactics.tactics)
    self.tactics.Bind(wx.EVT_COMBOBOX, self.update_tactics)
    label = wx.StaticText(self, label='Choose Tactics:', size=label_size)
    label.SetFont(font)
    label.SetForegroundColour(colour.BL)
    label.SetBackgroundColour(colour.LIME)
    self.vbox2.Add(label, proportion=1)
    self.vbox2.Add(self.tactics)
    self.InitUI()
    self.dc = wx.ClientDC(self)
    self.refresh()

  def update_lineups(self, event):
    for i in range(1, 22):
      pname = self.lineups[i].GetValue()
      players = [p for p in self.team if str(p) == pname]
      if len(players) > 0:
        player = players[0]
        player.update_lineup(i)
        self.lineups[i].SetSelection(self.lineups[i].GetSelection())
        self.lineups[i].SetStringSelection(str(player))
        players = [p for p in self.team if p.match.lineup == i]
        for player in players:
          if str(player) != pname:
            player.update_lineup(0)
    self.refresh()

  def update_formation(self, event):
    self.team.formation_change(self.formation.GetValue())
    self.refresh()

  def update_tactics(self, event):
    self.team.tactics_change(self.tactics.GetValue())
    self.refresh()

  def refresh(self):
    for i in range(1, 22):
      players = [p for p in self.team if p.match.lineup == i]
      if len(players) == 0:
        self.lineups[i].SetSelection(wx.NOT_FOUND)
        self.lineups[i].SetStringSelection('')
    self.team.update_playing_positions()
    self.draw_lineup()

  def draw_lineup(self):
    # self.dc.Clear()
    self.dc = wx.ClientDC(self)
    # print(self.dc)
    # self.dc.Clear()
    self.draw_pitch(self.dc, self.team.name)
    for i in range(1, 22):
      players = [p for p in self.team if p.match.lineup == i]
      if len(players) > 0:
        player = players[0]
        x, y = self.team.formation.get_coords(i)
        # print(player, x, y)
        self.draw_player(player, self.dc, x=x, y=y) 

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

        # pygame.init()

        self.Bind(wx.EVT_SIZE, self.OnSize)
        self._initialized = 1
    else:
      self._resized = 0

    x,y = self.GetSize()
    # self._surface = pygame.display.set_mode((x,y))

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

  app = wx.App(False)
  frame = DefaultFrame()
  panel = ManagePanel(frame)
  frame.sizer.Add(panel, 1, wx.EXPAND)
  frame.SetSizer(self.sizer)
  frame.SetSize((800, 600))
  frame.Centre()
  frame.Show()
  app.MainLoop()
