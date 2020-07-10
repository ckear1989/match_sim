
import pathlib
path = pathlib.Path(__file__).parent.absolute()
import random

import wx

import match_sim.cl.default as default

# https://wiki.wxpython.org/DoubleBufferedDrawing
# This has been set up to use the wx.BufferedDC if
# USE_BUFFERED_DC is True. Alternatively, it can use the raw
# wx.MemoryDC, etc.

# USE_BUFFERED_DC = False # use UpdateDrawing() method
USE_BUFFERED_DC = True  # use Draw() method

class BufferedWindow(wx.Window):
    '''
     A Buffered window class.

     To use it, subclass it and define a Draw() method that takes a DC
     to draw to. In that method, put the code needed to draw the picture
     you want. The window will automatically be double buffered, and the
     screen will be automatically updated when a Paint event is received
     (USE_BUFFERED_DC = True).

     When the drawing needs to change, your app needs to call the
     UpdateDrawing() method. Since the drawing is stored in a bitmap, you
     can also save the drawing to file by calling the SaveToFile() method.
    '''
    def __init__(self, *args, **kwargs):
        # Make sure the NO_FULL_REPAINT_ON_RESIZE style flag is set.
        # And define a new kwargs entry for wx.python
        kwargs['style'] = kwargs.setdefault('style', wx.NO_FULL_REPAINT_ON_RESIZE) | wx.NO_FULL_REPAINT_ON_RESIZE
        super().__init__( *args, **kwargs)

        # Setup event handlers for drawing 
        self.Bind(wx.EVT_PAINT,self.OnPaint)       
        self.Bind(wx.EVT_SIZE, self.OnSize)

        # OnSize called to make sure the buffer is initialized.
        # This might result in OnSize getting called twice on some
        # platforms at initialization, but little harm done.
        self.OnSize(None)
        self.paint_count = 0

    def Draw(self, dc):
        '''
         just here as a place holder.
         This method must be over-ridden when subclassed
        '''
        pass

    def OnPaint(self, event):
        '''
          All that is needed here is to move the buffer to the screen
        '''
        if USE_BUFFERED_DC:
            dc = wx.BufferedPaintDC(self, self._Buffer)
        else:
            dc = wx.PaintDC(self)
            dc.DrawBitmap(self._Buffer, 0, 0)

    def OnSize(self,event):
        '''
         The Buffer init is done here, to make sure the buffer is always
         the same size as the Window
        '''
        Size  = self.ClientSize

        # Make new offscreen bitmap: this bitmap will always have the
        # current drawing in it, so it can be used to save the image to
        # a file, or whatever.
        self._Buffer = wx.Bitmap(*Size)
        self.UpdateDrawing()

    def SaveToFile(self, FileName, FileType=wx.BITMAP_TYPE_PNG):
        '''
         This will save the contents of the buffer
         to the specified file. See the wx.Windows docs for 
         wx.Bitmap::SaveFile for the details
        '''
        self._Buffer.SaveFile(FileName, FileType)

    def UpdateDrawing(self):
        '''
         This would get called if the drawing is changed, for whatever reason.

         The idea here is that the drawing is based on some data generated
         elsewhere in the system. If that data changes, the drawing needs to
         be updated.

         This code re-draws the buffer, then calls Update, which forces a paint event.
        '''
        dc = wx.MemoryDC()
        dc.SelectObject(self._Buffer)
        self.Draw(dc)
        del dc      # need to get rid of the MemoryDC before Update() is called.
        self.Refresh()
        self.Update()
            
class DrawWindow(BufferedWindow):
    '''
     Purpose: Initialization for Draw()
    '''
    def __init__(self, *args, **kwargs):
        '''
         Any data the Draw() function needs must be initialized before
         initialization of BufferedWindow, since this will trigger the Draw
         function.
        ''' 
        self.DrawData = {}
        super().__init__(*args, **kwargs)  # initialize parent (BufferedWindow)

    def Draw(self, dc):
        '''
         Purpose: to generate all the cmds for drawing 
          Note:
           1. Overrides Draw() in BufferedWindow() 
        '''
        dc.SetBackground( wx.Brush("White") )
        dc.Clear() # make sure you clear the bitmap!

        # Here's the actual drawing code.
        for key, data in self.DrawData.items():
            if key == "Rectangles":
                dc.SetBrush(wx.BLUE_BRUSH)
                dc.SetPen(wx.Pen('VIOLET', 4))
                for r in data:
                    dc.DrawRectangle(*r)
            elif key == "Ellipses":
                dc.SetBrush(wx.Brush("GREEN YELLOW"))
                dc.SetPen(wx.Pen('CADET BLUE', 2))
                for r in data:
                    dc.DrawEllipse(*r)
            elif key == "Polygons":
                dc.SetBrush(wx.Brush("SALMON"))
                dc.SetPen(wx.Pen('VIOLET RED', 4))
                for r in data:
                    dc.DrawPolygon(r)

class MyFrame(wx.Frame):
    '''
     Purpose: initialize a frame to hold DC and setup menu bar
    '''
    def __init__(self, parent=None):    
        wx.Frame.__init__(self, parent,
                          size  = (500,500),
                          title = "Double Buffered Test",
                          style = wx.DEFAULT_FRAME_STYLE)

        ## Set up the MenuBar
        MenuBar   = wx.MenuBar()
        
        file_menu = wx.Menu()
        
        # Define each item in menu bar and their event handlers
        item = file_menu.Append(wx.ID_EXIT, "&Exit")
        self.Bind(wx.EVT_MENU, self.OnQuit, item)
        MenuBar.Append(file_menu, "&File")

        draw_menu = wx.Menu()
        item = draw_menu.Append(wx.ID_ANY, "&New Drawing","Update the Drawing Data")
        self.Bind(wx.EVT_MENU, self.NewDrawing, item)
        item = draw_menu.Append(wx.ID_ANY,'&Save Drawing\tAlt-I','')
        self.Bind(wx.EVT_MENU, self.SaveToFile, item)
        MenuBar.Append(draw_menu, "&Draw")

        self.SetMenuBar(MenuBar)
        self.Window = TemplatePanel(self) # initialize window for drawing
        self.Show()
        # Initialize a drawing -- it has to be done after Show() is called
        #   so that the Window is correctly sized.
        self.NewDrawing()

    def OnQuit(self,event):
        self.Close(True)
        
    def NewDrawing(self, event=None):
        '''
         Pupose: setup for updating drawing
        '''
        self.Window.DrawData = self.MakeNewData()
        self.Window.UpdateDrawing()

    def SaveToFile(self,event):
        '''
         Purpose: output image to a *.png file
        '''
        dlg = wx.FileDialog(self, "Choose a name for file to contain image",
                           defaultDir  = "",
                           defaultFile = "",
                           wildcard    = "*.png",
                           style       = wx.FD_SAVE)
        if dlg.ShowModal() == wx.ID_OK:
            self.Window.SaveToFile(dlg.GetPath(), wx.BITMAP_TYPE_PNG)
        dlg.Destroy()

    def MakeNewData(self):
        '''
         Purpose: generate some data for randomly shaped geometric 
                  structures (rectangles, ellipses and polygons)
        '''
        MaxX, MaxY = self.Window.GetClientSize() # to limit the size of these structures
        
        DrawData = {}
        # Define some random rectangles
        lst = []
        for i in range(5):
            w = random.randint(1,MaxX//2)
            h = random.randint(1,MaxY//2)
            x = random.randint(1,MaxX-w)
            y = random.randint(1,MaxY-h)
            lst.append( (x,y,w,h) )
        DrawData["Rectangles"] = lst

        # Define some random ellipses
        lst = []
        for i in range(5):
            w = random.randint(1,MaxX//2)
            h = random.randint(1,MaxY//2)
            x = random.randint(1,MaxX-w)
            y = random.randint(1,MaxY-h)
            lst.append( (x,y,w,h) )
        DrawData["Ellipses"] = lst

        # Define some random Polygons
        lst = []
        for i in range(3):
            points = []
            for j in range(random.randint(3,8)):
                point = (random.randint(1,MaxX),random.randint(1,MaxY))
                points.append(point)
            lst.append(points)
        DrawData["Polygons"] = lst

        return DrawData

class DemoApp(wx.App):
    '''
     Purpose: initialize frame to hold DC
      Note:
       1. Uses the default OnInit method in wx.App
    '''
    def OnInit(self):
        frame = MyFrame()
        self.SetTopWindow(frame)
        return True

class TemplateFrame(wx.Frame):
  def __init__(self):
    super().__init__(parent=None, title='Match Simulator 2020')
    self.sizer = wx.BoxSizer(wx.VERTICAL)
    self.SetSizer(self.sizer)
    self.SetSize((800, 600))
    self.Centre()

class TemplateButton(wx.Button):
  def __init__(self, parent, label):
    super().__init__(parent)
    # self.font = wx.SystemSettings.GetFont(wx.SYS_SYSTEM_FONT)
    # self.font.SetPointSize(15)
    # self.SetFont(self.font)
    png = wx.Image('{0}/../data/image/buttons/new0.png'.format(path), wx.BITMAP_TYPE_ANY)
    w = png.GetWidth() / 5
    h = png.GetHeight() / 5
    png = png.Scale(w, h)
    png = png.ConvertToBitmap()
    png.SetMask(wx.Mask())
    # print(png.GetMask())
    self.SetSize((w+10, h+10))
    self.SetBitmap(png)
    # print(self.GetSize())
    # print(png.GetSize())
    self.SetLabel(label)

class TemplatePanel(DrawWindow):
  def __init__(self, *args, **kwargs):
    '''
     Any data the Draw() function needs must be initialized before
     initialization of BufferedWindow, since this will trigger the Draw
     function.
    ''' 
    self.DrawData = {}
    super().__init__(*args, **kwargs)  # initialize parent (DrawWindow)
    self.main_sizer = wx.BoxSizer(wx.VERTICAL)
    self.font = wx.SystemSettings.GetFont(wx.SYS_SYSTEM_FONT)
    self.font.SetPointSize(15)

    self.hbox1 = wx.BoxSizer()
    self.txt_output = wx.TextCtrl(self,
      style=wx.TE_MULTILINE|wx.BORDER_SUNKEN|wx.TE_READONLY|wx.TE_RICH2, size=(400,200))
    self.currently_showing = ''
    self.txt_output.AppendText(str(self.currently_showing))
    self.hbox1.Add(self.txt_output, proportion=1, flag=wx.EXPAND)
    self.main_sizer.Add(self.hbox1, proportion=2, flag=wx.ALL|wx.EXPAND, border=20)

    self.hbox2 = wx.BoxSizer(wx.HORIZONTAL)
    self.exit_button = TemplateButton(self, 'Exit')
    self.hbox3 = wx.BoxSizer(wx.HORIZONTAL)
    self.hbox4 = wx.BoxSizer()
    self.hbox4.Add(self.exit_button, proportion=0)
    self.hbox2.Add(self.hbox3, proportion=0, flag=wx.TOP|wx.BOTTOM|wx.LEFT, border=5)
    self.hbox2.Add(self.hbox4, proportion=0, flag=wx.TOP|wx.BOTTOM|wx.RIGHT, border=5)

    self.main_sizer.Add(self.hbox2, proportion=0)
    self.SetSizer(self.main_sizer)
    self.SetAutoLayout(True)
    self.main_sizer.Fit(self)

  def Draw(self, dc):
    '''
     Purpose: to generate all the cmds for drawing 
      Note:
       1. Overrides Draw() in BufferedWindow() 
    '''
    # dc.SetBackground( wx.Brush("White") )
    dc.Clear() # make sure you clear the bitmap!
    bmp = wx.Bitmap(default.gui_background)
    dc.DrawBitmap(bmp, 0, 0)

  def UpdateDrawing(self):
    super().UpdateDrawing()
    self.Layout()

if __name__ == "__main__":
    # Ok, let's run it ...
    app = DemoApp(0)
    app.MainLoop()
