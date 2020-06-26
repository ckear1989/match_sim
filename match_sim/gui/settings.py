'''Store and update in game settings'''

import wx

from match_sim.gui.template import TemplatePanel
from match_sim.settings import Settings as ClSettings

class SettingsPanel(TemplatePanel):
  def __init__(self, parent):
    super().__init__(parent)
    self.currently_showing = ''
    self.txt_output.AppendText(str(self.currently_showing))
    self.SetSizer(self.main_sizer)

class Settings(ClSettings):
  '''Create object to store game settings populated with defaults'''
  def __init__(self):
    super().__init__()
