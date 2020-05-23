
import os
from settings import Settings
from team import Team
from season import Season

nl = '\n'
cl = 2 * (chr(27) + '[2J')
clear = lambda: os.system('cls' if os.name == 'nt' else 'clear')

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
  clear()
  choose_option(a, settings)

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
    team = Team(team_name)
    print(team)
    for player in team.players:
      print(player)
      print(team.players[player])
  season = Season(team)
  print(season)
  season.save()

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

