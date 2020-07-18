
from datetime import datetime

import wx

class MyDialog(wx.Dialog):
  def __init__(self, parent, title): 
    super(MyDialog, self).__init__(parent, title=title, size=(250, 150)) 
    panel = wx.Panel(self) 
    panel.main_sizer = wx.BoxSizer(wx.VERTICAL)
    panel.hbox1 = wx.BoxSizer(wx.HORIZONTAL)
    panel.hbox2 = wx.BoxSizer(wx.HORIZONTAL)
    panel.main_sizer.Add(panel.hbox1)
    panel.main_sizer.Add(panel.hbox2)
    self.start_date = wx.ComboBox(panel)
    self.end_date = wx.ComboBox(panel)
    self.ok_button = wx.Button(panel, wx.ID_OK, label="ok", size=(50, 20))
    self.cancel_button = wx.Button(panel, wx.ID_CANCEL, label="cancel", size=(50, 20))
    panel.hbox1.Add(self.start_date)
    panel.hbox1.Add(self.end_date)
    panel.hbox2.Add(self.ok_button)
    panel.hbox2.Add(self.cancel_button)
    panel.SetSizer(panel.main_sizer)

class TrainingReport():
  def __init__(self, parent):
    self.parent = parent
    self.training = self.parent.training
    self.report = ''
    if len(self.training.history.keys()) > 1:
      self.generate_report_dialogue()
    else:
      self.no_report_dialogue()

  def append_report(self, player):
    start_stats = self.training.history[self.start_date][str(player)]
    end_stats = self.training.history[self.start_date][str(player)]
    self.report += '\n{0}\n'.format(player)
    for stat in start_stats.__dict__.keys():
      if (isinstance(start_stats.__dict__[stat], float)) or \
        (isinstance(start_stats.__dict__[stat], int)):
        self.report += '{0} {1}\n'.format(stat, (end_stats.__dict__[stat] - start_stats.__dict__[stat]))

  def generate_report_dialogue(self):
    dlg = MyDialog(self.parent, 'Choose report dates')
    range_min = str(min(self.training.history.keys()))
    range_max = str(max(self.training.history.keys()))
    for adate in self.training.history.keys():
      dlg.start_date.Append(str(adate))
      dlg.end_date.Append(str(adate))
    dlg.start_date.SetValue(range_min)
    dlg.end_date.SetValue(range_max)
    resp = dlg.ShowModal()
    start_date = dlg.start_date.GetValue()
    end_date = dlg.end_date.GetValue()
    if resp == wx.ID_OK:
      if start_date:
        if end_date:
          if self.generate_report(start_date, end_date):
            self.sent_report_dialogue()
    elif resp == wx.ID_CANCEL:
      return

  def generate_report(self, start_date, end_date):
    self.start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
    self.end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
    if self.start_date < self.end_date:
      start_stats = self.training.history[self.start_date]
      end_stats = self.training.history[self.end_date]
      for player in end_stats:
        if player in start_stats:
          self.append_report(player)
      self.parent.inbox.add_training_message(self.report)
      return True

  def no_report_dialogue(self):
    dlg = wx.MessageDialog(self.parent, 'Sorry, not enough data to generate report', style=wx.OK)
    resp = dlg.ShowModal()
    if resp == wx.ID_OK:
      return

  def sent_report_dialogue(self):
    dlg = wx.MessageDialog(self.parent, 'Report generated, check your inbox', style=wx.OK)
    resp = dlg.ShowModal()
    if resp == wx.ID_OK:
      return
