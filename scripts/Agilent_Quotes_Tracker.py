"""


"""

"""
Created on Mon Dec 9 12:05:28 2019

TO-DO:
(X) - clear entry boxes when new QUOTE is created/submitted
( ) - import/export from and to .xlsx
( ) - reshape/resize table cells/cols depending on user input
( ) - EDITABLE type in OPEN_MODIFY_WINDOW
(X) - drop decimal places on the creation/completion timestamps
(X) - copy cell tab/feature
( ) - create button triggers virtual event hiding first 3 columns
( ) - RECALCULATE NEW "turn_around_time" (via SQLITE3) when copying

EDITS:
12/18/19 - made database accessible via anywhere by file_path to E_DRIVE
         - calls "new_records_validated()" function to fail-check new DB entry
12/26/19 - quotes naming convention to properly create _QUOTES_T_NUMBER_
         - added COLUMNS [initials], [sap_quote_number], and [product_number]
01/03/20 - changed CREATE tab to contain proper tk.StringVar variables (ttk)
01/09/20 - included validation checks for ACCOUNT ID, PF QUOTE #, SAP QUOTE #
01/14/20 - horizontal scroll bar on treeview, fixed STR conversion (CREATE TAB)
01/15/20 - added fixings/ability to change height of OPEN_MODIFY_WINDOW
01/16/20 - changed TRACKING_NUMBER naming convention to drop leading 3 zeros
01/17/20 - corrected decimal place formatting from timestamp strings
01/22/20 - whenever quotes are edited/updated... no long changes TS after sent
01/23/20 - version update check & set (if not most recent, quits out of app)
01/24/20 - almost finished with COPY function (working properly too)
01/28/20 - copy function, version check, and side scrollbar all COMPLETE
01/29/20 - fixed records that could be created with "Select: " as a type
01/29/20 - Began THREADING for REFRESH TABLE every few minutes...
01/31/20 - veritcal scrollbar, control + f to search
02/03/20 - BOUND control + f search to "application-level", SEARCH BAR GUI
02/03/20 - COPY FUNCTION requested change... why?
02/04/20 - fixed CLEAR MESSAGE error where Notes not clearing propely
02/05/20 - implemented **BOTH** copy functions, new and already existing...
02/06/20 - display columns after clicking on headers?
02/07/20 - added in DEV copies to use DUMMY databases
02/10/20 - re-arranged DEV & PROD instantiates... fixed DEV dummy 
02/11/20 - finished CONTROL + F Search Function (excludes tracking #...)
02/12/20 - PUSHED SECOND PROD. COPY
02/14/20 - removed LOGGER class to hopefully fix build issues...
02/14/20 - properly gets "NEW" timestamp when selected during CREATE-COPY
02/14/20 - properly displays table ressults in descending or by TRACK #
02/21/20 - BEGIN putting in "check_quote_completion" after "COPY-RECORD" runs
02/29/20 - header column functionality work-begin (treeview)
03/02/20 - logger re-implemented (FINALIZED!)
03/04/20 - STATUS column added to database backend

LATER:
    - CREATE button to shrink first 3 cols
    - notifications from TISS
    - SAP <--> ProdFlow two-way connection

@author: derbates
"""

# IMPORT THE GOODS
import os, sys, time
from time import sleep
import pathlib, glob
from pathlib import Path
import fnmatch, shutil
import datetime
import tkinter as tk
from threading import Thread
import tkinter.ttk as ttk
from ttkthemes import ThemedStyle
from tkinter import filedialog, messagebox
import sqlite3, logging, random
import pickle
import pyodbc
import pyautogui
import pandas as pd
import numpy as np
from pandas import Series, DataFrame
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from pynput import keyboard

class Logger(): # {
    
    def __init__(self, logging_output_dir): # {
        self.logging_output_dir = logging_output_dir
        #### INITIATING THE LOGGER OBJECT
        self.logger = logging.getLogger(__name__)
        
        # set the level of the logger (THIS IS SUPER USEFUL since it enables)
        # Explanation regarding the logger levels can be found here:
        # https://docs.python.org/3/howto/logging.html
        self.logger.setLevel(logging.DEBUG)
        
        # Create the logs.log file
        user_name = str(os.getlogin()) # get username 
        log_file_name = user_name + "-" + str(pd.Timestamp.now())[:10] + "-quotes-use"
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

class AgilentQuotesTracker():  # {
    
    #################################################
    #### check if DEV or PROD copy
    if fnmatch.fnmatch(str(sys.argv[0]), "*_dev*"): # {
        print(">>>> loading DEV >>>>>")
        #### set DEV values
        db_filename = "e:/_Quotes_Tracker/dev/data/quotes_tracker.db"
        t_count_filename = "e:/_Quotes_Tracker/dev/config/quotes_t_number.pkl"
        # VERSION CONTROL NUMBER
        version_number = "20.03.03"
        ver_file = Path("E:/_Quotes_Tracker/dev/config/ver_no.txt")
    # }
    else: # {
        print(">>>>> loading PROD >>>>>")
        #### set PROD values
        db_filename = "e:/_Quotes_Tracker/data/quotes_tracker.db"
        t_count_filename = "e:/_Quotes_Tracker/config/quotes_t_number.pkl"
        # VERSION CONTROL NUMBER
        version_number = "20.02.14" #01-29
        ver_file = Path("E:/_Quotes_Tracker/config/ver_no.txt")
    # }
    ##################################################
    
    #db_filename = "C:/Temp/E/data/quotes_tracker.db"
    #t_count_filename = "C:/Temp/E/config/quotes_t_number.pkl"
    time1 = ""
    # REGEX STRINGS FOR FILE NAMING CONVENTIONS
    account_id_regex = "????????"
    # [2020-01-09]\\account_id_regex = "[*][*][*][*][*][*][*][*][*]"
    pf_quote_regex = "[0-9][0-9][0-9][0-9][0-9][0-9][-][0-9][0-9][0-9]"
    sap_quote_regex = "[0-9][0-9][0-9][0-9][0-9][0-9][0-9]"
    # BOOL TO HOLD IF copy_tab IS OPEN OR NOT
    # originally set to True... becuase when first initiated...
    # calls function that sets it back to FAlSE (because its not shown)
    copy_tab = True
    

    def __init__(self, root, the_logger):  # {
        self.the_logger = the_logger
        """
        CHECK DEV. OR PROD. COPY HERE
        """
        """
        #################################################
        #### check if DEV or PROD copy
        if fnmatch.fnmatch(str(sys.argv[0]), "*_dev*"): # {
            the_logger.info(">>>> loading DEV >>>>>")
            #### set DEV values
            self.db_filename = "e:/_Quotes_Tracker/dev/data/quotes_tracker.db"
            self.t_count_filename = "e:/_Quotes_Tracker/dev/config/quotes_t_number.pkl"
            # VERSION CONTROL NUMBER
            self.version_number = "20.03.03"
            self.ver_file = Path("E:/_Quotes_Tracker/dev/config/ver_no.txt")
        # }
        else: # {
            the_logger.info(">>>>> loading PROD >>>>>")
            #### set PROD values
            self.db_filename = "e:/_Quotes_Tracker/data/quotes_tracker.db"
            self.t_count_filename = "e:/_Quotes_Tracker/config/quotes_t_number.pkl"
            # VERSION CONTROL NUMBER
            self.version_number = "20.02.14" #01-29
            self.ver_file = Path("E:/_Quotes_Tracker/config/ver_no.txt")
        # }
        ##################################################
        """
        """
        CHECK VERSION NO. HERE
        """
        ver_txt = pd.read_csv(self.ver_file, names=['version'], dtype=np.str)
        the_logger.info(type(ver_txt))
        the_logger.info(ver_txt)
        self.correct_ver = str(ver_txt["version"].iloc[0])
        the_logger.info("CORRECT (current) VERSION NO. == " + str(self.correct_ver))
        the_logger.info("current (actual) VERSION NO. == " + str(self.version_number))
        # CHECK IF RUNNING MOST RECENT VERSION OF APPLICATION
        if str(self.correct_ver) != str(self.version_number): # {
            the_logger.info("FAILLLLLLL! qutting in 5...")
            sleep(5)
            sys.exit(69)
        # }
        # [2020-02-12]\\self.the_logger = the_logger
        self.root = root
        self.root.title("Agilent Customs Quotes Request Log")
        the_logger.info("SCRIPT NAME == " + str(sys.argv[0]))
        self.root.resizable(width=True, height=True)
        """
        # SET WINDOW DIMENSIONS
        self.width_of_window = 800
        self.height_of_window = 400
        # GET SCREEN SIZE(S)
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        # SET SCREEN DIMENSION POSITIONS
        self.x_coordinate = (self.screen_width/2) - (self.width_of_window/2)
        self.y_coordinate = (self.screen_height/2) - (self.height_of_window/2)
        # SET LOCATION OF MAIN WINDOW
        self.root.geometry("%dx%d+%d+%d" % (self.width_of_window, 
                                            self.height_of_window, 
                                            self.x_coordinate,
                                            self.y_coordinate))
        """
        # [2019-12-12]\\self.root.minsize(height=1250)
        # [2020-01-07]\\self.root.minsize(width=1175, height=750)
        # [2020-01-14]\\self.root.minsize(width=1175, height=600)
        self.root.minsize(width=1000, height=400)
        # [2019-12-26]\\self.root.maxsize(width=1500, height=1250)
        # [2019-12-30]\\self.root.maxsize(width=1750, height=1250)
        # [2020-01-07]\\self.root.maxsize(width=2050, height=1050) # was 787
        # [2020-01-10]\\self.root.maxsize(width=1800, height=750)  # was (width=1920, height=1050)
        # CREATE DATAFRAME-DATABASE FROM FILE
        # [2019-12-11]\\self.quotes_db = self.create_database(db_csv=self.db_filename)
        # [2019-12-11]\\print(self.quotes_db)
        # CREATE TEMPORARY DATABASE / CONNECTION
        # [2019-12-11]\\self.temp_db = self.create_connection(db_csv=self.db_filename)
        # [2019-12-11]\\print(self.temp_db)
        self.create_gui(the_root = self.root)

    # }
    ####################################################################################################
    """
    def create_database(self, db_csv):  # {
        # TRY THE FOLLOWING
        try: #{
            # CREATE DATAFRAME FROM database file
            the_df = pd.read_csv(db_csv, dtype=np.str, engine='c')
            logging.info(the_df)
        # }
        except: #{
            errorMessage = str(sys.exc_info()[0]) + "\n"
            errorMessage = errorMessage + str(sys.exc_info()[1]) + "\n"
            errorMessage = errorMessage + str(sys.exc_info()[2]) + "\n"
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            typeE = str("TYPE : " + str(exc_type))
            fileE = str("FILE : " + str(fname))
            lineE = str("LINE : " + str(exc_tb.tb_lineno))
            messageE = str("MESG : " + "\n" + str(errorMessage))
            logging.critical("\n" + typeE +
                             "\n" + fileE +
                             "\n" + lineE +
                             "\n" + messageE)
            messagebox.showerror(title="ERROR!",
                                 message=typeE +
                                         "\n" + fileE +
                                         "\n" + lineE +
                                         "\n" + messageE)
        #}
        else: #{
            logging.info("Operation Completed Successfully...")
            # RETURN THE DATAFRAME
            return the_df
        #}
    # }
    """

    """
    def create_connection(self, db_csv):  # {
        # creates a database connection to a database that resides in the memory
        conn = None
        # TRY THE FOLLOWING
        try: #{
            conn = sqlite3.connect(':memory:')
            logging.info("SQLite version == " + str(sqlite3.version))
        # }
        except: #{
            errorMessage = str(sys.exc_info()[0]) + "\n"
            errorMessage = errorMessage + str(sys.exc_info()[1]) + "\n"
            errorMessage = errorMessage + str(sys.exc_info()[2]) + "\n"
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            typeE = str("TYPE : " + str(exc_type))
            fileE = str("FILE : " + str(fname))
            lineE = str("LINE : " + str(exc_tb.tb_lineno))
            messageE = str("MESG : " + "\n" + str(errorMessage))
            logging.critical("\n" + typeE +
                             "\n" + fileE +
                             "\n" + lineE +
                             "\n" + messageE)
            messagebox.showerror(title="ERROR!",
                                 message=typeE +
                                         "\n" + fileE +
                                         "\n" + lineE +
                                         "\n" + messageE)
        # }
        else: #{
            logging.info("Operation Completed Successfully...")
            # RETURN THE CONNECTION
            return conn
        # }
    # }
    """

    def execute_db_query(self, query, parameters=()):  # {
        # TRY THE FOLLOWING:
        try:  # {
            with sqlite3.connect(self.db_filename) as conn:  # {
                cursor = conn.cursor()
                query_result = cursor.execute(query, parameters)
                conn.commit()
            # }
            # [2019-12-11]\\return query_result
        # }
        except:  # {
            errorMessage = str(sys.exc_info()[0]) + "\n"
            errorMessage = errorMessage + str(sys.exc_info()[1]) + "\n"
            errorMessage = errorMessage + str(sys.exc_info()[2]) + "\n"
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            typeE = str("TYPE : " + str(exc_type))
            fileE = str("FILE : " + str(fname))
            lineE = str("LINE : " + str(exc_tb.tb_lineno))
            messageE = str("MESG : " + "\n" + str(errorMessage))
            self.the_logger.critical("\n" + typeE +
                             "\n" + fileE +
                             "\n" + lineE +
                             "\n" + messageE)
            messagebox.showerror(title="ERROR!",
                                 message=typeE +
                                         "\n" + fileE +
                                         "\n" + lineE +
                                         "\n" + messageE)
        # }
        else:  # {
            self.the_logger.info("Operation Completed Successfully...")
            return query_result

    # }
    
    """
    EXECUTES SQL QUERY AND RETURNS DATAFRAME FILLED WITH RESULTS
    """
    def execute_df_query(self, query, the_conn):  # {
        # TRY THE FOLLOWING
        try:  # {
            df = pd.read_sql_query(sql=str(query),
                                   con=the_conn)
        # }
        except:  # {
            errorMessage = str(sys.exc_info()[0]) + "\n"
            errorMessage += str(sys.exc_info()[1]) + "\n"
            errorMessage += str(sys.exc_info()[2]) + "\n"
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            typeE = str("TYPE : " + str(exc_type))
            fileE = str("FILE : " + str(fname))
            lineE = str("LINE : " + str(exc_tb.tb_lineno))
            messageE = str("MESG : " + "\n" + str(errorMessage))
            self.the_logger.critical("\n" + typeE +
                             "\n" + fileE +
                             "\n" + lineE +
                             "\n" + messageE)
            messagebox.showerror(title="ERROR!",
                                 message=typeE +
                                         "\n" + fileE +
                                         "\n" + lineE +
                                         "\n" + messageE)
        # }
        else:  # {
            self.the_logger.info("Operation Completed Successfully...")
        # }
        
        return df
    # }

    ###############################################################################################
    
    """
    def tick(self):  # {
        # get the current local time from the PC
        self.time2 = time.strftime('%H:%M:%S')
        # if time string has changed, update it
        if self.time2 != self.time1:  # {
            self.time1 = self.time2
            self.clock.config(text=self.time2)
        # }
        # calls itself every 200 milliseconds
        # to update the time display as needed
        # could use > 200 ms, but display gets jerky
        self.clock.after(200, self.tick)

    # }
    """
    
    def refresh_table(self): # {
        # BEGIN INFINITE LOOP
        while 1: # {
            print("hey")
            sleep(2)
        # }
    # }

    def create_gui(self, the_root):  # {
        # TRY THE FOLLOWING
        try:  # {
            # [2019-12-11]\\self.create_menubar()
            self.create_ttk_styles(the_style="blue", the_root=the_root)
            # [2019-12-11]\\self.create_menubar()
            self.create_menubar(the_root=the_root)
            self.create_left_side(the_root=the_root)
            self.create_tab_control(the_root=the_root)
            self.create_tab_containers(the_root=the_root)
            self.fill_tab_containers(the_root=the_root)
            self.create_right_side(the_root=the_root)
            self.create_tree_view(the_root=the_root)
            self.view_records()
            # [2020-03-02]\\self.root.config(menu=self.menubar)
            the_root.config(menu=self.menubar)
        # }
        except:  # {
            errorMessage = str(sys.exc_info()[0]) + "\n"
            errorMessage = errorMessage + str(sys.exc_info()[1]) + "\n"
            errorMessage = errorMessage + str(sys.exc_info()[2]) + "\n"
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            typeE = str("TYPE : " + str(exc_type))
            fileE = str("FILE : " + str(fname))
            lineE = str("LINE : " + str(exc_tb.tb_lineno))
            messageE = str("MESG : " + "\n" + str(errorMessage))
            self.the_logger.critical("\n" + typeE +
                             "\n" + fileE +
                             "\n" + lineE +
                             "\n" + messageE)
            messagebox.showerror(title="ERROR!",
                                 message=typeE +
                                         "\n" + fileE +
                                         "\n" + lineE +
                                         "\n" + messageE)
        # }
        else:  # {
            self.the_logger.info("Operation Completed Successfully...")
        # }

    # }

    def create_menubar(self, the_root):  # {
        self.menubar = tk.Menu(the_root)
        #### MENU-BAR ^^
        self.filemenu = tk.Menu(master=self.menubar,
                                borderwidth=3,
                                # [2020-02-14]\\background="#0C85CE",
                                background="#666699",
                                font=("Calibri", 16),
                                tearoff=0)
        self.filemenu.add_command(label="Import Settings...", command="")
        self.filemenu.add_command(label="Export Settings...", command="")
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Exit", command=the_root.destroy)
        #### FILE SUB-MENU ^^
        self.menubar.add_cascade(foreground="#000000", 
                                 label="File", 
                                 menu=self.filemenu, 
                                 activebackground="#d9d9d9", 
                                 activeforeground="#111111",
                                 # [2020-02-14]\\background="#d9d9d9")
                                 background="#666699")
        self.editmenu = tk.Menu(master=the_root,
                                borderwidth=3,
                                # [2020-02-14]\\background="#9e0ccf",
                                background="#666699",
                                font=("Calibri", 16),
                                tearoff=0)
        self.editmenu.add_command(label="Search", command="")
        self.editmenu.add_separator()
        self.editmenu.add_command(label="Select Regino", command="")
        self.editmenu.add_command(label="Select All", command="")
        #### EDIT SUB-MENU ^^
        self.menubar.add_cascade(label="Edit", menu=self.editmenu)
        self.viewmenu = tk.Menu(master=self.menubar,
                                borderwidth=3,
                                # [2020-02-14]\\background="#ffbf00",
                                background="#666699",
                                font=("Calibri", 16),
                                relief=tk.RIDGE,
                                tearoff=1)
        self.viewmenu.add_command(label="T-pickle (admin)", command=self.open_admin_window)
        # [2020-01-16]\\self.viewmenu.add_separator()
        # [2020-01-16]\\self.viewmenu.add_command(label="Filter Table", command="") # Help index
        self.viewmenu.add_command(label="REFRESH Table", command=self.view_records) # About...
        #### VIEW SUB-MENU ^^
        self.menubar.add_cascade(label="View", menu=self.viewmenu)
        self.helpmenu = tk.Menu(master=the_root,
                                 borderwidth=3,
                                 # [2020-02-14]\\background='#3d4043',
                                 background="#666699",
                                 font=("Calibri", 16),
                                 relief=tk.RIDGE,
                                 tearoff=0)
        self.helpmenu.add_command(label="Help", command="")  # Login/edit
        self.helpmenu.add_command(label="About", command=self.view_records)  # REFRESH TABLE
        self.helpmenu.add_command(label="Check for Updates...", command="")
        self.menubar.add_cascade(label="Help", menu=self.helpmenu)  # TABLE TOOLS
        #### HELP SUB-MENU ^^
    # }

    def create_ttk_styles(self, the_style, the_root):  # {
        # TRY THE FOLLOWING:
        try:  # {
            themes = sorted(ttk.Style().theme_names())
            for t in themes:  # {
                self.the_logger.info(str(t))
            # }
            # CONFIGURE THE STYLE
            # [2019-12-31]\\self.style = ttk.Style()
            self.style = ThemedStyle(the_root)
            # # STYLE THEME
            self.style.set_theme("blue") # radiance, black, scidblue, kroc, keramik, equilux
            # Modify the font of the body
            self.style.configure("mystyle.Treeview", highlightthickness=4, bd=4, font=('Calibri', 11))
            # Modify the font of the headings
            self.style.configure("mystyle.Treeview.Heading", font=('Calibri', 13, 'bold'))
            """
            # REMOVE THE BORDERS
            self.style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})])
            # BUTTON STYLE
            self.button_style = ttk.Style().configure("TButton", padding=4,
                                                      relief="groove", background="#96A853",
                                                      font=('Calibri', 8, 'bold'), foreground="#600080")
            """
        # }
        except:  # {
            errorMessage = str(sys.exc_info()[0]) + "\n"
            errorMessage = errorMessage + str(sys.exc_info()[1]) + "\n"
            errorMessage = errorMessage + str(sys.exc_info()[2]) + "\n"
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            typeE = str("TYPE : " + str(exc_type))
            fileE = str("FILE : " + str(fname))
            lineE = str("LINE : " + str(exc_tb.tb_lineno))
            messageE = str("MESG : " + "\n" + str(errorMessage))
            self.the_logger.error("\n" + typeE +
                          "\n" + fileE +
                          "\n" + lineE +
                          "\n" + messageE)
            messagebox.showerror(title="ERROR!",
                                 message=typeE +
                                         "\n" + fileE +
                                         "\n" + lineE +
                                         "\n" + messageE)
        # }
        else:  # {
            self.the_logger.info("Operation Completed Successfully...")
        # }

    # }

    def create_left_icon(self):  # {
        photo = tk.PhotoImage(file='icons/agilent_logo-Copy1.png')
        label = tk.Label(image=photo, bg="#0c85ce")
        label.image = photo
        label.grid(row=0, column=0, columnspan=2, sticky='SW')

    # }

    def create_left_side(self, the_root):  # {
        # CREATE FRAME CONTAINER
        self.leftframe = tk.Frame(the_root)
        # [2019-12-12]\\self.leftframe.pack(side=tk.LEFT, fill=tk.BOTH, expand=True) # fill=tk.Both
        # [2019-12-12]\\self.leftframe.pack(side=tk.LEFT, fill=tk.Y, expand=True)
        # [2019-12-12]\\self.leftframe.pack(side=tk.LEFT, fill=tk.BOTH, expand=False)
        # [2019-12-26]\\self.leftframe.pack(side=tk.LEFT, fill=tk.X, expand=False)
        self.leftframe.pack(side=tk.LEFT, fill=tk.Y, expand=False)
        # BIND FUNCTIONS TO FRAME
        # [2020-01-14\\self.leftframe.bind('<Leave>', self.clear_message_area)
        # [2020-02-12]\\self.leftframe.bind('<Enter>', self.clear_message_area)
        # [2020-02-12]\\self.leftframe.bind('<FocusOut>', self.clear_message_area)
        # [2020-02-12]\\self.leftframe.bind('<FocusIn>', self.view_records)
        # [2020-02-13]\\self.leftframe.bind('<FocusIn>', self.view_records)  ^^ CHANGE PARAMS to "event=None"
        # [2020-02-13]\\self.leftframe.bind('<Return>', self.turn_red) # self.view_records)

    # }

    def create_tab_control(self, the_root):  # {
        # TRY THE FOLLOWING
        try:  # {
            # CREATE MESSAGE AREA
            self.message = ttk.Label(master=self.leftframe, text='',
                                     font=("Times New Roman", 12, 'italic'), foreground='red')
            # self.message.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
            self.message.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
            self.message.bind("<Enter>", self.clear_message_area)
            # [2020-02-14]\\self.message.bind("<Enter>", self.copy_create_check)

            #### NOTEBOOK WIDGET
            self.tab_control = ttk.Notebook(self.leftframe)
            # ENABLE KEYBOARD TRAVERSAL
            # [2020-02-13]\\self.tab_control.enable_traversal()
            self.tab_control.enable_traversal()

            # TAB-1 // CREATE
            self.tab1 = ttk.Frame(master=self.tab_control)
            self.tab_control.add(self.tab1, text='CREATE')
            self.tab_control.pack(expand=2, fill=tk.BOTH)
            # BIND ENTER BUTTON ?
            self.tab1.bind('<Return>', self.turn_red)
            
            # [2020-2-05]\\
            # TAB-2 // COPY TOOLS
            self.tab2 = ttk.Frame(master=self.tab_control)
            self.tab_control.add(self.tab2, text='COPY')
            self.tab_control.pack(expand=2, fill=tk.BOTH)
            
            # BIND TAB EVENTS
            self.tab_control.bind("<<NotebookTabChanged>>", self.copy_create_check)
            # [2020-02-13]\\self.tab_control.bind("<Return>", self.turn_red)
            
            # [2020-01-15]
            """
            # TAB-3 // IMPORT TOOLS
            self.tab3 = ttk.Frame(master=self.tab_control)
            self.tab_control.add(self.tab3, text='IMPORT')
            # [2019-12-26]\\self.tab_control.pack(expand=2, fill=tk.BOTH)
            self.tab_control.pack(expand=2, fill=tk.BOTH)

            # TAB-4 // EXPORT TOOLS
            self.tab4 = ttk.Frame(master=self.tab_control)
            self.tab_control.add(self.tab4, text='EXPORT')
            self.tab_control.pack(expand=2, fill=tk.BOTH)
            """
            
            # [2020-01-03]
            """
            # UNIVERSAL BUTTON?
            self.uni_button = ttk.Button(master=self.leftframe, text="CREATE", state='disabled')
            self.uni_button.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
            """
            
        # }
        except:  # {
            errorMessage = str(sys.exc_info()[0]) + "\n"
            errorMessage = errorMessage + str(sys.exc_info()[1]) + "\n"
            errorMessage = errorMessage + str(sys.exc_info()[2]) + "\n"
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            typeE = str("TYPE : " + str(exc_type))
            fileE = str("FILE : " + str(fname))
            lineE = str("LINE : " + str(exc_tb.tb_lineno))
            messageE = str("MESG : " + "\n" + str(errorMessage))
            self.the_logger.error("\n" + typeE +
                          "\n" + fileE +
                          "\n" + lineE +
                          "\n" + messageE)
            messagebox.showerror(title="ERROR!",
                                 message=typeE +
                                         "\n" + fileE +
                                         "\n" + lineE +
                                         "\n" + messageE)
        # }
        else:  # {
            self.the_logger.info("Operation Completed Successfully...")
        # }

    # }

    def create_tab_containers(self, the_root):  # {
        # TRY THE FOLLOWING:
        try:  # {
            #### INSTANTIATE CREATE Tab
            # [2020-01-03]\\self.lblframe_create = ttk.LabelFrame(master=self.tab1, text="Enter the following information:")
            self.lblframe_create = ttk.Frame(master=self.tab1)
            # [2019-12-30]\\self.lblframe_create.pack(anchor=tk.CENTER, fill=tk.BOTH, expand=True)
            self.lblframe_create.pack(anchor=tk.CENTER, fill=tk.BOTH, expand=False)
            # [2020-02-13]\\self.lblframe_create.bind('<Return>', self.turn_red)
            
            #### INSTANTIATE COPY Tab
            self.lblframe_copy = ttk.Frame(master=self.tab2)
            self.lblframe_copy.pack(anchor=tk.CENTER, fill=tk.BOTH, expand=False)
            
            # Create the IMPORT Tab Container
            # [2020-02-05]\\self.lblframe_import = ttk.Frame(master=self.tab3)
            # [2020-02-05]\\self.lblframe_import.pack(anchor=tk.CENTER, fill=tk.BOTH, expand=False)
            
            # Create the EXPORT Tab Container
            # [2020-02-05]\\self.lblframe_export = ttk.Frame(master=self.tab4)
            # [2020-02-05]\\self.lblframe_export.pack(anchor=tk.CENTER, fill=tk.BOTH, expand=False)

            # Create the IMPORT Tab Container
            # [2020-01-03]\\self.lblframe_import = ttk.LabelFrame(master=self.tab2, text="ABOUT the Agilent Quotes Tracker:")
            # [2020-01-06]\\self.lblframe_import = ttk.Frame(master=self.tab2)
            # [2020-01-06]\\self.lblframe_import.pack(anchor=tk.CENTER, fill=tk.BOTH, expand=False)

            # Create the EXPORT Tab Container
            # [2020-01-03]\\self.lblframe_export = ttk.LabelFrame(master=self.tab3, text="Help Section:")
            # [2020-01-06]\\self.lblframe_export = ttk.Frame(master=self.tab3)
            # [2020-01-06]\\self.lblframe_export.pack(anchor=tk.CENTER, fill=tk.BOTH, expand=False)
            
            # Create the HELP Tab Container
            # [2019-12-13]\\self.lblframe_help = ttk.LabelFrame(master=self.tab4, text="EXPORT One or Multiple Quotes:")
            # [2019-12-13]\\self.lblframe_help.pack(anchor=tk.CENTER, fill=tk.BOTH, expand=True)

            # Create the UPDATE Tab Container
            # [2019-12-12]\\self.lblframe_update = ttk.LabelFrame(master=self.tab3, text="UPDATE")
            # [2019-12-12]\\self.lblframe_update.pack(anchor=tk.CENTER, fill=tk.BOTH, expand=False)

            # Create the DELETE Tab Container
            # [2019-12-12]\\self.lblframe_delete = ttk.LabelFrame(master=self.tab4, text="DELETE")

            # [2019-12-12]\\self.lblframe_delete.pack(anchor=tk.CENTER, fill=tk.BOTH, expand=False)
        # }
        except:  # {
            errorMessage = str(sys.exc_info()[0]) + "\n"
            errorMessage = errorMessage + str(sys.exc_info()[1]) + "\n"
            errorMessage = errorMessage + str(sys.exc_info()[2]) + "\n"
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            typeE = str("TYPE : " + str(exc_type))
            fileE = str("FILE : " + str(fname))
            lineE = str("LINE : " + str(exc_tb.tb_lineno))
            messageE = str("MESG : " + "\n" + str(errorMessage))
            self.the_logger.critical("\n" + typeE +
                             "\n" + fileE +
                             "\n" + lineE +
                             "\n" + messageE)
        # }
        else:  # {
            self.the_logger.info("Operation completed Successfully...")
        # }

    # }

    def fill_tab_containers(self, the_root):  # {
        # ()()()()()()()()()()()()()()()()()()()()()()()()()()(()()()()())
        #### () CREATE TAB CONTENTS ()
        # ()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()() #
        # TRY THE FOLLOWING
        try:  # {
            #### COMPANY NAME Input
            ttk.Label(master=self.lblframe_create,
                      text='Company Name: ').grid(row=0, column=0, padx=10, pady=10, sticky='nw')
            self.company_name = tk.StringVar(master=self.lblframe_create)
            ttk.Entry(master=self.lblframe_create,
                                          textvariable=self.company_name,
                                          width=20
                                          ).grid(row=0, column=1, padx=10, pady=10, sticky='w')
            
            #### CONTACT PERSON (NAME)
            ttk.Label(master=self.lblframe_create,
                      text='Contact Person: ').grid(row=2, column=0, padx=10, pady=10, sticky='nw')
            self.name = tk.StringVar(master=the_root)
            # [2020-01-07]\\self.name.set(value="Hot-Stuff")
            ttk.Entry(master=self.lblframe_create,
                                       textvariable=self.name,
                                       state='active',
                                       width=20
                                       ).grid(row=2, column=1, padx=10, pady=10, sticky='w')
            #### EMAIL ADDRESS #
            ttk.Label(master=self.lblframe_create,
                      text='Email Address: ').grid(row=3, column=0, padx=10, pady=10, sticky='nw')
            self.email = tk.StringVar(master=the_root)
            ttk.Entry(master=self.lblframe_create,
                                      textvariable=self.email,
                                      state='active',
                                      width=20
                                      ).grid(row=3, column=1, padx=10, pady=10, stick='w') 
            #### ACCOUNT ID #
            ttk.Label(master=self.lblframe_create,
                      text='Account ID: ').grid(row=4, column=0, padx=10, pady=10, sticky='nw')
            self.account_id = tk.StringVar(master=the_root)
            ttk.Entry(master=self.lblframe_create,
                                   textvariable=self.account_id,
                                   state='active',
                                   width=20
                                   ).grid(row=4, column=1, padx=10, pady=10, sticky='w')
            
            ##################################################################################
            
            self.sep_1 = ttk.Separator(master=self.lblframe_create, orient=tk.HORIZONTAL)
            self.sep_1.place(x=10, y=120, width=275, height=1)  # WAS y=160
            
            ####################################################################################
            
            # [2020-01-07]
            """
            # PROFLOW QUOTE NUMBER #
            ttk.Label(master=self.lblframe_create,
                      text='PF Quote #: ').grid(row=6, column=0, padx=10, pady=10, sticky='w')
            self.pf_quote_num = tk.StringVar(master=self.lblframe_create)
            ttk.Entry(master=self.lblframe_create,
                                      textvariable=self.pf_quote_num,
                                      state='active', 
                                      width=20
                                      ).grid(row=6, column=1, padx=10, pady=10, sticky='w')
            
            # SAP QUOTE NUMBER
            ttk.Label(master=self.lblframe_create,
                      text='SAP Quote #: ').grid(row=7, column=0, padx=10, pady=10, sticky='w')
            self.sap_quote_num = tk.StringVar(master=self.lblframe_create)
            ttk.Entry(master=self.lblframe_create,
                                      textvariable=self.sap_quote_num,
                                      state='active',
                                      width=20
                                      ).grid(row=7, column=1, padx=10, pady=10, sticky='w')
            
            # PRODUCT NUMBER
            ttk.Label(master=self.lblframe_create,
                      text='Product #: ').grid(row=8, column=0, padx=10, pady=10, sticky='w')
            self.product_number = tk.StringVar(master=self.lblframe_create)
            ttk.Entry(master=self.lblframe_create,
                                       textvariable=self.product_number,
                                       state='active',
                                       width=20,
                                       ).grid(row=8, column=1, padx=10, pady=10, sticky='w')
            """
            
            #### INITIALS #
            ttk.Label(master=self.lblframe_create,
                      text='Initials: ').grid(row=5, column=0, padx=10, pady=10, sticky='nw')
            self.initials = tk.StringVar(master=the_root)
            ttk.Entry(master=self.lblframe_create,
                                 textvariable=self.initials,
                                 state='active',
                                 width=20,
                                 ).grid(row=5, column=1, padx=10, pady=10, sticky='w')
            
            ########
            ##### TYPE #
            ttk.Label(master=self.lblframe_create,
                      text='Type: '
                      ).grid(row=6, column=0, padx=10, pady=10, sticky='nw')
            
            self.type_var = tk.StringVar(master=the_root, value="Select: ") #, value="email")
            """
            ttk.Radiobutton(master=self.lblframe_create,
                            variable=self.type_var,
                            value="web", text="web",
                            state=tk.ACTIVE,
                            width=20
                            ).grid(row=6, column=1, columnspan=2, sticky='w', padx=10, pady=10)
            ttk.Radiobutton(master=self.lblframe_create,
                            variable=self.type_var,
                            value="email", text="email",
                            state=tk.ACTIVE,
                            width=20
                            ).grid(row=6, column=1, columsnpan=3, sticky='e', padx=20, pady=10)
            
            """
            ttk.Combobox(self.lblframe_create,
                         width=18,
                         textvariable=self.type_var,
                         values=["web", "email"],
                         ).grid(row=6, column=1, padx=10, pady=10, sticky='w')
            """
            ttk.OptionMenu(self.lblframe_create, 
                           self.type_var, 
                           "Select: ", 
                           "web", 
                           "email", 
                           direction="right"
                           ).grid(row=6, column=1, padx=10, pady=10, sticky='w')
            """
            #########################################################################
            
            self.sep_2 = ttk.Separator(master=self.lblframe_create, orient=tk.HORIZONTAL)
            self.sep_2.place(x=10, y=250, width=275, height=1)  # WAS y=330
            
            ##########################################################################
            
            #### NOTES #
            ttk.Label(master=self.lblframe_create,
                      text='Notes: ').grid(row=7, column=0, padx=10, pady=10, sticky='nw')
            # [2020-01-03]\\self.notes = tk.StringVar(master=self.lblframe_create)
            self.notes = tk.StringVar(master=the_root, value="None")
            """
            self.notes = tk.Text(master=self.lblframe_create, 
                                 height=6,
                                 width=30,
                                 font=("Calibri", 12)
                                 ).grid(row=8, column=0, columnspan=2, padx=10, pady=10, sticky='w')
            """
            ttk.Entry(master=self.lblframe_create,
                                   width=20,
                                   textvariable=self.notes
                                   ).grid(row=7, column=1, padx=10, pady=10, sticky='w')
            """
            self.notes = tk.Text(master=self.lblframe_create, 
                            height=10,
                            width=20,
                            # wrap = 
                            # yscrollcommand = 
                            ).grid(row=7, column=0, columnspan=3, padx=10, pady=10, sticky='e') # WAS :e
            # INSERT blank STR into NOTES
            self.notes.insert(index=0, chars="")
            """
            
            
            # BIND ACTION TO CREATE BUTTON
            # [2020-02-05]\\create_button.bind("<Return>", self.add_new_record)
            # [2020-01-23]\\self.create_button.bind("<ButtonRelease-1>", self.on_create_button)
            # [2020-01-29]\\self.create_button.bind("<FocusIn>", self.turn_red)
            # [2020-01-29]\\self.create_button.bind("<Return>", self.turn_red)
            """
            # CHECK BUTTON (int var)
            self.copy_check_int = tk.IntVar(master=self.root)
            # CHECK BUTTON (for copy display/hide)
            self.create_copy_check = ttk.Checkbutton(master=self.lblframe_create,
                                                     text="COP(IES) ?",
                                                     command=self.copy_create_check,
                                                     variable=self.copy_check_int
                                                     ).grid(row=8, column=0, padx=10, pady=10, sticky='nw')
            # << CREATE-COPY >> BUTTON
            self.create_copy_button = ttk.Button(master=self.lblframe_create,
                                                 text="Create-COPY",
                                                 command="",
                                                 state=tk.DISABLED
                                                 ).grid(row=9, column=0, padx=10, pady=10, sticky='n')
            """
            
            #########################################################################
            
            self.sep_3 = ttk.Separator(master=self.lblframe_create, orient=tk.HORIZONTAL)
            self.sep_3.place(x=10, y=340, width=275, height=1)  # WAS y=330
            
            ##########################################################################
            
            ttk.Label(master=self.lblframe_create,
                      text="Number to Create: ").grid(row=8, column=0, padx=10, pady=10, sticky='nw')
            #### SPINBOX (copies while create) 
            ### tk.IntVar (self.num_of_copies)
            self.num_of_copies = tk.IntVar(master=self.lblframe_create, value="1")
            # SPINBOX SPINBOX
            self.copy_spinbox = ttk.Spinbox(master=self.lblframe_create, 
                               from_=1, 
                               to=10, 
                               width=19,
                               textvariable=self.num_of_copies,
                               state=tk.ACTIVE
                               ).grid(row=8, column=1, padx=10, pady=10, sticky='w')
            # [2020-02-06]\\self.copy_spinbox.bind("<<Increment>>", self.turn_red)
            #### CREATE BUTTON #
            self.create_button = ttk.Button(master=self.lblframe_create, 
                                       text="CREATE",
                                       # IF COPY AMOUNT IS SET TO ZERO THEN CALL NORMAL CREATE... ELSE CALL "check" which then calls CREATE loops
                                       command=self.add_new_record, # [2020-02-06]\\if int(self.num_of_copies.get()) <= 0 else self.copy_create_check,
                                       width=20
                                       ).grid(row=9, column=0, columnspan=2, padx=10, pady=10, sticky='nw')
            # [2020-02-12]\\self.create_button.bind("<Enter>", self.view_records)
            #### CLEAR BUTTON #
            self.clear_button = ttk.Button(master=self.lblframe_create,
                                      text="CLEAR",
                                      command=self.clear_create_tab,
                                      width=10
                                      ).grid(row=9, column=0, columnspan=2, padx=10, pady=10, sticky='ne')
            """
            # <<< CLOCK (timestamp_test) >>>
            self.clock = ttk.Label(master=self.lblframe_create, font=("Calibri", 20, 'bold'),
                                   background='#2b303b', foreground="#bbc0c9")
            self.clock.grid(row=12, column=1, padx=5, pady=5, stick='w')
            """
            """
            # xXxXxXxXXxXXxXXxX
            # SUBMIT "CREATE" BUTTON
            ttk.Button(master=self.lblframe_create,
                       text="CREATE", width=24,
                       command=self.add_new_record).grid(row=15, column=0, columnspan=2, padx=5, pady=5, sticky='nesw')
            # CLEAR BUTTON
            ttk.Button(master=self.lblframe_create,
                       text="CLEAR", width=24,
                       command=self.add_new_record).grid(row=15, column=0, columnspan=2, padx=10, pady=10, sticky='n')
            """
            # TRACKING_NUMBER (tracking#) #
            # NAME #
            # EMAIL #
            # TYPE #
            # SENT #
            # OPEN_TIME (timestamp) #
            # CLOSE_TIME (end_timestamp) #
            # TURN_AROUND (overall timestamp) #
            # NOTES #
            # INITIALS (agilent worker) #
            # ACCOUNT ID #
            # PRODUCT NUMBER #
            # PRODFLOW QUOTE NUMBER #
            # SAP QUOTE NUMBER #
            # COMPANY NAME #
        # }
        except:  # {
            errorMessage = str(sys.exc_info()[0]) + "\n"
            errorMessage = errorMessage + str(sys.exc_info()[1]) + "\n"
            errorMessage = errorMessage + str(sys.exc_info()[2]) + "\n"
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            typeE = str("TYPE : " + str(exc_type))
            fileE = str("FILE : " + str(fname))
            lineE = str("LINE : " + str(exc_tb.tb_lineno))
            messageE = str("MESG : " + "\n" + str(errorMessage))
            self.the_logger.error("\n" + typeE +
                          "\n" + fileE +
                          "\n" + lineE +
                          "\n" + messageE)
            messagebox.showerror(title="ERROR!",
                                 message=typeE +
                                         "\n" + fileE +
                                         "\n" + lineE +
                                         "\n" + messageE)
        # }
        else:  # {
            self.the_logger.info("[CREATE-TAB] Operation Completed Successfully...")
        # }
        # ()()()()()()()()()()()()()()()()()()()()()()()()()()(()()()()())
        #### () COPY TAB CONTENTS () 
        # ()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()() #
        # TRY THE FOLLOWING
        try: # {
            # SELECTED TRACKING # (label)
            ttk.Label(master=self.lblframe_copy, 
                      text="Selected Tracking #: "
                      ).grid(row=0, column=0, padx=10, pady=10, sticky='nw')
            # SELECTED TRACKING # (stringVar)
            self.selected_tracking_num = tk.StringVar(master=self.lblframe_copy, value="None")
            # SELECTED TRACKING # (entry)
            ttk.Entry(master=self.lblframe_copy,
                      textvariable=self.selected_tracking_num,
                      state=tk.ACTIVE,
                      width=20
                      ).grid(row=0, column=1, padx=10, pady=10, sticky='w')
            # SELECTED TIME RECEIVED (label)
            ttk.Label(master=self.lblframe_copy,
                      text="Selected Timestamp: "
                      ).grid(row=1, column=0, padx=10, pady=10, sticky='nw')
            # SELECTED TIME RECEIVED (stringVar)
            self.selected_time_rec = tk.StringVar(master=self.lblframe_copy, value="None")
            # SELECTED TIME RECEIVED (entry)
            ttk.Entry(master=self.lblframe_copy,
                      textvariable=self.selected_time_rec,
                      state=tk.DISABLED,
                      width=20
                      ).grid(row=1, column=1, padx=10, pady=10, sticky='w')
            # SELECTED CELL 3 (INITIALS)
            # SELECTED CELL 4 (TYPE)
            # SELECTED CELL 5 (COMPANY)
            # SELECTED CELL 6 (CONTACT PERSON)
            # RADIOBOX (for current or "copied" timestamp)
            self.select_ts_2copy = tk.IntVar(master=the_root, value=1) # self.lblframe_copy
            ttk.Radiobutton(master=self.lblframe_copy,
                            text='COPY (old) timestamp',
                            value=1, 
                            variable=self.select_ts_2copy,
                            ).grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky='w')
            ttk.Radiobutton(master=self.lblframe_copy,
                            text='CREATE (new) timestamp',
                            value=2,
                            variable=self.select_ts_2copy,
                            # [2020-02-14\\command=self.copy_create_check
                            ).grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky='w')
            #### SPINBOX (new copies)
            ttk.Label(master=self.lblframe_copy,
                      text="Number of Copies: "
                      ).grid(row=4, column=0, padx=10, pady=10, sticky='nw')
            # SPINBOX (int var)
            #### tk.IntVar (self.num_of_new_copies)
            self.num_of_new_copies = tk.IntVar(master=self.lblframe_copy, value="1")
            # SPINBOX SPINBOX
            ttk.Spinbox(master=self.lblframe_copy, 
                               from_=1, 
                               to=10, 
                               width=19,
                               textvariable=self.num_of_new_copies
                               ).grid(row=4, column=1, padx=10, pady=10, sticky='w')
            #### COPY BUTTON
            self.copy_button = ttk.Button(master=self.lblframe_copy,
                                          text='COPY',
                                          command=self.copy_create_record,
                                          width=36
                                          ).grid(row=5, column=0, columnspan=2, rowspan=2, padx=10, pady=10, sticky='n')
        # }
        except: # {
            errorMessage = str(sys.exc_info()[0]) + "\n"
            errorMessage = errorMessage + str(sys.exc_info()[1]) + "\n"
            errorMessage = errorMessage + str(sys.exc_info()[2]) + "\n"
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            typeE = str("TYPE : " + str(exc_type))
            fileE = str("FILE : " + str(fname))
            lineE = str("LINE : " + str(exc_tb.tb_lineno))
            messageE = str("MESG : " + "\n" + str(errorMessage))
            self.the_logger.error("\n" + typeE +
                          "\n" + fileE +
                          "\n" + lineE +
                          "\n" + messageE)
            messagebox.showerror(title="ERROR!",
                                 message=typeE +
                                         "\n" + fileE +
                                         "\n" + lineE +
                                         "\n" + messageE)
        # }
        else: # {
            self.the_logger.info("[COPY-TAB] Operation Completed Successfully...")
        # }
    # }

    def create_right_side(self, the_root):  # {
        # Create a Frame Container
        self.rightframe = ttk.Frame(master=the_root)
        self.rightframe.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        """
        ################
        # PANED WINDOW #
        ################
        """
        # create PanedWindow
        pw = ttk.PanedWindow(master=the_root, orient=tk.HORIZONTAL)
        # pack into the TOP right side and fill whole
        pw.pack(side=tk.TOP, expand=tk.Y, fill=tk.BOTH)
        
        # BIND FUNCTIONS TO FRAME
        # [2020-01-10]\\self.rightframe.bind('<Enter>', self.clear_message_area)
    # }

    def create_tree_view(self, the_root):  # {
        # TRY THE FOLLOWING
        try:  # {
            # CREATE SCROLLBAR?
            self.scrollbar = ttk.Scrollbar(master=self.rightframe, orient = tk.HORIZONTAL)
            self.scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
            self.side_scrollbar = ttk.Scrollbar(master=self.rightframe, orient = tk.VERTICAL)
            self.side_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            
            # TABLE
            self.tree = ttk.Treeview(master=self.rightframe, style="mystyle.Treeview",
                                     height=30, columns=13, selectmode='browse')  # height = 20
            # [2020-02-29]\\
            """
            self.tree["columns"] = (
            "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven", "twelve", "thirteen")
            """
            self.tree['columns'] = (
            "Time Rec.", "Initials", "Type", "Company", 
            "Contact Person", "Email Address", "Account ID", 
            "Product #", "PF Quote #", "SAP Quote #", "Sent", "Time Sent", "Notes")
            self.tree.column('#0', anchor=tk.CENTER, width=90, minwidth=85, stretch=tk.NO)  # TRACKING #
            self.tree.column("Time Rec.", anchor=tk.CENTER, width=135, minwidth=120, stretch=tk.NO)  # TIME REC. // NAME
            self.tree.column("Initials", anchor=tk.CENTER, width=60, minwidth=60, stretch=tk.NO)  # INITIALS // EMAIL
            self.tree.column("Type", anchor=tk.CENTER, width=50, minwidth=50, stretch=tk.NO)  # TYPE
            self.tree.column("Company", anchor=tk.W, width=125, minwidth=120, stretch=tk.NO)  # COMPANY NAME //OPEN TIME
            self.tree.column("Contact Person", anchor=tk.CENTER, width=120, minwidth=100, stretch=tk.NO)  # CONTACT PERSON //SENT , 45, 45
            self.tree.column("Email Address", anchor=tk.W, width=175, minwidth=160, stretch=tk.NO)  #  EMAIL ADDRESS //TURN_AROUND, 100, 90
            self.tree.column("Account ID", anchor=tk.CENTER, width=80, minwidth=80, stretch=tk.NO)  # ACCOUNT ID // NOTES
            self.tree.column("Product #", anchor=tk.CENTER, width=100, minwidth=80, stretch=tk.NO)  # PRODUCT NUMBER //INITIALS
            self.tree.column("PF Quote #", anchor=tk.CENTER, width=85, minwidth=75, stretch=tk.NO)  # PF QUOTE #//  ACCOUNT ID
            self.tree.column("SAP Quote #", anchor=tk.CENTER, width=100, minwidth=75, stretch=tk.NO)  # SAP QUOTE # // PRODFLOW QUOTE #
            self.tree.column("Sent", anchor=tk.CENTER, width=60, minwidth=60, stretch=tk.NO)  # SENT
            self.tree.column("Time Sent", anchor=tk.CENTER, width=135, minwidth=120, stretch=tk.NO)  # TIME_SENT // SAP QUOTE #
            self.tree.column("Notes", anchor=tk.CENTER, width=175, minwidth=50, stretch=tk.YES)  # NOTES // PRICE

            # Definitions of Headings
            # [2019-12-05]\\self.tree.grid(row = 1, column = 0, columnspan = 8, sticky = 'S')
            self.tree.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
            self.tree.heading('#0', text='Tracking #', anchor=tk.CENTER, command=self._de_select_column)  # 'tracking_number' in BACKEND
            self.tree.heading('Time Rec.', text='Time Rec.', anchor=tk.CENTER, command=lambda: self._column_select()) # "Open_time" in BACKEND
            self.tree.heading('Initials', text='Initials', anchor=tk.CENTER, command=self._column_select)
            self.tree.heading('Type', text='Type', anchor=tk.CENTER, command=self._column_select)
            self.tree.heading('Company', text='Company', anchor=tk.CENTER) #, command=self._select_column)  # COMPANY_NAME
            self.tree.heading('Contact Person', text='Contact Person', anchor=tk.CENTER) #, command=self._select_column) # NAME IN BACKEND
            self.tree.heading('Email Address', text='Email Address', anchor=tk.CENTER) #, command=self._select_column)  #
            self.tree.heading('Account ID', text='Account ID', anchor=tk.CENTER) #, command=self._select_column)
            self.tree.heading("Product #", text='Product #', anchor=tk.CENTER) #, command=self._select_column)
            self.tree.heading('PF Quote #', text='PF Quote #', anchor=tk.CENTER) #, command=self._select_column)
            self.tree.heading('SAP Quote #', text='SAP Quote #', anchor=tk.CENTER) #, command=self._select_column)
            self.tree.heading('Sent', text='Sent', anchor=tk.CENTER) #, command=self._select_column)
            self.tree.heading('Time Sent', text='Time Sent', anchor=tk.CENTER) #, command=self._select_column)       # CLOSE TIME IN BACKEND
            self.tree.heading('Notes', text='Notes', anchor=tk.CENTER) #, command=self._select_column)
            # [2020-02-28]\\ self.tree.heading("#1" text="Time").bind("<Button-1>", self._column_sort)
            
            # CONFIG SCROLLBAR (horixontal/xview)
            self.scrollbar.config(command = self.tree.xview)
            self.side_scrollbar.config(command = self.tree.yview)
            
            # CONFIG TREEVIEW
            self.tree.config(xscrollcommand=self.scrollbar.set)
            self.tree.config(yscrollcommand=self.side_scrollbar.set)
            
            
            # BIND CLICK ACTIONS/EVENTS
            self.tree.bind("<<TreeviewSelect>>", self.on_single_click)
            self.tree.bind("<Double-1>", self.on_double_click)
            self.tree.bind_all("<Control-f>", self.open_search_window)
            # [2020-02-12]\\self.tree.bind("<Enter>", self.clear_message_area)
            self.tree.bind("<Enter>", self.clear_message_area)
            # [2020-02-12]\\self.tree.bind("<Leave>", self.view_records)
        # }
        except:  # {
            errorMessage = str(sys.exc_info()[0]) + "\n"
            errorMessage = errorMessage + str(sys.exc_info()[1]) + "\n"
            errorMessage = errorMessage + str(sys.exc_info()[2]) + "\n"
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            typeE = str("TYPE : " + str(exc_type))
            fileE = str("FILE : " + str(fname))
            lineE = str("LINE : " + str(exc_tb.tb_lineno))
            messageE = str("MESG : " + "\n" + str(errorMessage))
            self.the_logger.error("\n" + typeE +
                          "\n" + fileE +
                          "\n" + lineE +
                          "\n" + messageE)
            messagebox.showerror(title="ERROR!",
                                 message=typeE +
                                         "\n" + fileE +
                                         "\n" + lineE +
                                         "\n" + messageE)
        # }
        else:  # {
            self.the_logger.info("Operation Completed Successfully...")
        # }

    # }
    
    def _select_column(self, item=''): # {
        # TRY THE FOLLOWING
        try: # {
            self.tree["displaycolumns"] = ("one", "two", "three")
            # gets all values of the select row
            str_row = self.tree.item(self.tree.selection())
            #str_heading = str(self.tree.heading(column=str_row))
            print("STR ROW == " + str(str_row))
            # [2020-02-28]\\print("STR HEADING == " + str(self.tree.heading(column=self.tree.selection(self.tree["columns"]))))
            item = self.tree.selection()[0] # what row did you click on
            print(item)
            # GET/SET HEADING (main heading)
            heading = str(self.tree.heading(column="#0")['text'])
            heading_2 = str(self.tree.heading(column="one")['text'])
            print("HEADING (main) == " + str(heading))
            print("HEADING (two) == " + str(heading_2))
            show_heading = self.tree["columns"]
            print("HEADINGS == " + str(show_heading))
            # GET SELECTED COL HEADING
            #selected_heading = self.tree.heading(self.tree.item(self.tree.selection()))
            #selected_heading = self.tree.heading(self.tree.selection())
            selected_heading = self.tree.column(self.tree.item(self.tree.selection()), option='id')
            #selected_heading = self.tree.heading(column=self.tree.item(self.tree.selection()))
            str_selected_heading = str(selected_heading)
            print("STR == " + str(str_selected_heading))
            # [2020-02-11]\\selected_item = str(self.tree.selection()) ## get selected item
            selected_item = self.tree.item(self.tree.column())
            selected_col = str(self.tree.column(column="#0"))
            print('YOU SELECTED ' + str(selected_item))
            print('item == ' + str(item))
            #KEEP#print('heading == ' + str(self.tree.heading(column="#0")['text']))
            print('col == ' + str(selected_col))
            children = self.tree.get_children(item)
            print("CHILDREN == " + str(children))
            for child in children: # {
                text = self.tree.item(child, 'text')
                print(text)
            # }
            """
            for child in children: # {
                text = self.tree.item(child, 'text')
                # if text.startswith(self.entry.get()):
                if text.startswith(self.search_box_str.get()): # {
                    self.tree.selection_set(child)
                # }
            # }
            """
            # PRINT NUMBER OF COLUMNS BEING DISPLAYED 
            print("\n\tNUM OF COLS: " + str(len(self.tree["displaycolumns"])))
            # HIDE ALL BUT ONE COLUMN
            self.tree["displaycolumns"]=("one") # "two", "three", "four")
        # }
        except: # {
            errorMessage = str(sys.exc_info()[0]) + "\n"
            errorMessage = errorMessage + str(sys.exc_info()[1]) + "\n"
            errorMessage = errorMessage + str(sys.exc_info()[2]) + "\n"
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            typeE = str("TYPE : " + str(exc_type))
            fileE = str("FILE : " + str(fname))
            lineE = str("LINE : " + str(exc_tb.tb_lineno))
            messageE = str("MESG : " + "\n" + str(errorMessage))
            self.the_logger.error("\n" + typeE +
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
    
    def _de_select_column(self, item=''): # {
        print("DE-SELECTING ALL COLUMNS (showing all)...")
        # TRY THE FOLLOWING
        try: # {
            # SHOW ALL COLUMNS
            self.tree["displaycolumns"]=("Time Rec.", "Initials", "Type",
                                           "Company", "Contact Person", "Email Address",
                                           "Account ID", "Product #", "PF Quote #",
                                           "SAP Quote #", "Sent", "Time Sent", "Notes")
        # }
        except: # {
            errorMessage = str(sys.exc_info()[0]) + "\n"
            errorMessage = errorMessage + str(sys.exc_info()[1]) + "\n"
            errorMessage = errorMessage + str(sys.exc_info()[2]) + "\n"
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            typeE = str("TYPE : " + str(exc_type))
            fileE = str("FILE : " + str(fname))
            lineE = str("LINE : " + str(exc_tb.tb_lineno))
            messageE = str("MESG : " + "\n" + str(errorMessage))
            self.the_logger.error("\n" + typeE +
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
    
    def _column_sort(self, col, descending=False): # {
        # TRY THE FOLLOWING
        try: # {
            # grab values to sort as a list of typles (column value, column id)
            # e.g. [('Argentina', 'I001'), 'Australia', 'I002'), ('Brazil', 'I003'))]
            data = [(self.tree.set(child, col), child) for child in self.tree.get_children('')]
            
            # reorder data
            # tkinter looks after moving other items in
            # the same row
            data.sort(reverse=descending)
            for indx, item in enumerate(data): # {
                self.tree.move(item[1], '', indx)
            # }
            
            # reverse sort direction for next sort operation
            
        # }
        except: #{
            errorMessage = str(sys.exc_info()[0]) + "\n"
            errorMessage = errorMessage + str(sys.exc_info()[1]) + "\n"
            errorMessage = errorMessage + str(sys.exc_info()[2]) + "\n"
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            typeE = str("TYPE : " + str(exc_type))
            fileE = str("FILE : " + str(fname))
            lineE = str("LINE : " + str(exc_tb.tb_lineno))
            messageE = str("MESG : " + "\n" + str(errorMessage))
            self.the_logger.error("\n" + typeE +
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
    
    def _column_select(self): # {
        # TRY THE FOLLOWING:
        try: # {
            str_row = self.tree.item(self.tree.selection())
            print(str_row)
            # [2020-02-29]\\str_heading = self.tree.heading(str_row)
            # [2020-02-29]\\print(str_heading)
            item = self.tree.selection()
            #item = self.tree.heading(column=0)['text']
            print("ITEM == " + str(item))
            print(self.tree.heading(column=0)['text'])
            print(str(item))
            is_open = bool(self.tree.item(item)['open'])
            print("is_open:\t" + str(is_open))
            heading_2 = str(self.tree.heading(column="Time Rec.")['text'])
            print(heading_2)
            heading_3 = str(self.tree.heading(column=self.tree.selection()))
            print(heading_3)
            show_heading = self.tree["columns"]
            print("HEADINGS == " + str(show_heading))
        # } 
        except: # {
            errorMessage = str(sys.exc_info()[0]) + "\n"
            errorMessage = errorMessage + str(sys.exc_info()[1]) + "\n"
            errorMessage = errorMessage + str(sys.exc_info()[2]) + "\n"
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            typeE = str("TYPE : " + str(exc_type))
            fileE = str("FILE : " + str(fname))
            lineE = str("LINE : " + str(exc_tb.tb_lineno))
            messageE = str("MESG : " + "\n" + str(errorMessage))
            self.the_logger.error("\n" + typeE +
                          "\n" + fileE +
                          "\n" + lineE +
                          "\n" + messageE)
            messagebox.showerror(title="ERROR!",
                                 message=typeE +
                                         "\n" + fileE +
                                         "\n" + lineE +
                                         "\n" + messageE)
        # }
        else: # {
            self.the_logger.info("Operation Completed Successfully...")
        # }
    # }
    
    def clear_create_tab(self): # {
        # TRY THE FOLLOWING
        try: # {
            # ALL entry boxes in CREATE-TAB
            self.company_name.set("")       # company name
            self.name.set("")               # contact person's name
            self.email.set("")              # email address
            self.account_id.set("")         # account id
            self.initials.set("")           # initials
            self.type_var.set("Select: ")   # quote type
            # [2020-01-14]\\self.notes.set("")              
            # [2020-02-04]\\self.notes.insert(tk.INSERT, "") # notes
            self.num_of_copies.set("0") # posible copies to create
            self.notes.set("None")  # notes
        # }
        except: # { 
            errorMessage = str(sys.exc_info()[0]) + "\n"
            errorMessage = errorMessage + str(sys.exc_info()[1]) + "\n"
            errorMessage = errorMessage + str(sys.exc_info()[2]) + "\n"
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            typeE = str("TYPE : " + str(exc_type))
            fileE = str("FILE : " + str(fname))
            lineE = str("LINE : " + str(exc_tb.tb_lineno))
            messageE = str("MESG : " + "\n" + str(errorMessage))
            self.the_logger.error("\n" + typeE +
                          "\n" + fileE +
                          "\n" + lineE +
                          "\n" + messageE)
            messagebox.showerror(title="ERROR!",
                                 message=typeE +
                                         "\n" + fileE +
                                         "\n" + lineE +
                                         "\n" + messageE)
        # }
        else: # {
            # display message in the message area
            self.message['text'] = ' <<< Cleared CREATE TAB >>>'
            self.the_logger.info("Operation Completed Successfully...")
        # }
        
    # }
    
    def clear_message_area(self, event): # {
        # clear message area
        self.message['text'] = ''
    # }
    
    """
    def on_create_click(self, event): # {
        # TRY THE FOLLOWING
        try: # {
            # SHRINK DOWN FIRST 3 COLUMNS
            event.widget.column(column="#0", widht=50)
            event.widget.column(column="#1", width=50)
            event.widget.column(column="#2", width=50)
        # }
        except: # {
            errorMessage = str(sys.exc_info()[0]) + "\n"
            errorMessage = errorMessage + str(sys.exc_info()[1]) + "\n"
            errorMessage = errorMessage + str(sys.exc_info()[2]) + "\n"
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            typeE = str("TYPE : " + str(exc_type))
            fileE = str("FILE : " + str(fname))
            lineE = str("LINE : " + str(exc_tb.tb_lineno))
            messageE = str("MESG : " + "\n" + str(errorMessage))
            logging.error("\n" + typeE +
                          "\n" + fileE +
                          "\n" + lineE +
                          "\n" + messageE)
            messagebox.showerror(title="ERROR!",
                                 message=typeE +
                                         "\n" + fileE +
                                         "\n" + lineE +
                                         "\n" + messageE)
        # }
        else: # {
            logging.info("Operation Completed Successfully...")
        # }
    # }
    """
    
    def on_single_click(self, event): # {
        #### IF SELECTED HEADING... 
        #### change view of tree?
        # [2020-01-31]\\event.widget.yview()
        #event.widget.config(columns = ('tracking_number'))
        #event.widget.heading(column='tracking_number', )
        #event.widget.heading(column="#0", text="NEW TEXT", command=self.turn_red)
        # TRY THE FOLLOWING
        try: # {
            # gets all values of the select row
            test_str_library = self.tree.item(self.tree.selection())
            # prints dictionary of selected row
            print ("the test_str = \n", type(test_str_library), test_str_library, '\n')
            # WHICH ROW USER CLICKED ON
            item = self.tree.selection()[0]
            # WHICH << COL >> USER CLCKED ON
            #colly = self.tree.selection_set(column="#0")
            #print("\n\ttest-column: " + str(colly))
            print ("item clicked ", item)
            # PRINTS THE FIRST VALUE OF THE VALUES (the id value)
            # [2020-01-23]\\logging.info ("Time Rec: " + str(self.tree.item(item)['values'][0]))
            """
            IF THE RADIO BUTTON FOR (current TIMESTAMP) has been clicked?
            """
            # 1 == OLD
            # 2 == NEW
            # IF THE RADIO BUTTON VALUE IS EQUAL TO (new)
            if self.select_ts_2copy.get() == 2: # {
                # SET THE TIMESTAMP OF COPY TO BE (new) CURRENT TIME
                self.time_rec_2copy = str(pd.Timestamp.now())[:19]
            # }
            # ELSE... it is still set to 1?
            else: # {
                # ELSE... set to the timestamp of OLD TIMESTAMP FROM DB
                self.time_rec_2copy = str(self.tree.item(item)['values'][0])
            # }
            # [2020-01-29]\\self.time_rec_2copy = str(self.tree.item(item)['values'][0])
            print ("Time Rec: " + self.time_rec_2copy)
            self.initials_2copy = str(self.tree.item(item)['values'][1])
            print ("Initials: " + self.initials_2copy)
            self.type_2copy = str(self.tree.item(item)['values'][2])
            print ("Type: " + self.type_2copy)
            self.company_2copy = str(self.tree.item(item)['values'][3])
            print("Company: " + self.company_2copy)
            self.name_2copy = str(self.tree.item(item)['values'][4])
            print("Contact Person: " + self.name_2copy)
            self.email_2copy = str(self.tree.item(item)['values'][5])
            print ("Email: " + self.email_2copy)
            self.accountid_2copy = str(self.tree.item(item)['values'][6])
            print("Account ID: " + self.accountid_2copy)
            # PRODUCT #
            self.productnum_2copy = str(self.tree.item(item)['values'][7])
            print("Product #: " + self.productnum_2copy)
            # PF QUOTE #
            self.pf_quotenum_2copy = str(self.tree.item(item)['values'][8])
            print("Prodflow Quote #: " + self.pf_quotenum_2copy)
            # SAP QUOTE #
            self.sap_quotenum_2copy = str(self.tree.item(item)['values'][9])
            # SENT ?
            self.sent_2copy = str(self.tree.item(item)['values'][10])
            print("SENT == " + self.sent_2copy)
            # TIME SENT / close_time
            self.close_time_2copy = str(self.tree.item(item)['values'][11])
            print("TIME SENT / Close time == " + self.close_time_2copy)
            # Notes
            self.notes_2copy = str(self.tree.item(item)['values'][12])
            #### TURN AROUND TIME ????
            print("NOTES == " + str(self.notes_2copy))
            print (self.tree.item(item)['text'])
            # CHANGE THE COPY FILL TAB CONTAINER TO SHOW THE ABOVE VALUES
            self.selected_tracking_num.set(self.tree.item(item)['text'])
            # [2020-02-14]\\self.selected_time_rec.set(self.tree.item(item)['values'][0])
            self.selected_time_rec.set(self.time_rec_2copy)
        # }
        except: # {
            errorMessage = str(sys.exc_info()[0]) + "\n"
            errorMessage = errorMessage + str(sys.exc_info()[1]) + "\n"
            errorMessage = errorMessage + str(sys.exc_info()[2]) + "\n"
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            typeE = str("TYPE : " + str(exc_type))
            fileE = str("FILE : " + str(fname))
            lineE = str("LINE : " + str(exc_tb.tb_lineno))
            messageE = str("MESG : " + "\n" + str(errorMessage))
            self.the_logger.error("\n" + typeE +
                          "\n" + fileE +
                          "\n" + lineE +
                          "\n" + messageE)
            messagebox.showerror(title="ERROR!",
                                 message=typeE +
                                         "\n" + fileE +
                                         "\n" + lineE +
                                         "\n" + messageE)
        # }
        # TRY THE FOLLOWING
        try: # {
            # edit column?
            self.the_logger.info(str(event.widget.displaycolumns()))
            # [2020-01-15]\\event.widget['width'] = 2000
            # CHANGE THE WIDTH OF SELECT ROW
            self.the_logger.info(str(self.tree.column(column="#1", width=200)))
            test_column = self.tree.column(column="#0")
            # CHANGE ORDER OF DISPLAY COLUNS???
            self.the_logger.info("TEST_COLUMN == " + str(test_column))
            self.tree.set_children()
            """
            POPULATE THE "COPY" TAB CONTAINER WITH VALUES OF ROW SELECTED!
            """
            self.selected_cell.set(str(event.widget.get_children()))
        # }
        except: # {
            errorMessage = str(sys.exc_info()[0]) + "\n"
            errorMessage = errorMessage + str(sys.exc_info()[1]) + "\n"
            errorMessage = errorMessage + str(sys.exc_info()[2]) + "\n"
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            typeE = str("TYPE : " + str(exc_type))
            fileE = str("FILE : " + str(fname))
            lineE = str("LINE : " + str(exc_tb.tb_lineno))
            messageE = str("MESG : " + "\n" + str(errorMessage))
            
        # }
        else: # {
            self.the_logger.info("Operation Successfully Completed...")
        # }
        
    # }

    def on_double_click(self, event):  # {
        # TRY THE FOLLOWING
        try: #{
            # GET NUMBER OF CHILDREN (of ROOT)
            self.children_num = self.root.winfo_children()
            self.the_logger.info("\t CHILDREN BEFORE \n\t\t========>" + str(len(self.children_num)))
        # }
        except: # {
            self.the_logger.error("failed getting the children...")
        # }
        # TRY THE FOLLOWING
        try: # {
            # GET MOUSE LOCATION
            self.mouse_location = pyautogui.position()
            self.the_logger.info("MOUSE LOCATION:\n" + str(self.mouse_location))
            # GET SCREEN RESOLUTION/SIZE
            self.screen_resolution = pyautogui.size()
            self.the_logger.info("SCREEN SIZE:\n" + str(self.screen_resolution))
        # }
        except: # {
            self.the_logger.error("Error determining mouse location & screen size...")
        # }
        # TRY THE FOLLOWING
        try: # {
            # [2019-12-12]\\selected_track_num = self.tree.selection()[0]  # which tracking number you selected
            item = self.tree.selection()[0]  # which row did you click on
            print("ITEM CLICKED ", str(item))  # variable that represents the row you clicked on
            # [2019-12-12]\\item_2 = self.tree.item(self.tree.selection())  # gets all the values of the selected row
            # [20190-12-12]\\print('the test_str = ', type(item_2), item_2, '\n') # prints a dictionary of the selected row
            print(str(self.tree.item(item)['values'][0]))  # prints the first value of the values (the id value)
            # [2019-12-12]\\item_2 = str(self.tree.item(self.tree.selection())['columns'][0])
            # [2019-12-12]\\logging.info("ITEM 2 == " + str(item_2))
            # [2019-12-13]\\messagebox.showinfo(title="test:", message="you clicked on:\n" + str(self.tree.item(item, option="text")))
            selected_tracking_number = str(self.tree.item(item, option="text"))
            selected_time_rec = str(self.tree.item(item)['values'][1])# WAS 1
            selected_name = str(self.tree.item(item)['values'][5])  # WAS 1
            selected_email = str(self.tree.item(item)['values'][6]) # WAS 2
            selected_type = str(self.tree.item(item)['values'][7])  # WAS 3
            selected_sent = str(self.tree.item(item)['values'][12])  # WAS 4
            selected_notes = str(self.tree.item(item)['values'][11])  # WAS 6
            selected_initials = str(self.tree.item(item)['values'][2])  # WAS 7
            selected_account_id = str(self.tree.item(item)['values'][3])  # WAS 8
            selected_prodflow_quote_number = str(self.tree.item(item)['values'][9])  # WAS 9
            selected_sap_quote_number = str(self.tree.item(item)['values'][10])  # WAS 10
            selected_product_number = str(self.tree.item(item)['values'][8])  # WAS 11
            selected_company_name = str(self.tree.item(item)['values'][4])  # WAS 12
            # NEED ONE MORE HERE
            # CREATE LIST TO HOLD SELECTIONS
            selection_list = [selected_tracking_number,
                              selected_time_rec,
                              selected_name,
                              selected_email,
                              selected_type,
                              selected_sent,
                              selected_notes,
                              selected_initials,
                              selected_account_id,
                              selected_prodflow_quote_number,
                              selected_sap_quote_number,
                              selected_product_number,
                              selected_company_name]
            self.the_logger.info(str(selection_list))
            selection_string = str("YOU SELECTED:\n"
                                   + selected_time_rec + "\n" + selected_name + "\n"
                                   + selected_email + "\n" + selected_type + "\n"
                                   + selected_sent + "\n" + selected_notes + "\n"
                                   + selected_initials + "\n" + selected_account_id + "\n"
                                   + selected_prodflow_quote_number + "\n" + selected_sap_quote_number + "\n"
                                   + selected_product_number + "\n" + selected_company_name
                                   )
            self.the_logger.info(str(selection_string))
            ############################################## 
            # CHECK IF ANOTHER WINDOW IS ALREADY OPEN (greaater than 6)
            if len(self.children_num) > 6: # {
                messagebox.showwarning(title="WARNING:", message="ATTEMPTED TO OPEN MULTIPLE WINDOWS:\nCannot perform action while other window open!")
            # }
            else: # {
                # SEND SELECTIONS AND OPEN MODIFY WINDOW
                self.open_modify_window(selected_item=item, 
                                        the_selection_list=selection_list, 
                                        window_location=str(self.mouse_location)
                                        )
            # }
            # [2019-12-12]\\messagebox.showwarning(title=str(pd.Timestamp.now()), message=str(selection_string))
            # [2019-12-12]\\messagebox.showinfo(title="yupp!", message=str(self.tree.item(item_2, "text")))
        # }
        except IndexError: # {
            messagebox.showwarning(title="ALERT!",
                                   message=" Future Feature !\n Sorry for any inconvience(s)!")
        # }
        except: # {
            errorMessage = str(sys.exc_info()[0]) + "\n"
            errorMessage = errorMessage + str(sys.exc_info()[1]) + "\n"
            errorMessage = errorMessage + str(sys.exc_info()[2]) + "\n"
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            typeE = str("TYPE : " + str(exc_type))
            fileE = str("FILE : " + str(fname))
            lineE = str("LINE : " + str(exc_tb.tb_lineno))
            messageE = str("MESG : " + "\n" + str(errorMessage))
            self.the_logger.error("\n" + typeE +
                          "\n" + fileE +
                          "\n" + lineE +
                          "\n" + messageE)
            messagebox.showerror(title="ERROR!",
                                 message=typeE +
                                         "\n" + fileE +
                                         "\n" + lineE +
                                         "\n" + messageE)
        # }
        else: # {
            self.the_logger.info("Operation Completed Successfully...")
        # }
        self.the_logger.info("\t CHILDREN AFTER \n\t\t========>" + str(len(self.children_num)))
    # }
    
    
    def on_search(self, item=''): # {
        print("SEARCHING...")
        search_cat = str(self.combo_box_str.get())
        print("category>>>" + search_cat)
        print("critera... " + str(self.search_box_str.get()))
        children = self.tree.get_children() # variable to store the dictionary str
        # TRY THE FOLLOWING
        try: # {
            # CHECK IF SEARCH FOR TRACKING # or OTHER
            if str(search_cat) == "Tracking #": # {
                print("REQUESTING TRACKING #...")
                for child in children: # {
                    # variable to hold the cell TEXT ['text']
                    text_Text = (self.tree.item(child)["text"])
                    print(text_Text)
                    # CREATE VARIABLE CONTAINING TEXT
                    text_to_search = str(text_Text) # int(search_dict.get(str(search_cat)))
                    print("\n\t VAR RETURNS: " + str(text_to_search))
                    # CHECK IF SEARCH IS VALID (back part of STR)
                    if str(text_Text).endswith(self.search_box_str.get()): # {
                    #.startswith(self.search_box_str.get()): # {
                        print("CONTAINS VALUE (at end)!")
                    # }
                    # ELSE... IF... check front part of STR
                    elif str(text_Text).startswith(self.search_box_str.get()): # {
                        print("CONTAINS VALUE (at beg)!")
                    # }
                    # ELSE... IF... check AT LEAST CONTAINS somewhere
                    elif int(str(text_Text).find(self.search_box_str.get())) != -1: # {
                        print("CONTAINS VALUE (inside)!")
                    # }
                    else: # {
                        print("DOES NOT")
                        # DETACH CHILD FROM TREE (to only show search)
                        self.tree.detach(child)
                    # }
                # }
            # }
            # ELSE... if searching for << ANY OTHER >> Criteria...
            else: # {
                for child in children: # {
                    # variable to hold the cell values (dictionary)
                    values_Values = (self.tree.item(child)["values"])
                    print(values_Values)
                    # [2020-02-11]\\print("VALUE OF VALUES DOG == " + str(values_Values[str(search_cat)]))
                    # CREATE DICTIONARY CONTIANING VALUES
                    search_dict = {
                        "Time Rec.": 0,
                        "Initials": 1,
                        "Type": 2,
                        "Company": 3,
                        "Contact Person": 4,
                        "Email Address": 5,
                        "Account ID": 6,
                        "Product #": 7,
                        "PF Quote #": 8,
                        "SAP QUOTE #": 9,
                        "Sent": 10,
                        "Time Sent": 11,
                        "Notes": 12
                    }
                    # DETERMINE WHICH VALUE OF VALUES TO LOOK FOR WHEN COMPARING TO SEARCH
                    value_to_search = int(search_dict.get(str(search_cat)))
                    print("\n\t DIC RETURNS: " + str(value_to_search))
                    # CHECK IF SEARCH IS VALID
                    if str(values_Values[value_to_search]).startswith(self.search_box_str.get()): # {
                        print("CONTAINS VALUE (at beg)!")
                    # }
                    elif str(values_Values[value_to_search]).endswith(self.search_box_str.get()): # {
                        print("CONTAINS VALUE (at end)!")
                    # }
                    else: # {
                        print("DOES NOT")
                        # DETACH CHILD FROM TREE (to only show search)
                        self.tree.detach(child)
                    # }
                    """
                    # LOOP THRU TUPLE
                    for value in values_Values: # {
                        # CHECK IF VALUE MATCHES SEARCH CRITERIA
                        if str(value).startswith(self.search_box_str.get()): # {
                            print("CONTAINS VALUE!")
                            self.tree.detach(child)
                            #self.tree.item(child, text="blob", values=("foo", "bar"))
                        # }
                        else: # {
                            # DELETE BOX
                            print("DOES NOT CONTAIN")
                            # DETACH
                            #self.tree.detach(child)
                            #self.tree.item(child, text="blob", values=("foo", "bar"))
                            #print(child)
                        # }
                    # }
                    print(str(type(values_Values)))
                    print("LEN of VALUE == " + str(len(values_Values)))
                    print("VALUES == " + str(values_Values))
                    print("time rec == " + str(values_Values[0]))
                    print("Initials == " + str(values_Values[1]))
                    print("Type == " + str(values_Values[2]))
                    print("Company == " + str(values_Values[3]))
                    print("Contact Person == " + str(values_Values[4]))
                    print("Email Address == " + str(values_Values[5]))
                    print("Account ID == " + str(values_Values[6]))
                    print("Product # == " + str(values_Values[7]))
                    print("SAP Quote # == " + str(values_Values[8]))
                    print("Sent == " + str(values_Values[9]))
                    print("time sent == " + str(values_Values[10]))
                    print("notes == " + str(values_Values[11]))
                    """
                    """
                    text = self.tree.item(child, 'text')
                    if text.startswith(self.search_box_str.get()): # {
                        self.tree.selection_set(child)
                        return True
                    # }
                    else:# {
                        res = self.on_search(child)
                        if res: # {
                            return True
                        # }
                    """
                # }
            # }
        # }
        except: # {
            errorMessage = str(sys.exc_info()[0]) + "\n"
            errorMessage = errorMessage + str(sys.exc_info()[1]) + "\n"
            errorMessage = errorMessage + str(sys.exc_info()[2]) + "\n"
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            typeE = str("TYPE : " + str(exc_type))
            fileE = str("FILE : " + str(fname))
            lineE = str("LINE : " + str(exc_tb.tb_lineno))
            messageE = str("MESG : " + "\n" + str(errorMessage))
            self.the_logger.error("\n" + typeE +
                          "\n" + fileE +
                          "\n" + lineE +
                          "\n" + messageE)
            messagebox.showerror(title="ERROR!",
                                 message=typeE +
                                         "\n" + fileE +
                                         "\n" + lineE +
                                         "\n" + messageE)
        # }
        else: # {
            self.the_logger.info("Operation Completed Successfully...")
        # }
        # TRY THE FOLLOWING
        try: # {
            x = self.tree.get_children()
            # changing all children from root item
            for item in x: # {
                # [2020-02-03]\\self.tree.item(item, text="blub", values=("foo", "bar"))
                """
                self.tree.item(item, text="robert", values=("nub", "noob"))
                """
            # }
        # }
        except: # {
            errorMessage = str(sys.exc_info()[0]) + "\n"
            errorMessage = errorMessage + str(sys.exc_info()[1]) + "\n"
            errorMessage = errorMessage + str(sys.exc_info()[2]) + "\n"
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            typeE = str("TYPE : " + str(exc_type))
            fileE = str("FILE : " + str(fname))
            lineE = str("LINE : " + str(exc_tb.tb_lineno))
            messageE = str("MESG : " + "\n" + str(errorMessage))
            self.the_logger.error("\n" + typeE +
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
    
    # CALLED WHEN NOTEBOOK TAB IS SWITCHED/CHANGED
    def copy_create_check(self, event): # {
        # CALL UPDATE RECORDS
        self.view_records()
        print("\n\tself.num_of_copies.get() == " + str(self.num_of_copies.get()))
        print("\tself.num_of_new_copies.get() == " + str(self.num_of_new_copies.get()))
        print("\n\n\t value of CHECK BOX " + str(self.select_ts_2copy.get()))
        """
        
        "new_copies" are create in "COPY" tab
        "copies" are made while creating a new quote
        
        FOR each num in "num_of_copies.get()", call the ADD NEW RECORD function
        make sure 
        
        """
        ## IF THE COPY HAS BEEN SWITCHED TOO....
        if self.copy_tab is False: # {
            # change bool to true because user is on "copy"
            self.copy_tab = True
            # set OTHER NUMBER To 0?
            print("\t<<SET CREATE TAB TO ZERO>>")
            # CODE TO HIDE COLUMNS
            #self.tree["displaycolumns"]=("one", "two", "three", "four")
        # }
        # else.... IT HAS BEEN SWITCHED AWAY FORM...
        else: # {
            # change bool to false because user is on "create"
            self.copy_tab = False
            # set OTHER NUMBER To 0?
            print("\t<<SET COPY TAB TO ZERO>>")
            # CODE TO HIDE COLUMNS
            #self.tree["displaycolumns"]=("five", "six", "seven", "eight")
        # } 
        print("\n\tCOPY TAB BOOL = " + str(self.copy_tab))
        """
        # TRY THE FOLLOWING
        try: # {
            # CHECK NUMBER OF COPIES USER ENTERED:
            print("num of copies? \n\t " + str(self.num_of_copies.get()))
            # CHECK STATE OF CHECK BUTTON
            if int(self.copy_check_int.get()) == 0: # {
                print("NOT CHECKED!")
                # DECTIVATE THE SPINBOX SO IT CANT BE USED!
                self.copy_spinbox['state'] = tk.DISABLED
            # }
            else: # {
                print("CHECKED!")
                # SET SPINBOX TO BE ACTIVE!
                self.copy_spinbox['state'] = tk.ACTIVE
                # SET "create button" to inactive
                # [2020-02-05]\\self.create_button.state = tk.DISABLED
                # [2020-02-05]\\self.create_button['state'] = tk.DISABLED
            # }
        # }
        except: # {
            errorMessage = str(sys.exc_info()[0]) + "\n"
            errorMessage = errorMessage + str(sys.exc_info()[1]) + "\n"
            errorMessage = errorMessage + str(sys.exc_info()[2]) + "\n"
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            typeE = str("TYPE : " + str(exc_type))
            fileE = str("FILE : " + str(fname))
            lineE = str("LINE : " + str(exc_tb.tb_lineno))
            messageE = str("MESG : " + "\n" + str(errorMessage))
            logging.error("\n" + typeE +
                          "\n" + fileE +
                          "\n" + lineE +
                          "\n" + messageE)
            messagebox.showerror(title="ERROR!",
                                 message=typeE +
                                 "\n" + fileE +
                                 "\n" + lineE +
                                 "\n" + messageE)
        # }
        """
    # }
    
    """
    MAKES COPIES OF A RECORD THAT HAS ALREADY BEEN CREATED
    """
    def copy_create_record(self): # {
        # TRY THE FOLLOWING
        try: # {
            confirm_box = messagebox.askokcancel(title="CONFIRM COPY", 
                                                 message="are you sure?\n"
                                                 )
            # IF THE USER CONFIRMS!
            if str(confirm_box) == "True": # {
                self.the_logger.info("\n\t>>>>>>>>>> USER selected YES!!!")
                # TRY THE FOLLOWING
                try: # {
                    self.the_logger.info("COPY " + str(self.num_of_copies.get()) + " ENTRIES !!")
                    # GET number to copy and set as INT
                    copy_num = int(self.num_of_new_copies.get())
                    # set counter
                    counter = 0
                    while copy_num > counter: # {
                        # BEGIN POPULATING FIELDS THAT WILL BE USED TO CREATE "copy"
                        track_num = [self.create_file_name_convention(the_pickle=self.t_count_filename, number_of_digits=8)]
                        the_name = self.name_2copy
                        the_email = self.email_2copy
                        the_type = self.type_2copy
                        the_sent = self.sent_2copy
                        open_time = self.time_rec_2copy
                        close_time = self.close_time_2copy
                        # [2020-01-26]\\turn_around = self.
                        turn_around = "None"
                        the_notes = self.notes_2copy
                        the_initials = self.initials_2copy
                        the_account_id_num = self.accountid_2copy
                        the_prodflow_quote_num = self.pf_quotenum_2copy
                        the_sap_quote_num = self.sap_quotenum_2copy
                        the_product_number = self.productnum_2copy
                        the_company_name = self.company_2copy
                        self.the_logger.info("le copy # " + str(counter + 1) + ":\n")
                        copy_str = str("time REC: " + self.time_rec_2copy + "\n" 
                                       + "initials: " + self.initials_2copy + "\n"
                                       + "type: " + self.type_2copy + "\n"
                                       + "time rec: " + self.time_rec_2copy + "\n"
                                       + "company name: " + self.company_2copy + "\n"
                                       + "contact name: " + self.name_2copy + "\n"
                                       + "email address: " + self.email_2copy + "\n"
                                       + "accountid: " + self.accountid_2copy + "\n"
                                       + "prodflow quote # " + self.pf_quotenum_2copy + "\n"
                                       + "sap quote # " + self.sap_quotenum_2copy + "\n"
                                       + "product #: " + self.productnum_2copy + "\n"
                                       + "sent?: " + self.sent_2copy + "\n"
                                       )
                        """
                        *************************
                        MUST BE THE SAME AS THE SQLite COLUMN NAMES
                        ****************************
                        """
                        copy_entry_dict = {'tracking_number': track_num,
                                           'name': the_name,
                                           'email': the_email,
                                           'type': the_type,
                                           'sent': the_sent,
                                           'open_time': open_time,
                                           'close_time': close_time,
                                           'turn_around': turn_around,
                                           'notes': the_notes,
                                           'initials': the_initials,
                                           'account_id': the_account_id_num,
                                           'prodflow_quote_number': the_prodflow_quote_num,
                                           'sap_quote_number': the_sap_quote_num,
                                           'product_number': the_product_number,
                                           'company_name': the_company_name
                                           # [2019-12-31]\\'price': the_price
                                           }
                        # CREATE EMPTY DATAFRAME
                        copy_entry_df = pd.DataFrame(data=copy_entry_dict, index=None, dtype=np.str)
                        # CREATE ENGINE (for sending to Database)
                        # [2020-02-10]\\engine = create_engine('sqlite:///e:/_Quotes_Tracker/data/quotes_tracker.db')
                        engine = create_engine('sqlite:///' + str(self.db_filename))
                        # SEND DATAFRAME TO DATABASE
                        copy_entry_df.to_sql(name="quotes", con=engine, if_exists="append", index=False)
                        # UPDATE DISPLAY MESSAGE
                        self.message['text'] = "COPIED QUOTE \n#{}\nCREATED!".format(str(track_num))
                        """
                        messagebox.showinfo(title="le copy # " + str(counter + 1), 
                                    message=">>>>>>>>>>>>>>>\n" + str(copy_str))
                        """
                        # increment counter
                        counter += 1
                    # }
                    else: # {
                        self.the_logger.info("fin...")
                    # }
                    # gets all values of the select row
                    test_str_library = self.tree.item(self.tree.selection())
                    # WHICH ROW USER CLICKED ON
                    item = self.tree.selection()[0] 
                    print("TIME REC == " + str(item))
                    # [2020-01-24]\\test_time_rec = self.selected_cell.set(self.tree.item(item)['text'])
                    print("copied TIME REC == " + str(self.time_rec_2copy))
                # }
                except: # {
                    errorMessage = str(sys.exc_info()[0]) + "\n"
                    errorMessage = errorMessage + str(sys.exc_info()[1]) + "\n"
                    errorMessage = errorMessage + str(sys.exc_info()[2]) + "\n"
                    exc_type, exc_obj, exc_tb = sys.exc_info()
                    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                    typeE = str("TYPE : " + str(exc_type))
                    fileE = str("FILE : " + str(fname))
                    lineE = str("LINE : " + str(exc_tb.tb_lineno))
                    messageE = str("MESG : " + "\n" + str(errorMessage))
                    self.the_logger.error("\n" + typeE +
                                  "\n" + fileE +
                                  "\n" + lineE +
                                  "\n" + messageE)
                    messagebox.showerror(title="ERROR!",
                                         message=typeE +
                                         "\n" + fileE +
                                         "\n" + lineE +
                                         "\n" + messageE)
                # }
                else: # {
                    self.the_logger.info("Operation Completed Successfully...")
                    # REFRESH TABLE!
                    self.view_records()
                # }
            # }
            else: # {
                messagebox.showwarning(title="BACKED OUT", message="did not copy")
                self.the_logger.info("\n\t>>>>>>>>>> USER selected NO!!!")
            # }
        # }
        except: # {
            errorMessage = str(sys.exc_info()[0]) + "\n"
            errorMessage = errorMessage + str(sys.exc_info()[1]) + "\n"
            errorMessage = errorMessage + str(sys.exc_info()[2]) + "\n"
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            typeE = str("TYPE : " + str(exc_type))
            fileE = str("FILE : " + str(fname))
            lineE = str("LINE : " + str(exc_tb.tb_lineno))
            messageE = str("MESG : " + "\n" + str(errorMessage))
            self.the_logger.error("\n" + typeE +
                          "\n" + fileE +
                          "\n" + lineE +
                          "\n" + messageE)
            messagebox.showerror(title="ERROR!",
                                 message=typeE +
                                 "\n" + fileE +
                                 "\n" + lineE +
                                 "\n" + messageE)
        # }
        else: # {
            self.the_logger.info("Operation Completed Successfully...")
        # }
        # [2020-01-23]\\
        """
        # TRY THE FOLLOWING
        try: # {
            # CHANGE THE WIDTH OF THE FIRST 3 COLUMNS
            self.tree.column(column="#0", width=50)
            self.tree.column(column="#1", width=50)
            self.tree.column(column="#2", width=50)
            self.tree.column(column="#13", width=175)
        # }
        except: # {
            errorMessage = str(sys.exc_info()[0]) + "\n"
            errorMessage = errorMessage + str(sys.exc_info()[1]) + "\n"
            errorMessage = errorMessage + str(sys.exc_info()[2]) + "\n"
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            typeE = str("TYPE : " + str(exc_type))
            fileE = str("FILE : " + str(fname))
            lineE = str("LINE : " + str(exc_tb.tb_lineno))
            messageE = str("MESG : " + "\n" + str(errorMessage))
            logging.error("\n" + typeE +
                          "\n" + fileE +
                          "\n" + lineE +
                          "\n" + messageE)
            messagebox.showerror(title="ERROR!",
                                 message=typeE +
                                 "\n" + fileE +
                                 "\n" + lineE +
                                 "\n" + messageE)
        # }
        else: # {
            logging.info("Operation Completed Successfully...")
        # }
        """
    # }
    
    """
    def check_version_number(self, the_version_file): # {
        # TRY THE FOLLOWING
        try: # {
            print("CHECKING VER...")
            # LOAD IN VER FILE
            df_ver_file = pd.read_csv(self.ver_file, header=None, engine='python')
            print(df_ver_file)
            sleep(30)
        # }
        except: # {
            errorMessage = str(sys.exc_info()[0]) + "\n"
            errorMessage = errorMessage + str(sys.exc_info()[1]) + "\n"
            errorMessage = errorMessage + str(sys.exc_info()[2]) + "\n"
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            typeE = str("TYPE : " + str(exc_type))
            fileE = str("FILE : " + str(fname))
            lineE = str("LINE : " + str(exc_tb.tb_lineno))
            messageE = str("MESG : " + "\n" + str(errorMessage))
            logging.error("\n" + typeE +
                          "\n" + fileE +
                          "\n" + lineE +
                          "\n" + messageE)
            messagebox.showerror(title="ERROR!",
                                 message=typeE +
                                         "\n" + fileE +
                                         "\n" + lineE +
                                         "\n" + messageE)
        # }
        else: # {
            logger.the_logger.info("Operation Completed ")
        # }
    # }
    """
    
    def check_version_number_in_thread(self): # {
        print("THREAD-check-ver")
        # START THREAD THREAD
        # [2020-03-02]\\self.thread = Thread(None, self.check_version_number, None, (), {})
        self.thread = Thread(None, CheckVersionNumber, None, (), {})
        # [2020-03-02]\\self.thread = Thread(None, RefreshTable, None, (), {})
        self.thread.start()
    # }

    ######################################################################################################
    # QUOTE NUMBER CONVENTION AND PROGRESS CHECKS #
    ###############################################

    def check_quote_completion(self, the_df):  # {
        # CREATE ENGINE (for pulling from Database)
        # [2020-02-10]\\engine = create_engine('sqlite:///e:/_Quotes_Tracker/data/quotes_tracker.db')
        engine = create_engine('sqlite:///' + str(self.db_filename))
        # USE ENGINE TO CONNECT TO DATABASE
        # [2020-01-17]\\cnxn = pyodbc.connect(engine)
        # [2020-02-10]\\conn = sqlite3.connect("E:/_Quotes_Tracker/data/quotes_tracker.db")
        conn = sqlite3.connect(str(self.db_filename))
        # SEND DATAFRAME TO DATABASE
        # [2020-01-16]\\new_entry_df.to_sql(name="quotes", con=engine, if_exists="append", index=False)
        # TRY THE FOLLOWING
        try:  # {
            # LIST TO HOLD RESULTS
            result = []
            # FOR EACH ROW-ENTRY IN "sent" COLUMN
            for value in the_df["sent"]:  # {
                if value is False:  # {
                    # append nothing (Keeping index)
                    result.append("")
                # }
            # }
            else:  # {
                # MAKE SURE "turn_around" IS ALSO EMPTY
                if str(the_df["turn_around"]):  # {
                    # CREATE TIMESTAMP FOR "meow"
                    meow_ts = pd.Timestamp.now()
                    # APPEND TO RESULT
                    result.append(str(meow_ts))
                # }
                else:  # {
                    self.the_logger.info("NOT EMPTY!")
                # }
            # }
            # OVERWRITE COL?
            the_df["turn_around"] = result
            self.the_logger.info(the_df)
            # RETURN DATAFRAME TO REPLACE OLD/OUTDATED ONE
            return the_df
        # }
        except:  # {
            errorMessage = str(sys.exc_info()[0]) + "\n"
            errorMessage = errorMessage + str(sys.exc_info()[1]) + "\n"
            errorMessage = errorMessage + str(sys.exc_info()[2]) + "\n"
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            typeE = str("TYPE : " + str(exc_type))
            fileE = str("FILE : " + str(fname))
            lineE = str("LINE : " + str(exc_tb.tb_lineno))
            messageE = str("MESG : " + "\n" + str(errorMessage))
            self.the_logger.error("\n" + typeE +
                          "\n" + fileE +
                          "\n" + lineE +
                          "\n" + messageE)
            messagebox.showerror(title="ERROR!",
                                 message=typeE +
                                         "\n" + fileE +
                                         "\n" + lineE +
                                         "\n" + messageE)
        # }
        else:  # {
            self.the_logger.info("Operation Completed Successfully...")
        # }

    # }

    """
    TAKES IN:
        (1) pickle of current "Quotes-Number" count
        (2) TOTAL number of digits to complete with zfill
        >>> increments that by 1 and overwrites the file <<<
    RETURNS:
        (1) string with proper file naming convention for database use
    """

    def create_file_name_convention(self, the_pickle, number_of_digits):  # {
        # TRY THE FOLLOWING:
        try:  # {
            # LOAD IN PICKLE FROM FILE
            with open(Path(the_pickle), 'rb') as le_pickle:  # {
                # LOAD PICKLE AS TYPE INT
                current_count = int(pickle.load(le_pickle))
            # }
            # DISPLAY VALUE FOR DEBUG
            self.the_logger.info("current count == " + str(current_count))
            # INCREASE COUNT
            current_count += 1
            # CREATE STRING WITH COUNT + zero fill
            count_str = str(current_count).zfill(int(number_of_digits))
            self.the_logger.info("count_str == " + str(count_str))
            # CREATE STRING
            file_name_conv = str("T" + count_str)
            self.the_logger.info("FINAL RESULT == " + str(file_name_conv))
        # }
        except:  # {
            errorMessage = str(sys.exc_info()[0]) + "\n"
            errorMessage = errorMessage + str(sys.exc_info()[1]) + "\n"
            errorMessage = errorMessage + str(sys.exc_info()[2]) + "\n"
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            typeE = str("TYPE : " + str(exc_type))
            fileE = str("FILE : " + str(fname))
            lineE = str("LINE : " + str(exc_tb.tb_lineno))
            messageE = str("MESG : " + "\n" + str(errorMessage))
            self.the_logger.error("\n" + typeE +
                  "\n" + fileE +
                  "\n" + lineE +
                  "\n" + messageE)
        # }
        else:  # {
            self.the_logger.info("Operation Completed Successfully...")
        # }
        finally:  # {
            self.the_logger.info("... saving COUNT TO PICKLE == " + str(current_count))
            # OVERWRITE PICKLE WITH NEW INCREMENTED COUNT
            with open(Path(the_pickle), 'wb') as le_pickle:  # {
                # SAVE PICKLE AS TYPE INT
                pickle.dump(current_count, le_pickle)
            # }
            # RETURN THE STRING
            return file_name_conv
        # }

    # }
    
    def check_quote_convention(self, event): #{
        # TRY THE FOLLOWING
        try: # {
            print("STATUS == " + str(self.new_status_var.get()))
            # ASSIGN ENTRY INPUT TO STR
            # [2020-01-07]\\test_regex = str(self.pf_quote_num.get())
            # [2020-01-09]\\test_regex = str(self.new_pf_quote_num_entry_widget.get())
            test_regex = str(self.new_pf_quote_num.get())
            self.the_logger.info("TEST-REGEX:\t" + str(test_regex))
            self.the_logger.info("\n" + str(self.pf_quote_regex))
            # display message
            self.message['text'] = ' ===== EDIT QUOTE [!] ===== '
            # CHECK IF THE PF QUOTE # DOESNT MATCH
            if fnmatch.fnmatch(test_regex, str(self.pf_quote_regex)) or fnmatch.fnmatch(test_regex, str('')): # {
                # keep submit button ACTIVE
                self.the_logger.info("PF-QUOTE-#... PASSES")
                event.widget['state'] = tk.ACTIVE
                # test display message?
                # [2020-01-14]\\self.left_transient['text'] = ' <<< PF-QUOTE-#... correct >>>'
                # display message
                self.message['text'] += '\n <<< PF-QUOTE-#... correct >>>'
                # NoW CHECK IF SAP QUOTE # DOESNT MATCH
                test_regex = str(self.new_sap_quote_num.get())
                if fnmatch.fnmatch(test_regex, str(self.sap_quote_regex)) or fnmatch.fnmatch(test_regex, str('')): # {
                    # keep submit button ACTIVE
                    self.the_logger.info("SAP-QUOTE-#... PASSES")
                    event.widget['state'] = tk.ACTIVE
                    # display message
                    self.message['text'] += '\n <<< SAP-QUOTE-#... correct >>>'
                    # NOW CHECK IF ACCOUNT ID DOESNT MATCH
                    test_regex = str(self.new_account_id.get())
                    if fnmatch.fnmatch(test_regex, str(self.account_id_regex)): # {
                        # keep submit button ACTIVE
                        self.the_logger.info("ACCOUNT ID... PASSES")
                        event.widget['state'] = tk.ACTIVE
                        # display message
                        self.message['text'] += '\n <<< ACCOUNT-ID... correct >>>'
                    # }
                    else: # {
                        # keep submit button DISABLED
                        self.the_logger.info("ACCOUNT ID... FAILED")
                        event.widget['state'] = tk.DISABLED
                        # display message
                        self.message['text'] = " <<< ACCOUNT ID... incorrect >>>"
                        self.message['text'] += "\n <<< 8-digit-alphanumeric"
                    # }
                # }
                else: # {
                    # keep submit button DISABED
                    self.the_logger.info("SAP-QUOTE-#... FAILED")
                    event.widget['state'] = tk.DISABLED
                    # display message
                    self.message['text'] += "\n <<< SAP-QUOTE-#... incorrect >>> "
                    self.message['text'] += "\n <<< 7-digit-numeric"
                # } 
            # }
            else: # {
                # keep submit button DISABLED
                self.the_logger.info("PF-QUOTE-#... FAILED")
                event.widget['state'] = tk.DISABLED
                # display message
                self.message['text'] += '\n <<< PF-QUOTE-#... incorrect >>>'
                self.message['text'] += '\n <<< Format: MMDDYY-XXX >>>'
            # }
        # }
        except: # {
            errorMessage = str(sys.exc_info()[0]) + "\n"
            errorMessage = errorMessage + str(sys.exc_info()[1]) + "\n"
            errorMessage = errorMessage + str(sys.exc_info()[2]) + "\n"
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            typeE = str("TYPE : " + str(exc_type))
            fileE = str("FILE : " + str(fname))
            lineE = str("LINE : " + str(exc_tb.tb_lineno))
            messageE = str("MESG : " + "\n" + str(errorMessage))
            self.the_logger.error("\n" + typeE +
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

    ###################################################################################################
    # ADD / UPDATE / DELETE FUNCTION BELOW #
    ########################################

    def add_new_record(self):  # {
        # TRY THE FOLLOWING
        try:  # {
            # CHECK IF RECORD IS VALIDATED (every box)
            if self.new_records_validated():  # {
                display_str = "YOU ENTERED:\n\n" 
                display_str += "contact name:\t\t" + str(self.name.get()) + "\n"
                display_str += "email address:\t\t" + str(self.email.get()) + "\n"
                display_str += "company name:\t\t" + str(self.company_name.get()) + "\n"
                display_str += "initials:\t\t\t" + str(self.initials.get()) + "\n"
                display_str += "account id:\t\t" + str(self.account_id.get()) + "\n"
                display_str += "PF Quote #:\t\tNONE\n"
                display_str += "SAP Quote #:\t\tNONE\n"
                display_str += "product #:\t\tNONE\n"
                display_str += "-------------------------------------------\n"
                display_str += "notes:\n\t\t"
                display_str += str(self.notes.get())  # ("1.0", tk.END))
                # ASK THE USER IF THEY ARE SURE WITH THEIR COMPLETION?
                confirm_box = messagebox.askokcancel(title="Confirm Create", message=str(display_str))
                self.the_logger.info(confirm_box)
                if str(confirm_box) == "True":  # {
                    # IF THE USER SAID YES.... ADD NEW RECORD!
                    self.the_logger.info("...ADDING NEW RECORD...")
                    """
                    ############################################################
                    << CHECK NUMBER OF NEW RECORDS TO ADD >>
                    ############################################################
                    """
                    print("\n\t self.num_of_copies.get() == " + str(self.num_of_copies.get()))
                    # CHECK NUMBER OF COPIES USER WISHES TO MAKE:
                    if int(self.num_of_copies.get()) > 1: # {
                        real_number_to_create = int(self.num_of_copies.get())
                        print("\n\t... WISHES TO CREATE multiple NEW ENTRIES... " + str(real_number_to_create))
                    # }
                    # ELSE... USER DIDNT CHANGE NUMBER.. so set to 1 by default
                    else: # { 
                        real_number_to_create = 1
                        print("n\t... WISHES TO CREATE (one) SINGLE ENTRY... ")
                    # }
                    """
                    <<<<<<<<<<<<<<<<<<< LOOOP & CREATE (copies of) RECORD >>>>>>>>>>>>>>>
                    """
                    # LOOP FOR EACH INSTANCE OF "real_number_to_create"
                    while int(real_number_to_create) > 0: # {
                        # create ENTRY variables
                        # [2019-12-26]\\track_num = [self.quote_number_convention()]  # auto-creates number
                        track_num = [self.create_file_name_convention(the_pickle=self.t_count_filename, number_of_digits=8)]
                        the_name = [str(self.name.get())]
                        the_email = [str(self.email.get())]
                        the_type = [str(self.type_var.get())]
                        # [2020-01-08]\\the_sent = [str(self.radio_sent_var.get())]
                        the_sent = [str("False")]
                        open_time = [str(pd.Timestamp.now())[:19]]
                        close_time = [str("None")]
                        turn_around = [str("None")]  # np.Nan?
                        # [2019-12-18]\\the_notes = [str(self.notes.get())]
                        # IF NOTES IS LEFT EMPTY ADD IN THAT IT IS SO
                        if str(self.notes.get()) == "":  # {
                            # SET NOTES TO STRING OF "none"
                            the_notes = ["None"]
                        # }
                        # ELSE ITS NOT EMPTY SO ASSIGN TO DATAFRAME
                        else:  # {
                            # [2020-01-14]\\the_notes = [str(self.notes.get("1.0", tk.END))]
                            the_notes = [str(self.notes.get())]
                        # }
                        the_initials = [str(self.initials.get())]
                        the_account_id_num = [str(self.account_id.get())]
                        # [2020-01-10]\\the_prodflow_quote_num = [str(self.prodflow_quote_num.get())]
                        # [2020-01-10]\\the_sap_quote_num = [str(self.sap_quote_num.get())]
                        # [2020-01-10]\\the_product_number = [str(self.product_num.get())]
                        the_prodflow_quote_num = [""]
                        the_sap_quote_num = [""]
                        the_product_number = [""]
                        the_company_name = [str(self.company_name.get())]
                        # [2019-12-12]\\ts_meow = [str(pd.Timestamp.now())]
                        # DICTIONARY OF LISTS
                        """
                        *************************
                        MUST BE THE SAME AS THE SQLite COLUMN NAMES
                        ****************************
                        """
                        new_entry_dict = {'tracking_number': track_num,
                                          'name': the_name,
                                          'email': the_email,
                                          'type': the_type,
                                          'sent': the_sent,
                                          'open_time': open_time,
                                          'close_time': close_time,
                                          'turn_around': turn_around,
                                          'notes': the_notes,
                                          'initials': the_initials,
                                          'account_id': the_account_id_num,
                                          'prodflow_quote_number': the_prodflow_quote_num,
                                          'sap_quote_number': the_sap_quote_num,
                                          'product_number': the_product_number,
                                          'company_name': the_company_name
                                          # [2019-12-31]\\'price': the_price
                                          }
                        # CREATE EMPTY DATAFRAME
                        new_entry_df = pd.DataFrame(data=new_entry_dict, index=None, dtype=np.str)
                        # CREATE ENGINE (for sending to Database)
                        # [2020-02-10]\\engine = create_engine('sqlite:///e:/_Quotes_Tracker/data/quotes_tracker.db')
                        engine = create_engine('sqlite:///' + str(self.db_filename))
                        # SEND DATAFRAME TO DATABASE
                        new_entry_df.to_sql(name="quotes", con=engine, if_exists="append", index=False)
                        # UPDATE DISPLAY MESSAGE
                        self.message['text'] = "NEW QUOTE \n#{}\nCREATED!".format(str(track_num))
                        """
                        # CREATE ENTRY
                        print("create entry " + str(real_number_to_create))
                        """
                        # decrement count
                        real_number_to_create -= 1
                    # }
                    else: # {
                        print("create entry 0... so finished!")
                    # }
                    # [2020-02-10]\\stop_input = input("did they work?")
                    """
                    # create ENTRY variables
                    # [2019-12-26]\\track_num = [self.quote_number_convention()]  # auto-creates number
                    track_num = [self.create_file_name_convention(the_pickle=self.t_count_filename, number_of_digits=8)]
                    the_name = [str(self.name.get())]
                    the_email = [str(self.email.get())]
                    the_type = [str(self.type_var.get())]
                    # [2020-01-08]\\the_sent = [str(self.radio_sent_var.get())]
                    the_sent = [str("False")]
                    open_time = [str(pd.Timestamp.now())[:19]]
                    close_time = [str("None")]
                    turn_around = [str("None")]  # np.Nan?
                    # [2019-12-18]\\the_notes = [str(self.notes.get())]
                    # IF NOTES IS LEFT EMPTY ADD IN THAT IT IS SO
                    if str(self.notes.get()) == "":  # {
                        # SET NOTES TO STRING OF "none"
                        the_notes = ["None"]
                    # }
                    # ELSE ITS NOT EMPTY SO ASSIGN TO DATAFRAME
                    else:  # {
                        # [2020-01-14]\\the_notes = [str(self.notes.get("1.0", tk.END))]
                        the_notes = [str(self.notes.get())]
                    # }
                    the_initials = [str(self.initials.get())]
                    the_account_id_num = [str(self.account_id.get())]
                    # [2020-01-10]\\the_prodflow_quote_num = [str(self.prodflow_quote_num.get())]
                    # [2020-01-10]\\the_sap_quote_num = [str(self.sap_quote_num.get())]
                    # [2020-01-10]\\the_product_number = [str(self.product_num.get())]
                    the_prodflow_quote_num = [""]
                    the_sap_quote_num = [""]
                    the_product_number = [""]
                    the_company_name = [str(self.company_name.get())]
                    # [2019-12-12]\\ts_meow = [str(pd.Timestamp.now())]
                    # DICTIONARY OF LISTS
                    #*************************
                    #MUST BE THE SAME AS THE SQLite COLUMN NAMES
                    #****************************
                    new_entry_dict = {'tracking_number': track_num,
                                      'name': the_name,
                                      'email': the_email,
                                      'type': the_type,
                                      'sent': the_sent,
                                      'open_time': open_time,
                                      'close_time': close_time,
                                      'turn_around': turn_around,
                                      'notes': the_notes,
                                      'initials': the_initials,
                                      'account_id': the_account_id_num,
                                      'prodflow_quote_number': the_prodflow_quote_num,
                                      'sap_quote_number': the_sap_quote_num,
                                      'product_number': the_product_number,
                                      'company_name': the_company_name
                                      # [2019-12-31]\\'price': the_price
                                      }
                    # CREATE EMPTY DATAFRAME
                    new_entry_df = pd.DataFrame(data=new_entry_dict, index=None, dtype=np.str)
                    # CREATE ENGINE (for sending to Database)
                    engine = create_engine('sqlite:///e:/_Quotes_Tracker/data/quotes_tracker.db')
                    # SEND DATAFRAME TO DATABASE
                    new_entry_df.to_sql(name="quotes", con=engine, if_exists="append", index=False)
                    # UPDATE DISPLAY MESSAGE
                    self.message['text'] = "NEW QUOTE \n#{}\nCREATED!".format(str(track_num))
                    # CLEAR ENTRY BOXES
                    # [2020-01-10]\\
                    self.name.delete(0, tk.END)
                    self.email.delete(0, tk.END)
                    self.notes.delete(0, tk.END)
                    self.initials.delete(0, tk.END)
                    self.account_id.delete(0, tk.END)
                    self.prodflow_quote_num.delete(0, tk.END)
                    self.sap_quote_num.delete(0, tk.END)
                    self.product_num.delete(0, tk.END)
                    self.company_name.delete(0, tk.END)
                    self.type_var.set("Select: ")
                    # [2019-12-31]\\self.price.delete(0, tk.END)
                    """
                    #### CLEAR ENTRY BOXES
                    self.company_name.set("")
                    self.name.set("")
                    self.email.set("")
                    self.notes.set("")
                    # [2020-01-14]\\self.notes.insert(tk.INSERT, "")
                    self.initials.set("")
                    self.account_id.set("")
                    # removed [2020-01-10] - re added [2020-02-06]\\
                    # [2020-01-10]\\self.prodflow_quote_num.set("")
                    # [2020-01-10]\\self.sap_quote_num.set("")
                    # [2020-01-10]\\self.product_num.set("")
                    # [2020-02-10]\\self.prodflow_quote_num.set("")
                    # [2020-02-10]\\self.quote_num.set("")
                    # [2020-02-10]\\self.product_num.set("")
                    # [2020-02-10]\\self.company_name.set("")
                    self.type_var.set("Select: ")
                    # SET COPIES BACK TO 1
                    self.num_of_copies.set("1")
                    self.num_of_new_copies.set("1")
                # }
                else:  # {
                    # SHOW WARNING BOX
                    messagebox.showwarning(title="WARNING!", message='You were not sure...')
                # }
            # }
            else:  # {
                # [2020-01-07]\\self.message['text'] = ' >>>>>>>>>>>>><<<<<<<<<<<<<\n [Initials], [Type], [AccountID],\n [Product #], [PF Quote #], [SAP Quote #]\n CANNOT BE left BLANK! \n >>>>>>>>>>>>><<<<<<<<<<<<<'
                self.message['text'] = ' >>>>>>>>>>>>>><<<<<<<<<<<<<<\n [Initials], [Type], and/or [AccountID]\n CANNOT  BE  LEFT  BLANK! \n >>>>>>>>>>>>>><<<<<<<<<<<<<<'
            # }
            # CALL FUNCTION TO UDPATE TABlE DISPLAY
            self.view_records()
            # [2020-01-23]\\
            """
            #############################################################
            # MINIMIZE THE FIRST 3 COLUMNS 
            # TRY THE FOLLOWING
            try: # {
                # CHANGE THE WIDTH OF THE FIRST 3 COLUMNS
                self.tree.column(column="#0", width=50)
                self.tree.column(column="#1", width=50)
                self.tree.column(column="#2", width=50)
                self.tree.column(column="#13", width=175)
            # }
            except: # {
                errorMessage = str(sys.exc_info()[0]) + "\n"
                errorMessage = errorMessage + str(sys.exc_info()[1]) + "\n"
                errorMessage = errorMessage + str(sys.exc_info()[2]) + "\n"
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                typeE = str("TYPE : " + str(exc_type))
                fileE = str("FILE : " + str(fname))
                lineE = str("LINE : " + str(exc_tb.tb_lineno))
                messageE = str("MESG : " + "\n" + str(errorMessage))
                logging.error("\n" + typeE +
                              "\n" + fileE +
                              "\n" + lineE +
                              "\n" + messageE)
                messagebox.showerror(title="ERROR!",
                                     message=typeE +
                                         "\n" + fileE +
                                         "\n" + lineE +
                                         "\n" + messageE)
            # }
            else: # {
                logging.info("Operation Completed Successfully...")
            # }
            ##############################################################
            """
        # }
        except:  # {
            errorMessage = str(sys.exc_info()[0]) + "\n"
            errorMessage = errorMessage + str(sys.exc_info()[1]) + "\n"
            errorMessage = errorMessage + str(sys.exc_info()[2]) + "\n"
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            typeE = str("TYPE : " + str(exc_type))
            fileE = str("FILE : " + str(fname))
            lineE = str("LINE : " + str(exc_tb.tb_lineno))
            messageE = str("MESG : " + "\n" + str(errorMessage))
            self.the_logger.error("\n" + typeE +
                          "\n" + fileE +
                          "\n" + lineE +
                          "\n" + messageE)
            messagebox.showerror(title="ERROR!",
                                 message=typeE +
                                         "\n" + fileE +
                                         "\n" + lineE +
                                         "\n" + messageE)
        # }
        else:  # {
            self.the_logger.info("Operation Completed Successfully...")
        # }

    # }
            
    def account_id_validated(self, the_str): # {
        # TRY THE FOLLOWING
        try: # {
            # CHECK FOR PROPER NAMING CONVENTION
            if fnmatch.fnmatch(the_str, str(self.account_id_regex)): # {
                return True
            # }
            else: # {
                return False
            # }
        # }
        except: # {
            pass
        # }
        else: # {
            self.the_logger.info("Operation Completed Successfully...")
        # }
    # }
    
    def pf_quote_num_validated(self, the_str): # {
        # TRY THE FOLLOWING
        try: # {
            pass
        # }
        except: # {
            pass
        # }
    # }
    
    def sap_quote_num_validated(self, the_str): # {
        # TRY THE FOLLOWING
        try: # {
            pass
        # }
        except: # {
            pass
        # }
    # }
    
    def turn_red(self, event): # {
        self.message['text'] = 'YOU HIT ENETER BOIII'
        print("turn red!")
        # PRIN OUT SELECTED TAB?
        selected_tab = self.tab_control.tabs()
        print("selected tab:\n\t" + str(selected_tab))
        # [2020-02-6]\\print("THIS WIDGET's TEXT:\n" + str(event.widget['text']))
        #self.message['text'] = "SOOOUP"
        # [2020-01-08]\\event.widget["activeforeground"] = "red"  
    # }

    def new_records_validated(self):  # {
        self.the_logger.info("NAME:\n <" + str(self.name.get()) + ">")
        self.the_logger.info("TYPE:\n <" + str(self.type_var.get()) + ">")
        # TRY THE FOLLOWING
        try:  # {
            return len(str(self.initials.get())) != 0 \
                   and str(self.type_var.get()) != "Select: " \
                   and len(str(self.account_id.get())) != 0
                   # [2020-01-07]\\and len(self.pf_quote_num.get()) != 0 \
                   # [2020-01-07]\\and len(self.sap_quote_num.get()) != 0 \
                   # [2020-01-07]\\and len(self.product_number.get()) != 0
            # [2019-12-18]\\and len(self.radio_type_var.get()) != 0 \
            # [2019-12-18]\\and len(self.radio_sent_var.get()) != 0
            # [2019-12-18]\\and len(self.notes.get()) != 0
        # }
        except:  # {
            errorMessage = str(sys.exc_info()[0]) + "\n"
            errorMessage = errorMessage + str(sys.exc_info()[1]) + "\n"
            errorMessage = errorMessage + str(sys.exc_info()[2]) + "\n"
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            typeE = str("TYPE : " + str(exc_type))
            fileE = str("FILE : " + str(fname))
            lineE = str("LINE : " + str(exc_tb.tb_lineno))
            messageE = str("MESG : " + "\n" + str(errorMessage))
            self.the_logger.error("\n" + typeE +
                          "\n" + fileE +
                          "\n" + lineE +
                          "\n" + messageE)
            messagebox.showerror(title="ERROR!",
                                 message=typeE +
                                         "\n" + fileE +
                                         "\n" + lineE +
                                         "\n" + messageE)
        # }
        else:  # {
            self.the_logger.info("Operation Completed Successfully...")
        # }

    # }
    
    def updated_records_validated(self, a_product_num, a_pf_num, a_sap_num): # {
        self.the_logger.info("Validating FILE NAME conventions...")
        # TRY THE FOLLOWING
        try: # {
            pass
        # }
        except: # {
            pass
        # }
    # }

    def view_records(self):  # {
        self.the_logger.info("Begin Populating TreeView...")
        # display message
        # [2020-02-06]\\self.message['text'] = " <<< Updating / Refreshing Table >>> "
        # TRY THE FOLLOWING
        try:  # {
            items = self.tree.get_children()
            for item in items:  # {
                self.tree.delete(item)
            # }
            # [2020-01-03]\\query = 'SELECT * FROM quotes ORDER BY name desc'
            # [2020-02-14]\\query = 'SELECT * FROM quotes ORDER BY open_time desc'
            # [2020-03-04]\\query = "SELECT * FROM quotes WHERE [status] != '" + str("void") + "' ORDER BY tracking_number desc"
            # query = 'SELECT * FROM quotes WHERE [status] is NULL ORDER BY tracking_number desc'
            query = "SELECT * FROM quotes WHERE [status] is NULL OR [status] != '" + str("void") + "' ORDER BY tracking_number desc"
            quote_tracker_entries = self.execute_db_query(query)
            for row in quote_tracker_entries:  # {
                # [2020-01-14]\\print("PRINTING ROW:\n\t" + str(row))
                # [2020-02-05]\\
                """
                logging.info("TRACKING # == " + str(row[0]))
                logging.info("Time REC. === " + str(row[5])) #  WAS NAME [row=1]
                logging.info("Initials == " + str(row[9]))  # WAS EMAIL [row=2]
                logging.info("Type == " + str(row[3]))
                logging.info("COMPANY NAME == " + str(row[14]))  # WAS SENT [row=4]
                logging.info("CONTACT PERSON == " + str(row[1]))  # WAS open_time [row=5]
                logging.info("EMAIL ADDRESS == " + str(row[2]))  # WAS close_time [row=6]
                logging.info("Account ID == " + str(row[10]))  # WAS turn_around [row=7]
                logging.info("PRODUCT NUMBER == " + str(row[15])) # WAS notes [row=8]
                logging.info("PF Quote # == " + str(row[11]))  # WAS INITIALS [row=9]
                logging.info("SAP Quote # == " + str(row[12]))  # WAS Account ID [row=10]
                # [2019-12-31]\\logging.info("NOTES == " + str(row[8])) # WAS PRODFLOW QUOTE # [row=11]
                logging.info("SENT == " + str(row[4])) 
                logging.info("Time Sent. == " + str(row[6])) # WAS SAP QUOTE # [row=12]
                # [2019-12-31]\\logging.info("SENT  == " + str(row[4]))  # WAS SAP QUOTE # [row=12]
                # [2019-12-31]\\logging.info("Time Sent. == " + str(row[6])) # WAS PRICE [row=13]
                logging.info("NOTES == " + str(row[8]))  # WAS PRODFLOW QUOTE # [row=11]
                logging.info("TURN AROUND TIME (if any) == " + str(row[7]))
                """
                # CREATE LIST TO HOLD RECORD ENTRY
                # [Tracking #] [Name] [Email] [Type] [Timestamp/open_time]
                # [2019-12-31]
                """
                record_entry = [str(row[1]), str(row[2]), str(row[3]), str(row[5]),
                                str(row[4]), str(row[7]), str(row[8]), str(row[9]),
                                str(row[10]), str(row[11]), str(row[12]), str(row[13])]
                """
                record_entry = [str(row[5]), str(row[9]), str(row[3]), str(row[14]),
                                str(row[1]), str(row[2]), str(row[10]), str(row[15]),
                                str(row[11]), str(row[12]), str(row[4]), str(row[6]), str(row[8])]
                # INSERT RECORD ENTRY INTO TREE
                self.tree.insert('', 0, text=str(row[0]), values=record_entry)
            # }
        # }
        except:  # {
            errorMessage = str(sys.exc_info()[0]) + "\n"
            errorMessage = errorMessage + str(sys.exc_info()[1]) + "\n"
            errorMessage = errorMessage + str(sys.exc_info()[2]) + "\n"
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            typeE = str("TYPE : " + str(exc_type))
            fileE = str("FILE : " + str(fname))
            lineE = str("LINE : " + str(exc_tb.tb_lineno))
            messageE = str("MESG : " + "\n" + str(errorMessage))
            self.the_logger.error("\n" + typeE +
                          "\n" + fileE +
                          "\n" + lineE +
                          "\n" + messageE)
            messagebox.showerror(title="ERROR!",
                                 message=typeE +
                                         "\n" + fileE +
                                         "\n" + lineE +
                                         "\n" + messageE)
        # }
        else:  # {
            self.the_logger.info("Operation Completed Successfully...")
        # }

    # }
    
    def is_valid_account_id(self, the_str): # {
        # the_str - value in %P
        if fnmatch.fnmatch(the_str, str(self.account_id_regex)): # {
            return True
        # }
    # }
    
    def open_search_window(self, event): # {
        # TRY THE FOLLOWING
        try: #{
            # GET NUMBER OF CHILDREN (of ROOT)
            self.children_num = self.root.winfo_children()
            self.the_logger.info("\t CHILDREN BEFORE \n\t\t========>" + str(len(self.children_num)))
        # }
        except: # {
            self.the_logger.error("failed getting the children...")
        # }
        # TRY THE FOLLOWING
        try: # {
            # GET MOUSE LOCATION
            self.mouse_location = pyautogui.position()
            self.the_logger.info("MOUSE LOCATION:\n" + str(self.mouse_location))
            # GET SCREEN RESOLUTION/SIZE
            self.screen_resolution = pyautogui.size()
            self.the_logger.info("SCREEN SIZE:\n" + str(self.screen_resolution))
        # }
        except: # {
            self.the_logger.error("Error determining mouse location & screen size...")
        # }
        # TRY THE FOLLOWING
        try: # {
            if len(self.children_num) > 6: # {
                messagebox.showwarning(title="WARNING:", message="ATTEMPTED TO OPEN MULTIPLE WINDOWS:\nCannot perform action while other window open!")
            # }
            else: # {
                self.search_box = tk.Toplevel(master=self.root)
                # [2020-02-11]\self.search_box.wm_transient(master=self.root)  # MAKE WINDOW TRANS
                self.search_box.wm_transient(master=self.root) # MAKE WINDOW TRANS
                self.search_box.title("[FILTER/SEARCH] - Agilent Custom Quotes Request Log")
                xindex = str(self.mouse_location).find("x=", 0, len(str(self.mouse_location)))
                xend = str(self.mouse_location).find(",", 0, len(str(self.mouse_location)))
                yindex = str(self.mouse_location).find("y=", 0, len(str(self.mouse_location)))
                yend = str(self.mouse_location).rfind(')', 0, len(str(self.mouse_location)))
                x_val = int(str(self.mouse_location)[xindex+2:xend])
                y_val = int(str(self.mouse_location)[yindex+2:yend])
                self.the_logger.info("X == " + str(x_val))
                self.the_logger.info("Y == " + str(y_val))
                # CREATE STR TO HOLD X AND Y LOCATION POSITIONS
                location_str = str('' + str(int(x_val-385)) + "+" + str(int(y_val)) + '')
                self.search_box.geometry(str('450x175+' + location_str))
                self.search_box.resizable(width=False, height=True)
                # [2020-02-03]\\self.search_box.minsize(width=425, height=50)
                # [2020-02-03]\\self.search_box.maxsize(width=550, height=125)
                self.search_box.minsize(width=450, height=175)
                self.search_box.maxsize(width=450, height=350)
                # [2020-02-10]\\self.search_box.minsize(width=450, height=375)
                # [2020-02-10]\\self.search_box.maxsize(width=700, height=600)
                
                # STR holding the search user entered
                # [2020-02-03]\\self.search_box_str = tk.StringVar(master=self.search_box, value=None)
                self.search_box_str = tk.StringVar(master=self.root, value="enter search here...")
                # [2020-02-10]\\self.search_box_str.bind("<Key>", self.on_search)
                
                #### tk.StringVar
                # variable to hold str in combobox
                self.combo_box_str = tk.StringVar(master=self.search_box, value="Tracking #")
                
                """
                ttk.OptionMenu(self.search_box, 
                           self.type_var, 
                           "Select: ", 
                           "web", 
                           "email", 
                           direction="right"
                           ).grid(row=6, column=1, padx=10, pady=10, sticky='w')
                """
                
                #### COMBOBOX
                ttk.Combobox(master=self.search_box,
                             #width=20,
                             textvariable=self.combo_box_str,
                             values=["Tracking #",
                                     "Time Rec.",
                                     "Initials",
                                     "Type",
                                     "Company",
                                     "Contact Person",
                                     "Email Address",
                                     "Account ID",
                                     "Product #",
                                     "PF Quote #",
                                     "SAP QUOTE #",
                                     "Sent",
                                     "Time Sent",
                                     "Notes"]
                             ).pack(side=tk.TOP, fill=tk.BOTH, expand=False)
                
                ttk.Entry(master=self.search_box,
                          textvariable=self.search_box_str,
                          font=("Calibri", 32)
                          #width=40
                          ).pack(side=tk.TOP, fill=tk.BOTH, expand=True)
                
                submit_search = ttk.Button(master=self.search_box,
                                           text="SEARCH",
                                           command=self.on_search,
                                           #width=30
                                           ).pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
                ttk.Button(master=self.search_box,
                           text='REVERT',
                           command=self.view_records,
                           #width=30
                           ).pack(side=tk.RIGHT, fill=tk.BOTH, expand=False)
                self.search_box.focus_set()
                self.the_logger.info("FOCUS == " + str(self.search_box.focus_get()))
                
                
                # GIVE FOCUS TO (ENTRY) SEARCH BOX
                self.search_box.focus_set()
                
                self.search_box.mainloop()
            # }
        # }
        except: # {
            errorMessage = str(sys.exc_info()[0]) + "\n"
            errorMessage = errorMessage + str(sys.exc_info()[1]) + "\n"
            errorMessage = errorMessage + str(sys.exc_info()[2]) + "\n"
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            typeE = str("TYPE : " + str(exc_type))
            fileE = str("FILE : " + str(fname))
            lineE = str("LINE : " + str(exc_tb.tb_lineno))
            messageE = str("MESG : " + "\n" + str(errorMessage))
            self.the_logger.error("\n" + typeE +
                          "\n" + fileE +
                          "\n" + lineE +
                          "\n" + messageE)
            messagebox.showerror(title="ERROR!",
                                 message=typeE +
                                         "\n" + fileE +
                                         "\n" + lineE +
                                         "\n" + messageE)
        # }
        # TRY THE FOLLOWING
        try: # {
            # SET TAGS TO SEARCH CRITERIA
            self.tree.item('00001', tags = ('search'))
            # CHANGE TAGS TO DISPLAY SEARCH RESULTS
            self.tree.tag_configure('search', background = 'yellow')
        # }
        except: # {
            print("FAIL")
        # }
    # }

    def open_modify_window(self, selected_item, the_selection_list, window_location):  # {
        # TRY THE FOLLOWING
        try:  # {
            self.the_logger.info("...MODIFYING RECORD...")
            self.the_logger.info("SELECTION LIST:\n" + str(the_selection_list))
            self.the_logger.info(the_selection_list[1])
            # tracking_number = str(self.tree.item(item)['values'][0])
            # track_num = self.tree.item(self.tree.selection()['text'])
            # old_name = self.tree.item(self.tree.selection())['values'][0]
            self.transient = tk.Toplevel(master=self.root)
            self.transient.wm_transient(master=self.root)  # MAKE WINDOW TRANS
            self.transient.title("EDIT QUOTE - Agilent Custom Quotes Request Log")
            #self.transient.withdraw()
            """
            ################
            # PANED WINDOW #
            ################
            """
            # [2020-01-14]\\THE BELOW WAS 
            """
            self.pw = tk.PanedWindow(master=self.transient, orient=tk.VERTICAL)
            self.pw.pack(side=tk.TOP, expand=tk.Y, fill=tk.BOTH) # padx='2m', pady=2
            self.top_transient = ttk.Label(master=self.pw, text=' >>> Paned Message Panel <<<',
                                            background='#0073e6', foreground='#cc0000', anchor=tk.N)
            self.bottom_transient = ttk.Frame(master=self.pw) # MAIN FRAME
            self.pw.add(self.top_transient)
            self.pw.add(self.bottom_transient)
            self.pw.configure(sashrelief=tk.RAISED)
            """
            """
            ######################################################
            # GET WINDOW GEOMETRY
            ######################################################
            """
            xindex = str(window_location).find("x=", 0, len(str(window_location)))
            xend = str(window_location).find(",", 0, len(str(window_location)))
            yindex = str(window_location).find("y=", 0, len(str(window_location)))
            yend = str(window_location).rfind(')', 0, len(str(window_location)))
            x_val = int(str(window_location)[xindex+2:xend])
            y_val = int(str(window_location)[yindex+2:yend])
            self.the_logger.info("X == " + str(x_val))
            self.the_logger.info("Y == " + str(y_val))
            # CREATE STR TO HOLD X AND Y LOCATION POSITIONS
            location_str = str('' + str(int(x_val-385)) + "+" + str(int(y_val)) + '')
            self.transient.geometry(str('385x255+' + location_str))
            self.transient.resizable(width=False, height=True)
            ##################################################################################
            #### NOTEBOOK WIDGET
            # [2020-01-14]\\transient_tabs = ttk.Notebook(self.right_transient)
            transient_tabs = ttk.Notebook(self.transient)
            # [2020-01-15]\\transient_tabs = ttk.Notebook(self.bottom_transient)
            
            # <><><><><><<><<><><<><><><><><><><><><><><><><><><><><><><><> #
            #### TAB-1 // OLD TRACKING #
            tab_tracking_info = ttk.Frame(master=transient_tabs)
            transient_tabs.add(tab_tracking_info, text='Tracking Info')
            transient_tabs.pack(expand=2, fill=tk.BOTH)
            
            # TRACKING NUMBER #
            ttk.Label(master=tab_tracking_info, 
                      text='Tracking #: '
                      ).grid(row=0, column=0, padx=10, pady=10)
            # GET TRACKING NUMBER FROM "selection_list"
            the_tracking_number = str(the_selection_list[0])
            # TK VARIABLE TO HOLD INPUT As STR
            self.tracking_num = tk.StringVar(master=tab_tracking_info, 
                                             value=the_tracking_number
                                             )
            ttk.Entry(master=tab_tracking_info, 
                                     state='readonly',
                                     textvariable=self.tracking_num,
                                     width=36,
                                     ).grid(row=0, column=1, padx=10, pady=10, sticky='w')
            # TIME RECEIVED (open_time) #
            ttk.Label(master=tab_tracking_info,
                      text='Time Received: '
                      ).grid(row=1, column=0, padx=10, pady=10, sticky='e')
            # GET TIME RECIEVED FROM "self.tree" (old)
            the_time_rec = str(self.tree.item(selected_item)['values'][0])
            self.open_time = tk.StringVar(master=tab_tracking_info,
                                          value=the_time_rec,
                                          )
            ttk.Entry(master=tab_tracking_info,
                                 state='readonly',
                                 textvariable=self.open_time,
                                 width=36,
                                 ).grid(row=1, column=1, padx=10, pady=10, sticky='w')
            # INITIALS #
            ttk.Label(master=tab_tracking_info,
                      text='Initials: '
                      ).grid(row=2, column=0, padx=10, pady=10, sticky=None)
            # GET INITIALS FROM "selection_list"[1] (old)
            the_initials = str(the_selection_list[1])
            self.new_initials = tk.StringVar(master=tab_tracking_info, value=the_initials)
            new_initials_entry_widget = ttk.Entry(master=tab_tracking_info,
                                 state='active',
                                 textvariable=self.new_initials,
                                 width=36,
                                 ).grid(row=2, column=1, padx=10, pady=10, sticky=None)
            # TYPE #
            ttk.Label(master=tab_tracking_info,
                      text='Type: '
                      ).grid(row=3, column=0, padx=10, pady=10, sticky=None)
            # GET RADIO TYPE FROM "selection_list"[7] (old)
            self.new_type_var = tk.StringVar(master=tab_tracking_info, value=str(the_selection_list[7]))
            radio_type_1 = ttk.Radiobutton(master=tab_tracking_info,
                                  variable=self.new_type_var,
                                  value="web", text="web", state=tk.DISABLED, width=20)
            radio_type_1.grid(row=3, column=1, columnspan=2, sticky='w', padx=10, pady=10)
            radio_type_2 = ttk.Radiobutton(master=tab_tracking_info,
                                           variable=self.new_type_var,
                                           value="email", text="email", state=tk.DISABLED, width=20)
            radio_type_2.grid(row=3, column=1, columnspan=3, sticky='e', padx=10, pady=10)
            
            # <><><><><><><><><><><><><><><><><><><><><><><><><><><><><> #
            
            # <><><><><><><><><><><<><><><><><><><><><><><><><><><><><><> #
            #### TAB-2 // ACCOUNT INFO #
            tab_account_info = ttk.Frame(master=transient_tabs)
            transient_tabs.add(tab_account_info, text='Account Info ')
            transient_tabs.pack(expand=2, fill=tk.BOTH)
            
            # COMPANY NAME #
            ttk.Label(master=tab_account_info,
                      text='Company Name: '
                      ).grid(row=0, column=0, padx=10, pady=10)
            # GET COMPANY NAME FROM "selection_list"[8] (old)
            the_company_name = str(the_selection_list[8])
            self.new_company_name = tk.StringVar(master=tab_account_info, value=the_company_name)
            new_company_name_entry_widget = ttk.Entry(master=tab_account_info, 
                                                      state='active',
                                                      textvariable=self.new_company_name,
                                                      width=36
                                                      ).grid(row=0, column=1, padx=10, pady=10, sticky=None)
            
            # CONTACT PERSON #
            ttk.Label(master=tab_account_info,
                      text='Contact Person: '
                      ).grid(row=1, column=0, padx=10, pady=10)
            # GET CONTACT PERSON FROM "selection_list"[12] (old)
            the_contact_person = str(the_selection_list[12])
            self.new_name = tk.StringVar(master=tab_account_info, value=the_contact_person)
            new_contact_person_entry_widget = ttk.Entry(master=tab_account_info, 
                                                        state='active',
                                                        textvariable=self.new_name,
                                                        width=36
                                                        ).grid(row=1, column=1, padx=10, pady=10, sticky=None)
            
            # EMAIL ADDRESS #
            ttk.Label(master=tab_account_info,
                      text="Email Address: "
                      ).grid(row=2, column=0, padx=10, pady=10)
            # GET EMAIL ADDRESS FROM "selection_list"[2] (old)
            the_email_address = str(the_selection_list[2])
            self.new_email = tk.StringVar(master=tab_account_info, value=the_email_address)
            new_email_address_entry_widget = ttk.Entry(master=tab_account_info, 
                      state='active',
                      textvariable=self.new_email,
                      width=36
                      ).grid(row=2, column=1, padx=10, pady=10, sticky=None)
            
            # ACCOUNT ID #
            ttk.Label(master=tab_account_info,
                      text="Account ID: "
                      ).grid(row=3, column=0, padx=10, pady=10)
            # GET ACCOUNT ID FROM "selection_list"[3] (old)
            the_account_id = str(the_selection_list[3])
            self.new_account_id = tk.StringVar(master=tab_account_info, value=the_account_id)
            new_account_id_entry_widget = ttk.Entry(master=tab_account_info, 
                                                    state='active',
                                                    textvariable=self.new_account_id, 
                                                    width=36
                                                    ).grid(row=3, column=1, padx=10, pady=10, sticky=None)
            
            # <><><><><><><><><><><><><><><><><><><><><><><><><><><<><>< #
            #### TAB-3 // QUOTE INFO #
            tab_quote_info = ttk.Frame(master=transient_tabs)
            validation = tab_quote_info.register(self.account_id_validated)
            transient_tabs.add(tab_quote_info, text='Quote Info ')
            transient_tabs.pack(expand=2, fill=tk.BOTH)
            
            # PRODUCT NUMBER #
            ttk.Label(master=tab_quote_info,
                      text="Product #: "
                      ).grid(row=0, column=0, padx=10, pady=10, sticky=None)
            # GET PRODUCT NUMBER FROM "selection_list"[4] (old)
            the_product_number = str(the_selection_list[4])
            self.new_product_number = tk.StringVar(master=tab_quote_info, value=the_product_number)
            new_product_number_entry_widget = ttk.Entry(master=tab_quote_info, 
                                                        state='normal', 
                                                        textvariable=self.new_product_number,
                                                        width=40,
                                                        validate='focusout',
                                                        #validatecommand=(validation, '%P')
                                                        ).grid(row=0, column=1, padx=10, pady=10, sticky=None)
            # [2020-01-08]\\new_product_number_entry_widget['validatecommand'] = (self.root.register(self.is_valid_account_id), '%P')
            
            #####################
            # BIND ENTRY WIDGET #
            #####################
            # [2020-01-08]\\new_product_number_entry_widget.bind('<Key>', self.account_id_validated)
            # PRODFLOW QUOTE NUMBER #
            ttk.Label(master=tab_quote_info,
                      text="PF Quote #: "
                      ).grid(row=1, column=0, padx=10, pady=10, sticky=None)
            # GET PF QUOTE # FROM "selection_list"[11] (old)
            the_pf_quote_num = str(the_selection_list[11])
            self.new_pf_quote_num = tk.StringVar(master=tab_quote_info, value=the_pf_quote_num)
            """
            ############################################################
            # BIND VALIDATION ???
            ############################################################
            """
            validation = self.root.register(self.account_id_validated)
            new_pf_quote_num_entry_widget = ttk.Entry(master=tab_quote_info, 
                                     state=tk.NORMAL, 
                                     textvariable=self.new_pf_quote_num,
                                     width=40,
                                     #validate='focusout',
                                     #validatecommand=(validation, '%P')
                                     ).grid(row=1, column=1, padx=10, pady=10, sticky=None)
            # new_pf_quote_num_entry_widget.bind('<FocusOut>', self.check_quote_convention)
            # [2020-01-08]\\new_pf_quote_num_entry_widget.bind('<FocusIn>', self.turn_red)
            # [2020-01-08]\\new_pf_quote_num_entry_widget['validatecommand'] = (self.root.register(self.is_valid_account_id), '%P')
            # [2020-01-08]\\new_pf_quote_num_entry_widget.bind('<FocusOut>', self.turn_red)
            
            # SAP QUOTE NUMBER #
            ttk.Label(master=tab_quote_info,
                      text="SAP Quote #: "
                      ).grid(row=2, column=0, padx=10, pady=10, sticky=None)
            # GET SAP QUOTE # FROM "selection_list"[9] (old)
            the_sap_quote_num = str(the_selection_list[9]).zfill(7)
            self.new_sap_quote_num = tk.StringVar(master=tab_quote_info, value=the_sap_quote_num)
            new_sap_quote_num_entry_widget = ttk.Entry(master=tab_quote_info, 
                                      state='active', 
                                      textvariable=self.new_sap_quote_num,
                                      width=40).grid(row=2, column=1, padx=10, pady=10, sticky=None)
            
            # SENT OR NOT? #
            ttk.Label(master=tab_quote_info,
                      text='Sent: '
                      ).grid(row=3, column=0, padx=10, pady=10, sticky=None)
            # GET RADIO TYPE FROM "selection_list"[10] (old)
            the_radio_sent_var = str(the_selection_list[10])
            self.the_logger.info("\n\t>>>> SENT? <<<< " + str(the_radio_sent_var))
            self.radio_sent_var = tk.BooleanVar(master=self.root, value=the_radio_sent_var)
            self.the_logger.info("\n\t>>> STILL? <<<< " + str(self.radio_sent_var.get()))
            # CREATE VAR TO HOLD (new) VALUE
            new_radio_sent_var = tk.BooleanVar(master=tab_quote_info, value=bool(self.radio_sent_var))
            # CREATE RADIO BUTTON ** BASED ON CONDITIONS **
            if bool(self.radio_sent_var.get()) is True: # {
                self.the_logger.info(">>>>>>>>>> IS TRUE!")
                self.radio_sent_1 = ttk.Radiobutton(master=tab_quote_info,
                                                    state=tk.DISABLED,
                                                    value=True,
                                                    variable=new_radio_sent_var,
                                                    text="Yes", width=20)
                self.radio_sent_1.grid(row=3, column=1, columnspan=2, sticky='w', padx=10, pady=10)
                self.radio_sent_2 = ttk.Radiobutton(master=tab_quote_info,
                                                    state=tk.DISABLED,
                                                    value=False,
                                                    variable=new_radio_sent_var,
                                                    text="No", width=20)
                self.radio_sent_2.grid(row=3, column=1, columnspan=3, sticky='e', padx=10, pady=10)
            # }
            elif bool(self.radio_sent_var.get()) is False: # {
                self.the_logger.info(">>>>>>>>> IS FALSE!")
                self.radio_sent_1 = ttk.Radiobutton(master=tab_quote_info,
                                                    state=tk.ACTIVE,
                                                    value=True,
                                                    variable=self.radio_sent_var,
                                                    text="Yes", width=20)
                self.radio_sent_1.grid(row=3, column=1, columnspan=2, sticky='w', padx=10, pady=10)
                self.radio_sent_2 = ttk.Radiobutton(master=tab_quote_info,
                                                    state=tk.ACTIVE,
                                                    value=False,
                                                    variabl=self.radio_sent_var,
                                                    text="No", width=20)
                self.radio_sent_2.grid(row=3, column=1, columnspan=3, sticky='e', padx=10, pady=10)
            # }
            """
            self.radio_sent_1 = ttk.Radiobutton(master=tab_quote_info, 
                                           # [2020-01-09]\\state=tk.ACTIVE if len(self.new_pf_quote_num.get()) != 0 and len(self.new_sap_quote_num.get()) != 0 and len(self.new_product_number.get()) != 0 else tk.DISABLED,
                                           # [2020-01-09]\\state = tk.DISABLED if bool(the_radio_sent_var) is True else tk.ACTIVE,
                                           state = tk.ACTIVE if bool(the_radio_sent_var) is False else tk.DISABLED,
                                           variable=new_radio_sent_var,
                                           #value=True if bool(the_radio_sent_var) is True else False, 
                                           text="Yes", width=20)
            self.radio_sent_1.grid(row=3, column=1, columnspan=2, sticky='w', padx=10, pady=10)
            self.radio_sent_2 = ttk.Radiobutton(master=tab_quote_info,
                                           # [2020-01-09]\\state=tk.ACTIVE if len(self.new_pf_quote_num.get()) != 0 else tk.DISABLED,
                                           # [2020-01-09]\\state = tk.ACTIVE if bool(the_radio_sent_var) is False else tk.DISABLED,
                                           # [2020-01-09]\\state = tk.DISABLED if bool(the_radio_sent_var) is True else tk.ACTIVE,
                                           state = tk.ACTIVE, 
                                           variable=new_radio_sent_var,
                                           #value=True if bool(the_radio_sent_var) is False else False, 
                                           text="No", width=20)
            self.radio_sent_2.grid(row=3, column=1, columnspan=3, sticky='e', padx=10, pady=10)
            if bool(the_selection_list[10]) is True: # {
                self.radio_sent_1['state'] = tk.DISABLED
                self.radio_sent_1['value'] = True
                self.radio_sent_2['state'] = tk.DISABLED
                self.radio_sent_2['value'] = False
            # }
            elif bool(the_selection_list[10]) is False: # {
                self.radio_sent_1['state'] = tk.ACTIVE
                self.radio_sent_1['value'] = False
                self.radio_sent_2['state'] = tk.ACTIVE
                self.radio_sent_2['value'] = True
            # }
            """
            
            # <><><><><><><><><><><><><<><><><><><><><><><><><><><><><>< #
            
            # <><><><><><><><><><><><><><><><><><><><><><><><><>
            tab_notes_section = ttk.Frame(master=transient_tabs)
            transient_tabs.add(tab_notes_section, text='Notes ')
            transient_tabs.pack(expand=2, fill=tk.BOTH)
            
            #### TAB-4 // NOTES #
            ttk.Label(master=tab_notes_section,
                      text="Notes: "
                      ).grid(row=0, column=0, padx=10, pady=10, sticky='w')
            # GET NOTES FROM "selection_list"[5] (old)
            the_notes_var = str(the_selection_list[5])
            self.new_notes_var = tk.StringVar(master=tab_notes_section, value=the_notes_var)
            new_notes_entry_widget = tk.Text(master=tab_notes_section, 
                                             height=10, 
                                             width=36,
                                             font=("Calibri", 10)
                                             )
            # insert text into box
            new_notes_entry_widget.insert(tk.INSERT, the_notes_var)
            new_notes_entry_widget.grid(row=0, column=1, padx=10, pady=10, sticky='e')
            
            # [2020-01-06]\\new_notes_text_widget = tk.Text(master=tab_notes_section, height=10, width=36)
            """
            new_notes_entry_widget = tk.Entry(master=tab_notes_section, 
                                               state=tk.NORMAL,
                                               textvariable=self.new_notes_var,
                                               width=20,
                                               ).grid(row=0, column=1, columnspan=4,
                                                      rowspan=2, padx=10, pady=10, sticky='e')
            """
            # FILL NOTES SECTION
            # [2020-01-06]\\notes.insert(tk.INSERT, str("<old notes here>"))
            # [2020-01-06]\\new_notes_text_widget.insert(tk.INSERT, str(the_notes_var))
            # [2020-01-06]\\new_notes_text_widget.grid(row=0, column=1, columnspan=4,
                       #rowspan=2, padx=10, pady=10, sticky='e')
            
            # <><><><><><><<><><><><><><><><><><><><><><><<><><>
            # TAB-5 // HELP TAB # 
            """
            tab_help_info = ttk.Frame(master=transient_tabs)
            transient_tabs.add(tab_help_info, text='Help ')
            transient_tabs.pack(expand=3, fill=tk.BOTH)
            
            # LABELFRAME(S)
            lblframe_help_info = ttk.LabelFrame(master=tab_help_info, text="Section 1")
            lblframe_help_info.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
            
            lblframe_help_info_2 = ttk.LabelFrame(master=tab_help_info, text="Section 2")
            lblframe_help_info_2.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
            """
            
            #### TAB-5 // STATUS TAB
            # FOC
            # AWAITING TECH REVIEW
            # RETURNED / VOID
            # SALES REVIEW
            tab_status = ttk.Frame(master=transient_tabs)
            transient_tabs.add(tab_status, text='STATUS ')
            transient_tabs.pack(expand=2, fill=tk.BOTH)
            
            ttk.Label(master=tab_status,
                      text='Status: '
                      ).grid(row=0, column=0, padx=10, pady=10, sticky='w')
            # ALLOW USER TO SET STATUS!
            the_status_var = str("status_var")
            # [2020-03-04]\\self.new_status_var = tk.StringVar(master=tab_status, value=the_status_var)
            self.new_status_var = tk.IntVar(master=tab_status, value= 0)
            R1 = tk.Radiobutton(tab_status, text="AWAITING SALES REVIEW", variable=self.new_status_var, value = 1)
            R1.grid(row=1, column=0, padx=10, pady=10, sticky='w')
            R2 = tk.Radiobutton(tab_status, text="AWAITING TECH REVIEW", variable=self.new_status_var, value = 2)
            R2.grid(row=1, column=1, padx=10, pady=10, sticky='w')
            R3 = tk.Radiobutton(tab_status, text="FOC", variable=self.new_status_var, value = 3)
            R3.grid(row=2, column=0, padx=10, pady=10, sticky='w')
            R4 = tk.Radiobutton(tab_status, text="RETURNED/VOID", variable=self.new_status_var, value = 4)
            R4.grid(row=2, column=1, padx=10, pady=10, sticky='w')
            """
            new_status_list_box = tk.Listbox(master=tab_status,
                                             height=10,
                                             width=36,
                                             font=("Calibri", 10),
                                             relief=tk.RIDGE,
                                             selectmode='extended'
                                             )
            # insert [**SELECTABLE VALUES**] INTO LIST BOX
            new_status_list_box.insert(0, "FOC")
            new_status_list_box.insert(tk.END, "Awaiting Technical Review")
            new_status_list_box.insert(tk.END, "Returned/VOID")
            new_status_list_box.insert(tk.END, "Awating Sales Review")
            new_status_list_box.grid(row=0, column=1, padx=10, pady=10, sticky='e')
            """
            
            
            #####################################################################################
            # BUTTON (FRAME)
            # button_frame = ttk.Frame(master=root).pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
            
            # SUBMIT BUTTON
            submit_button = ttk.Button(self.transient, text="SUBMIT", command=lambda: self.update_record(
                newname=str(self.new_name.get()), # old_contact_name
                newemail=str(self.new_email.get()), # old_email_address=
                the_type=str(the_selection_list[7]), #
                newcompanyname=str(self.new_company_name.get()), # old_company_name
                newsent=str(new_radio_sent_var.get()) if self.radio_sent_var.get() is True else str(self.radio_sent_var.get()), 
                old_sent=str(the_selection_list[10]), #str(self.radio_sent_var.get()),
                open_time=str(self.tree.item(selected_item)['values'][0]),
                # [2020-01-14]\\newnotes=str(self.new_notes_var.get()), #old_notes=str(the_selection_list[5]),
                newnotes=str(new_notes_entry_widget.get("1.0", tk.END)),
                newinitials=str(self.new_initials.get()), #old_initials=str(the_selection_list[1]),
                newaccountid=str(self.new_account_id.get()), #old_account_id=str(the_selection_list[3]),
                newproductnum=str(self.new_product_number.get()), #old_product_num=str(the_selection_list[4]),
                newpfnum=str(self.new_pf_quote_num.get()), #old_pf_num=str(the_selection_list[11]),
                newsapnum=str(self.new_sap_quote_num.get()), # old_sap_num=str(the_selection_list[9]),
                tracking_number=str(the_selection_list[0])))
            submit_button.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            submit_button.bind('<Enter>', self.check_quote_convention)
            submit_button.bind('<Leave>', self.check_quote_convention)
            # [2020-01-08]\\submit_button.bind('<FocusOut>', self.check_quote_convention)
            # [2020-01-08]\\submit_button.bind('<Key>', self.check_quote_convention)
            
            # CANCEL BUTTON
            cancel_button = ttk.Button(self.transient, text="CANCEL", command=self.transient.destroy)
            cancel_button.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
            
            """
            validate_button = ttk.Button(self.transient, text="VALIDATE")
            validate_button.bind("<Enter>", self.turn_red)
            validate_button.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
            """
            self.transient.mainloop()
        # }
        except:  # {
            errorMessage = str(sys.exc_info()[0]) + "\n"
            errorMessage = errorMessage + str(sys.exc_info()[1]) + "\n"
            errorMessage = errorMessage + str(sys.exc_info()[2]) + "\n"
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            typeE = str("TYPE : " + str(exc_type))
            fileE = str("FILE : " + str(fname))
            lineE = str("LINE : " + str(exc_tb.tb_lineno))
            messageE = str("MESG : " + "\n" + str(errorMessage))
            self.the_logger.error("\n" + typeE +
                          "\n" + fileE +
                          "\n" + lineE +
                          "\n" + messageE)
            messagebox.showerror(title="ERROR!",
                                 message=typeE +
                                         "\n" + fileE +
                                         "\n" + lineE +
                                         "\n" + messageE)
        # }
        else:  # {
            self.the_logger.info("Operation Completed Successfully...")
        # }

    # }
    
    def open_admin_window(self): # {
        # TRY THE FOLLOWING
        try: # {
            self.admin_transient = tk.Toplevel(master=self.root)
            # [2020-03-02]\\self.admin_transient = tk.Toplevel(master=the_root)
            self.admin_transient.title("ADMIN TOOLS - Agilent Custom Quotes Request Log")
            self.admin_transient.geometry('500x60+250+250')
            self.admin_transient.resizable(width=False, height=False)
            # LABEL 
            ttk.Label(master=self.admin_transient, 
                      text="Current T-#: "
                      ).grid(row=0, column=0, padx=10, pady=10, sticky='e')
            
            # PULL T-NUMBER FROM PICKLE
            with open(Path(self.t_count_filename), 'rb') as f: # {
                # load value from file
                quotes_t_number = pickle.load(f)
            # }
            
            t_pickle_var = tk.IntVar(master=self.admin_transient, 
                                        value=str(quotes_t_number)
                                        )
            # SPINBOX FOR ADMIN
            ttk.Spinbox(master=self.admin_transient,
                        from_=0,
                        to=999999,
                        textvariable=t_pickle_var
                        ).grid(row=0, column=1, padx=10, pady=10, sticky='w')
            # [2020-01-16]]\\
            """
            ttk.Entry(master=self.admin_transient,
                      textvariable=t_pickle_var
                      ).grid(row=0, column=1, padx=10, pady=10, sticky='e')
            """
            # SUBMIT BUTTON
            ttk.Button(master=self.admin_transient,
                       text="SUBMIT OVERWRITE",
                       ).grid(row=0, column=2, columnspan=2, padx=10, pady=10, sticky='e')
            self.admin_transient.mainloop()
        # }
        except: # {
            errorMessage = str(sys.exc_info()[0]) + "\n"
            errorMessage = errorMessage + str(sys.exc_info()[1]) + "\n"
            errorMessage = errorMessage + str(sys.exc_info()[2]) + "\n"
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            typeE = str("TYPE : " + str(exc_type))
            fileE = str("FILE : " + str(fname))
            lineE = str("LINE : " + str(exc_tb.tb_lineno))
            messageE = str("MESG : " + "\n" + str(errorMessage))
            self.the_logger.error("\n" + typeE +
                          "\n" + fileE +
                          "\n" + lineE +
                          "\n" + messageE)
            messagebox.showerror(title="ERROR!",
                                 message=typeE +
                                         "\n" + fileE +
                                         "\n" + lineE +
                                         "\n" + messageE)
        # }
        else: # {
            self.the_logger.info("Operation Completed Successfully...")
        # }
    # }

    def update_record(self, newname,
                      newemail, the_type,
                      newcompanyname,
                      newsent, old_sent, open_time,
                      newnotes,
                      newinitials,
                      newaccountid,
                      newproductnum,
                      newpfnum,
                      newsapnum, tracking_number):  # {
        # [2020-01-10]\\messagebox.showinfo(message="NEW-SENT: \t" + str(newsent))
        # CALL THE "check_quote_progress() FUNCTION HERE
        # [ 2019-12-27 ] == addition of "initials" into METHOD
        # [ 2019-12-30 ] == addition of "account_id" and "prodflow quote #"
        # [ 2019-12-30 ] == addition of "sap quote #" and "price"
        """
        # TRY THE FOLLOWING
        try: # {
            # CHECK & VALIDATE THE ENTRY BOXES SO NONE ARE EMPTY
            if self.updated_records_validated(new_name=newname, new_email=newemail,
                                              new_initals=newinitials, new_account_id=newaccountid,
                                              new_price=newprice): # {
                print("NONE LEFT EMPTY!")
            # }
            else: # {
                print("LEFT SOME EMPTY YOU NOOB!")
            # }
        # }
        except: # {
            print("FAILLLLLL")
        # }
        """
        # IF NONE OF THE **IMPORTANT** ENTRY BOXES ARE LEFT EMPTY
        if len(str(newinitials)) != 0 and len(str(newaccountid)) != 0:  # {
            self.the_logger.info("UPDATE-RECORD FIELDS ARE ALL FILLED IN COMPLETELY!")
            # SETUP STR TO HOLD THE VALUES THE USER WISHES TO CHANGE
            display_str = "YOU ENTERED:\n\n" 
            display_str += "contact name:\t\t" + str(newname) + "\n"
            display_str += "email address:\t\t" + str(newemail) + "\n"
            display_str += "company name:\t\t" + str(newcompanyname) + "\n"
            display_str += "sent:\t\t\t" + str(newsent) + "\n"
            display_str += "initials:\t\t\t" + str(newinitials) + "\n"
            display_str += "account id:\t\t" + str(newaccountid) + "\n"
            display_str += "new product #:\t\t" + str(newproductnum) + "\n"
            display_str += "new PF Quote #:\t\t" + str(newpfnum) + "\n"
            display_str += "new SAP Quote #:\t\t" + str(newsapnum) + "\n"
            display_str += "-------------------------------------------------------------\n"
            display_str += "new notes:\n\n" + str(newnotes) + "\n"
            # ASK THE USER IF THEY ARE SURE WITH THEIR COMPLETION?
            confirm_box = messagebox.askokcancel(title="Confirm Update", message=str(display_str))
            self.the_logger.info(confirm_box)
            if str(confirm_box) == "True":  # {
                # TRY THE FOLLOWING
                try: # {
                    # create engine
                    # [2020-02-10]\\engine = create_engine('sqlite:///e:/_Quotes_Tracker/data/quotes_tracker.db')
                    engine = create_engine('sqlite:///' + str(self.db_filename))
                    # Create connection to DB (from engine)
                    conn = engine.connect()
                    # PULL ENTIRE DB INTO A DATAFRAME
                    # [2020-01-21]\\SQL_Table = pd.read_sql_table(table_name="quotes", con=conn, index_col=["tracking_number"])
                    # CREATE STR VARIABLE TO HOLD SQL QUERY
                    sql_query = "SELECT * FROM [quotes] WHERE [tracking_number] = '" + str(tracking_number) + "'"
                    self.the_logger.info("THE_QUERY == " + str(sql_query))
                    self.SQL_Table = pd.read_sql_query(sql=str(sql_query),
                                                  con=conn)
                    self.the_logger.info(self.SQL_Table.describe())
                    """
                    <<<<<<<<<< DETERMINE WHICH ROWS ARE "newly_sent" >>>>>>>>>
                    """
                    # [2020-01-21]\\ DETERMINED THAT pd.read_sql_query better!
                    """
                    # USING BOOLEAN VALUES
                    # create variable with TRUE IF sent is TRUE
                    all_sent = SQL_Table['sent'] =="True"
                    # create variable with TRUE if turn_around is NOT "None"
                    already_sent = SQL_Table['turn_around'] != "None"
                    # create variable with TRUE if turn_around is "None"
                    recently_sent = SQL_Table['turn_around'] == "None"
                    # select all cases where SENT IS TRUE and TURN_AROUND is NONE
                    self.need_timestamps = SQL_Table[all_sent & recently_sent]
                    # ALSO CREATE DATAFRAME WHERE ALL SENT IS TRUE
                    self.sent_df = SQL_Table[all_sent]
                    logging.info(self.need_timestamps.describe())
                    logging.info(type(self.need_timestamps))
                    """
                    """
                    <<<<<<<<<<<< LOOP THRU DATAFRAME PULLED FROM DB >>>>>>>>>>
                    """
                    """
                    # counter
                    x = 0
                    # WHILE WE ARE STILL LOOPING THRU DATAFRAME...
                    while x < len(self.need_timestamps): # {
                        logging.info("==========")
                        name = str(self.need_timestamps.iloc[x, 0])
                        email = str(self.need_timestamps.iloc[x, 1])
                        type_ = str(self.need_timestamps.iloc[x, 2])
                        sent_ = str(self.need_timestamps.iloc[x, 3])
                        open_time = pd.Timestamp(self.need_timestamps.iloc[x, 4])
                        close_time = pd.Timestamp(self.need_timestamps.iloc[x, 5])
                        turn_around = str(self.need_timestamps.iloc[x, 6])
                        notes  = str(self.need_timestamps.iloc[x, 7])
                        ##########################################
                        # CREATE TEMPORARY TIMESTAMP FOR MEOW
                        meow_ts = pd.Timestamp.now()
                        # COMPUTE TURN AROUND TIME
                        time_start = pd.Timestamp(open_time)
                        logging.info("TIME START == " + str(time_start)[:19])
                        logging.info("TIME END == " + str(meow_ts)[:19])
                        # [2020-01-21]\\run_time = str(meow_ts - time_start)[:18]
                        run_time = str(close_time - time_start)[:18]
                        logging.info("RUN TIME == " + str(run_time))
                        # INCREMENT X
                        x += 1
                    # }
                    else: #{
                        logging.info("Succesfully looped thru " + str(x) + "entries...")
                    # }
                    """
                # }
                except: # {
                    logging.info("FAILED PULLING DB into DATAFRAME!")
                    errorMessage = str(sys.exc_info()[0]) + "\n"
                    errorMessage = errorMessage + str(sys.exc_info()[1]) + "\n"
                    errorMessage = errorMessage + str(sys.exc_info()[2]) + "\n"
                    exc_type, exc_obj, exc_tb = sys.exc_info()
                    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                    typeE = str("TYPE : " + str(exc_type))
                    fileE = str("FILE : " + str(fname))
                    lineE = str("LINE : " + str(exc_tb.tb_lineno))
                    messageE = str("MESG : " + "\n" + str(errorMessage))
                    self.the_logger.error("\n" + typeE +
                                  "\n" + fileE +
                                  "\n" + lineE +
                                  "\n" + messageE)
                    messagebox.showerror(title="ERROR!",
                                         message=typeE +
                                         "\n" + fileE +
                                         "\n" + lineE +
                                         "\n" + messageE)
                # }
                else: # {
                    self.the_logger.info("[pull-DB_2_DF] Operation Completed Successfully...")
                    # CLOSE CONNECTION?
                    conn.close()
                # }
                # TRY THE FOLLOWING
                try:  # {
                    self.the_logger.info("UPDATING RECORD...")
                    self.the_logger.info("NEW_SENT RADIO VAR [passed_thru_function] == " + str(newsent))
                    # CHECK IF SENT HAS BEEN SWITCHED!
                    """
                    [2020-01-16]
                    << edited so that it updates:
                        name, email, type, notes, initials, account_id, 
                        prodflow_quote_number, sap_quote_number, company_name, product_number
                        THEN call FUNCTION or pull entire database as DATAFRAME 
                    """
                    # DETERMINE IF SENT OR NOT PRIOR TO UPDATE
                    # [2020-01-22]\\is_sent = self.SQL_Table["turn_around"].isin(["None"])
                    # [2020-01-22]\\logging.info("IS_SENT:\n" + str(is_sent.describe()))
                    # newly_sent = self.SQL_Table["turn_around"].isin(["None"]) # boolean value
                    # IF THERE IS ALREADY A TIMESTAMP (aready closed)
                    ###########################################################################
                    # IF SO UPDATE: sent, close_time, turn_around AND ALSO name, email, notes
                    # [2019-12-27]\\if bool(newsent) is True:  # {
                    if newsent == "True":  # {
                        # get/check if there are any "NONE" values in turn around column
                        newly_sent = self.SQL_Table["turn_around"].isin(["None"])
                        # [2020-01-22]\\
                        """
                        messagebox.showinfo(message=str(newly_sent))
                        messagebox.showinfo(message=str(self.SQL_Table["close_time"][0]))
                        messagebox.showinfo(message=str(newly_sent[0]))
                        """
                        # IF THE QUOTE HAS ALREADY BEEN "sent"
                        if bool(newly_sent[0]) is False: # {
                            # reassign closing time to old value
                            closing_time = str(self.SQL_Table["close_time"][0])
                            messagebox.showinfo(message="closing_time == " + str(closing_time))
                            # reassign "run_time" to old turn_around value
                            run_time = str(self.SQL_Table["turn_around"][0])
                            messagebox.showwarning(title="ALREADY CLOSED (previous submit)",
                                                message="There is ALREADY A TIMESTAMP (already closed)")
                        # }
                        # ELSE... IT HAS NOT BEEN SENT YET (no turn around / close time)
                        else: # {
                            # GET START TIME
                            start_time = pd.Timestamp(ts_input=str(self.SQL_Table["open_time"][0]))
                            self.the_logger.info("START-TIME == " + str(start_time))
                            # CREATE TEMPORARY TIMESTAMP
                            time_meow = pd.Timestamp.now()
                            # DETERMINE TURN_AROUND TIME
                            run_time = str(time_meow - start_time)[:18]
                            self.the_logger.info("RUN-TIME == " + str(run_time))
                            # set close time to the current time
                            closing_time = str(time_meow)[:19]
                            # [2020-01-22]\\message_str = "\nclose time: " + str(closing_time) + "\nTurn around: " + str(run_time)
                            """
                            messagebox.showinfo(title="NEWLY CLOSED ! (this submit)", 
                                                message="SHOWING INFO:\nTURN AROUND TIME: " + str(self.SQL_Table["turn_around"][0]) + message_str)
                            """
                        # }
                        # CHECKED IF THERE IS NO TURN AROUND TIME
                        self.the_logger.info("YES THERE IS TURN AROUND! NO NEED TO UPDATE CLOSE TIME")
                        self.the-logger.info(self.SQL_Table["close_time"][0])
                        query = 'UPDATE quotes ' \
                                'SET name=?, email=?, type=?, sent=?, close_time=?, turn_around=?, notes=?, initials=?, account_id=?, prodflow_quote_number=?, sap_quote_number=?, company_name=?, product_number=?' \
                                'WHERE tracking_number=?'
                        parameters = (newname, newemail, the_type, newsent, str(closing_time), # WAS: time_meow
                                      str(run_time), newnotes, newinitials, newaccountid,
                                      newpfnum, newsapnum, newcompanyname, newproductnum,
                                      tracking_number)
                        # EXECUTE
                        self.execute_db_query(query, parameters)
                        self.transient.destroy()
                        self.message['text'] = 'Quote Record of {} modified'.format(tracking_number)
                        self.view_records()
                    # }
                    # NOT BEEN SWITCHED OVER YET
                    # ONLY UPDATE: name, email, notes,
                    # [2019-12-29]... initials
                    # [2019-12-30]... ACCOUNT_ID, PRODFLOW QUOTE #, SAP QUOTE #
                    # [2020-01-07]... COMPANY NAME
                    else:  # {
                        self.the_logger.info("\n\t\t\t>>>>>>> NOT SWITCH [sent] OVER!")
                        # CLOSING TIME == OLD CLOSING TIME
                        query = 'UPDATE quotes SET name=?, email=?, type=?, notes=?, initials=?, account_id=?, prodflow_quote_number=?, sap_quote_number=?, company_name=?, product_number=?' \
                                'WHERE tracking_number=? '
                        parameters = (newname, newemail, the_type, newnotes, newinitials,
                                      newaccountid, newpfnum, newsapnum, newcompanyname, newproductnum,
                                      tracking_number)
                        self.the_logger.info("QUERY:\n" + str(query) + "\nPARAMS:\n" + str(parameters))
                        # EXECUTE
                        self.execute_db_query(query, parameters)
                        self.transient.destroy()
                        self.message['text'] = 'Quote Record of {} modified'.format(tracking_number)
                        self.view_records()
                    # }
                    ##############################################################################
                # }
                except:  # {
                    errorMessage = str(sys.exc_info()[0]) + "\n"
                    errorMessage = errorMessage + str(sys.exc_info()[1]) + "\n"
                    errorMessage = errorMessage + str(sys.exc_info()[2]) + "\n"
                    exc_type, exc_obj, exc_tb = sys.exc_info()
                    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                    typeE = str("TYPE : " + str(exc_type))
                    fileE = str("FILE : " + str(fname))
                    lineE = str("LINE : " + str(exc_tb.tb_lineno))
                    messageE = str("MESG : " + "\n" + str(errorMessage))
                    self.the_logger.error("\n" + typeE +
                                  "\n" + fileE +
                                  "\n" + lineE +
                                  "\n" + messageE)
                    messagebox.showerror(title="ERROR!",
                                         message=typeE +
                                                 "\n" + fileE +
                                                 "\n" + lineE +
                                                 "\n" + messageE)
                # }
                else:  # {
                    self.the_logger.info("Operation Completed Successfully...")
                # }
            # }
            else:  # {
                self.the_logger.info("USER SELECTED NOT READY !...")
                self.transient.destroy()
            # }
        # }
        else:  # {
            # [2020-01-10]\\self.message['text'] = 'MISSING REQUIRED FIELDS(S):\n Initals\n AccountID'
            messagebox.showwarning(parent=self.root, title="WARNING", message="MISSING REQUIRED FIELD(S):\n\n\tInitials\n\nPlease re-open quote to edit")
            # EXIT OUT OF ADD-ON BOX
            self.transient.destroy()
        # }

    # }

    """
    def updated_records_validated(self, new_name, new_email, new_initials,
                                  new_account_id, new_price): # {
        # TRY THE FOLLOWING
        try: # {
            return len(new_name) != 0 \
                and len(new_email) != 0 \
                    and len(new_initials) != 0 \
                        and len(new_account_id) != 0 \
                            and len(new_price) != 0
        # }
        except: # {
            errorMessage = str(sys.exc_info()[0]) + "\n"
            errorMessage = errorMessage + str(sys.exc_info()[1]) + "\n"
            errorMessage = errorMessage + str(sys.exc_info()[2]) + "\n"
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            typeE = str("TYPE : " + str(exc_type))
            fileE = str("FILE : " + str(fname))
            lineE = str("LINE : " + str(exc_tb.tb_lineno))
            messageE = str("MESG : " + "\n" + str(errorMessage))
            logging.error("\n" + typeE +
                          "\n" + fileE +
                          "\n" + lineE +
                          "\n" + messageE)
            messagebox.showerror(title="ERROR!",
                                 message=typeE +
                                         "\n" + fileE +
                                         "\n" + lineE +
                                         "\n" + messageE)
        # }
        else:  # {
            logging.info("Operation Completed Successfully...")
        # }
    # }
    """


# }

# [2020-01-31]\\//[2020-03-03]
"""
class RefreshTable(Thread): # {
    
    def __init__(self, root, duration): # {
        # [2020-01-30]\\super().__init__(root)
        # Initialize the Thread 
        Thread.__init__(self)
        self.root = root
        self.duration = duration
    # }
    
    def run(self): # {
        # Run the Thread
        amount = self.duration
        # BEGIN INFINITE LOOP
        while 1: # {
            print("SLEEPING FOR " + str(amount) + " SECONDS...")
            sleep(amount)
        # }
    # }
    
# }
"""

# [2020-03-02]\\
"""
def setup_logger():  # {
    # TRY THE FOLLOWING
    try:  # {
        logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s: %(message)s, FROM=%(funcName)s, LINENO=%(lineno)d',
                            datefmt='%Y-%m-%d-%H%M%S',
                            filemode='a')
    # }
    except:  # {
        errorMessage = str(sys.exc_info()[0]) + "\n"
        errorMessage = errorMessage + str(sys.exc_info()[1]) + "\n"
        errorMessage = errorMessage + str(sys.exc_info()[2]) + "\n"
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        typeE = str("TYPE : " + str(exc_type))
        fileE = str("FILE : " + str(fname))
        lineE = str("LINE : " + str(exc_tb.tb_lineno))
        messageE = str("MESG : " + "\n" + str(errorMessage))
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
    else:  # {
        logging.info("Operation Completed Successfully...")
    # }


# }
"""

# [2020-01-31]\\
"""
def create_threads(): # {
    # Create a group of threads
    for i in range(6): # {
        name = "Thread #%s" % (i+1)
        my_thread = RefreshTable(name, 5)
        my_thread.start()
    # }
# }
"""

class CheckVersionNumber(Thread): # {
    
    def __init__(self): # {
        # INIT the Thread
        Thread.__init__(self)
        self.run()
    # }
    
    def run(self): # {
        # Run the Thread
        while 1: # {
            # TRY THE FOLLOWING
            try: # {
                logger.info("CHECKING VER...")
                # LOAD IN VER FILE
                df_ver_file = pd.read_csv(AgilentQuotesTracker.ver_file, header=None, engine='python')
                logger.info(">> CORRECT (current) == " + str(df_ver_file.iloc[0, 0]))
                logger.info(">> current (actual) == " + str(AgilentQuotesTracker.version_number))
                # CHECK IF RUNNING MOST RECENT VERSION OF APPLICATION
                if str(df_ver_file.iloc[0, 0]) != str(AgilentQuotesTracker.version_number): # {
                    logger.error("FAILLLLLLL! qutting in 5...")
                    messagebox.showerror(title="Version ERROR!",
                                         message="Running out-dated version...\nNow exiting....")
                    sys.exit(69)
                # }
                else: # {
                    sleep(30)
                # } 
            # }
            except: # {
                errorMessage = str(sys.exc_info()[0]) + "\n"
                errorMessage = errorMessage + str(sys.exc_info()[1]) + "\n"
                errorMessage = errorMessage + str(sys.exc_info()[2]) + "\n"
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                typeE = str("TYPE : " + str(exc_type))
                fileE = str("FILE : " + str(fname))
                lineE = str("LINE : " + str(exc_tb.tb_lineno))
                messageE = str("MESG : " + "\n" + str(errorMessage))
                logger.error("\n" + typeE +
                              "\n" + fileE +
                              "\n" + lineE +
                              "\n" + messageE)
                messagebox.showerror(title="ERROR!",
                                     message=typeE +
                                         "\n" + fileE +
                                         "\n" + lineE +
                                         "\n" + messageE)
            # }
            else: # {
                #logger.the_logger.info("Operation Completed ")
                print("Operation Completed Succesfully")
            # }
        # } 
    # }
# }

# MAIN BOILERPLATE
if __name__ == "__main__":  # {
    # [2020-01-30]\\create_threads()
    # SETUP LOGGER
    # [2020-03-02]\\setup_logger()
    # [2020-02-12]\\logger = Logger(logging_output_dir="E:/_Quotes_Tracker/log/")
    # get/set username (person logged in)
    user = str(os.environ.get("USERNAME"))
    print("user:\t" + str(user))
    # create file path for user logs
    # [2020-03-02]\\user_path= os.path.join("E:/_Quotes_Tracker/log/", user)
    logger = Logger(logging_output_dir="E:/_Quotes_Tracker/log/").logger
    window = tk.Tk()
    application = AgilentQuotesTracker(root=window, the_logger=logger)
    # ver_checker = CheckVersionNumber()
    application.check_version_number_in_thread()
    # [2020-01-29]\\application.refresh_table()
    # [2020-01-03]\\application.tick()  # BEGIN "COUNTING" TIME(STAMP)
    window.config()
    window.mainloop()
# }