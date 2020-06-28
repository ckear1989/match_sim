
import pathlib
path = pathlib.Path(__file__).parent.absolute()

import wx

import match_sim.default as default
from match_sim.gui.template import TemplateFrame, TemplatePanel

LG = wx.Colour(22, 243, 59)
DG = wx.Colour(5, 88, 19)
DR = wx.Colour(250, 0, 0)
BL = wx.Colour(0, 0, 0)
WH = wx.Colour(255, 255, 255)

def add_player(pitch, color, centre):
  # pygame.draw.circle(pitch, color, centre, 10)
  return pitch

class PaintPanel(TemplatePanel):
  def __init__(self, parent):
    super().__init__(parent)
    self.txt_output.Destroy()
    self.exit_button.Destroy()
    self.InitUI()

  def InitUI(self): 
    self.Bind(wx.EVT_PAINT, self.OnPaint) 
    self.Centre() 
    self.Show(True)

  def OnPaint(self, event):
    dc = wx.PaintDC(self)
    brush = wx.Brush('white')
    dc.Clear()
    bmp = wx.Bitmap(default.gui_background)
    dc.DrawBitmap(bmp, 0, 0)
		
    font = wx.Font(18, wx.ROMAN, wx.ITALIC, wx.NORMAL) 
    dc.SetFont(font) 
    # dc.DrawText(self.team.name, 500, 10) 
		
    pen = wx.Pen(BL)
    dc.SetPen(pen)
    x, y, n = (340, 520, 5)
    x0 = 400
    y0 = 100
    for i in range(n):
      dc.SetBrush(wx.Brush(DG))
      dc.DrawRectangle(x0, y0 + (i*2*y/n/2), x, y/n/2)
      dc.SetBrush(wx.Brush(LG))
      dc.DrawRectangle(x0, y0 + (((i*2)+1)*y/n/2), x, y/n/2)
    pen = wx.Pen(WH)
    dc.SetPen(pen)
    # 6 yard box
    w = 40
    h = 10
    x1 = x0 + (x/2) - (w/2)
    y1 = y0 +1
    dc.DrawLineList([[x1, y1, x1, y1+h], [x1, y1+h, x1+w, y1+h], [x1+w, y1+h, x1+w, y1]])
    y1 = y0 + y -  2
    h = h*-1
    dc.DrawLineList([[x1, y1, x1, y1+h], [x1, y1+h, x1+w, y1+h], [x1+w, y1+h, x1+w, y1]])
    # penalty box
    w = 60
    h = 30
    x2 = x0 +(x/2) - (w/2)
    y2 = y0 + 1
    dc.DrawLineList([[x2, y2, x2, y2+h], [x2+w, y2, x2+w, y2+h]])
    y2 = y0 + y - 2
    h = h*-1
    dc.DrawLineList([[x2, y2, x2, y2+h], [x2+w, y2, x2+w, y2+h]])
    # 14
    x3 = x0 + 1
    h = 31
    w = x - 3
    y3 = y0 + h
    # 21
    h = 40
    y4 = y0 + h
    # 45
    h = 120
    y5 = y0 + h
    # 65
    h = 160
    y6 = y0 + h
    dc.DrawLineList([
      [x3, y3, x3+w, y3],
      [x3, y4, x3+w, y4],
      [x3, y5, x3+w, y5],
      [x3, y6, x3+w, y6]
    ])
    # 14
    x3 = x0 + 1
    h = 31
    w = x - 3
    y3 = y0 + y - h
    # 21
    h = 40
    y4 = y0 + y - h
    # 45
    h = 120
    y5 = y0 + y - h
    # 65
    h = 160
    y6 = y0 + y - h
    dc.DrawLineList([
      [x3, y3, x3+w, y3],
      [x3, y4, x3+w, y4],
      [x3, y5, x3+w, y5],
      [x3, y6, x3+w, y6]
    ])
    # HW
    w = 20
    x7 = x0 + (x/2) - (w/2)
    y7 = y0 + (y/2)
    dc.DrawLine(x7, y7, x7+w, y7)

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

