import wx

class MSPanel(wx.Panel):    
  def __init__(self, parent):
    super().__init__(parent)
    main_sizer = wx.BoxSizer(wx.VERTICAL)
    self.row_obj_dict = {}

    new_button = wx.Button(self, label='New')
    main_sizer.Add(new_button, 0, wx.ALL | wx.CENTER, 5)        
    load_button = wx.Button(self, label='Load')
    main_sizer.Add(load_button, 0, wx.ALL | wx.CENTER, 5)        
    exit_button = wx.Button(self, label='Exit')
    main_sizer.Add(exit_button, 0, wx.ALL | wx.CENTER, 5)        
    self.SetSizer(main_sizer)


class MSFrame(wx.Frame):    
  def __init__(self):
    super().__init__(parent=None,
                     title='Match Simulator 2020')
    self.panel = MSPanel(self)
    self.Show()

if __name__ == '__main__':
  app = wx.App(False)
  frame = MSFrame()
  app.MainLoop()
