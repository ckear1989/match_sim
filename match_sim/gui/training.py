
import wx

import match_sim.cl.default as default
from match_sim.gui.graphics import Colour
from match_sim.gui.template import TemplatePanel

class TrainingPanel(TemplatePanel):
  def __init__(self, parent):
    super().__init__(parent)
    game = self.GetParent().game
    self.training = game.teams[game.team].training
    self.txt_output.Destroy()
    self.label_size = wx.Size(180, 28)
    self.colour= Colour()
    self.font = wx.Font(18, wx.DECORATIVE, wx.BOLD, wx.NORMAL)
    self.days = {x: None for x in default.dow.keys() if len(x) > 2}
    self.schedule = {x: None for x in default.dow.keys() if len(x) > 2}
    for day in self.days.keys():
      label = wx.StaticText(self, label=day, size=self.label_size)
      label.SetFont(self.font)
      label.SetForegroundColour(self.colour.BL)
      label.SetBackgroundColour(self.colour.LIME)
      self.days[day] = wx.BoxSizer(wx.VERTICAL)
      self.days[day].Add(label, flag=wx.ALL, border=5)
      self.schedule[day] = wx.ComboBox(self, choices=[x for x in default.focus if len(x) > 2])
      self.schedule[day].Bind(wx.EVT_COMBOBOX, self.update_schedule)
      if day in self.training.schedule.keys():
        self.schedule[day].SetStringSelection(self.training.schedule[day])
      self.days[day].Add(self.schedule[day])
      self.hbox1.Add(self.days[day])

  def update_schedule(self, event):
    for day in self.days:
      focus = self.schedule[day].GetStringSelection()
      print(day, focus)
      self.training.get_schedule(day, focus)
      # if day in self.training.schedule:
      #   print(dow, self.training.schedule[day])
      #   label = wx.StaticText(self, label=self.training.schedule[day], size=self.label_size)
      #   label.SetFont(self.font)
      #   label.SetForegroundColour(self.colour.BL)
      #   label.SetBackgroundColour(self.colour.LIME)
      #   self.days[day].Add(label)
