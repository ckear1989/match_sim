
class MatchReport(list):

  def append(self, ts, ps):
    super().append('{0} {1}'.format(ts, ps))
