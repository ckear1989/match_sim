
class Folder(list):
  '''Folder for inbox object'''
  def __str__(self):
    return '\n'.join(['[{0}] {1}...'.format(self.index(x), x[:20].replace('\n', ' ')) for x in self])

class Inbox():
  '''Simulated email inbox for reports and communications'''
  def __init__(self, team):
    self.count = 0
    self.messages = {'read': Folder(), 'unread': Folder()}
    self.team_name = team.name
    self.team_manager = team.manager
    self.team_coach = team.coach
    self.add_welcome_message()

  def add_welcome_message(self):
    msg = 'Dear {0},\n'.format(self.team_manager)
    msg += 'Welcome to {0}.'.format(self.team_name)
    msg += 'The 2020 season will be tough.'
    msg += 'You will be expected to come first or second in '
    msg += 'the league group.  We would be delighted if you '
    msg += 'take the team to the second or third round of the cup.\n\n'
    msg += 'We hope you will work well with coach {0} and get the '.format(self.team_coach)
    msg += 'players into top condition.With your first match coming soon, '
    msg += 'we need you to put a training regime in place and sort out the team tactics '
    msg += 'and formation.\n\nFrom the board,\n{0}'.format(self.team_name)
    self.add_message(msg)

  def add_message(self, msg):
    self.messages['unread'].append(msg)
    self.update_count()

  def add_injury_message(self, player):
    injury = player.season.injury
    msg = 'Injury report\n'
    msg += '{0} gained injury on {1}.'.format(player, injury.gain_date)
    msg += 'During a match he {0} injured his {1}.'.format(
      injury.status.lower(), injury.part)
    msg += 'He is set to return on {0}.\n'.format(injury.return_date)
    msg += 'From {0}.'.format(self.team_coach)
    self.messages['unread'].append(msg)
    self.update_count()

  def add_suspension_message(self, player):
    susp = player.season.suspension
    msg = 'Suspension report\n'
    msg += '{0} gained a suspension on {1}.'.format(player, susp.gain_date)
    msg += 'During a match he got a {0} suspension.'.format(susp.status)
    msg += 'He is set to return on {0}.\n'.format(susp.return_date)
    msg += 'From {0}.'.format(self.team_coach)
    self.messages['unread'].append(msg)
    self.update_count()

  def add_match_message(self, match):
    log = match.report
    msg = 'Match report\n'
    msg += '{0} \n'.format(match)
    for atime in log:
      msg += '{0} {1}\n'.format(atime, log[atime])
    msg += 'From {0}.'.format(self.team_coach)
    self.messages['unread'].append(msg)
    self.update_count()

  def update_count(self):
    self.count = len(self.messages['unread'])

  def open(self):
    cmd = ''
    while cmd not in ['c', 'continue']:
      cmd = input(' '.join(['(u)nread', '(r)ead', '(c)ontinue\n']))
      if cmd in ['u', 'unread']:
        self.get_unread()
      elif cmd in ['r', 'read']:
        self.get_read()

  def clear(self):
    self.messages['read'] = Folder()

  def get_read(self, i=0):
    cmd = ''
    while cmd not in ['c', 'continue']:
      cmd = input(' '.join(['(n)ext', '(c)ontinue\n']))
      if cmd in ['n', 'next']:
        if len(self.messages['read']) > i:
          msg = self.messages['read'][i]
          print(msg)
          if len(self.messages['read']) > (i+1):
            self.get_read(i+1)
        else:
          print('No read emails')
          return

  def get_unread(self):
    cmd = ''
    while cmd not in ['c', 'continue']:
      cmd = input(' '.join(['(n)ext', '(c)ontinue\n']))
      if cmd in ['n', 'next']:
        if len(self.messages['unread']) > 0:
          msg = self.messages['unread'].pop(0)
          print(msg)
          self.messages['read'].append(msg)
          self.update_count()
          if len(self.messages['unread']) > 0:
            self.get_unread()
        else:
          print('No unread emails')
          return
