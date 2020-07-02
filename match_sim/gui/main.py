
import glob
import pickle
import time
import pathlib
path = pathlib.Path(__file__).parent.absolute()

import wx

import match_sim.default as default
from match_sim.gui.template import TemplatePanel, TemplateButton
from match_sim.gui.game import GamePanel, Game

class MSPanel(TemplatePanel):
  def __init__(self, parent):
    super().__init__(parent)
    self.new_button = TemplateButton(self, 'New')
    self.hbox3.Add(self.new_button, proportion=0)
    self.load_button = TemplateButton(self, 'Load')
    self.hbox3.Add(self.load_button, proportion=0)
    self.txt_output.Destroy()
    logo = wx.Image('{0}/../data/image/3dd982de-5e3b-4bcd-b9b8-88ce9bd03cce_200x200.png'.format(path), wx.BITMAP_TYPE_ANY).ConvertToBitmap()
    logo = wx.StaticBitmap(self, -1, logo, (10, 5), (logo.GetWidth(), logo.GetHeight()))
    self.hbox1.Add(logo, flag=wx.EXPAND|wx.CENTER|wx.ALL)
    self.SetSizer(self.main_sizer)

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

  def on_new(self, event):
    dlg = NewDialog()
    dlg.ShowModal()
    name = dlg.name.GetValue()
    team = dlg.team.GetString(dlg.team.GetSelection())
    if name:
      if team:
        self.game = Game(team, name)
        self.game_panel = GamePanel(self)
        self.sizer.Add(self.game_panel, 1, wx.EXPAND)
        self.game_panel.exit_button.Bind(wx.EVT_BUTTON, self.exit_game)
        self.game_panel.Show()
        self.main_panel.Hide()
        self.Layout()
    dlg.Destroy()

  def on_load(self, event):
    title = "Choose a game file:"
    dlg = wx.FileDialog(self, title, style=wx.DD_DEFAULT_STYLE)
    dlg.SetDirectory('{0}/../data/games/'.format(path))
    if dlg.ShowModal() == wx.ID_OK:
      game_listing = dlg.GetPath()
      with open(game_listing, 'rb') as f:
        self.game = pickle.load(f)
      self.game_panel = GamePanel(self)
      self.sizer.Add(self.game_panel, 1, wx.EXPAND)
      self.game_panel.exit_button.Bind(wx.EVT_BUTTON, self.exit_game)
      self.game_panel.Show()
      self.main_panel.Hide()
      self.Layout()
    dlg.Destroy()

  def on_inbox(self, apanel):
    self.inbox_panel = apanel(self)
    self.sizer.Add(self.inbox_panel, 1, wx.EXPAND)
    self.inbox_panel.exit_button.Bind(wx.EVT_BUTTON, self.exit_inbox)
    self.inbox_panel.Show()
    self.game_panel.Hide()
    self.Layout()

  def on_manage(self, apanel):
    self.manage_panel = apanel(self)
    self.sizer.Add(self.manage_panel, 1, wx.EXPAND)
    self.manage_panel.exit_button.Bind(wx.EVT_BUTTON, self.exit_manage)
    self.manage_panel.Show()
    self.game_panel.Hide()
    self.Layout()

  def on_lineup(self, apanel):
    self.lineup_panel = apanel(self)
    self.sizer.Add(self.lineup_panel, 1, wx.EXPAND)
    self.lineup_panel.exit_button.Bind(wx.EVT_BUTTON, self.exit_lineup)
    self.lineup_panel.Show()
    self.manage_panel.Hide()
    self.Layout()

  def on_training(self, apanel):
    self.training_panel = apanel(self)
    self.sizer.Add(self.training_panel, 1, wx.EXPAND)
    self.training_panel.exit_button.Bind(wx.EVT_BUTTON, self.exit_training)
    self.training_panel.Show()
    self.manage_panel.Hide()
    self.Layout()

  def on_stats(self, apanel):
    self.stats_panel = apanel(self)
    self.sizer.Add(self.stats_panel, 1, wx.EXPAND)
    self.stats_panel.exit_button.Bind(wx.EVT_BUTTON, self.exit_stats)
    self.stats_panel.Show()
    self.game_panel.Hide()
    self.Layout()

  def on_settings(self, apanel):
    self.settings_panel = apanel(self)
    self.sizer.Add(self.settings_panel, 1, wx.EXPAND)
    self.settings_panel.exit_button.Bind(wx.EVT_BUTTON, self.exit_settings)
    self.settings_panel.Show()
    self.game_panel.Hide()
    self.Layout()

  def on_match(self, apanel, match):
    self.match = match
    self.match_panel = apanel(self)
    self.sizer.Add(self.match_panel, 1, wx.EXPAND)
    self.match_panel.Show()
    self.game_panel.Hide()
    self.Layout()

  def exit_game(self, event):
    self.main_panel.Show()
    self.game_panel.Hide()
    self.Layout()

  def exit_inbox(self, event):
    self.game_panel.Show()
    self.inbox_panel.Hide()
    self.Layout()

  def exit_manage(self, event):
    self.game_panel.Show()
    self.manage_panel.Hide()
    self.Layout()

  def exit_lineup(self, event):
    self.manage_panel.Show()
    self.lineup_panel.Hide()
    self.Layout()

  def exit_training(self, event):
    self.manage_panel.Show()
    self.training_panel.Hide()
    self.Layout()

  def exit_stats(self, event):
    self.game_panel.Show()
    self.stats_panel.Hide()
    self.Layout()

  def exit_settings(self, event):
    self.game_panel.Show()
    self.settings_panel.Hide()
    self.Layout()

  def exit_match(self, event):
    self.game_panel.Show()
    self.match_panel.Hide()
    self.Layout()

  def on_exit(self, event):
    self.Destroy()

if __name__ == '__main__':
  app = wx.App(False)
  frame = MSFrame()
  frame.Show()
  app.MainLoop()
