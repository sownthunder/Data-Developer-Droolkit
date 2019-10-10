# -*- coding: utf-8 -*-
"""
Created on Wed Oct  9 14:16:30 2019

TAKEN FROM: "CofA_Custom_Crate_Creator_v1.py"
IMPLEMENTED fixes & better program structure

@author: derbates
"""

# IMPORT THE GOODS
import os, sys, time
from time import sleep
from pathlib import Path
import fnmatch, glob, shutil
import wmi, psutil
from PyPDF2 import PdfFileWriter, PdfFileReader
import tempfile
from zipfile import ZipFile
import pandas as pd
import numpy as np
from pandas import Series, DataFrame
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import logging

def create_custom_crate(): #{
    pass
#}

def select_zip_folder(): #{
    pass
#}

def select_batch_list(): #{
    pass
#}
    
def test_messagebox(): #{
    pass
#}

def setup_logger(): #{
    # TRY THE FOLLOWING
    try: #{
        logging.basicConfig(level=logging.INFO,
                           format='%(asctime)s : %(message)s',
                           datefmt='%Y-%m-%d-%H%M%S',
                           filemode='a')  #stream=sys.stdout)
    #}
    except: #{
        errorMessage = str(sys.exc_info()[0]) + "\n\t\t"
        errorMessage = errorMessage + str(sys.exc_info()[1]) + "\n\t\t"
        errorMessage = errorMessage + str(sys.exc_info()[2]) + "\n"
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        typeE = str("TYPE : " + str(exc_type))
        fileE = str("FILE : " + str(fname))
        lineE = str("LINE : " + str(exc_tb.tb_lineno))
        messageE = str("MESG : " + "\n" + str(errorMessage) + "\n")
        logging.error("\n" + typeE +
              "\n" + fileE +
              "\n" + lineE +
              "\n" + messageE)
    #}
    else: #{
        logging.info("[SETUP-LOGGER] SUCCESS! VERY NICE! ")
    #}
#}

if __name__ == "__main__": #{
    # SETUP LOGGER
    setup_logger()
    # TRY THE FOLLOWING:
    try: #{
        root = tk.Tk()
        }
    """
    # TRY THE FOLLOWING:
    try: #{
        # INSTANTIATE GLOBAL VARIABLES
        root = tk.Tk()
        selected_batch_list = False
        selected_zip_folder = False
        e1_var = tk.StringVar()
        e2_var = tk.StringVar()
        check_var = tk.IntVar()
        ##################################################
        # MAIN APP PROPERTIES
        # [2019-10-09]... root = tk.Tk()
        root.title('CofA_Custom_Crate')
        root.geometry('552x282+250+250')
        root.minsize(width=474, height=282)  # WAS: (width=375, height=275)
        root.maxsize(width=552, height=450)  # WAS: (width=False, height=False)
        root.resizable(width=True, height=True)
        b1 = tk.Button(master=root)
        #####################################################################################
        # TOP FRAME
        topframe = tk.Frame(master=root)
        topframe.pack(expand=1, fill=tk.BOTH, side=tk.TOP)
        
        e1_str = "<<INSERT BATCH LIST FILE HERE>>"
        e1_var.set(e1_str)
        
        # E1
        e1 = tk.Entry(master=topframe,
                      width=35,
                      textvariable=e1_var,
                      relief=tk.GROOVE,
                      cursor="rightbutton")
        e1.place(x=50, y=5, height=25, width=200)  # WAS: (height=30, width=200, x=50, y=20)
        
        # B1
        b1 = tk.Button(master=topframe, width=30,
                       text="Browse for BATCH_LIST",
                       font=("Sourcecode Semibold", 10),
                       command=select_batch_list,
                       relief=tk.GROOVE, cursor="pirate")
        b1.place(x=300, y=5, height=25, width=150)  # WAS: (height=30, width=100, x=250, y=20)
        # b1.config(command=test_messagebox)
        
        ######################################################################################
        # BOTTOM FRAME
        bottomframe = tk.Frame(master=root)
        bottomframe.pack(expand=1, fill=tk.BOTH, side=tk.BOTTOM)
        
        e2_str = "<<INSERT (to) ZIP FOLDER HERE>>"  # WAS: "C:/"
        e2_var.set(e2_str)
        
        # E2
        e2 = tk.Entry(master=bottomframe, width=20, textvariable=e2_var)
        e2.place(x=50, y=5, height=25, width=200)  # WAS: (x=50, y=30, height=30, width=200)
        
        # B2
        b2 = tk.Button(master=bottomframe, width=30,
                       text="Browse for ZIP Dir",
                       state=tk.DISABLED,
                       font=("Sourcecode Semibold", 10),
                       command=select_zip_folder,
                       relief=tk.GROOVE, cursor="spider")
        b2.place(x=300, y=5, height=25, width=150)  # WAS: (x=250, y=30, height=30, width=100)
        
        # CONFIRM BUTTON /b3
        b3 = tk.Button(master=bottomframe,
                       text="Confirm",
                       width=10,
                       state=tk.DISABLED,  # if b1_var.get() == False else tk.ENABLED,
                       font=("Sourcecode Semibold", 12),
                       command=create_custom_crate,  # WAS: custom_cofa_crate
                       relief=tk.RAISED, cursor="sb_down_arrow")
        b3.place(x=50, y=50, height=25, width=100)
        
        # CANCEL BUTTON /b4
        b4 = tk.Button(master=bottomframe, text="Cancel", width=10,
                       font=("Sourcecode Semibold", 12), command=root.destroy,
                       relief=tk.RAISED, cursor="circle")
        
        b4.place(x=150, y=50, height=25, width=100)
        
        # CHECK BUTOTNS FOR ( most recent / all ) SELECTION TYPES
        # CheckVar1 = tk.IntVar()
        # CheckVar2 = tk.IntVar()
        R1 = tk.Radiobutton(master=bottomframe, text="Most Recent CofA(s)", font=("Sourcecode Light", 12),
                            variable=check_var, value=1, state=tk.DISABLED, command=test_messagebox)
        R1.place(x=250, y=35, height=50, width=200)
        R2 = tk.Radiobutton(master=bottomframe, text="Return All CofA(s)", font=("Sourcecode Light", 12),
                            variable=check_var, value=2, state=tk.DISABLED, command=test_messagebox)
        R2.place(x=250, y=85, height=50, width=200)
        
        root.config()
        root.mainloop()
        ##################################################
    #}
    except: #{
        errorMessage = str(sys.exc_info()[0]) + "\n\t\t"
        errorMessage = errorMessage + str(sys.exc_info()[1]) + "\n\t\t"
        errorMessage = errorMessage + str(sys.exc_info()[2]) + "\n"
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        typeE = str("TYPE : " + str(exc_type))
        fileE = str("FILE : " + str(fname))
        lineE = str("LINE : " + str(exc_tb.tb_lineno))
        messageE = str("MESG : " + "\n" + str(errorMessage) + "\n")
        logging.error("\n" + typeE +
                      "\n" + fileE +
                      "\n" + lineE +
                      "\n" + messageE)
    #}
    else: #{
        print("SUCCESS! VERY NICE!")
    #}
    """
#}