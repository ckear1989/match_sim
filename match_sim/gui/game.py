
import wx

from match_sim.cl.game import Game as ClGame

class GamePanel(wx.Panel):
  def __init__(self, parent, game):
    super().__init__(parent)
    self.game = game
    self.SetBackgroundColour('#4f5049')
    main_sizer = wx.BoxSizer(wx.VERTICAL)

    hbox1 = wx.BoxSizer()
    self.txt_output = wx.TextCtrl(self,
      style=wx.TE_MULTILINE|wx.BORDER_SUNKEN|wx.TE_READONLY|wx.TE_RICH2, size=(400,200))
    hbox1.Add(self.txt_output, proportion=1, flag=wx.EXPAND)
    main_sizer.Add(hbox1, proportion=2, flag=wx.ALL|wx.EXPAND, border=20)

    # main_sizer.Add((-1, 100))

    hbox2 = wx.BoxSizer(wx.HORIZONTAL)
    continue_button = wx.Button(self, label='Continue')
    continue_button.Bind(wx.EVT_BUTTON, self.insert_text)
    hbox2.Add(continue_button, 1, wx.LEFT | wx.BOTTOM, 5)
    inbox_button = wx.Button(self, label='Inbox[{0}]'.format(self.game.inbox.count))
    inbox_button.Bind(wx.EVT_BUTTON, self.insert_text)
    hbox2.Add(inbox_button, 1, wx.LEFT | wx.BOTTOM, 5)
    manage_button = wx.Button(self, label='Manage')
    manage_button.Bind(wx.EVT_BUTTON, self.insert_text)
    hbox2.Add(manage_button, 1, wx.LEFT | wx.BOTTOM, 5)
    training_button = wx.Button(self, label='Training')
    training_button.Bind(wx.EVT_BUTTON, self.insert_text)
    hbox2.Add(training_button, 1, wx.LEFT | wx.BOTTOM, 5)
    stats_button = wx.Button(self, label='Stats')
    stats_button.Bind(wx.EVT_BUTTON, self.insert_text)
    hbox2.Add(stats_button, 1, wx.LEFT | wx.BOTTOM, 5)
    save_button = wx.Button(self, label='Save')
    save_button.Bind(wx.EVT_BUTTON, self.save_game)
    hbox2.Add(save_button, 1, wx.LEFT | wx.BOTTOM, 5)
    settings_button = wx.Button(self, label='Settings')
    settings_button.Bind(wx.EVT_BUTTON, self.insert_text)
    hbox2.Add(settings_button, 1, wx.LEFT | wx.BOTTOM, 5)
    self.exit_button = wx.Button(self, label='Exit')
    hbox2.Add(self.exit_button, 1, wx.LEFT | wx.BOTTOM, 5)
    main_sizer.Add(hbox2, proportion=0, flag=wx.LEFT|wx.BOTTOM, border=10)
    self.SetSizer(main_sizer)

  def save_game(self, event):
    self.game.save()

  def insert_text(self, event):
    self.txt_output.AppendText('debug')

class Game(ClGame):
  def __init__(self, team, name):
    super().__init__(team, name)
