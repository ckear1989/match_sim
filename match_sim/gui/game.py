
import wx

from match_sim.cl.game import Game as ClGame

class GamePanel(wx.Panel):
  def __init__(self, parent):
    super().__init__(parent)
    main_sizer = wx.BoxSizer(wx.VERTICAL)
    continue_button = wx.Button(self, label='Continue')
    main_sizer.Add(continue_button, 0, wx.ALL | wx.CENTER, 5)
    save_button = wx.Button(self, label='Save')
    main_sizer.Add(save_button, 0, wx.ALL | wx.CENTER, 5)
    self.exit_button = wx.Button(self, label='Exit')
    main_sizer.Add(self.exit_button, 0, wx.ALL | wx.CENTER, 5)
    self.SetSizer(main_sizer)

class Game(ClGame):
  def __init__(self, team, name):
    print('game started')
    super().__init__(team, name)
