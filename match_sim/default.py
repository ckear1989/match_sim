'''Store default parameters for game mechanics'''

import barnum
import random
import pathlib
path = pathlib.Path(__file__).parent.absolute()

random.seed(12345)
poss_teams = [barnum.create_city_state_zip()[1] for i in range(16)]

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
    'attacking': 50,
    'posession': 50,
    'defending': 50
  },
  'posession': {
    'attacking': 10,
    'posession': 60,
    'defending': 30
  },
  'blanket': {
    'attacking': 10,
    'posession': 10,
    'defending': 80
  },
  'attacking': {
    'attacking': 60,
    'posession': 20,
    'defending': 20
  },
  'gung-ho': {
    'attacking': 80,
    'posession': 10,
    'defending': 10
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
