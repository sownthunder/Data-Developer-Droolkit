# -*- coding: utf-8 -*-
"""
Created on Tue Feb  4 16:35:37 2020

Agilent_Directory_Digger_Tool.py

PERFORMS THE FOLLOWING FUNCTIONS:
    - present user with GUI
    - lets user select directory(ies?) (tk.filedialog)
    - lets user select option on said directories
        - scan within files for text
        - count number of files
        - count files by date
        - count files by string
        - zip or move files
    - lets user select output **TYPE** of file
        - csv
        - xlsx
        - txt
        - zip (if move or extraction of files)
    - lets user select output *LOCATION* of file (tk.filedialog)

@author: derbates
"""

# IMPORT THE GOODS
import os, sys, time
from time import sleep
from datetime import datetime
from pathlib import Path
import logging
import pandas as pd
import numpy as np
from pandas import Series, DataFrame
import tkinter as tk
import tkinter.ttk as ttk

class Logger(): # {
    
    def __init__(self, logging_output_dir): # {
        self.logging_output_dir = logging_output_dir
        # Initiating the Logger object
        self.logger = logging.getLogger(__name__)
        
         # Set the level of the logger (THIS IS SUPER USEFUL since it enables)
        # Explanation regarding the logger levels can be found here:
        # https://docs.python.org/3/howto/logging.html
        self.logger.setLevel(logging.DEBUG)
        
        # Create the logs.log file
        log_file_name = str(pd.Timestamp.now())[:10] + "-ph-viewer-stats"
        log_file_path = os.path.join(logging_output_dir, str(log_file_name) + ".log")
        file_handler = logging.FileHandler(log_file_path)
        
        # Create the console handler with a higher log level
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.ERROR)
        
        # Format the logs structure so that every line would include:
        # the time, name level name and log message
        formatter = logging.Formatter('%(asctime)s: %(message)s, FROM=%(funcName)s, LINENO=%(lineno)d, %(name)s - %(levelname)s')
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        # Adding the format handlers
        self.logger.addHandler(console_handler)
        self.logger.addHandler(file_handler)
        
        # and printing the logs to the console as well
        self.logger.addHandler(logging.StreamHandler(sys.stdout))
    # }
# }

class Agilent_Directory_Digger(): # {
    
    def __init__(self, root): # {
        self.root = root
        self.root.title("Agilent Directory Digger")
        self.root.resizable(width=True, height=True)
        # CALL GUI CREATION
        self.create_gui()
    # }
        
    def create_gui(self): # {
        ttk.Button(master=self.root, text="button").grid(row=0, column=0, padx=10, pady=10, sticky='nesw')
        
    # }
    
    def pull_creation_timestamp(self, a_file_path): # {
        # TRY THE FOLLOWING:
        try: #{
            # FORCE PATH VARIABLE
            the_path = Path(a_file_path)
            # GET MODIFIED TIME
            mtime = os.path.getmtime(the_path)
            # GET CREATE TIME
            ctime = os.path.getctime(the_path)
            # CREATE DATE VAR
            # IF CREATE TIME IS OLDER...
            if ctime < mtime:  # {
                # FORMAT DATE VAR as str
                date_time = datetime.fromtimestamp(ctime)
            # }
            # ELSE.... MODIFIED TIME IS OLDER...
            else:  # {
                # FORMAT DATE VAR as str
                date_time = datetime.fromtimestamp(mtime)
            # }
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
        # }
        else:  # {
            logging.info("SUCCESS! VERY NICE!")
            # RETURN THE DATE WE PULLED AS STRING
            return date_time
        #}
        finally:  # {
            logging.info("[pull_creation_timestamp] FIN...")
        #}
    # }
    
    def scan_directory(self, directory_to_scan, ignore_dir_list, file_type_list): # {
        # TRY THE FOLLOWING
        try: # {
            pass
        # }
        except: # {
            pass
        # }
    # }
# }

if __name__ == "__main__": # {
    # SETUP LOGGER
    logger = Logger(logging_output_dir=".").logger
    window = tk.Tk()
    application = Agilent_Directory_Digger(window)
    window.config()
    window.mainloop()
# }
