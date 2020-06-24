
import wx

import match_sim.default as default
from match_sim.cl.game import Game

class MSPanel(wx.Panel):
  def __init__(self, parent):
    super().__init__(parent)
    main_sizer = wx.BoxSizer(wx.VERTICAL)
    self.row_obj_dict = {}

    new_button = wx.Button(self, label='New')
    new_button.Bind(wx.EVT_BUTTON, self.on_new)
    main_sizer.Add(new_button, 0, wx.ALL | wx.CENTER, 5)
    load_button = wx.Button(self, label='Load')
    main_sizer.Add(load_button, 0, wx.ALL | wx.CENTER, 5)
    exit_button = wx.Button(self, label='Exit')
    exit_button.Bind(wx.EVT_BUTTON, self.on_exit)
    main_sizer.Add(exit_button, 0, wx.ALL | wx.CENTER, 5)
    self.SetSizer(main_sizer)

  def on_new(self, event):
    dlg = NewDialog()
    dlg.ShowModal()
    dlg.Destroy()

  def on_exit(self, event):
    self.Destroy()

class NewDialog(wx.Dialog):
  def __init__(self):
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
    name = self.name.GetValue()
    team = self.team.GetString(self.team.GetSelection())
    if name:
      if team:
        game = Game(team, name)
        game.save()
        game.cont()
    self.Close()

class MSFrame(wx.Frame):
  def __init__(self):
    super().__init__(parent=None, title='Match Simulator 2020')
    self.panel = MSPanel(self)
    self.Show()

if __name__ == '__main__':
  app = wx.App(False)
  frame = MSFrame()
  app.MainLoop()
