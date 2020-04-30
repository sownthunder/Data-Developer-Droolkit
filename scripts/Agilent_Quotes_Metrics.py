# -*- coding: utf-8 -*-
"""
Created on Tue Apr 28 15:15:15 2020

Agilent_Quotes_Metrics.py

USES: 
    - Agilent_CC_Creator_ttk.py
    - Custom_Create_v1
    - Custom_Crate_v2
    
PURPOSE:
    - pulls metrics for user between two specified dates
    
@author: derbates
"""

# IMPORT THE GOODS
import os, sys, time
from time import sleep
import pathlib, glob
from pathlib import Path
import fnmatch, shutil
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from pandas import Series, DataFrame
import logging
import tempfile, threading
from PyPDF2 import PdfFileReader, PdfFileWriter
from zipfile import ZipFile
import email, smtplib, ssl
import os.path as op
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
from ttkthemes import ThemedStyle
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox, filedialog 
from tkinter import constants, commondialog
import sqlite3

class Logger(): # {
    
    def __init__(self, logging_output_dir): # {
        self.logging_output_dir = logging_output_dir
        #### INITITATING THE LOGGER OBJECT
        self.logger = logging.getLogger(__name__)
        
        # set the level of the logger (THIS IS SUPER USEFUL since it enables)
        # Explanation regarding the logger levels can be found here:
        # https://docs.python.org/3/howto/logging.html
        self.logger.setLevel(logging.DEBUG)
        
        # Create the logs.log file
        user_name = str(os.getlogin()) # get username 
        log_file_name = user_name + "-" + str(pd.Timestamp.now())[:10] + "-CofA-E-Node-Wizard-use-"
        log_file_path = os.path.join(self.logging_output_dir, str(log_file_name) + ".log")
        file_handler = logging.FileHandler(log_file_path)
        
        # Create the console handler with a higher log level
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.ERROR)
        
        # Format the logs structure so that every line would incude:
        # the time, the message, the function, the line #, script and level name
        formatter = logging.Formatter('%(asctime)s: %(message)s, FROM=%(funcName)s, LINENO=%(lineno)d, %(name)s - %(levelname)s')
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        # Adding the formater handlers
        self.logger.addHandler(console_handler)
        self.logger.addHandler(file_handler)
        
        # and printing the logs to the console as well
        self.logger.addHandler(logging.StreamHandler(sys.stdout))
    # }
# }

"""
IF SCRIPT IS BEING CALLED ON THE DAILY BASIS (ie scan last night and today)
*** THEN USE THE OLD ALGORITHIM OF SCANNING ENTIRE DIRECTORY AND CHECK AGAINST
 EACH INDIVIDUAL FILE SEPERATELY AND CHECK IF WITHIN TIME RANGE... ***
 
 IF SCRIPT IS BEING CALLED AND WANTS >> A SPECIFIC DATE RANGE << THEN 
 ** CREATE THE IDX FRAME AND SORT INDEX AND FILTER ON TIMESTAMP **
"""
class Agilent_CC_Creator(): # {
    
    in_file = "C:/data/inbound/Agilent_CofA_Letterhead_03-21-19.pdf"
    # [2020-01-27]\\in_directory_1 = "F:/APPS/CofA/"
    # [2020-01-27]\\in_directory_2 = "G:/C of A's/Agilent/"
    # [2020-01-27]\\out_directory = "G:/C of A's/#Email Node/"
    f_drive_convention = "*[@]*.pdf"
    g_drive_convention = "[part]*[CofA]*[Lot]*[#]*.pdf"
    
    def __init__(self, root, the_logger): # {
        self.root = root
        self.the_logger = the_logger
        self.root.title("Agilent QUOTES Metrics")
        self.root.geometry('225x125+300+300')  # was 275x400
        self.root.resizable(width=True, height=True)
        # [2020-04-27]\\self.root.minsize(width=275, height=275)
        self.root.minsize(width=220, height=170)
        self.root.maxsize(width=250, height=200)
        # Get/Set USERNAME & DESKTOP DIRECTORIES
        
        
        self.create_gui(the_root = self.root)
        ####################################
        # INSTANTIATE/SETUP MAIN VARIABLES #
        # [2020-04-07]\\
        """
        self.in_directory = in_directory
        self.out_directory = out_directory
        self.ignore_list = ignore_list
        self.check_start = check_start
        self.check_end = check_end
        """
        # <<< CALL MAIN FUNCTION >>>
        #self.main(self.in_directory, self.out_directory, self.ignore_list,
        #          self.check_start, self.check_end)
        """
        in_directory, out_directory, ignore_list, check_start, check_end
        """
    # }
    
    def create_gui(self, the_root): # {
        # TRY THE FOLLOWING
        try: # {
            self.create_ttk_styles(the_root=the_root)
            self.create_main_frame(the_root=the_root)
        # }
        except: # {
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
        # }
    # }
    
    def create_ttk_styles(self, the_root): # {
        # TRY THE FOLLOWING
        try: # {
            self.style = ThemedStyle(the_root)
            # STYLE THEME
            self.style.set_theme("arc") # clearlooks, arc
        # }
        except: # {
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
        # }
    # }
    
    def create_main_frame(self, the_root): # {
        # TRY THE FOLLOWING
        try: # {
            self.mainframe = ttk.Frame(the_root)
            self.mainframe.pack(anchor=tk.CENTER, fill=tk.BOTH, expand=True)
            
            # TK VARIABLES TO HOLD TEXT INPUT
            self.start_date = tk.StringVar(master=the_root, value=str(pd.Timestamp.now())[:10])
            self.end_date = tk.StringVar(master=the_root, value=str(pd.Timestamp.now())[:10])
            self.label_text = tk.StringVar(master=the_root, value=str("Avg Turn Around Time:"))
            
            """
            # START/END DATE ENTRY/LABELS
            ttk.Label(master=self.mainframe, text="Start-Date:\t"
                      ).pack(anchor=tk.NW, fill=tk.BOTH, expand=True)
            ttk.Entry(master=self.mainframe, textvariable=self.start_date
                      ).pack(anchor=tk.NE, fill=tk.BOTH, expand=True)
            ttk.Label(master=self.mainframe, text="End-Date:\t"
                      ).pack(anchor=tk.SW, fill=tk.BOTH, expand=True)
            ttk.Entry(master=self.mainframe, textvariable=self.end_date
                      ).pack(anchor=tk.SE, fill=tk.BOTH, expand=True)
            """
            
            # IMPORT [PRODUCT_NO] LIST
            self.run_button = ttk.Button(master=self.mainframe, text="Pull (Avg. Turn Around Time)",
                                         command=self.determine_range)
            self.run_button.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
            
            # ENTRY BOX THAT WILL DISPLAY OUTPUT (avg turn around time)
            self.avg_turn_around_display = ttk.Entry(master=the_root, textvariable=self.label_text,
                                                     state=tk.DISABLED
                                                     )
            self.avg_turn_around_display.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        # }
        except: # {
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
        # }
    # }
    
    def determine_range(self): # {
        try: # {
            print("<< DETERMINE RANGE >>\n")
            # CALL FUNCTION/METHOD TO CREATE TABLE
            self.pull_from_sqlite_db("D:/_Quotes_Tracker/data/quotes_tracker.db")
            
        # }
        except: # {
            pass
        # }
    # }
    
    """
    DOES NOT RETURN DATAFRAME, BUT CREATES CLASS DF INSIDE
    """
    def pull_from_sqlite_db(self, the_sqlite_path): # {
        # TRY THE FOLLOWING
        try: # {
            print("<< pulling from SQLite db>>\n")
            # CREATE CONNECTIOn
            conn = sqlite3.connect(Path(the_sqlite_path))
            query = "SELECT * FROM quotes;"
            
            self.df_metrics = pd.read_sql_query(sql=query, con=conn,
                                                index_col=None, 
                                                parse_dates=['open_time', 'close_time']
                                                )
            print(self.df_metrics.info())
            # JUST TRACKING NUMBER ROW
            print(self.df_metrics['tracking_number'])
            # CREATE EMPTY LIST TO HOLD DATA
            datetimes = []
            turn_around = self.df_metrics["turn_around"]
            # CONVERT from STR to DATETIME
            # (going thru list and removing all "None")
            for entry in turn_around: # {
                if str(entry) == "None": # {
                    #print("NONE!")
                    pass
                # }
                else: # {
                    #print("DONE")
                    # append to list
                    datetimes.append(entry)
                # }
            # }
            print(len(datetimes))
            turn_around = pd.to_timedelta(datetimes)
            # create variable for 
            avg_turn_around_time = turn_around.mean()
            # FILL IN ENTRY BOX WITH THE ABOVE VALUE
            self.label_text.set("Avg Turn Around Time:\t" + str(avg_turn_around_time))
            """
            messagebox.showinfo(title="avg turn around time",
                                message="THOSE DATES:\n" + str(avg_turn_around_time))
            """
        # }
        except: # {
            pass
        # }
    # }
    
    """
    << MAIN FUNCTION LOGIC >>
    """
    def run(self): # {
        # TRY THE FOLLOWING
        try: # {
            pass
        # }
        except: # {
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
        # }
        # TRY THE FOLLOWING
        try: # {
            pass
        # }
        except: # {
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
        # }
    # }
    
# }

def main(): # {
    # TRY THE FOLLOWING
    try: # {
        # SETUP LOGGER
        logger = Logger(logging_output_dir="C:/Temp/").logger
        window = tk.Tk()
        application = Agilent_CC_Creator(root=window, the_logger=logger)
        window.config()
        window.mainloop()
    # }
    except: # {
        errorMessage = str(sys.exc_info()[0]) + "\n"
        errorMessage = errorMessage + str(sys.exc_info()[1]) + "\n\t\t"
        errorMessage = errorMessage + str(sys.exc_info()[2]) + "\n"
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        typeE = str("TYPE : " + str(exc_type))
        fileE = str("FILE : " + str(fname))
        lineE = str("LINE : " + str(exc_tb.tb_lineno))
        messageE = str("MESG : " + "\n\n" + str(errorMessage) + "\n")
        print("\n" + typeE + 
              "\n" + fileE + 
              "\n" + lineE + 
              "\n" + messageE)
        messagebox.showerror(title="ERROR!",
                             message=typeE +
                             "\n" + fileE +
                             "\n" + lineE +
                             "\n" + messageE)
    # }
# }

if __name__ == "__main__": # {
    # SETUP LOGGER
    # [2020-04-07]\\setup_logger()
    main()
# }

