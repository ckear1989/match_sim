
from match_sim.gui.template import TemplatePanel, TemplateButton

import wx

class ManagePanel(TemplatePanel):
  def __init__(self, parent):
    super().__init__(parent)
    lineup_button = TemplateButton(self, 'Lineup')
    lineup_button.Bind(wx.EVT_BUTTON, self.on_lineup)
    self.hbox3.Add(lineup_button)
    formation_button = TemplateButton(self, 'Formation')
    formation_button.Bind(wx.EVT_BUTTON, self.on_tactics)
    self.hbox3.Add(formation_button)
    tactics_button = TemplateButton(self, 'Tactics')
    tactics_button.Bind(wx.EVT_BUTTON, self.on_tactics)
    self.hbox3.Add(tactics_button)
    training_button = TemplateButton(self, 'Training')
    training_button.Bind(wx.EVT_BUTTON, self.on_training)
    self.hbox3.Add(training_button)
    self.SetSizer(self.main_sizer)

  def on_lineup(self, event):
    self.GetParent().hide_panel(self)
    self.GetParent().show_panel(LineupPanel)
    self.GetParent().Layout()

  def on_formation(self, event):
    self.GetParent().hide_panel(self)
    self.GetParent().show_panel(FormationPanel)
    self.GetParent().Layout()

  def on_tactics(self, event):
    self.GetParent().hide_panel(self)
    self.GetParent().show_panel(TacticsPanel)
    self.GetParent().Layout()

  def on_training(self, event):
    self.GetParent().hide_panel(self)
    self.GetParent().show_panel(TrainingPanel)
    self.GetParent().Layout()

class LineupPanel(TemplatePanel):
  def __init__(self, parent):
    super().__init__(parent)

class FormationPanel(TemplatePanel):
  def __init__(self, parent):
    super().__init__(parent)

class TacticsPanel(TemplatePanel):
  def __init__(self, parent):
    super().__init__(parent)

class TrainingPanel(TemplatePanel):
  def __init__(self, parent):
    super().__init__(parent)
