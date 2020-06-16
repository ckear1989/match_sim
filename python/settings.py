
import json

nl = '\n'

class Settings():
  def __init__(self):
    self.defaults_file = '../data/settings/defaults.json'
    self.defaults_file_test = '../data/settings/defaults_test.json'
    with open(self.defaults_file, 'r') as f:
      self.defaults = json.load(f)
    self.autosave = self.defaults['autosave']

  def update_setting(self, setting, value):
    if setting == 'autosave':
      self.autosave = value
      self.defaults['autosave'] = value
    with open(self.defaults_file, 'w') as f:
      json.dump(self.defaults, f)

  def get_settings(self):
    print(
      'settings',
      'autosave: %r' % self.autosave,
      sep=nl
    )
    setting = input()
    if setting == 'autosave: False':
      self.update_setting('autosave', False)
    elif setting == 'autosave: True':
      self.update_setting('autosave', True)

def test_settings():
  s = Settings()
  s.update_setting('autosave', False)

if __name__=="__main__":
  test_settings()

