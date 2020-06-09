
import os
import pickle

from settings import Settings
from team import Team
from season import Season
import default

nl = '\n'
cl = 2 * (chr(27) + '[2J')
clear = lambda: os.system('cls' if os.name == 'nt' else 'clear')

def home_screen(settings):
  print('hello')
  options = ['(n)ew', '(l)oad', '(s)ettings', '(e)xit']
  a = input('choose option:\n{0}\n'.format(' '.join(options)))
  clear()
  choose_option(a, settings)

def new_game():
  options = ['(e)asy', '(m)edium', '(h)ard']
  game_diff = input('choose difficulty:\n{0}\n'.format(' '.join(options)))
  team_name = input('choose team:\n{0}\n'.format(' '.join(default.poss_teams)))
  manager_name = input('manager name:\n')
  season = Season(team_name, manager_name)
  season.save()
  season.cont()

def load_game():
  games = os.listdir('../data/games/')
  games = [g.replace('.dat', '') for g in games]
  if games == []:
    print('\tno games found\n')
  else:
    lg = input('choose game:\n{0}\n'.format(' '.join(games)))
    if lg in games:
      with open('../data/games/%s.dat' % lg, 'rb') as f:
        season = pickle.load(f)
      season.save()
      season.cont()

def choose_option(txt, settings):
  if txt in ['n', 'new']:
    new_game()
  elif txt in ['l', 'load']:
    load_game()
  elif txt in ['s', 'settings']:
    settings.get_settings()
  elif txt in ['e', 'exit']:
    print('bye')
    exit()

if __name__=="__main__":

  while True:
    settings = Settings()
    home_screen(settings)

