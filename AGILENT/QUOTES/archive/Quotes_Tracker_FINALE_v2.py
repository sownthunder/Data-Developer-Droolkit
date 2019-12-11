# -*- coding: utf-8 -*-
"""
Created on Mon Dec 9 12:05:28 2019

A GARBAGE ATTEMPT AT MAKING IT SO THE DATABASE IS READ FROM  A.CSV
FILE ON HE SERVER AND THEN IMPORTED INTO A SQLite DATABASE THAT IS
STORED IN MEMORY AND NOT ON THE DISK SO MORE THAN ONE PERSON CAN ACCESS
THE DATABASE / APPLICATION AT A TIME WITHOUT HAVING ANY ERRORS

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
from threading import Thread, Timer
import pandas as pd
import numpy as np
from pandas import Series, DataFrame
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

class QuotesBook:  # {

    db_file = "C:/data/inbound/quotes_db.csv"
    time1 = ""

    def __init__(self, root):  # {
        # PULL DATAFRAME FROM .CSV FILE
        self.df = pd.read_csv(self.db_file, dtype=np.str, engine='python')
        print(self.df)
        sleep(30)
        # SETUP / ESTABLISH *TEMPORARY* DATABASE CONNECTION(S)
        self.engine = self.create_temp_database(the_df=self.df)
        # [2019-12-10]\\self.temp_db = self.create_temp_database(the_df=self.df)
        self.root = root
        self.root.title("AGILENT Quote Tracker")
        self.root.resizable(width=True, height=True)
        self.create_gui()
        # [2019-10-12]\\self.create_tree_view()
    # }

    def execute_db_query(self, the_database, query, parameters=()):  # {
        with sqlite3.connect(database=the_database) as conn:  # {
            cursor = conn.cursor()
            query_result = cursor.execute(query, parameters)
            conn.commit()
        # }
        return query_result
    # }

    def create_gui(self):  # {
        # TRY THE FOLLOWING
        try:  # {
            self.create_left_icon()
            self.create_paned_window()
            self.create_message_area()
            self.create_tree_view()
            self.create_buttons()
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
            logging.info("SUCCESS! VERY NICE!")
        # }
    # }

    def create_left_icon(self):  # {
        # TRY THE FOLLOWING
        try: # {
            photo = tk.PhotoImage(file="../icons/agilent_logo-Copy1.png")
            label = ttk.Label(image=photo)
            label.image = photo
            label.grid(row=0, column=0)
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
            logging.info("SUCCESS! VERY NICE!")
        #}
    # }

    def create_paned_window(self):  # {
        pass
    # }

    def create_message_area(self):  # {
        pass
    # }

    def create_tree_view(self):  # {
        # TRY THE FOLLOWING
        try: #{
            # CREATE TREE VIEW
            self.tree = ttk.Treeview(master=self.root, height=30, columns=8)
            self.tree["columns"] = ("one", "two", "three", "four", "five", "six")
            self.tree.column('#0', width=100, minwidth=90, stretch=tk.NO)
            self.tree.column("one", width=125, minwidth=125, stretch=tk.NO)
            self.tree.column("two", width=150, minwidth=150, stretch=tk.NO)
            self.tree.column("three", width=50, minwidth=50, stretch=tk.NO)
            self.tree.column("four", width=128, minwidth=128, stretch=tk.NO)
            self.tree.column("five", width=45, minwidth=45, stretch=tk.NO)
            self.tree.column("six", width=150, minwidth=150, stretch=tk.NO)

            # CREATE TREE HEADINGS
            self.tree.grid(row=1, column=0, columnspan=7)
            self.tree.heading('#0', text='Tracking #', anchor=tk.CENTER)
            self.tree.heading('#1', text='Name', anchor=tk.CENTER)
            self.tree.heading('#2', text='Email', anchor=tk.CENTER)
            self.tree.heading('#3', text='Type', anchor=tk.CENTER)
            self.tree.heading('#4', text='Timestamp', anchor=tk.CENTER)
            self.tree.heading('#5', text='Sent', anchor=tk.CENTER)
            self.tree.heading('#6', text='Notes', anchor=tk.CENTER)

            # CREATE CLICK BINDINGS
            self.tree.bind("<Double-1>", self.on_double_click)
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
            logging.info("SUCCESS! VERY NICE!")
        #}

    # }

    def create_buttons(self):  # {
        pass
    # }

    def on_double_click(self, event):  # {
        item = self.tree.selection()[0]
        # "you clicked on", self.tree.item(item, "text")
        messagebox.showinfo(title="test:", message="you clicked on" + str(self.tree.item(item, "text")))
    # }

    """
    CHECKS EVERY COL OF "Sent" OF EVERY ROW, and creates temp TIMESTAMP for each:
    Sent == False
    Turn_Around **is** empty
    """
    def check_quote_completion(self, the_dataframe):  # {
        # TRY THE FOLLOWING
        try:  # {
            # ITERTHRU DATAFRAME
            for row in the_dataframe.itertuples():  # {
                print(row)
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
            logging.info("SUCCESS! VERY NICE!")
    # }

    """
    creates a SQL-ALCHEMY "engine" to further create a connection to SQLite database
    that resides in memory, then imports the dataframe "the_df" into said database
    RETURNS: connection to SQLite db
    """
    def create_temp_database(self, the_df):  # {
        # TRY THE FOLLOWING
        try:  # {
            # CREATE CONNECTION TO IN-MEMORY DATABASE
            # [2019-12-10]\\engine = create_engine('sqlite://')
            conn = sqlite3.connect(':memory:')
            logging.info("SQLITE VERSION == " + str(sqlite3.version))
            # CREATE ENGINE FROM CONNECTION
            engine = create_engine(conn)
            # INSERT DATAFRAME TO BECOME TABLE/DATABASE
            the_df.to_sql(name="quotes", con=engine, if_exists="replace", index=False)
            # call function to populate tree
            # [2019-12-10]\\self.view_records()

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
        else: # {
            logging.info("SUCCESS! VERY NICE!!")
            return conn
        # }

    # }

    """
    called when new entry to DATABASE (dataframe) is needed to be created
    """
    def create_record_df(self, track_num, name, email, the_type, ts, sent):  # {
        print("call [CHECK_QUOTE_COMPLETEION] at end")
    # }

    """
    called when the temporary SQLite db connection needs to be closed
    """
    def close_connection(self, the_conn):  # {
        pass
    # }

    """
    updates the TEMP (in-memory) SQLITE database
    """
    def view_records(self):  # {
        logging.info("attempting to read in records for VIEWING...")
        # TRY THE FOLLOWING
        try:  # {
            items = self.tree.get_children()
            for item in items:  # {
                self.the_tree.delete(item)
            # }
            query = 'SELECT * FROM quotes ORDER BY TIMESTAMP desc'
            quote_tracker_entries = self.execute_db_query(the_database=self.engine, query=query)
            for row in quote_tracker_entries:  # {
                logging.info("TRACKING # == " + str(row[0]))
                logging.info("NAME == " + str(row[1]))
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
        else: # {
            logging.info("SUCCESS! VERY NICE!!")
        # }
    # }

    def overwrite_db_file(self, the_db_file):  # {
        # POPUP MESSAGEBOX CONFIRMING FOR USER
        messagebox.askyesnocancel(title="SAVING DB", message="are you sure chad?")
    # }

    def tick(self):  # {
        pass
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
        print("[setup_logger] Logger setup successfully")
    # }
# }

if __name__ == "__main__":  # {
    # LOGGER
    setup_logger()
    # TRY THE FOLLOWING
    try:  # {
        window = tk.Tk()
        application = QuotesBook(window)
        application.tick()
        window.mainloop()
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
        print("[main] Operation done successfully")
    # }
# }