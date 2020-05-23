
import os

nl = '\n'

def home_screen():
  print(
    'hello',
    'new load settings exit',
    sep=nl
  )

def get_team(tn):
  teama = {0: 'john smith'}
  teamb = {0: 'james smith'}
  return {
    'a': teama,
    'b': teamb
  }[tn]

def new_game():
  print(
    'choose difficulty',
    'easy medium hard',
    sep=nl
  )
  game_diff = input()
  poss_teams = ['a', 'b']
  print(
    'choose team:',
    'a',
    'b',
    sep=nl
  )
  team_name = input()
  if team_name in poss_teams:
    team = get_team(team_name)
    print(team)

def load_game():
  games = os.listdir('../data/games/')
  if games == []:
    print('no games found')
  else:
    print('choose game:')
    for game in games:
      print(game)

def settings():
  print('settings')

def choose_option(txt):
  if txt == 'new':
    new_game()
  elif txt == 'load':
    load_game()
  elif txt == 'settings':
    settings()
  elif txt == 'exit':
    print('bye')
    exit()

if __name__=="__main__":

  home_screen()
  while True:
    a = input()
    choose_option(a)

