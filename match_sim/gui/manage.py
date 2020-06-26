
from match_sim.gui.template import TemplatePanel, TemplateButton

import wx

class ManagePanel(TemplatePanel):
  def __init__(self, parent):
    super().__init__(parent)
    tactics_button = TemplateButton(self, 'Tactics')
    self.hbox3.Add(tactics_button, 1, wx.ALIGN_LEFT | wx.BOTTOM, 5)
    self.SetSizer(self.main_sizer)

