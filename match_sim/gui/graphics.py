
import pathlib
path = pathlib.Path(__file__).parent.absolute()

import wx

import match_sim.default as default
from match_sim.gui.template import TemplateFrame, TemplatePanel, TemplateButton

class Colour():
  def __init__(self):
    self.LG = wx.Colour(22, 243, 59)
    self.DG = wx.Colour(5, 88, 19)
    self.DR = wx.Colour(250, 0, 0)
    self.BL = wx.Colour(0, 0, 0)
    self.WH = wx.Colour(255, 255, 255)
    self.LIME = wx.Colour(135, 246, 157)

class PaintPanel(TemplatePanel):
  def __init__(self, parent, x0=None, y0=None):
    super().__init__(parent)
    self.txt_output.Destroy()
    self.test_button = TemplateButton(self, 'test')
    self.test_button.Bind(wx.EVT_BUTTON, self.test_draw)
    self.hbox3.Add(self.test_button, proportion=0)
    self.x, self.y = (85 * 4, 140 * 4)
    self.n = 5
    self.x0 = x0
    if self.x0 is None:
      self.x0 = 400
    self.y0 = y0
    if self.y0 is None:
      self.y0 = 100
    self.InitUI()

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

  def draw_player(self, player, dc=None, x=200, y=200):
    colour = Colour()
    if self.IsShownOnScreen():
      if not dc:
        dc = wx.ClientDC(self)
    font = wx.Font(8, wx.ROMAN, wx.BOLD, wx.NORMAL) 
    dc.SetFont(font) 
    dc.SetBrush(wx.Brush(colour.DR))
    dc.DrawCircle(self.x0+x, self.y0+y, 20)
    dc.SetBrush(wx.Brush(colour.WH))
    dc.DrawCircle(self.x0+x, self.y0+y, 14)
    dc.SetTextForeground(colour.BL)
    dc.SetTextBackground(colour.LIME)
    # print(dc.GetTextBackground())
    dc.DrawText(str(player), self.x0+x-30, self.y0+y)

  def draw_pitch(self, dc=None, title=None):	
    colour = Colour()
    if self.IsShownOnScreen():
      if not dc:
        dc = wx.ClientDC(self)
    # dc.Clear()
    # bmp = wx.Bitmap(default.gui_background)
    # dc.DrawBitmap(bmp, 0, 0)
    self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)
    font = wx.Font(18, wx.ROMAN, wx.ITALIC, wx.NORMAL) 
    dc.SetFont(font) 
    if title is not None:
      dc.DrawText(title, self.x0, 10) 
		
    pen = wx.Pen(colour.BL)
    dc.SetPen(pen)
    dc.SetBrush(wx.Brush(colour.BL))
    dc.DrawRectangle(self.x0-2, self.y0-2, self.x+2, self.y+2)
    for i in range(self.n):
      dc.SetBrush(wx.Brush(colour.DG))
      dc.DrawRectangle(self.x0, self.y0 + (i*2*self.y/self.n/2), self.x, self.y/self.n/2)
      dc.SetBrush(wx.Brush(colour.LG))
      dc.DrawRectangle(self.x0, self.y0 + (((i*2)+1)*self.y/self.n/2), self.x, self.y/self.n/2)
    pen = wx.Pen(colour.WH)
    dc.SetPen(pen)
    # 6M
    w = 14 * 4
    h = 4.5 * 4
    x1 = self.x0 + (self.x/2) - (w/2)
    y1 = self.y0 +1
    dc.DrawLineList([[x1, y1, x1, y1+h], [x1, y1+h, x1+w, y1+h], [x1+w, y1+h, x1+w, y1]])
    y1 = self.y0 + self.y -  2
    h = h * -1
    dc.DrawLineList([[x1, y1, x1, y1+h], [x1, y1+h, x1+w, y1+h], [x1+w, y1+h, x1+w, y1]])
    # penalty box
    w = 19 * 4
    h = 13 * 4
    x2 = self.x0 +(self.x/2) - (w/2)
    y2 = self.y0 + 1
    dc.DrawLineList([[x2, y2, x2, y2+h], [x2+w, y2, x2+w, y2+h]])
    y2 = self.y0 + self.y - 2
    h = h*-1
    dc.DrawLineList([[x2, y2, x2, y2+h], [x2+w, y2, x2+w, y2+h]])
    # 13M
    x3 = self.x0 + 1
    h = 13 * 4
    w = self.x - 3
    y3 = self.y0 + h
    # 20
    h = 20 * 4
    y4 = self.y0 + h
    # 45
    h = 45 * 4
    y5 = self.y0 + h
    # 65
    h = 65 * 4
    y6 = self.y0 + h
    dc.DrawLineList([
      [x3, y3, x3+w, y3],
      [x3, y4, x3+w, y4],
      [x3, y5, x3+w, y5],
      [x3, y6, x3+w, y6]
    ])
    # mirror
    h = 13 * 4
    y3 = self.y0 + self.y - h - 2
    h = 20 * 4
    y4 = self.y0 + self.y - h - 2
    h = 45 * 4
    y5 = self.y0 + self.y - h - 2
    h = 65 * 4
    y6 = self.y0 + self.y - h - 2
    dc.DrawLineList([
      [x3, y3, x3+w, y3],
      [x3, y4, x3+w, y4],
      [x3, y5, x3+w, y5],
      [x3, y6, x3+w, y6]
    ])
    # HW
    w = 20 * 4
    x7 = self.x0 + (self.x/2) - (w/2)
    y7 = self.y0 + (self.y/2)
    dc.DrawLine(x7, y7, x7+w, y7)
    # semi circles
    r = 13 * 4
    x8 = self.x0 + (self.x/2) - r
    y8 = self.y0 + (20 * 4)
    dc.SetBrush(wx.Brush(colour.LG))
    dc.DrawArc(x8, y8, x8 + (r*2), y8, x8 + r, y8)
    y8 = self.y0 + self.y - (20 * 4) - 2
    dc.SetBrush(wx.Brush(colour.DG))
    dc.DrawArc(x8 + (r*2), y8, x8, y8, x8 + r, y8)
    # penalty spots
    dc.SetPen(wx.Pen(colour.BL))
    dc.SetBrush(wx.Brush(colour.WH))
    x9 = self.x0 + (self.x/2)
    y9 = self.y0 + (11 * 4)
    dc.DrawCircle(x9, y9, 3)
    y10 = self.y0 + self.y - (11 * 4)
    dc.DrawCircle(x9, y10, 3)

  def get_pitch(self, event):	
    colour = Colour()
    self.dc = wx.PaintDC(self)
    self.dc.Clear()
    bmp = wx.Bitmap(default.gui_background)
    self.dc.DrawBitmap(bmp, 0, 0)
    font = wx.Font(18, wx.ROMAN, wx.ITALIC, wx.NORMAL) 
    self.dc.SetFont(font) 
    # dc.DrawText(self.team.name, 500, 10) 
		
    pen = wx.Pen(colour.BL)
    self.dc.SetPen(pen)
    for i in range(self.n):
      self.dc.SetBrush(wx.Brush(colour.DG))
      self.dc.DrawRectangle(self.x0, self.y0 + (i*2*self.y/self.n/2), self.x, self.y/self.n/2)
      self.dc.SetBrush(wx.Brush(colour.LG))
      self.dc.DrawRectangle(self.x0, self.y0 + (((i*2)+1)*self.y/self.n/2), self.x, self.y/self.n/2)
    pen = wx.Pen(colour.WH)
    self.dc.SetPen(pen)
    # 6M
    w = 14 * 4
    h = 4.5 * 4
    x1 = self.x0 + (self.x/2) - (w/2)
    y1 = self.y0 +1
    self.dc.DrawLineList([[x1, y1, x1, y1+h], [x1, y1+h, x1+w, y1+h], [x1+w, y1+h, x1+w, y1]])
    y1 = self.y0 + self.y -  2
    h = h * -1
    self.dc.DrawLineList([[x1, y1, x1, y1+h], [x1, y1+h, x1+w, y1+h], [x1+w, y1+h, x1+w, y1]])
    # penalty box
    w = 19 * 4
    h = 13 * 4
    x2 = self.x0 +(self.x/2) - (w/2)
    y2 = self.y0 + 1
    self.dc.DrawLineList([[x2, y2, x2, y2+h], [x2+w, y2, x2+w, y2+h]])
    y2 = self.y0 + self.y - 2
    h = h*-1
    self.dc.DrawLineList([[x2, y2, x2, y2+h], [x2+w, y2, x2+w, y2+h]])
    # 13M
    x3 = self.x0 + 1
    h = 13 * 4
    w = self.x - 3
    y3 = self.y0 + h
    # 20
    h = 20 * 4
    y4 = self.y0 + h
    # 45
    h = 45 * 4
    y5 = self.y0 + h
    # 65
    h = 65 * 4
    y6 = self.y0 + h
    self.dc.DrawLineList([
      [x3, y3, x3+w, y3],
      [x3, y4, x3+w, y4],
      [x3, y5, x3+w, y5],
      [x3, y6, x3+w, y6]
    ])
    # mirror
    h = 13 * 4
    y3 = self.y0 + self.y - h - 2
    h = 20 * 4
    y4 = self.y0 + self.y - h - 2
    h = 45 * 4
    y5 = self.y0 + self.y - h - 2
    h = 65 * 4
    y6 = self.y0 + self.y - h - 2
    self.dc.DrawLineList([
      [x3, y3, x3+w, y3],
      [x3, y4, x3+w, y4],
      [x3, y5, x3+w, y5],
      [x3, y6, x3+w, y6]
    ])
    # HW
    w = 20 * 4
    x7 = self.x0 + (self.x/2) - (w/2)
    y7 = self.y0 + (self.y/2)
    self.dc.DrawLine(x7, y7, x7+w, y7)
    # semi circles
    r = 13 * 4
    x8 = self.x0 + (self.x/2) - r
    y8 = self.y0 + (20 * 4)
    self.dc.DrawArc(x8, y8, x8 + (r*2), y8, x8 + r, y8)
    y8 = self.y0 + self.y - (20 * 4) - 2
    self.dc.DrawArc(x8 + (r*2), y8, x8, y8, x8 + r, y8)
    # penalty spots
    self.dc.SetPen(wx.Pen(colour.BL))
    self.dc.SetBrush(wx.Brush(colour.WH))
    x9 = self.x0 + (self.x/2)
    y9 = self.y0 + (11 * 4)
    self.dc.DrawCircle(x9, y9, 3)
    y10 = self.y0 + self.y - (11 * 4)
    self.dc.DrawCircle(x9, y10, 3)

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

