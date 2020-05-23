
import os
from settings import Settings

nl = '\n'

def home_screen(settings):
  print('hello')
  options = ['new', 'load', 'settings', 'exit']
  print(
    'choose option:',
    '\t'.join(options),
    nl,
    sep=nl
  )
  a = input()
  choose_option(a, settings)

def get_team(tn):
  teama = {0: 'john smith'}
  teamb = {0: 'james smith'}
  return {
    'a': teama,
    'b': teamb
  }[tn]

def new_game():
  options = ['easy', 'medium', 'hard']
  print(
    'choose difficulty',
    '\t'.join(options),
    nl,
    sep=nl
  )
  game_diff = input()
  poss_teams = ['a', 'b']
  print(
    'choose team:',
    '\t'.join(poss_teams),
    nl,
    sep=nl
  )
  team_name = input()
  if team_name in poss_teams:
    team = get_team(team_name)
    print(team)

def load_game():
  games = os.listdir('../data/games/')
  if games == []:
    print('\tno games found\n')
  else:
    print('choose game:')
    for game in games:
      print(game)

def choose_option(txt, settings):
  if txt == 'new':
    new_game()
  elif txt == 'load':
    load_game()
  elif txt == 'settings':
    settings.get_settings()
  elif txt == 'exit':
    print('bye')
    exit()

if __name__=="__main__":

  while True:
    settings = Settings()
    home_screen(settings)

