'''Homke screen welcome. Begin game'''

import os
import pickle
import pyfiglet

from match_sim.cl.game import Game
import match_sim.cl.default as default

def home_screen():
  '''Welcome user.  Offer option to begin or resume game'''
  print(pyfiglet.figlet_format('Match\nSimulator\n2020\n'))
  options = ['(n)ew', '(l)oad', '(e)xit']
  while True:
    choose_option(input('choose option:\n{0}\n'.format(' '.join(options))))

def new_game():
  '''Create new game'''
  default.check_save_dir()
  team_name = input('choose team:\n{0}\n'.format(' '.join(default.poss_teams)))
  if team_name not in default.poss_teams:
    print('{0} not found in possible teams'.format(team_name))
    new_game()
    return
  manager_name = input('manager name:\n')
  game = Game(team_name, manager_name)
  game.save()
  game.cont()

def load_game():
  '''Show existing games.  Ask user to choose their game'''
  default.check_save_dir()
  games = os.listdir(default.save_dir)
  games = [g.replace('.dat', '') for g in games]
  if games == []:
    print('\tno games found\n')
  else:
    pl_game = input('choose game:\n{0}\n'.format(' '.join(games)))
    if pl_game in games:
      with open('{0}/{1}.dat'.format(default.save_dir, pl_game), 'rb') as f:
        game = pickle.load(f)
      game.save()
      game.cont()

def choose_option(txt):
  '''Compare user text to available options. Call appropriate method'''
  if txt in ['n', 'new']:
    new_game()
  elif txt in ['l', 'load']:
    load_game()
  elif txt in ['e', 'exit']:
    print(pyfiglet.figlet_format('Goodbye\n'))
    exit()

if __name__ == "__main__":

  home_screen()
