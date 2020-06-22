
class Inbox():
  '''Simulated email inbox for reports and communications'''
  def __init__(self):
    self.count = 0
    self.messages = {'read':[], 'unread': []}

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

  def get_unread(self):
    cmd = ''
    while cmd not in ['c', 'continue']:
      cmd = input(' '.join(['(n)ext', '(c)ontinue\n']))
      if cmd in ['n', 'next']:
        if len(self.messages['unread']) > 0:
          msg = self.messages['unread'].pop(0)
          print(msg)
          self.messages['read'].append(msg)
          if len(self.messages['read']) > 0:
            self.get_unread()
        else:
          print('No unread emails')
