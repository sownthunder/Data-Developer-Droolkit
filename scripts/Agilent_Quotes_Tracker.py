"""
Created on Mon Dec 9 12:05:28 2019


@author: derbates
"""

# IMPORT THE GOODS
import os, sys, time
from time import sleep
from pathlib import Path
import datetime
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import sqlite3, logging, random
import pyodbc
import pandas as pd
import numpy as np
from pandas import Series, DataFrame
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

class AgilentQuotesTracker():  # {

    db_filename = "data/quotes_tracker.db"
    time1 = ""

    def __init__(self, root):  # {
        self.root = root
        self.root.title("Agilent Quotes Tracker")
        self.root.resizable(width=True, height=True)
        # [2019-12-12]\\self.root.minsize(height=1250)
        self.root.minsize(width=1175, height=375)
        self.root.maxsize(width=1500, height=1250)
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

    def execute_df_query(self, query, the_conn): # {
        # TRY THE FOLLOWING
        try: #{
            df = pd.read_sql_query(sql=str(query),
                                   con=the_conn)
        #}
        except: #{
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
        #}
        else: #{
            logging.info("Operation Completed Successfully...")
        #}
    #}

    ###############################################################################################

    def tick(self): # {
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
    #}

    def create_gui(self):  # {
        # TRY THE FOLLOWING
        try:  # {
            # [2019-12-11]\\self.create_menubar()
            self.create_ttk_styles()
            # [2019-12-11]\\self.create_menubar()
            self.create_left_side()
            self.create_tab_control()
            self.create_tab_containers()
            self.fill_tab_containers()
            self.create_right_side()
            self.create_tree_view()
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

    def create_menubar(self): # {
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
    #}

    def create_ttk_styles(self):  # {
        # TRY THE FOLLOWING:
        try: #{
            themes = sorted(ttk.Style().theme_names())
            for t in themes: # {
                logging.info(str(t))
            # }
            # CONFIGURE THE STYLE
            self.style = ttk.Style()
            # Modify the font of the body
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
        #}
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

    def create_left_side(self): # {
        # CREATE FRAME CONTAINER
        self.leftframe = tk.Frame(self.root)
        # [2019-12-12]\\self.leftframe.pack(side=tk.LEFT, fill=tk.BOTH, expand=True) # fill=tk.Both
        # [2019-12-12]\\self.leftframe.pack(side=tk.LEFT, fill=tk.Y, expand=True)
        # [2019-12-12]\\self.leftframe.pack(side=tk.LEFT, fill=tk.BOTH, expand=False)
        self.leftframe.pack(side=tk.LEFT, fill=tk.X, expand=False)
    #}

    def create_tab_control(self):  # {
        # TRY THE FOLLOWING
        try:  # {
            # CREATE MESSAGE AREA
            self.message = ttk.Label(master=self.leftframe, text='',
                                     font=("Sourcode Pro", 18), foreground='red')
            #self.message.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
            self.message.pack(side=tk.TOP, fill=tk.BOTH, expand=False)

            # NOTEBOOK WIDGET
            self.tab_control = ttk.Notebook(self.leftframe)

            # TAB-1 // CREATE
            self.tab1 = ttk.Frame(master=self.tab_control)
            self.tab_control.add(self.tab1, text='CREATE')
            self.tab_control.pack(expand=2, fill=tk.BOTH)

            # TAB-2 // IMPORT OPTIONS
            self.tab2 = ttk.Frame(master=self.tab_control)
            self.tab_control.add(self.tab2, text='EDIT')
            self.tab_control.pack(expand=2, fill=tk.BOTH)

            # TAB-3 // EXPORT OPTIONS
            self.tab3 = ttk.Frame(master=self.tab_control)
            self.tab_control.add(self.tab3, text='EXPORT')
            self.tab_control.pack(expand=2, fill=tk.BOTH)

            # TAB-4 // HELP SECTION
            self.tab4 = ttk.Frame(master=self.tab_control)
            self.tab_control.add(self.tab4, text="HELP")
            self.tab_control.pack(expand=2, fill=tk.BOTH)
        #}
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
            logging.error("\n" + typeE +
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
        #}

    # }

    def create_tab_containers(self):  # {
        # TRY THE FOLLOWING:
        try:  # {
            # Create the CREATE Tab Container
            self.lblframe_create = ttk.LabelFrame(master=self.tab1, text="Begin A New Quote:")
            self.lblframe_create.pack(anchor=tk.CENTER, fill=tk.BOTH, expand=True)

            # Create the IMPORT Tab Container
            self.lblframe_import = ttk.LabelFrame(master=self.tab2, text="EDIT An Existing Quote:")
            self.lblframe_import.pack(anchor=tk.CENTER, fill=tk.BOTH, expand=True)

            # Create the EXPORT Tab Container
            self.lblframe_export = ttk.LabelFrame(master=self.tab3, text="EXPORT One or Multiple Quotes:")
            self.lblframe_export.pack(anchor=tk.CENTER, fill=tk.BOTH, expand=True)

            # Create the HELP Tab Container
            self.lblframe_help = ttk.LabelFrame(master=self.tab4, text="Help Section:")
            self.lblframe_help.pack(anchor=tk.CENTER, fill=tk.BOTH, expand=True)

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
        try: #{
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
            self.radio_type_1.grid(row=2, column=1, sticky='w', padx=5, pady=5)
            self.radio_type_2 = ttk.Radiobutton(master=self.lblframe_create, variable=self.radio_type_var,
                                                value="email", text="Email", width=15)
            self.radio_type_2.grid(row=2, column=1, sticky='e', padx=5, pady=5)

            # xXxXxXxXxXxXxXxXx
            # Sent Input
            ttk.Label(master=self.lblframe_create, text='Sent: ').grid(row=3, column=0, padx=5,
                                                                       pady=5, stick='w')
            ##########################
            # RADIO-VARIABLE == BOOL #
            self.radio_sent_var = tk.BooleanVar(master=self.lblframe_create, value=False)
            ################################################################################
            self.radio_sent_1 = ttk.Radiobutton(master=self.lblframe_create, variable=self.radio_sent_var,
                                                value=True, text="Yes", width=15)  # style="TButton")
            self.radio_sent_1.grid(row=3, column=1, sticky='w', padx=5, pady=5)
            self.radio_sent_2 = ttk.Radiobutton(master=self.lblframe_create, variable=self.radio_sent_var,
                                                value=False, text="No", width=15)
            self.radio_sent_2.grid(row=3, column=1, sticky='e', padx=5, pady=5)

            # TRACKING NUMBER #
            ttk.Label(master=self.lblframe_create, text='Tracking #: ').grid(row=5, column=0,
                                                                             padx=5, pady=5, sticky='w')
            self.tracking_num = ttk.Entry(master=self.lblframe_create, width=24)
            self.tracking_num.grid(row=5, column=1, sticky='w', padx=5, pady=5)

            # Timestamp (start_time)
            self.start_time_var = tk.StringVar(master=self.lblframe_create)
            ttk.Label(master=self.lblframe_create, text="Timestamp: ").grid(row=6, column=0, padx=5, pady=5, sticky='w')

            # <<< CLOCK (timestamp_test) >>>
            self.clock = ttk.Label(master=self.lblframe_create, font=("Calibri", 20, 'bold'),
                                   background='#2b303b', foreground="#bbc0c9")
            self.clock.grid(row=6, column=1, padx=5, pady=5, stick='w')

            # xXxXxXxXxXxXxXxXx
            # Notes Section
            ttk.Label(master=self.lblframe_create, text="NOTES: ").grid(row=7, column=0, columnspan=2,
                                                                        padx=5, pady=5, sticky='w')
            self.notes = ttk.Entry(master=self.lblframe_create, width=24)
            self.notes.grid(row=8, column=0, columnspan=2, padx=5, pady=5, sticky='w')

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
            self.notes.grid(row=8, column=0, columnspan=2, padx=5, pady=5, sticky='n')
            # row = 6, column = 0, columnspan = 2 AND NO STICK OR PADX

            # xXxXxXxXXxXXxXXxX
            # SUBMIT "CREATE" BUTTON
            ttk.Button(master=self.lblframe_create,
                       text="CREATE", width=24,
                       command=self.add_new_record).grid(row=9, column=0, rowspan=1,
                                                         columnspan=2, padx=5, pady=5, sticky='nesw')
            # TRACKING_NUMBER (tracking#) #
            # NAME #
            # EMAIL #
            # TYPE #
            # SENT #
            # OPEN_TIME (timestamp) #
            # CLOSE_TIME (end_timestamp) #
            # TURN_AROUND (overall timestamp) #
            # NOTES #
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

    def create_right_side(self):  # {
        # Create a Frame Container
        self.rightframe = ttk.Frame(master=self.root)
        self.rightframe.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
    # }

    def create_tree_view(self):  # {
        # TRY THE FOLLOWING
        try: #{
            # TABLE
            self.tree = ttk.Treeview(master=self.rightframe, style="mystyle.Treeview",
                                     height=30, columns=8)  # height = 20
            self.tree["columns"] = ("one", "two", "three", "four", "five", "six", "seven")
            self.tree.column('#0', width=120, minwidth=115, stretch=tk.NO)
            self.tree.column("one", width=125, minwidth=125, stretch=tk.YES)
            self.tree.column("two", width=150, minwidth=150, stretch=tk.YES)
            self.tree.column("three", width=50, minwidth=50, stretch=tk.YES)
            self.tree.column("four", width=128, minwidth=128, stretch=tk.YES)
            self.tree.column("five", width=45, minwidth=45, stretch=tk.YES)
            self.tree.column("six", width=100, minwidth=90, stretch=tk.YES)
            self.tree.column("seven", width=100, minwidth=90, stretch=tk.NO)

            # Definitions of Headings
            # [2019-12-05]\\self.tree.grid(row = 1, column = 0, columnspan = 8, sticky = 'S')
            self.tree.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
            self.tree.heading('#0', text='Tracking #', anchor=tk.CENTER)
            self.tree.heading('#1', text='Name', anchor=tk.CENTER)
            self.tree.heading('#2', text='Email', anchor=tk.CENTER)
            self.tree.heading('#3', text='Type', anchor=tk.CENTER)
            self.tree.heading('#4', text='Timestamp', anchor=tk.CENTER) # "Open_time" in BACKEND
            self.tree.heading('#5', text='Sent', anchor=tk.CENTER)
            self.tree.heading('#6', text='Turn Around', anchor=tk.CENTER)
            self.tree.heading('#7', text='Notes', anchor=tk.CENTER)

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

    def on_add_record_button_click(self):  # {
        self.add_new_record()
    # }

    def on_double_click(self, event):  # {
        # [2019-12-12]\\selected_track_num = self.tree.selection()[0]  # which tracking number you selected
        item = self.tree.selection()[0]  # which row did you click on
        print("ITEM CLICKED ", str(item)) # variable that represents the row you clicked on
        # [2019-12-12]\\item_2 = self.tree.item(self.tree.selection())  # gets all the values of the selected row
        # [20190-12-12]\\print('the test_str = ', type(item_2), item_2, '\n') # prints a dictionary of the selected row
        print(self.tree.item(item)['values'][0]) # prints the first value of the values (the id value)
        # [2019-12-12]\\item_2 = str(self.tree.item(self.tree.selection())['columns'][0])
        # [2019-12-12]\\logging.info("ITEM 2 == " + str(item_2))
        messagebox.showinfo(title="test:", message="you clicked on:\n" + str(self.tree.item(item, option="text")))
        selected_name = str(self.tree.item(item)['values'][1])
        selected_email = str(self.tree.item(item)['values'][2])
        selected_type = str(self.tree.item(item)['values'][3])
        selected_sent = str(self.tree.item(item)['values'][4])
        selected_notes = str(self.tree.item(item)['values'][6])
        selection_string = "YOU SELECTED:\n" + selected_name + "\n" + selected_email + "\n" + selected_type + "\n" + selected_sent + "\n" + selected_notes
        messagebox.showwarning(title=str(pd.Timestamp.now()), message=str(selection_string))
        # [2019-12-12]\\messagebox.showinfo(title="yupp!", message=str(self.tree.item(item_2, "text")))
        """
        selected_open_time = 
        selected_close_time =
        selected_turn_around = 
        """
    # }

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

    ######################################################################################################
    # QUOTE NUMBER CONVENTION AND PROGRESS CHECKS #
    ###############################################

    def check_quote_completion(self, the_df):  #{
        # TRY THE FOLLOWING
        try: #{
            # LIST TO HOLD RESULTS
            result = []
            # FOR EACH ROW-ENTRY IN "sent" COLUMN
            for value in the_df["sent"]:  # {
                if value is False:  # {
                    # append nothing (Keeping index)
                    result.append("")
                # }
            # }
            else: #{
                # MAKE SURE "turn_around" IS ALSO EMPTY
                if str(the_df["turn_around"]):  # {
                    # CREATE TIMESTAMP FOR "meow"
                    meow_ts = pd.Timestamp.now()
                    # APPEND TO RESULT
                    result.append(str(meow_ts))
                #}
                else:  # {
                    logging.info("NOT EMPTY!")
                # }
            # }
            # OVERWRITE COL?
            the_df["turn_around"] = result
            logging.info(the_df)
            # RETURN DATAFRAME TO REPLACE OLD/OUTDATED ONE
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
            logging.error("\n" + typeE +
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
        #}
    #}

    """
    CREATES NEW QUOTE NUMBER ACCORDING TO NAMING CONVENTION:
    301 + (YYYYMMDD) + Hour + Minute
    Example: 301201912121051
    """
    def quote_number_convention(self): # {
        # CREATE TIME STAMP FOR QUOTE NUMBER CONVENTION
        date_object = datetime.date.today()
        time_object = str('{0:%Y%m%d%H%M}'.format(datetime.datetime.now()))
        logging.info(str("QUOTES naming conventino (today's example) : "), time_object)
        # RETURN STR CONTAINING PROPER NAMING
        return str("301" + time_object)
    # }

    ###################################################################################################
    # ADD / UPDATE / DELETE FUNCTION BELOW #
    ########################################

    """
    old "INSERT_RECORD"
    """
    def add_new_record(self):  # {
        # TRY THE FOLLOWING
        try:  # {
            logging.info("...ADDING NEW RECORD...")
            # create ENTRY variables
            track_num = [self.quote_number_convention()]  # auto-creates number
            the_name = [str(self.name.get())]
            the_email = [str(self.email.get())]
            the_type = [str(self.radio_type_var.get())]
            the_sent = [str(self.radio_sent_var.get())]
            open_time = [str(pd.Timestamp.now())]
            close_time = [str("")]
            turn_around = [str("None")]  # np.Nan?
            the_notes = [str(self.notes.get())]
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
                              'notes': the_notes}
            # CREATE EMPTY DATAFRAME
            new_entry_df = pd.DataFrame(data=new_entry_dict, index=None, dtype=np.str)
            # CREATE ENGINE (for sending to Database)
            engine = create_engine('sqlite:///data/quotes_tracker.db')
            # SEND DATAFRAME TO DATABASE
            new_entry_df.to_sql(name="quotes", con=engine, if_exists="append", index=False)
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
        return len(self.name.get()) != 0 and len(self.email.get()) !=0 and len(self.radio_type_var.get()) !=0 and len(self.radio_sent_var.get())
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
                logging.info("TRACKING # == " + str(row[0]))
                logging.info("NAME === " + str(row[1]))
                logging.info("Email == " + str(row[2]))
                logging.info("Type == " + str(row[3]))
                logging.info("Sent == " + str(row[4]))
                logging.info("Open_Time == " + str(row[5]))
                logging.info("Close_Time == " + str(row[6]))
                logging.info("Turn_Around == " + str(row[7]))
                logging.info("Notes == " + str(row[8]))
                # CREATE LIST TO HOLD RECORD ENTRY
                # [Tracking #] [Name] [Email] [Type] [Timestamp/open_time]
                record_entry = [str(row[1]), str(row[2]), str(row[3]), str(row[5]),
                                str(row[4]), str(row[7]), str(row[8])]
                # INSERT RECORD ENTRY INTO TREE
                self.tree.insert('', 0, text=str(row[0]), values=record_entry)
            # }
        #}
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

    def delete_record(self):  # {
        # TRY THE FOLLOWING
        try:  # {
            logging.info("DELETING RECORD")
            self.message['text'] = ''
            tracking_num = self.tree.item(self.tree.selection())['text']
            query = 'DELETE from quotes WHERE tracking_num = ?'
            self.execute_db_query(query, (tracking_num,))
            self.message['text'] = 'Quote Record for {} deleted'.format(tracking_num)
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
        else: # {
            logging.info("Operation Completed Successfully...")
        # }
    # }

    def open_modify_window(self):  # {
        # TRY THE FOLLOWING
        try: #{
            logging.info("MODIFYING RECORD")
            track_num = self.tree.item(self.tree.selection()['text'])
            old_name = self.tree.item(self.tree.selection())['values'][0]
            self.transient = tk.TopLevel(master=self.root)
            # TRACKING #
            ttk.Label(master=self.transient, text='Tracking #:').grid(row=0, column=1)
            ttk.Entry(master=self.transient, textvariable=tk.StringVar(
                self.transient, value=track_num), state='readonly').grid(row=0, colum=2)
            # OLD-NAME
            ttk.Label(master=self.transient, text="Old Name:").grid(row=1, column=1)
            ttk.Entry(self.transient, textvariable=tk.StringVar(
                self.transient, value=old_name), state='readonly').grid(row=1, column=2)
            # NEW-NAME
            ttk.Label(master=self.transient, text="New Name:").grid(
                row=2, column=1)
            new_name_entry_widget = ttk.Entry(self.transient)
            new_name_entry_widget.grid(row=2, column=2)
            ttk.Button(self.transient, text='Update Quote', command=lambda: self.update_record(
                newname=new_name_entry_widget.get(), old_name=old_name, tracking_number=track_num)).grid(row=3,
                                                                                                         column=2,
                                                                                                         sticky=tk.E)
            self.transient.mainloop()
            ############################
            # CALL UPDATE RECORD BELOW #
            ############################
        #}
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
            logging.error("\n" + typeE +
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
        # }
    # }

    def update_record(self, newname, old_name, newemail, old_email, newtype, old_type, newsent, old_sent,
                      newopentime, old_open_time, newclosetime, old_close_time, newturnaround, old_turn_around,
                      newnotes, old_notes, tracking_number):  # {
        # TRY THE FOLLOWING
        try: #{
            logging.info("UPDATING RECORD")
            logging.info("NEW name == " + str(newname))
        #}
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
            logging.error("\n" + typeE +
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
        # }
    # }

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