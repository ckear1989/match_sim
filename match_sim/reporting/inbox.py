
class Inbox():
  '''Simulated email inbox for reports and communications'''
  def __init__(self, team):
    self.count = 0
    self.messages = {'read':[], 'unread': []}
    self.add_welcome_message(team)

  def add_welcome_message(self, team):
    msg = 'Dear {0},\n'.format(team.manager)
    msg += 'Welcome to {0}.'.format(team.name)
    msg += 'The 2020 season will be tough.'
    msg += 'You will be expected to come first or second in'
    msg += 'the league group.  We would be delighted if you'
    msg += 'take the team to the second or third round of the cup.\n\n'
    msg += 'We hope you will work well with coach {0} and get the'.format(team.coach)
    msg += 'players into top condition.  With your first match coming soon,'
    msg += 'we need you to put a training regime in place and sort out the team tactics'
    msg += 'and formation.\n\nFrom the board,\n{0}'.format(team.name)
    self.add_message(msg)

  def add_message(self, msg):
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
    self.messages['read'] = []

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
