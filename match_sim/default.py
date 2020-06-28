'''Store default parameters for game mechanics'''

import os
import random
import pathlib
path = pathlib.Path(__file__).parent.absolute()

import barnum
import pyfiglet

random.seed(12345)
poss_teams = [barnum.create_city_state_zip()[1] for i in range(16)][:8]

save_dir = '{0}/data/games/'.format(path)
def check_save_dir():
  if os.path.isdir(save_dir) is False:
     os.mkdir(save_dir)

welcome_message = pyfiglet.figlet_format('Match\nSimulator\n2020\n')
image_dir = '{0}/data/image/'.format(path)
gui_background = '{0}{1}'.format(image_dir, 'puma-40-20-artificial-grass-2.jpg')

dow = {
  'monday': 0,
  'mo': 0,
  'tuesday': 1,
  'tu': 1,
  'wednesday': 2,
  'we': 2,
  'thursday': 3,
  'th': 3,
  'friday': 4,
  'fr': 4,
  'saturday': 5,
  'sa': 5,
  'sunday': 6,
  'su': 6
}

with open('{0}/data/defaults/training_focus.txt'.format(path), 'r') as f:
  focus = [x.strip() for x in f.readlines()]
focus += [f[:2] for f in focus]

formations = [
  '3-3-2-3-3',
  '3-3-3-3-2',
  '4-4-4-1-1',
  '5-5-3-0-1',
  '2-2-1-4-5'
]

formations_ascii = {x:open('{0}/data/formations/{1}.txt'.format(path, x)).read() for x in formations}

tactics = [
  'neutral',
  'posession',
  'blanket',
  'attacking',
  'gung-ho'
]

tactics_s = {
  'neutral': {
    'attacking': 60,
    'posession': 20,
    'defending': 20
  },
  'posession': {
    'attacking': 40,
    'posession': 40,
    'defending': 20
  },
  'blanket': {
    'attacking': 10,
    'posession': 10,
    'defending': 80
  },
  'attacking': {
    'attacking': 75,
    'posession': 15,
    'defending': 10
  },
  'gung-ho': {
    'attacking': 90,
    'posession': 8,
    'defending': 2
  }
}

body_parts = [
  'hand',
  'foot',
  'achilles',
  'hamstring',
  'calf',
  'knee',
  'back',
  'head',
  'penis'
]

suspensions = {
  'yellow': 14,
  'red': 28
}
