'''Store and update in game settings'''

import wx

from match_sim.cl.settings import Settings as ClSettings
from match_sim.gui.template import TemplatePanel

class SettingsPanel(TemplatePanel):
  def __init__(self, parent):
    super().__init__(parent)
    self.game = self.GetParent().game
    self.txt_output.Destroy()
    self.autosave = wx.CheckBox(self, label='Autosave')
    self.vbox1 = wx.BoxSizer(wx.VERTICAL)
    self.vbox1.Add(self.autosave, flag=wx.ALL, border=10)
    self.match_speed = wx.Slider(self, minValue=1, maxValue=70, style=wx.SL_HORIZONTAL|wx.SL_LABELS)
    self.vbox1.Add(wx.StaticText(self, label='Match Speed'), flag=wx.EXPAND|wx.LEFT|wx.TOP|wx.RIGHT, border=10)
    self.vbox1.Add(self.match_speed, flag=wx.EXPAND|wx.LEFT|wx.BOTTOM|wx.RIGHT, border=10)
    self.Bind(wx.EVT_CHECKBOX, self.checkbox)
    self.Bind(wx.EVT_SLIDER, self.slider)
    self.set_current()
    self.hbox1.Add(self.vbox1)
    self.SetSizer(self.main_sizer)

  def set_current(self):
    self.autosave.SetValue(self.game.settings.autosave)
    self.match_speed.SetValue(self.game.settings.match_speed)

  def checkbox(self, event):
    self.game.settings.autosave = self.autosave.IsChecked()

  def slider(self, event):
    self.game.settings.match_speed = self.match_speed.GetValue()

class Settings(ClSettings):
  def __init__(self):
    super().__init__()
