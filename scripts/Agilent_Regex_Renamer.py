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
    
- revised on 04/07/2020

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
from ttkthemes import ThemedStyle
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox, filedialog, commondialog

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

class Agilent_Regex_Renamer(): # {
    
    user_name = str(os.getlogin()) # get username
    outbound_dir = "C:/data/outbound/" + str(pd.Timestamp.now())[:10]
    desktop_dir = "OneDrive - Agilent Technologies/Desktop"
    
    def __init__(self, root, the_logger): # {
        print("init")
        self.root = root
        self.the_logger = the_logger
        self.root.title("Agilent Regex Renamer")
        self.root.geometry('325x355+300+300')
        self.root.resizable(width=False, height=False)
        # Get/SetUSERNAME & DESKTOP DIRECTORIES
        self.user_name_dir = os.path.join("C:/Users/", self.user_name)
        self.desktop_dir = os.path.join(self.user_name_dir, self.desktop_dir)
        print("USER DIR == " + str(self.user_name_dir))
        print("DESKTOP == " + str(self.desktop_dir))
        # CALL GUI CREATION
        self.create_gui(the_root = self.root)
    # }
        
    def create_gui(self, the_root): # {
        # TRY THE FOLLOWING
        try: # {
            self.create_ttk_styles(the_root=the_root)
        # }
        except: # {
            pass
        # }
        """
        <<< CREATE GUI >>
        """
        #####################
        # TRY THE FOLLOWING #
        #####################
        try: # {
            # TTK BUTTON for Directory Selector
            self.dir_select = ttk.Button(master=the_root, text="Select Directory",
                                         command=self.select_dir)
            self.dir_select.grid(row=0, column=0, padx=10, pady=10, sticky='nesw')
            # TKINTER VAR to hold DIRECTORY SELECTED BY USER
            self.dir_select_var = tk.StringVar(master=the_root)
            # ENTRY BOX TO SHOW DIRECTORY USER SELECTED
            ttk.Entry(master=the_root, textvariable=self.dir_select_var, 
                      state=tk.DISABLED#, width=50
                      ).grid(row=0, column=1, padx=10, pady=10, sticky='nesw')
            # TTK BUTTON for Export Location
            ttk.Button(master=self.root, text="EXPORT Location",
                       command=self.select_export_path
                       ).grid(row=1, column=0, padx=10, pady=10, sticky='nesw')
            # TKINTER VAR to hold EXPORT LOCATION SELECTED BY USER
            self.export_file_path_var = tk.StringVar(master=the_root)
            # ENTRY BOX TO SHOW EXPORT LOCATION
            ttk.Entry(master=the_root, textvariable=self.export_file_path_var,
                      state=tk.DISABLED#, width=25
                      ).grid(row=1, column=1, padx=10, pady=10, sticky='nesw')
            ##################################################################
            # REGEX FRAME 
            ##################################################################
            self.regexframe = ttk.LabelFrame(the_root, text="Regex Settings:")
            self.regexframe.grid(row=2, column=0, columnspan=2, padx=10, pady=10,
                                 sticky='nesw')
            # search regex label
            ttk.Label(master=self.regexframe, text="Search Criteria: "
                      ).grid(row=0, column=0, padx=10, pady=10, sticky='nesw')
            # TKINTER VAR TO HOLD REGEX SEARCH CRITERIA
            self.regex_search_var = tk.StringVar(master=self.regexframe)
            ttk.Entry(master=self.regexframe, textvariable=self.regex_search_var,
                      #width=50
                      ).grid(row=0, column=1, padx=10, pady=10, sticky='nesw')
            # change-to label
            ttk.Label(master=self.regexframe, text="Change-To Criteria: "
                      ).grid(row=1, column=0, padx=10, pady=10, sticky='nesw')
            # TKINTER VAR TO HOLD CHANGE-TO CRITERIA
            self.change_to_var = tk.StringVar(master=self.regexframe)
            ttk.Entry(master=self.regexframe, textvariable=self.change_to_var,
                      #width=50
                      ).grid(row=1, column=1, padx=10, pady=10, sticky='nesw')
            ###########################
            # CHECK-BUTTONS / OPTIONS #
            ###########################
            # TKINTER VAR TO HOLD CHECKBUTTON VALS
            self.check_1 = tk.IntVar(master=the_root)
            ttk.Checkbutton(master=self.regexframe, text="In-Place (overwrite)",
                            variable=self.check_1
                            ).grid(row=2, column=0, padx=10, pady=10, sticky='nesw')
            ttk.Checkbutton(master=self.regexframe, text="Recursive Search",
                            variable=self.check_1
                            ).grid(row=2, column=1, padx=10, pady=10, sticky='nesw')
            ttk.Checkbutton(master=self.regexframe, text="Copy/Move/Save Dups",
                            variable=self.check_1
                            ).grid(row=3, column=0, padx=10, pady=10, sticky='nesw')
            ttk.Checkbutton(master=self.regexframe, text="Dry-Run",
                            variable=self.check_1
                            ).grid(row=3, column=1, padx=10, pady=10, sticky='nesw')
            # TTK BUTTON TO RUN SCAN (only when locations have been selected)
            self.run_scan = ttk.Button(master=the_root, text="Run",
                                       command=self.run, state=tk.DISABLED
                                       )
            # ADD TO GRID (seperate line to avoid NONETYPE error)
            self.run_scan.grid(row=3, column=0, columnspan=2,
                                              padx=10, pady=10, sticky='nesw')
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
            self.style.set_theme("keramik")
        # }
        except: # {
            pass
        # }
    # }
    
    def select_dir(self): # {
        # TRY THE FOLLOWING
        try: # {
            print("SELECTING...")
            self.scan_directory = Path(filedialog.askdirectory(master=self.root,
                                                               title="Select SCAN Directory:"))
            # set the tkinter var to hold text of directory just selected....
            self.dir_select_var.set(str(self.scan_directory))
        # }
        except: # {
            pass
        # }
    # }
    
    def select_export_path(self): # {
        # TRY THE FOLLOWING
        try: # {
            print("Selecting EXPORT Location...")
            self.export_file_path = Path(filedialog.askdirectory(master=self.root,
                                                                 title="Select EXPORT Directory:"))
            # set the tkinter var to hold text of directory just selected...
            self.export_file_path_var.set(str(self.export_file_path))
            # SET RUN BUTTON TO BECOME ACTIVE!
            self.run_scan['state'] = tk.ACTIVE
            # CALL SCAN DIRECTORY () (to begin run)
            # self.scan_directory()
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
    
    def run(self): # {
        print("RUN...")
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

def main(): # {
    # TRY THE FOLLOWING: # {
    try: # {
        # SETUP LOGGER
        logger = Logger(logging_output_dir=".").logger
        window = tk.Tk()
        application = Agilent_Regex_Renamer(root = window, the_logger=logger)
        window.config()
        window.mainloop()
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

if __name__ == "__main__": # {
    # call main function
    print('hey')
    main()
# }
