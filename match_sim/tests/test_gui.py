
import wx
from time import sleep

from match_sim.gui.main import MSFrame

def test_open_gui():
  app = wx.App(False)
  frame = MSFrame()
  frame.Show()
  frame.Maximize(True)
  sleep(3)
  frame.Destroy()
  # app.MainLoop(3)

