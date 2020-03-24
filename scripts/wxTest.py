# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 08:57:49 2020

( ) - Filler Applicaion to be a place-holder for .exes
      that are not yet complete, but will be shortly.



@author: derbates
"""


# IMPORT THE GOODS
import os, sys, time
from time import sleep
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog, messagebox
from ttkthemes import ThemedStyle
import wx
import wx.html

class MyHtmlFrame(wx.Frame): # {
    
    def __init__(self, parent, title): # {
        wx.Frame.__init__(self, parent, -1, title, size = (600,400))
        html = wx.html.HtmlWindow(self)
        
    # }
    
# }

def main(): # {
    pass
# }

if __name__ == "__main__": # {
    app = wx.App()
    frm = MyHtmlFrame(None, "Simple HTML Browser")
    frm.Show()
    app.MainLoop()
# }