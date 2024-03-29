
import random

import wx

import match_sim.cl.default as default
from match_sim.gui.template import TemplateFrame, TemplatePanel, TemplateButton

class Colour():
  def __init__(self):
    self.VLG = wx.Colour(126, 255, 117)
    self.LG = wx.Colour(22, 243, 59)
    self.DG = wx.Colour(5, 88, 19)
    self.DR = wx.Colour(250, 0, 0)
    self.BL = wx.Colour(0, 0, 0)
    self.WH = wx.Colour(255, 255, 255)
    self.LIME = wx.Colour(135, 246, 157)
    self.YEL = wx.Colour(236, 213, 4)
    self.OR = wx.Colour(236, 128, 4)

class TeamColours():
  def __init__(self,
    home_p=None, home_s=None,
    away_p=None, away_s=None,
    goalkeeper_p=None, goalkeeper_s=None
  ):
    colour = Colour()
    all_colours = [
      colour.LG, colour.DG,
      colour.DR, colour.BL,
      colour.BL, colour.LIME,
      colour.YEL, colour.OR
    ]
    self.home_p = home_p
    self.home_s = home_s
    self.away_p = away_p
    self.away_s = away_s
    self.goalkeeper_p = goalkeeper_p
    self.goalkeeper_s = goalkeeper_s
    if self.home_p is None:
      self.home_p = random.choice(all_colours)
    if self.home_s is None:
      self.home_s = random.choice([x for x in all_colours if x != self.home_p])
    if self.away_p is None:
      self.away_p = self.home_s
    if self.away_s is None:
      self.away_s = self.home_p
    if self.goalkeeper_p is None:
      self.goalkeeper_p = random.choice(all_colours)
    if self.goalkeeper_s is None:
      self.goalkeeper_s = random.choice(all_colours)

class PaintPanel(TemplatePanel):
  def __init__(self, parent, x0=None, y0=None):
    self.x, self.y = (85 * 4, 140 * 4)
    self.n = 5
    self.x0 = x0
    if self.x0 is None:
      self.x0 = 400
    self.y0 = y0
    if self.y0 is None:
      self.y0 = 100
    super().__init__(parent)
    self.txt_output.Destroy()
    self.test_button = TemplateButton(self, 'test')
    self.test_button.Bind(wx.EVT_BUTTON, self.test_draw)
    self.hbox3.Add(self.test_button, proportion=0)
    # self.InitUI()

  def InitUI(self): 
    self.Bind(wx.EVT_PAINT, self.get_pitch) 
    self.Centre() 
    self.Show(True)

  def test_draw(self, event):	
    dc = wx.ClientDC(self)
    font = wx.Font(18, wx.ROMAN, wx.ITALIC, wx.NORMAL) 
    dc.SetFont(font) 
    dc.DrawText('hello', 500, 10)
    x = 200
    y = 200
    dc.DrawCircle(self.x0+x, self.y0+y, 50)

  def draw_manager(self, manager, dc=None, x=200, y=200,
    x0=None, y0=None):
    if x0 is None:
      x0 = self.x0
    if y0 is None:
      y0 = self.y0
    colour = Colour()
    if self.IsShownOnScreen():
      if not dc:
        dc = wx.ClientDC(self)
    dc.SetBrush(wx.Brush(colour.WH))
    dc.DrawCircle(x0+x, y0+y, 20)
    dc.SetBrush(wx.Brush(colour.BL))
    dc.DrawCircle(x0+x, y0+y, 14)
    font = wx.Font(8, wx.ROMAN, wx.BOLD, wx.NORMAL) 
    dc.SetFont(font)
    dc.DrawText(manager, x0+x-30, y0+y+18)

  def draw_player(self, player, dc=None, x=200, y=200,
    x0=None, y0=None, colour_p=None, colour_s=None):
    if x0 is None:
      x0 = self.x0
    if y0 is None:
      y0 = self.y0
    colour = Colour()
    if colour_p is None:
      colour_p = colour.WH
    if colour_s is None:
      colour_s = colour.DR
    if self.IsShownOnScreen():
      if not dc:
        dc = wx.ClientDC(self)
    dc.SetBrush(wx.Brush(colour_s))
    dc.DrawCircle(x0+x, y0+y, 20)
    dc.SetBrush(wx.Brush(colour_p))
    dc.DrawCircle(x0+x, y0+y, 14)
    if player.season.injury.status is not None:
      dc.SetTextForeground(colour.DR)
      font = wx.Font(10, wx.ROMAN, wx.BOLD, wx.NORMAL) 
      dc.SetFont(font)
      dc.DrawRotatedText('injured', x0+x-20, y0+y-18, -45)
    if player.season.suspension.status is not None:
      dc.SetTextForeground(colour.DR)
      font = wx.Font(10, wx.ROMAN, wx.BOLD, wx.NORMAL) 
      dc.SetFont(font)
      dc.DrawRotatedText('suspended', x0+x-20, y0+y-18, -45)
    font = wx.Font(8, wx.ROMAN, wx.BOLD, wx.NORMAL) 
    dc.SetFont(font)
    if colour_p == colour.BL:
      dc.SetTextForeground(colour.WH)
    else:
      dc.SetTextForeground(colour.BL)
    if player.match.lineup > 0:
      dc.DrawText(str(player.match.lineup), x0+x-3, y0+y-5)
    dc.SetTextForeground(colour.BL)
    dc.DrawText(str(player), x0+x-30, y0+y+18)

  def draw_player_match(self, player, dc=None, x=200, y=200,
    x0=None, y0=None, colour_p=None, colour_s=None):
    if x0 is None:
      x0 = self.x0
    if y0 is None:
      y0 = self.y0
    self.draw_player(player, dc, x, y, x0, y0, colour_p, colour_s)
    if player.match.score.scoren > 0:
      if self.IsShownOnScreen():
        if not dc:
          dc = wx.ClientDC(self)
      dc.DrawText(str(player.match.score), x0+x-30, y0+y+28)
    if len(player.match.cards) > 0:
      for card in player.match.cards:
        if card == 'y':
          dc.SetBrush(wx.Brush(Colour().YEL))
          dc.DrawRectangle(x0+x-28, y0+y, 6, 12)
        elif card == 'r':
          dc.SetBrush(wx.Brush(Colour().DR))
          dc.DrawRectangle(x0+x-28, y0+y, 6, 12)

  def draw_pitch(self, dc=None, title=None, x0=None, y0=None, header_border=False):
    if x0 is None:
      x0 = self.x0
    if y0 is None:
      y0 = self.y0
    colour = Colour()
    if self.IsShownOnScreen():
      if not dc:
        dc = wx.ClientDC(self)
    font = wx.Font(18, wx.ROMAN, wx.ITALIC, wx.NORMAL) 
    dc.SetFont(font) 
    if title is not None:
      dc.DrawText(title, x0, 10) 
    dc.SetPen(wx.Pen(colour.BL))
    dc.SetBrush(wx.Brush(colour.BL))
    dc.DrawRectangle(x0-3, y0-3, self.x+6, self.y+6)
    if header_border:
      dc.DrawRectangle(x0-3, y0-34, self.x+6, 4)
      dc.DrawRectangle(x0-3, y0-34, 4, y0)
      dc.DrawRectangle(x0+self.x-1, y0-34, 4, y0)
    for i in range(self.n):
      dc.SetBrush(wx.Brush(colour.VLG))
      dc.SetPen(wx.Pen(colour.VLG))
      dc.DrawRectangle(x0, y0 + (i*2*self.y/self.n/2), self.x, self.y/self.n/2)
      dc.SetBrush(wx.Brush(colour.LG))
      dc.SetPen(wx.Pen(colour.LG))
      dc.DrawRectangle(x0, y0 + (((i*2)+1)*self.y/self.n/2), self.x, self.y/self.n/2)
    dc.SetPen(wx.Pen(colour.WH))
    # 6M
    w = 14 * 4
    h = 4.5 * 4
    x1 = x0 + (self.x/2) - (w/2)
    y1 = y0 +1
    dc.DrawLineList([[x1, y1, x1, y1+h], [x1, y1+h, x1+w, y1+h], [x1+w, y1+h, x1+w, y1]])
    y1 = y0 + self.y -  2
    h = h * -1
    dc.DrawLineList([[x1, y1, x1, y1+h], [x1, y1+h, x1+w, y1+h], [x1+w, y1+h, x1+w, y1]])
    # penalty box
    w = 19 * 4
    h = 13 * 4
    x2 = x0 +(self.x/2) - (w/2)
    y2 = y0 + 1
    dc.DrawLineList([[x2, y2, x2, y2+h], [x2+w, y2, x2+w, y2+h]])
    y2 = y0 + self.y - 2
    h = h*-1
    dc.DrawLineList([[x2, y2, x2, y2+h], [x2+w, y2, x2+w, y2+h]])
    # 13M
    x3 = x0 + 1
    h = 13 * 4
    w = self.x - 3
    y3 = y0 + h
    # 20
    h = 20 * 4
    y4 = y0 + h
    # 45
    h = 45 * 4
    y5 = y0 + h
    # 65
    h = 65 * 4
    y6 = y0 + h
    dc.DrawLineList([
      [x3, y3, x3+w, y3],
      [x3, y4, x3+w, y4],
      [x3, y5, x3+w, y5],
      [x3, y6, x3+w, y6]
    ])
    # mirror
    h = 13 * 4
    y3 = y0 + self.y - h - 2
    h = 20 * 4
    y4 = y0 + self.y - h - 2
    h = 45 * 4
    y5 = y0 + self.y - h - 2
    h = 65 * 4
    y6 = y0 + self.y - h - 2
    dc.DrawLineList([
      [x3, y3, x3+w, y3],
      [x3, y4, x3+w, y4],
      [x3, y5, x3+w, y5],
      [x3, y6, x3+w, y6]
    ])
    # HW
    w = 20 * 4
    x7 = x0 + (self.x/2) - (w/2)
    y7 = y0 + (self.y/2)
    dc.DrawLine(x7, y7, x7+w, y7)
    # semi circles
    r = 13 * 4
    x8 = x0 + (self.x/2) - r
    y8 = y0 + (20 * 4)
    dc.SetBrush(wx.Brush(colour.LG))
    dc.DrawArc(x8, y8, x8 + (r*2), y8, x8 + r, y8)
    y8 = y0 + self.y - (20 * 4) - 2
    dc.SetBrush(wx.Brush(colour.VLG))
    dc.DrawArc(x8 + (r*2), y8, x8, y8, x8 + r, y8)
    # penalty spots
    dc.SetPen(wx.Pen(colour.BL))
    dc.SetBrush(wx.Brush(colour.WH))
    x9 = x0 + (self.x/2)
    y9 = y0 + (11 * 4)
    dc.DrawCircle(x9, y9, 3)
    y10 = y0 + self.y - (11 * 4)
    dc.DrawCircle(x9, y10, 3)

  def get_pitch(self, event):
    colour = Colour()
    dc = wx.PaintDC(self)
    dc.Clear()
    self.draw_pitch(dc, x0=self.x0, y0=self.y0)

class PaintFrame(TemplateFrame):
  def __init__(self):
    super().__init__()
    self.panel = PaintPanel(self)
    self.sizer.Add(self.panel, 1, wx.EXPAND)
    self.SetSizer(self.sizer)
    self.SetSize((800, 600))
    self.Centre()

if __name__ == "__main__":

  app = wx.App(False)
  frame = PaintFrame()
  frame.Show()
  app.MainLoop()

