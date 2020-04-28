# -*- coding: utf-8 -*-
"""
Created on Tue Apr 28 13:05:40 2020

wxPython

@author: derbates
"""

# IMPORT THE GOODS
import os, sys, time
from time import sleep
import wx

class DerivedApp(wx.App): # {

    def OnInit(self): # {
        the_frame = wx.Frame(None, -1)

        # Other initialization code...
        the_frame.Show(True)
        return True
    # }
# }

def main(): # {
    app = wx.App()
    DerivedApp(None)
    app.MainLoop()
# }

if __name__ == "__main__": # {
    main()
# }