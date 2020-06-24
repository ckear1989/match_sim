
import wx

from match_sim.cl.game import Game as ClGame

class GamePanel(wx.Panel):
  def __init__(self, parent, game):
    super().__init__(parent)
    self.game = game
    main_sizer = wx.BoxSizer(wx.VERTICAL)
    continue_button = wx.Button(self, label='Continue')
    continue_button.Bind(wx.EVT_BUTTON, self.insert_text)
    main_sizer.Add(continue_button, 0, wx.ALL | wx.CENTER, 5)
    save_button = wx.Button(self, label='Save')
    save_button.Bind(wx.EVT_BUTTON, self.save_game)
    main_sizer.Add(save_button, 0, wx.ALL | wx.CENTER, 5)
    self.exit_button = wx.Button(self, label='Exit')
    main_sizer.Add(self.exit_button, 0, wx.ALL | wx.CENTER, 5)
    self.txt_output = wx.TextCtrl(
      self, -1,
      style=wx.TE_MULTILINE|wx.BORDER_SUNKEN|wx.TE_READONLY|
      wx.TE_RICH2, size=(200,100)
    )
    main_sizer.Add(self.txt_output, 0, wx.ALL | wx.CENTER, 5)
    self.SetSizer(main_sizer)

  def save_game(self, event):
    self.game.save()

  def insert_text(self, event):
    self.txt_output.AppendText('debug')

class Game(ClGame):
  def __init__(self, team, name):
    super().__init__(team, name)
