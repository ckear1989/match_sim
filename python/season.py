
import pickle

class Season():
  def __init__(self, team):
    self.team = team
    self.save_file = '../data/games/%s.dat' % self.team.name

  def save(self):
    with open(self.save_file, 'wb') as f:
      pickle.dump(self, f)

  def load(self):
    return pickle.load(self.save_file)

