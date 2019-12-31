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

@author: derbates
"""

# IMPORT THE GOODS
import os, sys, time
from time import sleep
from pathlib import Path
import datetime
import tkinter as tk
import tkinter.ttk as ttk
from ttkthemes import ThemedStyle
from tkinter import filedialog, messagebox
import sqlite3, logging, random
import pickle
import pyodbc
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

    def __init__(self, root):  # {
        self.root = root
        self.root.title("Agilent Quotes Tracker")
        self.root.resizable(width=True, height=True)
        # [2019-12-12]\\self.root.minsize(height=1250)
        self.root.minsize(width=1175, height=250)
        # [2019-12-26]\\self.root.maxsize(width=1500, height=1250)
        # [2019-12-30]\\self.root.maxsize(width=1750, height=1250)
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

    def create_gui(self):  # {
        # TRY THE FOLLOWING
        try:  # {
            # [2019-12-11]\\self.create_menubar()
            self.create_ttk_styles()
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
        self.filemenu = tk.Menu(master=self.menubar,
                                borderwidth=4,
                                background="#0C85CE",
                                font=("Comfortaa", 12),
                                tearoff=0)
        self.filemenu.add_command(label="Import", command="")
        self.filemenu.add_command(label="Export", command="")

        self.filemenu.add_separator()

        self.filemenu.add_command(label="Exit", command=self.root.quit)
        self.menubar.add_cascade(label="File", menu=self.filemenu)
        self.editmenu = tk.Menu(master=self.root,
                                borderwidth=4,
                                background="#9e0ccf",
                                font=("Impact", 24),
                                tearoff=0)
        self.editmenu.add_command(label="Filter Table", command="")

        self.editmenu.add_separator()

        self.editmenu.add_command(label="Copy Cell", command="")
        self.editmenu.add_command(label="Select All", command="")

        self.menubar.add_cascade(label="Edit", menu=self.editmenu)
        self.helpmenu = tk.Menu(master=self.menubar,
                                background="#ffbf00",
                                font=("Courier New", 48),
                                relief=tk.GROOVE,
                                tearoff=0)
        self.helpmenu.add_command(label="Help Index", command="")
        self.helpmenu.add_command(label="About...", command="")
        self.menubar.add_cascade(label="Help", menu=self.helpmenu)

    # }

    def create_ttk_styles(self):  # {
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
            self.style.set_theme("scidblue") # radiance, black, scidpink, kroc, keramik, equilux
            # Modify the font of the body
            self.style.configure("mystyle.Treeview", highlightthickness=4, bd=4, font=('Calibri', 11))
            # Modify the font of the headings
            self.style.configure("mystyle.Treeview.Heading", font=('Calibri', 12, 'bold'))
            # REMOVE THE BORDERS
            self.style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})])
            # BUTTON STYLE
            self.button_style = ttk.Style().configure("TButton", padding=4,
                                                      relief="groove", background="#96A853",
                                                      font=('Calibri', 8, 'bold'), foreground="#600080")
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

    # }

    def create_tab_control(self):  # {
        # TRY THE FOLLOWING
        try:  # {
            # CREATE MESSAGE AREA
            self.message = ttk.Label(master=self.leftframe, text='',
                                     font=("Sourcode Pro", 14), foreground='red')
            # self.message.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
            self.message.pack(side=tk.TOP, fill=tk.BOTH, expand=False)

            # NOTEBOOK WIDGET
            self.tab_control = ttk.Notebook(self.leftframe)

            # TAB-1 // CREATE
            self.tab1 = ttk.Frame(master=self.tab_control)
            self.tab_control.add(self.tab1, text='Tracking Info')
            self.tab_control.pack(expand=2, fill=tk.BOTH)

            # TAB-2 // ABOUT INFORMATION
            self.tab2 = ttk.Frame(master=self.tab_control)
            self.tab_control.add(self.tab2, text='Account Info')
            self.tab_control.pack(expand=2, fill=tk.BOTH)

            # TAB-3 // HELP OPTIONS
            self.tab3 = ttk.Frame(master=self.tab_control)
            self.tab_control.add(self.tab3, text='Quote Info')
            # [2019-12-26]\\self.tab_control.pack(expand=2, fill=tk.BOTH)
            self.tab_control.pack(expand=2, fill=None)

            """
            # TAB-4 // HELP SECTION
            self.tab4 = ttk.Frame(master=self.tab_control)
            self.tab_control.add(self.tab4, text="EXPORT")
            self.tab_control.pack(expand=2, fill=tk.BOTH)
            """
            
            # UNIVERSAL BUTTON?
            self.uni_button = ttk.Button(master=self.leftframe, text="CREATE", state='disabled')
            self.uni_button.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
            
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
            self.lblframe_create = ttk.LabelFrame(master=self.tab1, text="Input Tracking Information:")
            # [2019-12-30]\\self.lblframe_create.pack(anchor=tk.CENTER, fill=tk.BOTH, expand=True)
            self.lblframe_create.pack(anchor=tk.CENTER, fill=tk.BOTH, expand=False)

            # Create the IMPORT Tab Container
            self.lblframe_import = ttk.LabelFrame(master=self.tab2, text="ABOUT the Agilent Quotes Tracker:")
            self.lblframe_import.pack(anchor=tk.CENTER, fill=tk.BOTH, expand=False)

            # Create the EXPORT Tab Container
            self.lblframe_export = ttk.LabelFrame(master=self.tab3, text="Help Section:")
            self.lblframe_export.pack(anchor=tk.CENTER, fill=tk.BOTH, expand=False)

            """[2019-12-13]"""
            """
            # Create the HELP Tab Container
            self.lblframe_help = ttk.LabelFrame(master=self.tab4, text="EXPORT One or Multiple Quotes:")
            self.lblframe_help.pack(anchor=tk.CENTER, fill=tk.BOTH, expand=True)
            """

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
            # Name Input
            ttk.Label(master=self.lblframe_create, text='Name: ').grid(row=0, column=0, padx=5,
                                                                       pady=5, sticky='w')
            self.name = ttk.Entry(master=self.lblframe_create, width=24)  # [2019-11-18]\\ borderwidth=3)
            self.name.grid(row=0, column=1, sticky='w', padx=5, pady=5)

            # xXxXxXxXxXxXxXxXx
            # Email Input
            ttk.Label(master=self.lblframe_create, text='Email: ').grid(row=1, column=0, padx=5,
                                                                        pady=5, sticky='w')
            self.email = ttk.Entry(master=self.lblframe_create, width=24)  # [2019-11-18]\\ borderwidth=3)
            self.email.grid(row=1, column=1, sticky='w', padx=5, pady=5)

            # xXxXxXxXxXxXxXxXx
            # Type Input
            ttk.Label(master=self.lblframe_create, text='Type: ').grid(row=2, column=0, padx=5,
                                                                       pady=5, sticky='w')
            ############################
            # RADIO-VARIABLE == STRING #
            self.radio_type_var = tk.StringVar(master=self.lblframe_create, value="email")
            ################################################################################
            self.radio_type_1 = ttk.Radiobutton(master=self.lblframe_create, variable=self.radio_type_var,
                                                value="web", text="Web", width=15)  # style="TButton")
            self.radio_type_1.grid(row=2, column=1, columnspan=2, sticky='w', padx=5, pady=5)
            self.radio_type_2 = ttk.Radiobutton(master=self.lblframe_create, variable=self.radio_type_var,
                                                value="email", text="Email", width=15)
            self.radio_type_2.grid(row=2, column=1, columnspan=2, sticky='e', padx=55, pady=5)

            # xXxXxXxXxXxXxXxXx
            # Sent Input
            ttk.Label(master=self.lblframe_create, text='Sent: ').grid(row=3, column=0, padx=5,
                                                                       pady=5, stick='w')
            ##########################
            # RADIO-VARIABLE == BOOL #
            self.radio_sent_var = tk.BooleanVar(master=self.lblframe_create, value=False)
            ################################################################################
            self.radio_sent_1 = ttk.Radiobutton(master=self.lblframe_create, variable=self.radio_sent_var,
                                                value=True, text="Yes", width=15, state=tk.DISABLED)  # style="TButton")
            self.radio_sent_1.grid(row=3, column=1, sticky='w', padx=5, pady=5)
            self.radio_sent_2 = ttk.Radiobutton(master=self.lblframe_create, variable=self.radio_sent_var,
                                                value=False, text="No", width=15)
            self.radio_sent_2.grid(row=3, column=1, sticky='e', padx=5, pady=5)

            # TRACKING NUMBER #
            ttk.Label(master=self.lblframe_create, text='Tracking #: ').grid(row=5, column=0,
                                                                             padx=5, pady=5, sticky='w')
            self.tracking_num = ttk.Entry(master=self.lblframe_create, width=24, state='readonly')
            self.tracking_num.grid(row=5, column=1, sticky='w', padx=5, pady=5)

            # Timestamp (start_time)
            self.start_time_var = tk.StringVar(master=self.lblframe_create)
            ttk.Label(master=self.lblframe_create, text="Timestamp: ").grid(row=6, column=0, padx=5, pady=5, sticky='w')

            # <<< CLOCK (timestamp_test) >>>
            self.clock = ttk.Label(master=self.lblframe_create, font=("Calibri", 20, 'bold'),
                                   background='#2b303b', foreground="#bbc0c9")
            self.clock.grid(row=6, column=1, padx=5, pady=5, stick='w')

            # Initials (agilent worker)
            self.initials_var = tk.StringVar(master=self.lblframe_create)
            ttk.Label(master=self.lblframe_create, text='Initials: ', font=("Calibri", 12, 'bold'),
                      background='#666666', foreground='#000000').grid(row=7, column=0, sticky='w', padx=5, pady=5)
            self.initials = ttk.Entry(master=self.lblframe_create, width=24)
            self.initials.grid(row=7, column=1, sticky='w', padx=5, pady=5)

            # account_id [row=8]
            self.account_id_var = tk.StringVar(master=self.lblframe_create)
            ttk.Label(master=self.lblframe_create, text="Account ID: ").grid(row=8, column=0, sticky='w', padx=5,
                                                                             pady=5)
            self.account_id = ttk.Entry(master=self.lblframe_create, width=24)
            self.account_id.grid(row=8, column=1, sticky='w', padx=5, pady=5)
            
            # PRODUCT_NUMBER [row=9]
            self.product_num_var = tk.StringVar(master=self.lblframe_create)
            ttk.Label(master=self.lblframe_create, text='Product #: ').grid(row=9, column=0, sticky='w', padx=5,
                                                                            pady=5)
            self.product_num = ttk.Entry(master=self.lblframe_create, width=24)
            self.product_num.grid(row=9, column=1, sticky='w', padx=5, pady=5)

            # prodflow quote number [row=10]
            self.prodflow_quote_var = tk.StringVar(master=self.lblframe_create)
            ttk.Label(master=self.lblframe_create, text='Prodflow Quote #: ').grid(row=10, column=0, sticky='w', padx=5,
                                                                                   pady=5)
            self.prodflow_quote_num = ttk.Entry(master=self.lblframe_create, width=24)
            self.prodflow_quote_num.grid(row=10, column=1, sticky='w', padx=5, pady=5)

            # SAP quote number [row=11]
            self.sap_quote_var = tk.StringVar(master=self.lblframe_create)
            ttk.Label(master=self.lblframe_create, text='SAP Quote #: ').grid(row=11, column=0, sticky='w', padx=5,
                                                                              pady=5)
            self.sap_quote_num = ttk.Entry(master=self.lblframe_create, 
                                           textvariable=self.sap_quote_var,
                                           width=24)
            self.sap_quote_num.grid(row=11, column=1, sticky='w', padx=5, pady=5)
            
            # company name [row=12]
            self.company_var= tk.StringVar(master=self.lblframe_create)
            ttk.Label(master=self.lblframe_create, text='Company Name: ').grid(row=12, column=0, sticky='w', padx=5, pady=5)
            self.company_name = ttk.Entry(master=self.lblframe_create, 
                                          textvariable=self.company_var, 
                                          width=24)
            self.company_name.grid(row=12, column=1, sticky='w', padx=5, pady=5)

            # price [row=11]
            """ [2019-12-31] """
            """
            self.price_var = tk.IntVar(master=self.lblframe_create)
            ttk.Label(master=self.lblframe_create, text='Price: ').grid(row=11, column=0, sticky='w', padx=5, pady=5)
            self.price = ttk.Entry(master=self.lblframe_create, width=24)
            self.price.grid(row=11, column=1, sticky='w', padx=5, pady=5)
            """

            # notes [row=13/14]
            # xXxXxXxXxXxXxXxXx
            # Notes Section
            ttk.Label(master=self.lblframe_create, text="NOTES: ").grid(row=13, column=0,
                                                                        padx=5, pady=5, sticky='w')
            self.notes_var = tk.StringVar(master=self.lblframe_create)
            self.notes = tk.Entry(master=self.lblframe_create, 
                                  textvariable=self.notes_var, 
                                  width=24)
            # [2019-12-30]\\self.notes = ttk.Entry(master=self.lblframe_create, width=24)
            self.notes.grid(row=13, column=1, columnspan=2, rowspan=2, padx=5, pady=5, sticky='w')

            """[2019-12-12]"""
            """
            self.notes = ttk.Notebook(master=self.lblframe_create, height=200, width=200, padding=(1, 1))
            # Create the pages
            self.note_tab = tk.Text(master=self.lblframe_create, height=15, width=15,
                                    background="#96A853")  # ttk.Frame(master = self.notes)
            self.trackingnum_tab = tk.Text(master=self.lblframe_create, height=15, width=15,
                                           background="#2D323C")
            self.quotenum_tab = tk.Text(master=self.lblframe_create, height=15, width=15,
                                        background="#96A853")
            self.timestamp_tab = tk.Text(master=self.lblframe_create, height=15, width=15)
            # Add them to the notebook
            self.notes.add(self.note_tab, text="NOTES", )
            self.notes.add(self.trackingnum_tab, text="NOTES 2")
            self.notes.add(self.quotenum_tab, text="NOTES 3")
            self.notes.add(self.timestamp_tab, text="NOTES 4")
            """

            # keep_em_seperated = ttk.Separator(master=self.lblframe_create, orient=tk.HORIZONTAL)
            # keep_em_seperated.grid(row=6, column=0, columnspan=4)

            # [2019-11-20]\\self.notes.grid(row=5, column=0, columnspan=2, padx=5, sticky='n')
            # [2019-12-29]\\self.notes.grid(row=8, column=0, columnspan=2, padx=5, pady=5, sticky='n')
            # row = 6, column = 0, columnspan = 2 AND NO STICK OR PADX

            # xXxXxXxXXxXXxXXxX
            # SUBMIT "CREATE" BUTTON
            ttk.Button(master=self.lblframe_create,
                       text="CREATE", width=24,
                       command=self.add_new_record).grid(row=15, column=0, columnspan=2, padx=5, pady=5, sticky='nesw')
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

    # }

    def create_tree_view(self):  # {
        # TRY THE FOLLOWING
        try:  # {
            # TABLE
            self.tree = ttk.Treeview(master=self.rightframe, style="mystyle.Treeview",
                                     height=30, columns=13)  # height = 20
            self.tree["columns"] = (
            "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven", "twelve", "thirteen")
            self.tree.column('#0', anchor=tk.W, width=125, minwidth=125, stretch=tk.NO)  # TRACKING #
            self.tree.column("one", anchor=tk.W, width=175, minwidth=150, stretch=tk.NO)  # TIME REC. // NAME
            self.tree.column("two", anchor=tk.CENTER, width=50, minwidth=50, stretch=tk.NO)  # INITIALS // EMAIL
            self.tree.column("three", anchor=tk.CENTER, width=50, minwidth=50, stretch=tk.NO)  # TYPE
            self.tree.column("four", anchor=tk.CENTER, width=75, minwidth=75, stretch=tk.NO)  # COMPANY NAME //OPEN TIME
            self.tree.column("five", anchor=tk.W, width=100, minwidth=75, stretch=tk.NO)  # CONTACT PERSON //SENT , 45, 45
            self.tree.column("six", anchor=tk.CENTER, width=175, minwidth=125, stretch=tk.NO)  #  EMAIL ADDRESS //TURN_AROUND, 100, 90
            self.tree.column("seven", anchor=tk.CENTER, width=100, minwidth=100, stretch=tk.NO)  # ACCOUNT ID // NOTES
            self.tree.column("eight", anchor=tk.CENTER, width=85, minwidth=75, stretch=tk.NO)  # PRODUCT NUMBER //INITIALS
            self.tree.column("nine", anchor=tk.CENTER, width=85, minwidth=75, stretch=tk.NO)  # PF QUOTE #//  ACCOUNT ID
            self.tree.column("ten", anchor=tk.CENTER, width=100, minwidth=75, stretch=tk.NO)  # SAP QUOTE # // PRODFLOW QUOTE #
            self.tree.column("eleven", anchor=tk.CENTER, width=50, minwidth=50, stretch=tk.NO)  # SENT
            self.tree.column("twelve", anchor=tk.CENTER, width=125, minwidth=100, stretch=tk.NO)  # TIME_SENT // SAP QUOTE #
            self.tree.column("thirteen", anchor=tk.E, width=75, minwidth=75, stretch=tk.YES)  # NOTES // PRICE

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

    def on_double_click(self, event):  # {
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
            selected_time_rec = str(self.tree.item(item)['values'][1]) 
            selected_name = str(self.tree.item(item)['values'][5])  # WAS 1
            selected_email = str(self.tree.item(item)['values'][6]) # WAS 2
            selected_type = str(self.tree.item(item)['values'][3])  # WAS 3
            selected_sent = str(self.tree.item(item)['values'][12])  # WAS 4
            selected_notes = str(self.tree.item(item)['values'][11])  # WAS 6
            selected_initials = str(self.tree.item(item)['values'][2])  # WAS 7
            selected_account_id = str(self.tree.item(item)['values'][7])  # WAS 8
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
            self.open_modify_window(selected_item=item, the_selection_list=selection_list)
            # [2019-12-12]\\messagebox.showwarning(title=str(pd.Timestamp.now()), message=str(selection_string))
            # [2019-12-12]\\messagebox.showinfo(title="yupp!", message=str(self.tree.item(item_2, "text")))
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
    def on_delete_selected_button_selected(self):  # {
        # TRY THE FOLLOWING
        try:  # {
            test_item = self.tree.item(self.tree.selection())['values'][0]
            test_name = str(self.tree.item(self.tree.selection())['values'][0])
            test_two = str(self.tree.item(self.tree.selection())['values'][1])
            print(str(self.tree.item(self.tree.selection())['columns'][3]))
            print(str(self.tree.item(self.tree.selection())['columns'][4]))
            # print(str(self.tree.item(self.tree.selection())['values'][5]))
            # print(str(self.tree.item(self.tree.selection())['values'][6]))
            # print(str(self.tree.item(self.tree.selection())['values'][7]))
            # print(str(self.tree.item(self.tree.selection())['values'][8]))
            the_timestamp = str(self.tree.item(self.tree.selection())['columns'][3])
            self.open_modify_window(tracking_num="", the_name=test_name,
                                         the_email=test_two, the_type="",
                                         the_ts=the_timestamp, the_sent="",
                                         quote_num="", product_num="", the_notes="")
        # }
        except IndexError as e:  #{
            self.message['text'] = "No Item selected to modify:\n[" + str(e) + "]"
            return
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

    """
    CREATES NEW QUOTE NUMBER ACCORDING TO NAMING CONVENTION:
    301 + (YYYYMMDD) + Hour + Minute
    Example: 301201912121051
    """

    """
    def quote_number_convention(self):  # {
        # TRY THE FOLLOWING:
        try:  # {
            pass
        # }
        except:  # {
            pass
        # }
        # CREATE TIME STAMP FOR QUOTE NUMBER CONVENTION
        date_object = datetime.date.today()
        time_object = str('{0:%Y%m%d%H%M}'.format(datetime.datetime.now()))
        logging.info(str("QUOTES naming conventino (today's example) : "), time_object)
        # RETURN STR CONTAINING PROPER NAMING
        return str("301" + time_object)

    # }
        """

    ###################################################################################################
    # ADD / UPDATE / DELETE FUNCTION BELOW #
    ########################################

    """
    old "INSERT_RECORD"
    """

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
                the_type = [str(self.radio_type_var.get())]
                the_sent = [str(self.radio_sent_var.get())]
                open_time = [str(pd.Timestamp.now())]
                close_time = [str("")]
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
                the_prodflow_quote_num = [str(self.prodflow_quote_num.get())]
                the_sap_quote_num = [str(self.sap_quote_num.get())]
                the_product_number = [str(self.product_num.get())]
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
                engine = create_engine('sqlite:///e:/_Quotes_Tracker/data/quotes_tracker.db')
                # SEND DATAFRAME TO DATABASE
                new_entry_df.to_sql(name="quotes", con=engine, if_exists="append", index=False)
                # UPDATE DISPLAY MESSAGE
                self.message['text'] = "NEW QUOTE \n#{}\nCREATED!".format(str(track_num))
                # CLEAR ENTRY BOXES
                self.name.delete(0, tk.END)
                self.email.delete(0, tk.END)
                self.notes.delete(0, tk.END)
                self.initials.delete(0, tk.END)
                self.account_id.delete(0, tk.END)
                self.prodflow_quote_num.delete(0, tk.END)
                self.sap_quote_num.delete(0, tk.END)
                self.product_num.delete(0, tk.END)
                self.company_name.delete(0, tk.END)
                # [2019-12-31]\\self.price.delete(0, tk.END)
            # }
            else:  # {
                self.message['text'] = ' [Initials, Type, Company Name,\n AccountID, Product #,\n Prodflow Quote # & SAP Quote #]\n CANNOT be left blank!'
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

    def new_records_validated(self):  # {
        # TRY THE FOLLOWING
        try:  # {
            return len(self.name.get()) != 0 \
                   and len(self.email.get()) != 0 \
                   and len(self.initials.get()) != 0 \
                   and len(self.account_id.get()) != 0
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

    def view_records(self):  # {
        logging.info("Begin Populating TreeView...")
        # TRY THE FOLLOWING
        try:  # {
            items = self.tree.get_children()
            for item in items:  # {
                self.tree.delete(item)
            # }
            query = 'SELECT * FROM quotes ORDER BY name desc'
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

    def open_modify_window(self, selected_item, the_selection_list):  # {
        # TRY THE FOLLOWING
        try:  # {
            logging.info("MODIFYING RECORD")
            print("SELECTION LIST:\n" + str(the_selection_list))
            print(the_selection_list[1])
            # tracking_number = str(self.tree.item(item)['values'][0])
            # track_num = self.tree.item(self.tree.selection()['text'])
            # old_name = self.tree.item(self.tree.selection())['values'][0]
            self.transient = tk.Toplevel(master=self.root)
            self.transient.resizable(width=False, height=False)
            # TRACKING #
            ttk.Label(master=self.transient, text='Tracking #:').grid(row=0, column=0)
            tk.Entry(master=self.transient, font=("Calibri", 12), textvariable=tk.StringVar(
                self.transient, value=str(the_selection_list[0])), state='readonly').grid(row=0, column=1)
            test_name = str(self.tree.item(selected_item)['values'][0])
            # OLD-NAME
            ttk.Label(master=self.transient, text="OLD Name:").grid(row=1, column=0)
            tk.Entry(self.transient, textvariable=tk.StringVar(
                self.transient, value=test_name), state='readonly').grid(row=1, column=1)
            # NEW-NAME
            ttk.Label(master=self.transient, text="NEW Name:").grid(row=1, column=2)
            new_name_entry_widget = ttk.Entry(self.transient)
            new_name_entry_widget.grid(row=1, column=3)
            # OLD-EMAIL
            ttk.Label(master=self.transient, text="OLD Email:").grid(row=2, column=0)
            tk.Entry(self.transient, textvariable=tk.StringVar(
                self.transient, value=str(the_selection_list[1])), state='readonly').grid(row=2, column=1)
            # NEW-EMAIL
            ttk.Label(master=self.transient, text="NEW Email:").grid(row=2, column=2)
            new_email_entry_widget = ttk.Entry(self.transient)
            new_email_entry_widget.grid(row=2, column=3)
            # THE TYPE #
            ttk.Label(master=self.transient, text="Type:").grid(row=3, column=0)
            tk.Entry(master=self.transient, textvariable=tk.StringVar(
                self.transient, value=str(the_selection_list[2])), state='readonly').grid(row=3, column=1)
            # OLD-SENT #
            ttk.Label(master=self.transient, text="OLD Sent:").grid(row=4, column=0)
            tk.Entry(master=self.transient, textvariable=tk.StringVar(
                self.transient, value=str(the_selection_list[4])), state='readonly').grid(row=4, column=1)
            # NEW-SENT #
            ttk.Label(master=self.transient, text="NEW Sent:").grid(row=4, column=2)
            new_sent_radio_var = tk.BooleanVar(master=self.transient, value=False)  # bool(the_selection_list[4]))
            ####### VARIABLE FOR RADIO_SENT BOOLEAN
            sent_bool = bool(new_sent_radio_var.get())
            print("NEW_SENT_RADIO_VAR.get() // sent_bool // == " + str(sent_bool))
            print("NEW_SENT_RADIO_VAR.get() == " + str(new_sent_radio_var.get()))
            new_sent_radio_widget_1 = ttk.Radiobutton(master=self.transient, variable=new_sent_radio_var,
                                                      value=True, text="Yes", width=12).grid(row=4, column=3,
                                                                                             padx=5, sticky='w')
            new_sent_radio_widget_2 = ttk.Radiobutton(master=self.transient, variable=new_sent_radio_var,
                                                      value=False, text="No", width=12).grid(row=4, column=3,
                                                                                             padx=65, sticky='e')
            # TIMESTAMP (open_time) #
            ttk.Label(master=self.transient, text="Timetamp:").grid(row=5, column=0)
            open_time_entry_widget = tk.Entry(master=self.transient, textvariable=tk.StringVar(
                self.transient, value=str(the_selection_list[3])), state='readonly').grid(row=5, column=1)
            # OLD-INITIALS #
            ttk.Label(master=self.transient, text="OLD Initials:").grid(row=6, column=0)
            tk.Entry(master=self.transient, textvariable=tk.StringVar(
                self.transient, value=str(the_selection_list[6])), state='readonly').grid(row=6, column=1)
            # NEW-INITIALS #
            ttk.Label(master=self.transient, text="NEW Initials:").grid(row=6, column=2)
            new_initials_entry_widget = tk.Entry(master=self.transient)
            new_initials_entry_widget.grid(row=6, column=3)
            # OLD-ACCOUNT-ID #
            ttk.Label(master=self.transient, text="OLD Account ID:").grid(row=7, column=0)
            tk.Entry(master=self.transient, textvariable=tk.StringVar(
                self.transient, value=str(the_selection_list[7])), state='readonly').grid(row=7, column=1)
            # NEW-ACCOUNT-ID #
            ttk.Label(master=self.transient, text="NEW Account ID:").grid(row=7, column=2)
            new_account_id_entry_widget = tk.Entry(master=self.transient)
            new_account_id_entry_widget.grid(row=7, column=3)
            # THE PRODFLOW QUOTE NUMBER #
            ttk.Label(master=self.transient, text='Prodflow Quote #:').grid(row=8, column=0)
            tk.Entry(master=self.transient, textvariable=tk.StringVar(
                self.transient, value=str(the_selection_list[8])), state='readonly').grid(row=8, column=1)
            # THE SAP QUOTE NUMBER #
            ttk.Label(master=self.transient, text='SAP Quote #:').grid(row=9, column=0)
            tk.Entry(master=self.transient, textvariable=tk.StringVar(
                self.transient, value=str(the_selection_list[9])), state='readonly').grid(row=9, column=1)
            # OLD-PRICE #
            ttk.Label(master=self.transient, text='OLD Price:').grid(row=10, column=0)
            tk.Entry(master=self.transient, textvariable=tk.StringVar(
                self.transient, value=str(the_selection_list[10])), state='readonly').grid(row=10, column=1)
            # NEW-PRICE #
            ttk.Label(master=self.transient, text='NEW Price:').grid(row=10, column=2)
            new_price_entry_widget = tk.Entry(master=self.transient)
            new_price_entry_widget.grid(row=10, column=3)
            # NOTES #
            # [2019-12-27]\\ttk.Label(master=self.transient, text="Notes:").grid(row=6, column=0)
            ttk.Label(master=self.transient, text="Notes:").grid(row=11, column=0)
            new_notes_text_widget = tk.Text(master=self.transient, height=10, width=24)  # .grid(row=6, column=1)
            new_notes_text_widget.insert(tk.INSERT, str(the_selection_list[5]))
            # [2019-12-27]\\new_notes_text_widget.grid(row=6, column=1, columnspan=3, padx=5, pady=5, sticky='nesw')
            new_notes_text_widget.grid(row=11, column=1, columnspan=3, padx=5, pady=5, sticky='nesw')
            ##################
            # CONFIRM BUTTON #
            ttk.Button(master=self.transient, text='UPDATE', width=15, command=lambda: self.update_record(
                newname=new_name_entry_widget.get(), old_name=test_name,
                newemail=new_email_entry_widget.get(), old_email=str(the_selection_list[1]),
                the_type=str(the_selection_list[2]),
                # newsent=str(new_sent_radio_var.get())
                newsent=str(sent_bool), old_sent=str(the_selection_list[4]),
                open_time=str(the_selection_list[3]),
                newnotes=str(new_notes_text_widget.get(index1="1.0", index2=tk.END)),
                old_notes=str(the_selection_list[5]),
                newinitials=new_initials_entry_widget.get(), old_initials=str(the_selection_list[6]),
                newaccountid=str(new_account_id_entry_widget.get()),
                old_account_id=str(the_selection_list[7]),
                the_prodflow_quote_num=str(the_selection_list[8]),
                the_sap_quote_num=str(the_selection_list[9]),
                newprice=str(new_price_entry_widget.get()), old_price=str(the_selection_list[10]),
                tracking_number=str(the_selection_list[0]))).grid(row=12, column=1, padx=5, pady=5)
            #################
            # CANCEL BUTTON #
            ttk.Button(master=self.transient, text='CANCEL', width=15, command=self.transient.destroy).grid(row=12,
                                                                                                            column=2,
                                                                                                            padx=5,
                                                                                                            pady=5)
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

    def update_record(self, newname, old_name, newemail,
                      old_email, the_type, newsent,
                      old_sent, open_time, newnotes,
                      old_notes, newinitials,
                      old_initials, newaccountid,
                      old_account_id, the_prodflow_quote_num,
                      the_sap_quote_num, newprice,
                      old_price, tracking_number):  # {
        """
        CALL THE "check_quote_progress() FUNCTION HERE
        [ 2019-12-27 ] == addition of "initials" into METHOD
        [ 2019-12-30 ] == addition of "account_id" and "prodflow quote #"
        [ 2019-12-30 ] == addition of "sap quote #" and "price"
        """
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
        """
        if self.updated_records_validated(new_name=newname,
                                          new_email=newemail,
                                          new_initials=newinitials,
                                          new_account_id=newaccountid,
                                          new_price=newprice): # {
            print("filled out fcomplete!")
        # }
        """

        # IF NONE OF THE **IMPORTANT** ENTRY BOXES ARE LEFT EMPTY
        if len(str(newname)) != 0 and len(newemail) != 0 and len(newaccountid) != 0 and len(newprice) != 0:  # {
            logging.info("UPDATE-RECORD FIELDS ARE ALL FILLED IN COMPLETELY!")
            # ASK THE USER IF THEY ARE SURE WITH THEIR COMPLETION?
            confirm_box = messagebox.askyesno(title="Confirm Update", message="are you sure?")
            if str(confirm_box) == "yes":  # {
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
                        time_start = pd.Timestamp(ts_input=open_time)
                        print("TIME START == " + str(time_start))
                        run_time = time_meow - time_start
                        print("RUN TIME == " + str(run_time))
                        query = 'UPDATE quotes ' \
                                'SET name=?, email=?, type=?, sent=?, close_time=?, turn_around=?, notes=?, initials=?, account_id=?, prodflow_quote_number=?, sap_quote_number=?, price=?' \
                                'WHERE tracking_number=?'
                        parameters = (newname, newemail, the_type, newsent, str(time_meow),
                                      str(run_time), newnotes, newinitials, newaccountid,
                                      the_prodflow_quote_num, the_sap_quote_num, newprice,
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
                    # [2019-12-30]... ACCOUNT_ID, PRODFLOW QUOTE #, SAP QUOTE #, PRICE
                    else:  # {
                        print("\n\t\t\t>>>>>>> NOPE")
                        query = 'UPDATE quotes SET name=?, email=?, type=?, notes=?, initials=?, account_id=?, prodflow_quote_number=?, sap_quote_number=?, price=?' \
                                'WHERE tracking_number=? '
                        parameters = (newname, newemail, the_type, newnotes, newinitials,
                                      newaccountid, the_prodflow_quote_num, the_sap_quote_num,
                                      newprice, tracking_number)
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
            # }
        # }
        else:  # {
            messagebox.showwarning(parent=self.root, title="WARNING:", message="MISSING REQUIRED FIELD(S)!")
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
    application.tick()  # BEGIN "COUNTING" TIME(STAMP)
    window.config()
    window.mainloop()
# }