'''Store and update in game settings'''

import json
import pathlib
path = pathlib.Path(__file__).parent.absolute()

from utils import is_int

class Settings():
  '''Create object to store game settings populated with defaults'''
  def __init__(self):
    self.defaults_file = '{0}/data/settings/defaults.json'.format(path)
    self.defaults_file_test = '{0}/data/settings/defaults_test.json'.format(path)
    with open(self.defaults_file, 'r') as f:
      self.defaults = json.load(f)
    self.autosave = self.defaults['autosave']
    self.match_speed = self.defaults['match_speed']

  def update_setting(self, setting, value):
    '''Update class attribute with user input'''
    if setting == 'autosave':
      self.autosave = value
    if setting == 'match_speed':
      self.match_speed = value

  def get_settings(self):
    '''Ask user for input and check validity'''
    print(
      'settings',
      'autosave: %r' % self.autosave,
      'match_speed: %d' % self.match_speed,
      sep='\n'
    )
    setting = input()
    if ':' in setting:
      setting0 = setting.split(':')[0]
      setting1 = setting.split(':')[1].strip()
      if setting == 'autosave: False':
        self.update_setting('autosave', False)
      elif setting == 'autosave: True':
        self.update_setting('autosave', True)
      elif setting0 == 'match_speed':
        if is_int(setting1):
          if 0 < int(setting1) <= 70:
            self.update_setting('match_speed', int(setting1))

def test_settings():
  '''Test case for local use'''
  test_s = Settings()
  test_s.update_setting('autosave', False)

if __name__ == "__main__":
  test_settings()
