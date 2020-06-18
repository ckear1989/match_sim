'''Homke screen welcome. Begin game'''

import os
import pickle

from season import Season
import default

def home_screen():
  '''Welcome user.  Offer option to begin or resume game'''
  print('hello')
  options = ['(n)ew', '(l)oad', '(e)xit']
  choose_option(input('choose option:\n{0}\n'.format(' '.join(options))))

def new_game():
  '''Create new game'''
  team_name = input('choose team:\n{0}\n'.format(' '.join(default.poss_teams)))
  if team_name not in default.poss_teams:
    print('{0} not found in possible teams'.format(team_name))
  manager_name = input('manager name:\n')
  season = Season(team_name, manager_name)
  season.save()
  season.cont()

def load_game():
  '''Show existing games.  Ask user to choose their game'''
  games = os.listdir('../data/games/')
  games = [g.replace('.dat', '') for g in games]
  if games == []:
    print('\tno games found\n')
  else:
    pl_game = input('choose game:\n{0}\n'.format(' '.join(games)))
    if pl_game in games:
      with open('../data/games/%s.dat' % pl_game, 'rb') as f:
        season = pickle.load(f)
      season.save()
      season.cont()

def choose_option(txt):
  '''Compare user text to available options. Call appropriate method'''
  if txt in ['n', 'new']:
    new_game()
  elif txt in ['l', 'load']:
    load_game()
  elif txt in ['e', 'exit']:
    print('bye')
    exit()

if __name__ == "__main__":

  while True:
    home_screen()
