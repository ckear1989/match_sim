
with open('../data/defaults/poss_teams.txt', 'r') as f:
  poss_teams = [x.strip() for x in f.readlines()]

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

with open('../data/defaults/training_focus.txt', 'r') as f:
  focus = [x.strip() for x in f.readlines()]
focus += [f[:2] for f in focus]

