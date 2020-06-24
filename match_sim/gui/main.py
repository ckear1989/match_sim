
import glob
import pickle
import time

import wx

import match_sim.default as default
from match_sim.gui.game import GamePanel, Game

class MSPanel(wx.Panel):
  def __init__(self, parent):
    super().__init__(parent)
    main_sizer = wx.BoxSizer(wx.VERTICAL)
    self.SetSize((800, 600))
    self.new_button = wx.Button(self, label='New')
    main_sizer.Add(self.new_button, 0, wx.ALL | wx.CENTER, 5)
    self.load_button = wx.Button(self, label='Load')
    main_sizer.Add(self.load_button, 0, wx.ALL | wx.CENTER, 5)
    self.exit_button = wx.Button(self, label='Exit')
    main_sizer.Add(self.exit_button, 0, wx.ALL | wx.CENTER, 5)
    self.SetSizer(main_sizer)

class NewDialog(wx.Dialog):
  def __init__(self):
    self.game = None
    title = 'New Game'
    super().__init__(parent=None, title=title)
    self.main_sizer = wx.BoxSizer(wx.VERTICAL)
    self.name = wx.TextCtrl(self)
    self.add_widgets('Name', self.name)
    self.team = wx.ListBox(self, choices=default.poss_teams)
    self.team.SetSelection(0)
    self.add_widgets('Team', self.team)
    btn_sizer = wx.BoxSizer()
    start_btn = wx.Button(self, label='Start')
    start_btn.Bind(wx.EVT_BUTTON, self.on_start)
    btn_sizer.Add(start_btn, 0, wx.ALL, 5)
    btn_sizer.Add(wx.Button(self, id=wx.ID_CANCEL), 0, wx.ALL, 5)
    self.main_sizer.Add(btn_sizer, 0, wx.CENTER)
    self.SetSizer(self.main_sizer)

  def add_widgets(self, label_text, text_ctrl):
    row_sizer = wx.BoxSizer(wx.HORIZONTAL)
    label = wx.StaticText(self, label=label_text, size=(50, -1))
    row_sizer.Add(label, 0, wx.ALL, 5)
    row_sizer.Add(text_ctrl, 1, wx.ALL | wx.EXPAND, 5)
    self.main_sizer.Add(row_sizer, 0, wx.EXPAND)

  def on_start(self, event):
    self.Close()

class MSFrame(wx.Frame):
  def __init__(self):
    super().__init__(parent=None, title='Match Simulator 2020')
    self.main_panel = MSPanel(self)
    self.sizer = wx.BoxSizer(wx.VERTICAL)
    self.sizer.Add(self.main_panel, 1, wx.EXPAND)
    self.main_panel.new_button.Bind(wx.EVT_BUTTON, self.on_new)
    self.main_panel.load_button.Bind(wx.EVT_BUTTON, self.on_load)
    self.main_panel.exit_button.Bind(wx.EVT_BUTTON, self.on_exit)
    self.SetSizer(self.sizer)
    self.SetSize((800, 600))
    self.Centre()

  def create_game_panel(self, game):
    self.game_panel = GamePanel(self, game)
    self.sizer.Add(self.game_panel, 1, wx.EXPAND)
    self.game_panel.exit_button.Bind(wx.EVT_BUTTON, self.show_main_panel)
    self.game_panel.Hide()

  def on_new(self, event):
    dlg = NewDialog()
    dlg.ShowModal()
    name = dlg.name.GetValue()
    team = dlg.team.GetString(dlg.team.GetSelection())
    if name:
      if team:
        game = Game(team, name)
        self.create_game_panel(game)
        self.show_game_panel()
    dlg.Destroy()

  def on_load(self, event):
    title = "Choose a game file:"
    dlg = wx.FileDialog(self, title, style=wx.DD_DEFAULT_STYLE)
    if dlg.ShowModal() == wx.ID_OK:
      game_listing = dlg.GetPath()
      with open(game_listing, 'rb') as f:
        game = pickle.load(f)
      self.create_game_panel(game)
      self.show_game_panel()
    dlg.Destroy()

  def show_game_panel(self):
    self.game_panel.Show()
    self.main_panel.Hide()
    self.Layout()

  def show_main_panel(self, event):
    self.main_panel.Show()
    self.game_panel.Hide()
    self.Layout()

  def on_exit(self, event):
    self.Destroy()

if __name__ == '__main__':
  app = wx.App(False)
  frame = MSFrame()
  frame.Show()
  app.MainLoop()