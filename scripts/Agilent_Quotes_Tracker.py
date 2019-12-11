"""
Created on Mon Dec 9 12:05:28 2019


@author: derbates
"""

# IMPORT THE GOODS
import os, sys, time
from time import sleep
from pathlib import Path
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
        self.root.minsize(height=1250)
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
            pass
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
        self.leftframe.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    #}

    def create_tab_control(self):  # {
        # TRY THE FOLLOWING
        try:  # {
            # CREATE MESSAGE AREA
            self.message = ttk.Label(master=self.leftframe, text='',
                                     font=("Sourcode Pro", 18), foreground='red')
            self.message.pack(side=tk.TOP, expand=True, fill=tk.BOTH)

            # NOTEBOOK WIDGET
            self.tab_control = ttk.Notebook(self.leftframe)

            # TAB-1
            self.tab1 = ttk.Frame(master=self.tab_control)
            self.tab_control.add(self.tab1, text='CREATE')
            self.tab_control.pack(expand=2, fill=tk.BOTH)

            # TAB-2
            self.tab2 = ttk.Frame(master=self.tab_control)
            self.tab_control.add(self.tab2, text='READ')
            self.tab_control.pack(expand=2, fill=tk.BOTH)

            # TAB-3
            self.tab3 = ttk.Frame(master=self.tab_control)
            self.tab_control.add(self.tab3, text='UPDATE')
            self.tab_control.pack(expand=2, fill=tk.BOTH)

            # TAB-4
            self.tab4 = ttk.Frame(master=self.tab_control)
            self.tab_control.add(self.tab4, text="DELETE")
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
            # Create the Tab Container
            self.lblframe_create = ttk.LabelFrame(master=self.tab1, text="CREATE")
            self.lblframe_create.pack(anchor=tk.CENTER, fill=tk.BOTH, expand=False)

            # Create the READ Tab Container
            self.lblframe_read = ttk.LabelFrame(master=self.tab2, text="READ")
            self.lblframe_read.pack(anchor=tk.CENTER, fill=tk.BOTH, expand=False)

            # Create the UPDATE Tab Container
            self.lblframe_update = ttk.LabelFrame(master=self.tab3, text="UPDATE")
            self.lblframe_update.pack(anchor=tk.CENTER, fill=tk.BOTH, expand=False)

            # Create the DELETE Tab COntainer
            self.lblframe_delete = ttk.LabelFrame(master=self.tab4, text="DELETE")

            self.lblframe_delete.pack(anchor=tk.CENTER, fill=tk.BOTH, expand=False)
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

            # <<< CLOCK (timestamp_test) >>>
            self.clock = ttk.Label(master=self.lblframe_create, font=("Times", 20, 'bold'), background='green')
            self.clock.grid(row=7, column=1, padx=5, pady=5, stick='w')

            # xXxXxXxXxXxXxXxXx
            # Notes Section
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
            self.notes.add(self.trackingnum_tab, text="TRACKING #")
            self.notes.add(self.quotenum_tab, text="QUOTE #")
            self.notes.add(self.timestamp_tab, text="TIMESTAMP")

            # keep_em_seperated = ttk.Separator(master=self.lblframe_create, orient=tk.HORIZONTAL)
            # keep_em_seperated.grid(row=6, column=0, columnspan=4)

            # [2019-11-20]\\self.notes.grid(row=5, column=0, columnspan=2, padx=5, sticky='n')
            self.notes.grid(row=8, column=0, columnspan=2, padx=5, pady=5, sticky='n')
            # row = 6, column = 0, columnspan = 2 AND NO STICK OR PADX

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
            self.tree.column('#0', width=100, minwidth=90, stretch=tk.NO)
            self.tree.column("one", width=125, minwidth=125, stretch=tk.NO)
            self.tree.column("two", width=150, minwidth=150, stretch=tk.NO)
            self.tree.column("three", width=50, minwidth=50, stretch=tk.NO)
            self.tree.column("four", width=128, minwidth=128, stretch=tk.NO)
            self.tree.column("five", width=45, minwidth=45, stretch=tk.NO)
            self.tree.column("six", width=100, minwidth=90, stretch=tk.NO)
            self.tree.column("seven", width=100, minwidth=90, stretch=tk.YES)

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
        item = self.tree.selection()['columns']
        messagebox.showinfo(title="test:", message="you clicked on" + str(self.tree.item(item, "text")))
    # }

    def on_delete_selected_button_selected(self):  # {
        self.message['text'] = ''
        # TRY THE FOLLOWING
        try:  # {
            self.tree.item(self.tree.selection())['columns'][0]
            logging.info(str(self.tree.item(self.tree.selection())['columns'][2]))
        # }
        except IndexError as e:  # {
            self.message['text'] = "No Item selected to modify:\n[" + str(e) + "]"
            return
        # }
        # TRY THE FOLLOWING
        try:  # {
            test_name = str(self.tree.item(self.tree.selection())['columns'][0])
            test_two = str(self.tree.item(self.tree.selection())['columns'][1])
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
            track_num = str(self.tracking_num.get())
            the_name = str(self.name.get())
            the_email = str(self.email.get())
            the_type = str(self.radio_type_var.get())
            the_sent = str(self.radio_sent_var.get())
            ts_meow = str(pd.Timestamp.now())
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
                record_entry = [str(row[0]), str(row[1]), str(row[2]), str(row[3]),
                                str(row[5]), str(row[4]), str(row[8])]
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

    # }

    def delete_record(self):  # {
        # TRY THE FOLLOWING
        try:  # {
            logging.info("DELETING RECORD")
        # }
        except:  # {
            pass
        # }
        else: # {
            logging.info("Operation Completed Successfully...")
        # }
    # }

    def open_modify_window(self):  # {
        pass
    # }

    def update_record(self, track_num, name, email, the_type, sent, open_ts, close_ts, turn_around, notes):  # {
        # TRY THE FOLLOWING
        try: #{
            logging.info("UPDATING RECORD")
            logging.info("NEW name == " + str(name))
        #}
        except: #{
            pass
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
    window.config()
    window.mainloop()
# }