import wx

########################################################################
class TabPanel(wx.Panel):
    """
    This will be the first notebook tab
    """
    #----------------------------------------------------------------------
    def __init__(self, parent):
        """"""
 
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)
 
        sizer = wx.BoxSizer(wx.VERTICAL)
        txtOne = wx.TextCtrl(self, wx.ID_ANY, "")
        txtTwo = wx.TextCtrl(self, wx.ID_ANY, "")
 
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(txtOne, 0, wx.ALL, 5)
        sizer.Add(txtTwo, 0, wx.ALL, 5)
 
        self.SetSizer(sizer)

 
########################################################################
class ChoicebookDemo(wx.Choicebook):
    """
    Choicebook class
    """
 
    #----------------------------------------------------------------------
    def __init__(self, parent):
        wx.Choicebook.__init__(self, parent, wx.ID_ANY)
 
        # Create the first tab and add it to the notebook
        tabOne = TabPanel(self)
        tabOne.SetBackgroundColour("Gray")
        self.AddPage(tabOne, "Book One")
 
        # Create and add the second tab
        tabTwo = TabPanel(self)
        self.AddPage(tabTwo, "Book Two")
 
        # Create and add the third tab
        self.AddPage(TabPanel(self), "Book Three")
 
        self.Bind(wx.EVT_CHOICEBOOK_PAGE_CHANGED, self.OnPageChanged)
        self.Bind(wx.EVT_CHOICEBOOK_PAGE_CHANGING, self.OnPageChanging)
 
    #----------------------------------------------------------------------
    def OnPageChanged(self, event):
        old = event.GetOldSelection()
        new = event.GetSelection()
        sel = self.GetSelection()
        print("OnPageChanged,  old:%d, new:%d, sel:%d\n" % (old, new, sel))
        event.Skip()
 
    #----------------------------------------------------------------------
    def OnPageChanging(self, event):
        old = event.GetOldSelection()
        new = event.GetSelection()
        sel = self.GetSelection()
        print('OnPageChanging, old:%d, new:%d, sel:%d\n' % (old, new, sel))
        event.Skip()
 
########################################################################
class DemoFrame(wx.Frame):
    """
    Frame that holds all other widgets
    """
 
    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        wx.Frame.__init__(self, None, wx.ID_ANY,
                          "Choicebook Tutorial",
                          size=(600,400))
        panel = wx.Panel(self)
 
        notebook = ChoicebookDemo(panel)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(notebook, 1, wx.ALL|wx.EXPAND, 5)
        panel.SetSizer(sizer)
        self.Layout()
 
        self.Show()
 
#----------------------------------------------------------------------
if __name__ == "__main__":
    app = wx.PySimpleApp()
    frame = DemoFrame()
    app.MainLoop()