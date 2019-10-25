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
    # RE-INSTANTIATE GLOBALS
    global root, e1_var, selected_batch_list, b2
    logging.info("BATCH_LIST_SELECTED(bool)==" + str(selected_batch_list))
    # TRY THE FOLLOWING
    try: #{
        root.filename = filedialog.askopenfilename(initialdir="C:/",
                                                   title="Select BATCH LIST",
                                                   filetypes=(("csv files", "*.csv"),
                                                              ("xlsx files", "*.xlsx"),
                                                              ("all files", "*.*")))
        logging.info(root.filename)
        e1_var.set(root.filename)
        # CREATE FILE_PATH FOR "BATCH_LIST"
        batch_path = Path(root.filename)
        # ENABLE ZIP DIR SELECTION BUTTON... WAS: CONFIRM BUTTON
        b2.configure(state=tk.ACTIVE)
        # CALL THE DISPLAY FUNCTION
        display_batch_list(batch_path)
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
        pass
    #}
    finally: #{
        # SET BOOL TO TRUE
        selected_batch_list = True
        logging.info("BATCH_LIST_SELECTED(bool)==" + str(select_batch_list))
    #}
    
#}

def display_batch_list(file_path): #{
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

def test_popup(): #{
    # RE-INSTANTIATE GLOBALS
    global root
    # get root pos
    #x_pos = root.
    #y_pos = root.y
    # MAIN TOP LEVEL PROPERTIES
    toplevel = tk.Toplevel(master=root)
    toplevel.geometry("250x250+" + str(x_pos) + "+" + str(y_pos))
    toplevel.title("test")
    
    toplevel.config()
    toplevel.mainloop()
    
#}

if __name__ == "__main__": #{
    # SETUP LOGGER
    setup_logger()
    # TRY THE FOLLOWING:
    try: #{
        root = tk.Tk()
        root.title('CofA_Custom_Crate_v2.exe')
        root.geometry('650x150+250+250')  # (width x height + xPost + yPos)
        root.minsize(width=625, height=125)
        root.maxsize(width=750, height=175)
        
        # TKINTER VARIABLES:
        check_var = tk.BooleanVar()
        entry1_var = tk.StringVar(master=root, value="<<batch file location>>")
        entry2_var = tk.StringVar(master=root, value="<<zip folder location>>")
        
        #########################################################
        # TOP-FRAME
        topframe = tk.Frame(master=root)
        topframe.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        batch_entrybox = tk.Entry(master=topframe, width=25,
                                  textvariable=entry1_var,
                                  font=("Liberation Serif", 12),  # was: 15
                                  bd=4)
        batch_entrybox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        batch_button = tk.Button(master=topframe, width=25, height=1,
                                 text="Browse for Batch", command=test_popup,
                                 font=("Courier New", 10),
                                 bg="#cccc00", fg="#000000")  # WAS: #008080
        batch_button.pack(side=tk.RIGHT, fill=tk.BOTH, expand=False)  # WAS: true
        
        ############################################################
        # MIDDLE-FRAME
        middleframe = tk.Frame(master=root)
        middleframe.pack(anchor=tk.CENTER, fill=tk.BOTH, expand=True)
        
        zip_entrybox = tk.Entry(master=middleframe, width=25,
                                textvariable=entry2_var,
                                font=("Liberation Serif", 12),  # was: 15
                                bd=4)
        zip_entrybox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        zip_button = tk.Button(master=middleframe, width=25, height=1,
                               text="Browse for Zip", command=test_popup,
                               font=("Courier New", 10),
                               bg="#cccc00", fg="#000000")  # WAS: #008080
        zip_button.pack(side=tk.RIGHT, fill=tk.BOTH, expand=False)  # WAS: true
        
        #########################################################
        # BOTTOM-FRAME
        bottomframe = tk.Frame(master=root)
        bottomframe.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        
        #####################################################################
        # bottomleft
        bottomleft = tk.Frame(master=bottomframe)
        bottomleft.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        confirm_button = tk.Button(master=bottomleft, text="Confirm",
                                   font=("Courier New", 10),
                                   bg="#0099cc", fg="#000000",
                                   width=25, height=1, relief=tk.GROOVE)
        confirm_button.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        cancel_button = tk.Button(master=bottomleft, text="Cancel",
                                  font=("Courier New", 10),
                                  bg="#0099cc", fg="#000000",
                                  width=25, height=1, relief=tk.GROOVE)
        cancel_button.pack(side=tk.RIGHT, fill=tk.BOTH, expand=False)
        
        #####################################################################
        # bottomright
        bottomright = tk.Frame(master=bottomframe)
        bottomright.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)  # was: FALSE
        
        R1 = tk.Radiobutton(master=bottomright, text="Most Recent CofA(s)",
                            font=("Lucida Sans Typewriter", 10), width=25, height=1,
                            variable=check_var, value=1, state=tk.DISABLED,
                            bg="#0099cc", fg="#ffffff", command=test_messagebox)
        R1.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        #R1.place(x=250, y=35, height=50, width=200)
        
        R2 = tk.Radiobutton(master=bottomright, text="Return All CofA(s)", 
                            font=("Lucida Sans Typewriter", 10), width=25, height=1,
                            variable=check_var, value=2, state=tk.DISABLED, 
                            bg="#0099cc", fg="#000000")
        #R2.place(x=250, y=85, height=50, width=200)
        R2.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        
        root.config()
        root.mainloop()
        
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
#}