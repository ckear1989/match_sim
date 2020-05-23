
def choose_option(txt):
  if txt == 'new':
    print txt
  elif txt == 'exit':
    print 'bye'
    exit()

if __name__=="__main__":

  print 'hello'
  while True:
    a = raw_input()
    choose_option(a)

