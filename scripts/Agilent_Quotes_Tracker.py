"""


"""

"""
Created on Mon Dec 9 12:05:28 2019

TO-DO:
( ) - clear entry boxes when new QUOTE is created/submitted
( ) - import/export from and to .xlsx

EDITS:
12/18/19 - made database accessible via anywhere by file_path to E_DRIVE
         - calls "new_records_validated()" function to fail-check new DB entry
12/26/19 - quotes naming convention to properly create _QUOTES_T_NUMBER_
         - added COLUMNS [initials], [sap_quote_number], and [product_number]
01/03/20 - changed CREATE tab to contain proper tk.StringVar variables (ttk)
01/09/20 - included validation checks for ACCOUNT ID, PF QUOTE #, SAP QUOTE #

@author: derbates
"""

# IMPORT THE GOODS
import os, sys, time
from time import sleep
from pathlib import Path
import fnmatch, glob, shutil
import datetime
import tkinter as tk
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


class AgilentQuotesTracker():  # {

    db_filename = "E:/_Quotes_Tracker/data/quotes_tracker.db"
    #db_filename = "C:/Temp/E/data/quotes_tracker.db"
    t_count_filename = "E:/_Quotes_Tracker/config/quotes_t_number.pkl"
    #t_count_filename = "C:/Temp/E/config/quotes_t_number.pkl"
    time1 = ""
    # REGEX STRINGS FOR FILE NAMING CONVENTIONS
    account_id_regex = "????????"
    # [2020-01-09]\\account_id_regex = "[*][*][*][*][*][*][*][*][*]"
    pf_quote_regex = "[0-9][0-9][0-9][0-9][0-9][0-9][-][0-9][0-9][0-9]"
    sap_quote_regex = "[0-9][0-9][0-9][0-9][0-9][0-9][0-9]"
    

    def __init__(self, root):  # {
        self.root = root
        self.root.title("Agilent Quotes Tracker")
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
        self.root.minsize(width=1175, height=600)
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
        self.create_gui()

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
        else:  # {
            logging.info("Operation Completed Successfully...")
            return query_result

    # }

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
        else:  # {
            logging.info("Operation Completed Successfully...")
        # }

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

    def create_gui(self):  # {
        # TRY THE FOLLOWING
        try:  # {
            # [2019-12-11]\\self.create_menubar()
            self.create_ttk_styles(the_style="radiance")
            # [2019-12-11]\\self.create_menubar()
            self.create_menubar()
            self.create_left_side()
            self.create_tab_control()
            self.create_tab_containers()
            self.fill_tab_containers()
            self.create_right_side()
            self.create_tree_view()
            self.view_records()
            self.root.config(menu=self.menubar)
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
        else:  # {
            logging.info("Operation Completed Successfully...")
        # }

    # }

    def create_menubar(self):  # {
        self.menubar = tk.Menu(self.root)
        # MENU-BAR ^^
        self.filemenu = tk.Menu(master=self.menubar,
                                borderwidth=3,
                                background="#0C85CE",
                                font=("Comfortaa", 16),
                                tearoff=0)
        self.filemenu.add_command(label="Update Log", command="")
        self.filemenu.add_command(label="About", command="")
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Exit", command=self.root.destroy)
        # FILE SUB-MENU ^^
        self.menubar.add_cascade(foreground="#000000", 
                                 label="File", 
                                 menu=self.filemenu, 
                                 activebackground="#d9d9d9", 
                                 activeforeground="#111111",
                                 background="#d9d9d9")
        self.editmenu = tk.Menu(master=self.root,
                                borderwidth=3,
                                background="#9e0ccf",
                                font=("Impact", 16),
                                tearoff=0)
        self.editmenu.add_command(label="Search", command="")
        self.editmenu.add_separator()
        self.editmenu.add_command(label="Copy Cell", command="")
        self.editmenu.add_command(label="Select All", command="")
        # EDIT SUB-MENU ^^
        self.menubar.add_cascade(label="Edit", menu=self.editmenu)
        self.helpmenu = tk.Menu(master=self.menubar,
                                borderwidth=3,
                                background="#ffbf00",
                                font=("Courier New", 16),
                                relief=tk.GROOVE,
                                tearoff=0)
        self.helpmenu.add_command(label="Help Index", command="")
        self.helpmenu.add_command(label="About...", command="")
        # HELP SUB-MENU ^^ 
        self.menubar.add_cascade(label="Help", menu=self.helpmenu)
        self.adminmenu = tk.Menu(master=self.root,
                                 borderwidth=3,
                                 background='#3d4043',
                                 font=("Sourcecode Pro", 16),
                                 relief=tk.RIDGE,
                                 tearoff=1)
        self.adminmenu.add_command(label="Login/edit", command="")
        self.adminmenu.add_command(label="RESRESH TABLE", command=self.view_records)
        self.menubar.add_cascade(label="Table Tools", menu=self.adminmenu)
        # ADMIN SUB-MENU ^^
    # }

    def create_ttk_styles(self, the_style):  # {
        # TRY THE FOLLOWING:
        try:  # {
            themes = sorted(ttk.Style().theme_names())
            for t in themes:  # {
                logging.info(str(t))
            # }
            # CONFIGURE THE STYLE
            # [2019-12-31]\\self.style = ttk.Style()
            self.style = ThemedStyle(self.root)
            # # STYLE THEME
            self.style.set_theme("blue") # radiance, black, scidblue, kroc, keramik, equilux
            # Modify the font of the body
            self.style.configure("mystyle.Treeview", highlightthickness=4, bd=4, font=('Calibri', 9))
            # Modify the font of the headings
            self.style.configure("mystyle.Treeview.Heading", font=('Calibri', 12, 'bold'))
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

    def create_left_icon(self):  # {
        photo = tk.PhotoImage(file='icons/agilent_logo-Copy1.png')
        label = tk.Label(image=photo, bg="#0c85ce")
        label.image = photo
        label.grid(row=0, column=0, columnspan=2, sticky='SW')

    # }

    def create_left_side(self):  # {
        # CREATE FRAME CONTAINER
        self.leftframe = tk.Frame(self.root)
        # [2019-12-12]\\self.leftframe.pack(side=tk.LEFT, fill=tk.BOTH, expand=True) # fill=tk.Both
        # [2019-12-12]\\self.leftframe.pack(side=tk.LEFT, fill=tk.Y, expand=True)
        # [2019-12-12]\\self.leftframe.pack(side=tk.LEFT, fill=tk.BOTH, expand=False)
        # [2019-12-26]\\self.leftframe.pack(side=tk.LEFT, fill=tk.X, expand=False)
        self.leftframe.pack(side=tk.LEFT, fill=tk.Y, expand=False)
        # BIND FUNCTIONS TO FRAME
        self.leftframe.bind('<Leave>', self.clear_message_area)

    # }

    def create_tab_control(self):  # {
        # TRY THE FOLLOWING
        try:  # {
            # CREATE MESSAGE AREA
            self.message = ttk.Label(master=self.leftframe, text='',
                                     font=("Times New Roman", 12, 'italic'), foreground='red')
            # self.message.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
            self.message.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

            # NOTEBOOK WIDGET
            self.tab_control = ttk.Notebook(self.leftframe)

            # TAB-1 // CREATE
            self.tab1 = ttk.Frame(master=self.tab_control)
            self.tab_control.add(self.tab1, text='CREATE')
            self.tab_control.pack(expand=2, fill=tk.BOTH)
            
            
            # TAB-2 // FILTER TOOLS
            self.tab2 = ttk.Frame(master=self.tab_control)
            self.tab_control.add(self.tab2, text='FILTER')
            self.tab_control.pack(expand=2, fill=tk.BOTH)

            # TAB-3 // IMPORT TOOLS
            self.tab3 = ttk.Frame(master=self.tab_control)
            self.tab_control.add(self.tab3, text='IMPORT')
            # [2019-12-26]\\self.tab_control.pack(expand=2, fill=tk.BOTH)
            self.tab_control.pack(expand=2, fill=tk.BOTH)

            # TAB-4 // EXPORT TOOLS
            self.tab4 = ttk.Frame(master=self.tab_control)
            self.tab_control.add(self.tab4, text='EXPORT')
            self.tab_control.pack(expand=2, fill=tk.BOTH)
            
            
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

    def create_tab_containers(self):  # {
        # TRY THE FOLLOWING:
        try:  # {
            # Create the CREATE Tab Container
            # [2020-01-03]\\self.lblframe_create = ttk.LabelFrame(master=self.tab1, text="Enter the following information:")
            self.lblframe_create = ttk.Frame(master=self.tab1)
            # [2019-12-30]\\self.lblframe_create.pack(anchor=tk.CENTER, fill=tk.BOTH, expand=True)
            self.lblframe_create.pack(anchor=tk.CENTER, fill=tk.BOTH, expand=False)
            
            # Create the FILTER Tab Container
            self.lblframe_filter = ttk.Frame(master=self.tab2)
            self.lblframe_filter.pack(anchor=tk.CENTER, fill=tk.BOTH, expand=False)
            
            # Create the IMPORT Tab Container
            self.lblframe_import = ttk.Frame(master=self.tab3)
            self.lblframe_import.pack(anchor=tk.CENTER, fill=tk.BOTH, expand=False)
            
            # Create the EXPORT Tab Container
            self.lblframe_export = ttk.Frame(master=self.tab4)
            self.lblframe_export.pack(anchor=tk.CENTER, fill=tk.BOTH, expand=False)

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
            logging.critical("\n" + typeE +
                             "\n" + fileE +
                             "\n" + lineE +
                             "\n" + messageE)
        # }
        else:  # {
            logging.info("Operation completed Successfully...")
        # }

    # }

    def fill_tab_containers(self):  # {
        # TRY THE FOLLOWING
        try:  # {
            # ()()()()()()()()()()()()()()()()()()()()()()()()()()(()()()()())
            # () CREATE TAB CONTENTS () #
            # ()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()() #
            # COMPANY NAME Input
            ttk.Label(master=self.lblframe_create,
                      text='Company Name: ').grid(row=0, column=0, padx=10, pady=10, sticky='nw')
            self.company_name = tk.StringVar(master=self.lblframe_create)
            ttk.Entry(master=self.lblframe_create,
                                          textvariable=self.company_name,
                                          width=20
                                          ).grid(row=0, column=1, padx=10, pady=10, sticky='w')
            
            # CONTACT PERSON (NAME)
            ttk.Label(master=self.lblframe_create,
                      text='Contact Person: ').grid(row=2, column=0, padx=10, pady=10, sticky='nw')
            self.name = tk.StringVar(master=self.root)
            # [2020-01-07]\\self.name.set(value="Hot-Stuff")
            ttk.Entry(master=self.lblframe_create,
                                       textvariable=self.name,
                                       state='active',
                                       width=20
                                       ).grid(row=2, column=1, padx=10, pady=10, sticky='w')
            # EMAIL ADDRESS #
            ttk.Label(master=self.lblframe_create,
                      text='Email Address: ').grid(row=3, column=0, padx=10, pady=10, sticky='w')
            self.email = tk.StringVar(master=self.root)
            ttk.Entry(master=self.lblframe_create,
                                      textvariable=self.email,
                                      state='active',
                                      width=20
                                      ).grid(row=3, column=1, padx=10, pady=10, stick='nw') 
            # ACCOUNT ID #
            ttk.Label(master=self.lblframe_create,
                      text='Account ID: ').grid(row=4, column=0, padx=10, pady=10, sticky='w')
            self.account_id = tk.StringVar(master=self.root)
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
            
            # INITIALS #
            ttk.Label(master=self.lblframe_create,
                      text='Initials: ').grid(row=5, column=0, padx=10, pady=10, sticky='w')
            self.initials = tk.StringVar(master=self.root)
            ttk.Entry(master=self.lblframe_create,
                                 textvariable=self.initials,
                                 state='active',
                                 width=20,
                                 ).grid(row=5, column=1, padx=10, pady=10, sticky='w')
            
            ########
            # TYPE #
            ttk.Label(master=self.lblframe_create,
                      text='Type: '
                      ).grid(row=6, column=0, padx=10, pady=10, sticky='w')
            
            self.type_var = tk.StringVar(master=self.root) #, value="email")
            """
            ttk.Radiobutton(master=self.lblframe_create,
                            variable=self.type_var,
                            value="web", text="web", 
                            state=tk.ACTIVE, 
                            width=20
                            ).grid(row=5, column=1, columnspan=2, sticky='w', padx=10, pady=10)
            ttk.Radiobutton(master=self.lblframe_create,
                            variable=self.type_var,
                            value="email", text="email", 
                            state=tk.ACTIVE,
                            width=20
                            ).grid(row=5, column=1, columnspan=3, sticky='e', padx=10, pady=10)
            """
            ttk.OptionMenu(self.lblframe_create, 
                           self.type_var, 
                           "Select: ", 
                           "web", 
                           "email", 
                           direction="right"
                           ).grid(row=6, column=1, padx=10, pady=10, sticky='w')
            
            #########################################################################
            
            self.sep_2 = ttk.Separator(master=self.lblframe_create, orient=tk.HORIZONTAL)
            self.sep_2.place(x=10, y=250, width=275, height=1)  # WAS y=330
            
            ##########################################################################
            
            # NOTES #
            ttk.Label(master=self.lblframe_create,
                      text='Notes: ').grid(row=7, column=0, padx=10, pady=10, sticky='nw')
            # [2020-01-03]\\self.notes = tk.StringVar(master=self.lblframe_create)
            self.notes = tk.StringVar(master=self.root, value="")
            
            ttk.Entry(master=self.lblframe_create,
                                   width=20,
                                   textvariable=self.notes
                                   ).grid(row=7, column=1, padx=10, pady=10, sticky='e')
            
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
            
            # CREATE BUTTON #
            self.create_button = ttk.Button(master=self.lblframe_create, 
                                       text="CREATE",
                                       command=self.add_new_record
                                       ).grid(row=8, column=0, padx=10, pady=10, sticky='n')
            
            # CLEAR BUTTON #
            self.clear_button = ttk.Button(master=self.lblframe_create,
                                      text="CLEAR"
                                      ).grid(row=8, column=1, padx=10, pady=10, sticky='n')
            
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

    def create_right_side(self):  # {
        # Create a Frame Container
        self.rightframe = ttk.Frame(master=self.root)
        self.rightframe.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        """
        ################
        # PANED WINDOW #
        ################
        """
        # create PanedWindow
        pw = ttk.PanedWindow(master=self.root, orient=tk.HORIZONTAL)
        # pack into the TOP right side and fill whole
        pw.pack(side=tk.TOP, expand=tk.Y, fill=tk.BOTH)
        # BIND FUNCTIONS TO FRAME
        # [2020-01-10]\\self.rightframe.bind('<Enter>', self.clear_message_area)
    # }

    def create_tree_view(self):  # {
        # TRY THE FOLLOWING
        try:  # {
            # TABLE
            self.tree = ttk.Treeview(master=self.rightframe, style="mystyle.Treeview",
                                     height=30, columns=13, selectmode='browse')  # height = 20
            self.tree["columns"] = (
            "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven", "twelve", "thirteen")
            self.tree.column('#0', anchor=tk.W, width=100, minwidth=100, stretch=tk.NO)  # TRACKING #
            self.tree.column("one", anchor=tk.W, width=150, minwidth=150, stretch=tk.NO)  # TIME REC. // NAME
            self.tree.column("two", anchor=tk.CENTER, width=50, minwidth=50, stretch=tk.NO)  # INITIALS // EMAIL
            self.tree.column("three", anchor=tk.CENTER, width=50, minwidth=50, stretch=tk.NO)  # TYPE
            self.tree.column("four", anchor=tk.W, width=100, minwidth=100, stretch=tk.NO)  # COMPANY NAME //OPEN TIME
            self.tree.column("five", anchor=tk.W, width=100, minwidth=100, stretch=tk.NO)  # CONTACT PERSON //SENT , 45, 45
            self.tree.column("six", anchor=tk.W, width=160, minwidth=150, stretch=tk.NO)  #  EMAIL ADDRESS //TURN_AROUND, 100, 90
            self.tree.column("seven", anchor=tk.CENTER, width=80, minwidth=80, stretch=tk.NO)  # ACCOUNT ID // NOTES
            self.tree.column("eight", anchor=tk.CENTER, width=100, minwidth=80, stretch=tk.NO)  # PRODUCT NUMBER //INITIALS
            self.tree.column("nine", anchor=tk.CENTER, width=85, minwidth=75, stretch=tk.NO)  # PF QUOTE #//  ACCOUNT ID
            self.tree.column("ten", anchor=tk.CENTER, width=100, minwidth=75, stretch=tk.NO)  # SAP QUOTE # // PRODFLOW QUOTE #
            self.tree.column("eleven", anchor=tk.CENTER, width=50, minwidth=50, stretch=tk.NO)  # SENT
            self.tree.column("twelve", anchor=tk.CENTER, width=125, minwidth=100, stretch=tk.NO)  # TIME_SENT // SAP QUOTE #
            self.tree.column("thirteen", anchor=tk.CENTER, width=75, minwidth=75, stretch=tk.YES)  # NOTES // PRICE

            # Definitions of Headings
            # [2019-12-05]\\self.tree.grid(row = 1, column = 0, columnspan = 8, sticky = 'S')
            self.tree.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
            self.tree.heading('#0', text='Tracking #', anchor=tk.CENTER)  # 'tracking_number' in BACKEND
            self.tree.heading('#1', text='Time Rec.', anchor=tk.CENTER) # "Open_time" in BACKEND
            self.tree.heading('#2', text='Initials', anchor=tk.CENTER)
            self.tree.heading('#3', text='Type', anchor=tk.CENTER)
            self.tree.heading('#4', text='Company', anchor=tk.CENTER)  # COMPANY_NAME
            self.tree.heading('#5', text='Contact Person', anchor=tk.CENTER) # NAME IN BACKEND
            self.tree.heading('#6', text='Email Address', anchor=tk.CENTER)  #
            self.tree.heading('#7', text='Account ID', anchor=tk.CENTER)
            self.tree.heading("#8", text='Product #', anchor=tk.CENTER)
            self.tree.heading('#9', text='PF Quote #', anchor=tk.CENTER)
            self.tree.heading('#10', text='SAP Quote #', anchor=tk.CENTER)
            self.tree.heading('#11', text='Sent', anchor=tk.CENTER)
            self.tree.heading('#12', text='Time Sent', anchor=tk.CENTER)       # CLOSE TIME IN BACKEND
            self.tree.heading('#13', text='Notes', anchor=tk.CENTER)

            # BIND CLICK ACTIONS/EVENTS
            self.tree.bind("<Double-1>", self.on_double_click)
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
    
    def clear_message_area(self, event): # {
        # clear message area
        self.message['text'] = ''
    # }

    def on_double_click(self, event):  # {
        # TRY THE FOLLOWING
        try: #{
            # GET NUMBER OF CHILDREN (of ROOT)
            self.children_num = self.root.winfo_children()
            logging.info("\t CHILDREN BEFORE \n\t\t========>" + str(len(self.children_num)))
        # }
        except: # {
            logging.erro("failed getting the children...")
        # }
        # TRY THE FOLLOWING
        try: # {
            # GET MOUSE LOCATION
            self.mouse_location = pyautogui.position()
            logging.info("MOUSE LOCATION:\n" + str(self.mouse_location))
            # GET SCREEN RESOLUTION/SIZE
            self.screen_resolution = pyautogui.size()
            logging.info("SCREEN SIZE:\n" + str(self.screen_resolution))
        # }
        except: # {
            logging.error("Error determining mouse location & screen size...")
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
            logging.info(str(selection_list))
            selection_string = str("YOU SELECTED:\n"
                                   + selected_time_rec + "\n" + selected_name + "\n"
                                   + selected_email + "\n" + selected_type + "\n"
                                   + selected_sent + "\n" + selected_notes + "\n"
                                   + selected_initials + "\n" + selected_account_id + "\n"
                                   + selected_prodflow_quote_number + "\n" + selected_sap_quote_number + "\n"
                                   + selected_product_number + "\n" + selected_company_name
                                   )
            logging.info(str(selection_string))
            # SEND SELECTIONS AND OPEN MODIFY WINDOW
            self.open_modify_window(selected_item=item, 
                                    the_selection_list=selection_list, 
                                    window_location=str(self.mouse_location)
                                    )
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
        logging.info("\t CHILDREN AFTER \n\t\t========>" + str(len(self.children_num)))
    # }

    ######################################################################################################
    # QUOTE NUMBER CONVENTION AND PROGRESS CHECKS #
    ###############################################

    def check_quote_completion(self, the_df):  # {
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
                    logging.info("NOT EMPTY!")
                # }
            # }
            # OVERWRITE COL?
            the_df["turn_around"] = result
            logging.info(the_df)
            # RETURN DATAFRAME TO REPLACE OLD/OUTDATED ONE
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
            print("current count == " + str(current_count))
            # INCREASE COUNT
            current_count += 1
            # CREATE STRING WITH COUNT + zero fill
            count_str = str(current_count).zfill(int(number_of_digits))
            print("count_str == " + str(count_str))
            # CREATE STRING
            file_name_conv = str("T000" + count_str)
            print("FINAL RESULT == " + str(file_name_conv))
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
        # }
        else:  # {
            print("Operation Completed Successfully...")
        # }
        finally:  # {
            print("... saving COUNT TO PICKLE == " + str(current_count))
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
            # ASSIGN ENTRY INPUT TO STR
            # [2020-01-07]\\test_regex = str(self.pf_quote_num.get())
            # [2020-01-09]\\test_regex = str(self.new_pf_quote_num_entry_widget.get())
            test_regex = str(self.new_pf_quote_num.get())
            print("TEST-REGEX:\t" + str(test_regex))
            print("\n" + str(self.pf_quote_regex))
            # display message
            self.message['text'] = ' ===== EDIT QUOTE [!] ===== '
            # CHECK IF THE PF QUOTE # DOESNT MATCH
            if fnmatch.fnmatch(test_regex, str(self.pf_quote_regex)) or fnmatch.fnmatch(test_regex, str('')): # {
                # keep submit button ACTIVE
                print("PF-QUOTE-#... PASSES")
                event.widget['state'] = tk.ACTIVE
                # test display message?
                self.left_transient['text'] = ' <<< PF-QUOTE-#... correct >>>'
                # display message
                self.message['text'] += '\n <<< PF-QUOTE-#... correct >>>'
                # NoW CHECK IF SAP QUOTE # DOESNT MATCH
                test_regex = str(self.new_sap_quote_num.get())
                if fnmatch.fnmatch(test_regex, str(self.sap_quote_regex)) or fnmatch.fnmatch(test_regex, str('')): # {
                    # keep submit button ACTIVE
                    print("SAP-QUOTE-#... PASSES")
                    event.widget['state'] = tk.ACTIVE
                    # display message
                    self.message['text'] += '\n <<< SAP-QUOTE-#... correct >>>'
                    # NOW CHECK IF ACCOUNT ID DOESNT MATCH
                    test_regex = str(self.new_account_id.get())
                    if fnmatch.fnmatch(test_regex, str(self.account_id_regex)): # {
                        # keep submit button ACTIVE
                        print("ACCOUNT ID... PASSES")
                        event.widget['state'] = tk.ACTIVE
                        # display message
                        self.message['text'] += '\n <<< ACCOUNT-ID... correct >>>'
                    # }
                    else: # {
                        # keep submit button DISABLED
                        print("ACCOUNT ID... FAILED")
                        event.widget['state'] = tk.DISABLED
                        # display message
                        self.message['text'] = " <<< ACCOUNT ID... incorrect >>>"
                        self.message['text'] += "\n <<< 8-digit-alphanumeric"
                    # }
                # }
                else: # {
                    # keep submit button DISABED
                    print("SAP-QUOTE-#... FAILED")
                    event.widget['state'] = tk.DISABLED
                    # display message
                    self.message['text'] += "\n <<< SAP-QUOTE-#... incorrect >>> "
                    self.message['text'] += "\n <<< 7-digit-numeric"
                # } 
            # }
            else: # {
                # keep submit button DISABLED
                print("PF-QUOTE-#... FAILED")
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
    # }

    ###################################################################################################
    # ADD / UPDATE / DELETE FUNCTION BELOW #
    ########################################

    def add_new_record(self):  # {
        # TRY THE FOLLOWING
        try:  # {
            # CHECK IF RECORD IS VALIDATED (every box)
            if self.new_records_validated():  # {
                logging.info("...ADDING NEW RECORD...")
                # create ENTRY variables
                # [2019-12-26]\\track_num = [self.quote_number_convention()]  # auto-creates number
                track_num = [self.create_file_name_convention(the_pickle=self.t_count_filename, number_of_digits=8)]
                the_name = [str(self.name.get())]
                the_email = [str(self.email.get())]
                the_type = [str(self.type_var.get())]
                # [2020-01-08]\\the_sent = [str(self.radio_sent_var.get())]
                the_sent = [str("False")]
                open_time = [str(pd.Timestamp.now())]
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
                    the_notes = [str(self.notes.get())]
                # }
                the_initials = [str(self.initials.get())]
                the_account_id_num = [str(self.account_id.get())]
                # [2020-01-10]\\the_prodflow_quote_num = [str(self.prodflow_quote_num.get())]
                # [2020-01-10]\\the_sap_quote_num = [str(self.sap_quote_num.get())]
                # [2020-01-10]\\the_product_number = [str(self.product_num.get())]
                the_prodflow_quote_num = [str("None")]
                the_sap_quote_num = [str("None")]
                the_product_number = [str("None")]
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
                                  'account_id': str(the_account_id_num),
                                  'prodflow_quote_number': str(the_prodflow_quote_num),
                                  'sap_quote_number': str(the_sap_quote_num),
                                  'product_number': str(the_product_number),
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
                """
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
                self.name.set("")
                self.email.set("")
                self.notes.set("")
                self.initials.set("")
                self.account_id.set("")
                # [2020-01-10]\\self.prodflow_quote_num.set("")
                # [2020-01-10]\\self.sap_quote_num.set("")
                # [2020-01-10]\\self.product_num.set("")
                self.company_name.set("")
                self.type_var.set("Select: ")
            # }
            else:  # {
                # [2020-01-07]\\self.message['text'] = ' >>>>>>>>>>>>><<<<<<<<<<<<<\n [Initials], [Type], [AccountID],\n [Product #], [PF Quote #], [SAP Quote #]\n CANNOT BE left BLANK! \n >>>>>>>>>>>>><<<<<<<<<<<<<'
                self.message['text'] = ' >>>>>>>>>>>>>><<<<<<<<<<<<<<\n [Initials], [Type], and/or [AccountID]\n CANNOT  BE  LEFT  BLANK! \n >>>>>>>>>>>>>><<<<<<<<<<<<<<'
            # }
            # CALL FUNCTION TO UDPATE TABlE DISPLAY
            self.view_records()
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
            logging.info("Operation Completed Successfully...")
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
        print("THIS WIDGET's TEXT:\n" + str(event.widget['text']))
        # [2020-01-08]\\event.widget["activeforeground"] = "red"
        
    # }

    def new_records_validated(self):  # {
        print("NAME:\n" + str(self.name.get()))
        # TRY THE FOLLOWING
        try:  # {
            return len(str(self.initials.get())) != 0 \
                   and str(self.type_var.get()) != "Select:" \
                   and len(str(self.account_id.get())) != 0 \
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
    
    def updated_records_validated(self, a_product_num, a_pf_num, a_sap_num): # {
        logging.info("Validating FILE NAME conventions...")
        # TRY THE FOLLOWING
        try: # {
            pass
        # }
        except: # {
            pass
        # }
    # }

    def view_records(self):  # {
        logging.info("Begin Populating TreeView...")
        # display message
        self.message['text'] = " <<< Updating / Refreshing Table >>> "
        # TRY THE FOLLOWING
        try:  # {
            items = self.tree.get_children()
            for item in items:  # {
                self.tree.delete(item)
            # }
            # [2020-01-03]\\query = 'SELECT * FROM quotes ORDER BY name desc'
            query = 'SELECT * FROM quotes ORDER BY open_time desc'
            quote_tracker_entries = self.execute_db_query(query)
            for row in quote_tracker_entries:  # {
                print("PRINTING ROW:\n\t" + str(row))
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
    
    def is_valid_account_id(self, the_str): # {
        # the_str - value in %P
        if fnmatch.fnmatch(the_str, str(self.account_id_regex)): # {
            return True
        # }
    # }

    def open_modify_window(self, selected_item, the_selection_list, window_location):  # {
        # TRY THE FOLLOWING
        try:  # {
            logging.info("...MODIFYING RECORD...")
            print("SELECTION LIST:\n" + str(the_selection_list))
            print(the_selection_list[1])
            # tracking_number = str(self.tree.item(item)['values'][0])
            # track_num = self.tree.item(self.tree.selection()['text'])
            # old_name = self.tree.item(self.tree.selection())['values'][0]
            self.transient = tk.Toplevel(master=self.root)
            self.transient.wm_transient(master=self.root)  # MAKE WINDOW TRANS
            self.transient.title("EDIT QUOTE - Agilent Quotes Tracker")
            #self.transient.withdraw()
            """
            ################
            # PANED WINDOW #
            ################
            """
            self.pw = ttk.PanedWindow(master=self.transient, orient=tk.HORIZONTAL)
            self.pw.pack(side=tk.TOP, expand=tk.Y, fill=tk.BOTH) # padx='2m', pady=2
            self.left_transient = ttk.Label(master=self.pw, text='This is the\nLeft side.',
                                            background='gold', anchor=tk.CENTER)
            self.right_transient = ttk.Frame(master=self.pw) # MAIN FRAME
            self.pw.add(self.left_transient)
            self.pw.add(self.right_transient)
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
            print("X == " + str(x_val))
            print("Y == " + str(y_val))
            # CREATE STR TO HOLD X AND Y LOCATION POSITIONS
            location_str = str('' + str(int(x_val-385)) + "+" + str(int(y_val)) + '')
            self.transient.geometry(str('385x255+' + location_str))
            self.transient.resizable(width=False, height=False)
            ##################################################################################
            # NOTEBOOK WIDGET
            transient_tabs = ttk.Notebook(self.right_transient)
            
            # <><><><><><<><<><><<><><><><><><><><><><><><><><><><><><><><> #
            # TAB-1 // OLD TRACKING INFO #
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
                                     width=40,
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
                                 width=40,
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
                                 width=40,
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
            # TAB-2 // ACCOUNT INFO #
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
                                                      width=40
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
                                                        width=40
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
                      width=40
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
                                                    width=40
                                                    ).grid(row=3, column=1, padx=10, pady=10, sticky=None)
            
            # <><><><><><><><><><><><><><><><><><><><><><><><><><><<><>< #
            # TAB-3 // QUOTE INFO #
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
            print("\n\t>>>> SENT? <<<< " + str(the_radio_sent_var))
            self.radio_sent_var = tk.BooleanVar(master=self.root, value=the_radio_sent_var)
            print("\n\t>>> STILL? <<<< " + str(self.radio_sent_var.get()))
            # CREATE VAR TO HOLD (new) VALUE
            new_radio_sent_var = tk.BooleanVar(master=tab_quote_info, value=bool(self.radio_sent_var))
            # CREATE RADIO BUTTON ** BASED ON CONDITIONS **
            if bool(self.radio_sent_var.get()) is True: # {
                print(">>>>>>>>>> IS TRUE!")
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
                print(">>>>>>>>> IS FALSE!")
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
            
            # NOTES #
            ttk.Label(master=tab_notes_section,
                      text="Notes: "
                      ).grid(row=0, column=0, padx=10, pady=10, sticky='w')
            # GET NOTES FROM "selection_list"[5] (old)
            the_notes_var = str(the_selection_list[5])
            self.new_notes_var = tk.StringVar(master=tab_notes_section, value=the_notes_var)
            # [2020-01-06]\\new_notes_text_widget = tk.Text(master=tab_notes_section, height=10, width=36)
            new_notes_entry_widget = tk.Entry(master=tab_notes_section, 
                                               state=tk.NORMAL,
                                               textvariable=self.new_notes_var,
                                               width=20
                                               ).grid(row=0, column=1, columnspan=4,
                                                      rowspan=2, padx=10, pady=10, sticky='e')
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
                newnotes=str(self.new_notes_var.get()), #old_notes=str(the_selection_list[5]),
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
            logging.info("UPDATE-RECORD FIELDS ARE ALL FILLED IN COMPLETELY!")
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
            # ASK THE USER IF THEY ARE SURE WITH THEIR COMPLETION?
            confirm_box = messagebox.askokcancel(title="Confirm Update", message=str(display_str))
            print(confirm_box)
            if str(confirm_box) == "True":  # {
                # TRY THE FOLLOWING
                try:  # {
                    print("UPDATING RECORD...")
                    print("NEW_SENT RADIO VAR [passed_thru_function] == " + str(newsent))
                    # CHECK IF SENT HAS BEEN SWITCHED!
                    # IF SO UPDATE: sent, close_time, turn_around AND ALSO name, email, notes
                    # [2019-12-27]\\if bool(newsent) is True:  # {
                    if newsent == "True":  # {
                        print("\n\t\t\t>>>> SWITCHING OVER!")
                        # CREATE TEMPORARY TIMESTAMP
                        time_meow = pd.Timestamp.now()
                        print("TIME MEOW == " + str(time_meow))
                        print("open_time == " + str(open_time))
                        print("old_sent == " + str(old_sent))
                        # COMPUTE TURN AROUND TIME
                        time_start = pd.Timestamp(open_time)
                        print("TIME START == " + str(time_start))
                        run_time = time_meow - time_start
                        print("RUN TIME == " + str(run_time))
                        query = 'UPDATE quotes ' \
                                'SET name=?, email=?, type=?, sent=?, close_time=?, turn_around=?, notes=?, initials=?, account_id=?, prodflow_quote_number=?, sap_quote_number=?, company_name=?, product_number=?' \
                                'WHERE tracking_number=?'
                        parameters = (newname, newemail, the_type, newsent, str(time_meow),
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
                        print("\n\t\t\t>>>>>>> NOPE")
                        query = 'UPDATE quotes SET name=?, email=?, type=?, notes=?, initials=?, account_id=?, prodflow_quote_number=?, sap_quote_number=?, company_name=?, product_number=?' \
                                'WHERE tracking_number=? '
                        parameters = (newname, newemail, the_type, newnotes, newinitials,
                                      newaccountid, newpfnum, newsapnum, newcompanyname, newproductnum,
                                      tracking_number)
                        print("QUERY:\n" + str(query) + "\nPARAMS:\n" + str(parameters))
                        # EXECUTE
                        self.execute_db_query(query, parameters)
                        self.transient.destroy()
                        self.message['text'] = 'Quote Record of {} modified'.format(tracking_number)
                        self.view_records()
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
            else:  # {
                logging.info("USER SELECTED NOT READY !...")
                self.transient.destroy()
            # }
        # }
        else:  # {
            # [2020-01-10]\\self.message['text'] = 'MISSING REQUIRED FIELDS(S):\n Initals\n AccountID'
            messagebox.showwarning(parent=self.root, title="WARNING:", message="MISSING REQUIRED FIELD(S):\n\n\tInitials\n\nPlease re-open quote to edit")
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

# MAIN BOILERPLATE
if __name__ == "__main__":  # {
    # SETUP LOGGER
    setup_logger()
    window = tk.Tk()
    application = AgilentQuotesTracker(window)
    # [2020-01-03]\\application.tick()  # BEGIN "COUNTING" TIME(STAMP)
    window.config()
    window.mainloop()
# }