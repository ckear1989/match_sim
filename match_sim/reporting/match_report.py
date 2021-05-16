
class MatchReport(dict):

  def append(self, ts, ps):
    self[ts] = ps
