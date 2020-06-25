
import glob
import pickle
import time

import wx

import match_sim.default as default
from match_sim.gui.game import GamePanel, Game
from match_sim.gui.inbox import InboxPanel
from match_sim.gui.manage import ManagePanel
from match_sim.gui.stats import StatsPanel
from match_sim.gui.settings import SettingsPanel

class MSPanel(wx.Panel):
  def __init__(self, parent):
    super().__init__(parent)
    self.SetBackgroundColour("white")
    main_sizer = wx.BoxSizer(wx.VERTICAL)
    font = wx.SystemSettings.GetFont(wx.SYS_SYSTEM_FONT)
    font.SetPointSize(15)
    welcome_message = wx.StaticText(self, label=default.welcome_message)
    welcome_message.SetFont(font)
    hbox1 = wx.BoxSizer()
    hbox1.Add(welcome_message, proportion=1, flag=wx.ALL|wx.EXPAND, border=10)
    main_sizer.Add(hbox1, proportion=1)
    hbox2 = wx.BoxSizer(wx.HORIZONTAL)
    self.new_button = wx.Button(self, label='New', size=(100, 30))
    self.new_button.SetFont(font)
    hbox2.Add(self.new_button, proportion=0, flag=wx.ALL|wx.CENTER, border=5)
    self.load_button = wx.Button(self, label='Load', size=(100, 30))
    self.load_button.SetFont(font)
    hbox2.Add(self.load_button, proportion=0, flag=wx.ALL|wx.CENTER, border=5)
    self.exit_button = wx.Button(self, label='Exit', size=(100, 30))
    self.exit_button.SetFont(font)
    hbox2.Add(self.exit_button, proportion=0, flag=wx.ALL|wx.CENTER, border=5)
    main_sizer.Add(hbox2, proportion=0)
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
    self.game_panel.exit_button.Bind(wx.EVT_BUTTON, self.exit_game_panel)
    self.game_panel.Hide()

  def create_inbox_panel(self, game):
    self.inbox_panel = InboxPanel(self, game)
    self.sizer.Add(self.inbox_panel, 1, wx.EXPAND)
    self.inbox_panel.exit_button.Bind(wx.EVT_BUTTON, self.exit_inbox_panel)
    self.inbox_panel.Hide()

  def create_manage_panel(self):
    self.manage_panel = ManagePanel(self)
    self.sizer.Add(self.manage_panel, 1, wx.EXPAND)
    self.manage_panel.exit_button.Bind(wx.EVT_BUTTON, self.exit_manage_panel)
    self.manage_panel.Hide()

  def create_stats_panel(self):
    self.stats_panel = StatsPanel(self)
    self.sizer.Add(self.stats_panel, 1, wx.EXPAND)
    self.stats_panel.exit_button.Bind(wx.EVT_BUTTON, self.exit_stats_panel)
    self.stats_panel.Hide()

  def create_settings_panel(self):
    self.settings_panel = SettingsPanel(self)
    self.sizer.Add(self.settings_panel, 1, wx.EXPAND)
    self.settings_panel.exit_button.Bind(wx.EVT_BUTTON, self.exit_settings_panel)
    self.settings_panel.Hide()

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

  def on_inbox(self, event):
    self.create_inbox_panel(self.game_panel.game)
    self.show_inbox_panel()

  def on_manage(self, event):
    self.create_manage_panel()
    self.show_manage_panel()

  def on_stats(self, event):
    self.create_stats_panel()
    self.show_stats_panel()

  def on_settings(self, event):
    self.create_settings_panel()
    self.show_settings_panel()

  def show_game_panel(self):
    self.game_panel.Show()
    self.main_panel.Hide()
    self.Layout()

  def exit_game_panel(self, event):
    self.main_panel.Show()
    self.game_panel.Hide()
    self.Layout()

  def show_inbox_panel(self):
    self.inbox_panel.Show()
    self.game_panel.Hide()
    self.Layout()

  def exit_inbox_panel(self, event):
    self.game_panel.Show()
    self.inbox_panel.Hide()
    self.Layout()

  def show_manage_panel(self):
    self.manage_panel.Show()
    self.game_panel.Hide()
    self.Layout()

  def exit_manage_panel(self, event):
    self.game_panel.Show()
    self.manage_panel.Hide()
    self.Layout()

  def show_stats_panel(self):
    self.stats_panel.Show()
    self.game_panel.Hide()
    self.Layout()

  def exit_stats_panel(self, event):
    self.game_panel.Show()
    self.stats_panel.Hide()
    self.Layout()

  def show_settings_panel(self):
    self.settings_panel.Show()
    self.game_panel.Hide()
    self.Layout()

  def exit_settings_panel(self, event):
    self.game_panel.Show()
    self.settings_panel.Hide()
    self.Layout()

  def on_exit(self, event):
    self.Destroy()

if __name__ == '__main__':
  app = wx.App(False)
  frame = MSFrame()
  frame.Show()
  app.MainLoop()
