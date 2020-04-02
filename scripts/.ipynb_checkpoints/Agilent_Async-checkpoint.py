# -*- coding: utf-8 -*- 
"""
Created on Wed April 01 00:69:00 2020

howdy

@ author: derbates
"""

# IMPORT THE GOODS
import os, sys, time
from time import sleep
import tkinter as tk
import tkiner.ttk as ttk
from tkinter import filedialog, messagebox
from ttkthemes import ThemedStyle

class Agilent_Async(): # {
    
    user_name = str(os.getlogin()) # get username 
    outbound_dir = "C:/data/outbound/"
    desktop_dir = "OneDrive - Agilent Technologies/Desktop" #C:/Users/derbates
    
    def __init__(self, root, the_logger): # {
        self.root = root
        self.root.title("<Insert Title Here>")
        self.geometry('315x200+300+300')
        self.root.resizable(width=False, height=False)
        # Get/Set USERNAME & DESKTOP DIRECTORIES
        # CREATE GUI
        self.create_gui(the_root = self.root)
    # }
    
    def create_gui(self, the_root): # {
        # TRY THE FOLLOWING
        try: # {
            pass
        # }
        except: # {
            pass
        # }
    # }
    
    def create_ttk_styles(self, the_root): # {
        # TRY THE FOLLOWING
        try: # {
            # CONFIGURE THE TTK STYLE
            self.style = ThemedStyle(the_root)
            # STYLE THEME
            self.style.set_theme("scidblue")
        # }
        except: # {
            pass
        # }
    # }
    
    def create_label_frame(self, the_root): # {
        # TRY THE FOLLOWING
        try: # {
            self.labelframe = ttk.Frame(the_root)
            self.labelframe.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        # }
        except: # {
            pass
        # }
    # }
    
    def create_main_frame(self, the_root): # {
        # TRY THE FOLLOWING
        try: # {
            self.mainframe = ttk.Frame(self.labelframe)
            self.mainframe.pack(anchor=tk.CENTER, fill=tk.BOTH, expand=True)
            # INSUFFICIENT RAM LABEL
            ram_label =ttk.Label(master=self.mainframe, text="Please Wait...\nAllocating RAM...")
            ram_label.pack(anchor=tk.CENTER, fill=tk.BOTH, expand=False)
        # }
        except: # {
            pass
        # }
    # }
# }

def main(): # {
    # TRY THE FOLLOWING
    try: # {
        window = tk.Tk()
        application = Agilent_Async(root = window, the_logger = None)
        window.config()
        window.mainloop()
    # }
    except: # {
        pass
    # }
# }

if __name__ == "__main__": # {
    main()
# }