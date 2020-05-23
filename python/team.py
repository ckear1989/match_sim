
import random

first_names = [
  'Adam',
  'Brendan',
  'Ciaran',
  'Declan',
  'Eoghan'
]

last_names = [
  'Andrews',
  'Banagher',
  'Conroy',
  'Driscoll',
  'Evans'
]

class Team():
  def __init__(self, name, players=None):
    self.name = name
    if players is None:
      self.players = {}
      random.seed(name)
      for i in range(14):
        self.players[i] = '%s %s' % (
          random.choice(first_names), random.choice(last_names)
        )
    else:
      self.players = players

