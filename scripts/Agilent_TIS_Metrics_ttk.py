# -*- coding: utf-8 -*-
"""
Created on Wed Mar 18 14:48:03 2020
UPDATED on Thu Apr 02 13:11:00 2020

TIS_Metrics_ttk (using tkinter library)

TABLES USED:
    - tblProdflow
    - ORDERS

===================================================
- Takes the INPUT OF USER (month?)
- pulls tables from Prodflow
- Returns desired matches with "Materials_List.csv"
===================================================

@author: derbates
"""

# IMPORT THE GOODS
import os, sys, time
from time import sleep
from pathlib import Path
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from pandas import Series, DataFrame
import logging
import pyodbc
from openpyxl import Workbook, load_workbook
from openpyxl.drawing.image import Image
from openpyxl.utils.dataframe import dataframe_to_rows
import tempfile
import logging
from threading import Thread
from ttkthemes import ThemedStyle
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox, filedialog, commondialog

class Logger(): # {
    
    def __init__(self, logging_output_dir): # {
        self.logging_output_dir = logging_output_dir
        # INITIATING THE LOGGER OBJECT
        self.logger = logging.getLogger(__name__)
        
        # set the level of the logger (THIS IS SUPER USEFUL since it enables)
        # Explanation regarding the logger levels can be found here:
        # https://docs.python.org/3/howto/logging.html
        self.logger.setLevel(logging.DEBUG)
        
        # Create the logs.log file
        user_name = str(os.getlogin()) # get username
        log_file_name = user_name + "." + str(pd.Timetsamp.now())[:10] + "-quotes-use"
        log_file_path = os.path.join(self.logging_output_dir, str(log_file_name) + ".log")
        file_handler = logging.FileHandler(log_file_path)
        
        # Create the console handler with a higher log level
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.ERROR)
        
        # Format the logs structure so that every line would include:
        # the time, the message, the function, the line #, script and level name
        formatter = logging.Formatte('%(asctime)s: %(message)s, FROM=%(funcName)s, LINENO=%(lineno)d, %(name)s - %(levelname)s')
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        # Adding the formater handlers
        self.logger.addHandler(console_handler)
        self.logger.addHandler(file_handler)
        
        # and printing the logs to the console as well
        self.logger.addHandler(logging.StreamHandler(sys.stdout))
    # }
# }

class Agilent_TIS_Metrics(): # {
    
    user_name = str(os.getlogin()) # get username
    outbound_dir = "C:/data/outbound/" + str(pd.Timestamp.now())[:10]
    desktop_dir = "OneDrive - Agilent Technologies/Desktop"
    
    # BOOL VALUES TO HOLD "unlock conditions"
    is_imported = False
    
    def __init__(self, root, the_logger): # {
        self.root = root
        self.the_logger = the_logger
        self.root.title("TIS Metrics")
        self.root.geometry('315x200+300+300')
        self.root.resizable(width=True, height=True)
        self.root.minsize(width=100, height=100)
        self.root.maxsize(width=400, height=400)
        # Get/Set USERNAME & DESKTOP DIRECTORIES
        self.user_name_dir = os.path.join("C:/Users/", self.user_name)
        self.desktop_dir = os.path.join(self.user_name_dir, self.desktop_dir)
        print("USER DIR == " + str(self.user_name_dir))
        print("DESKTOP == " + str(self.desktop_dir))
        # INITALIZE UI
        self.create_gui(the_root = self.root)
    # }
    
    def create_gui(self, the_root): # {
        # TRY THE FOLLOWING
        try: # {
            self.create_ttk_styles(the_root=the_root)
            # [2020-04-13]\\self.create_label_frame(the_root=the_root)
            self.create_main_frame(the_root=the_root)
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
    
    def create_ttk_styles(self, the_root): # {
        # TRY THE FOLLOWING
        try: # {
            self.style = ThemedStyle(the_root)
            # STYLE THEME
            self.style.set_theme("arc") # clearlooks, ITFT1, smog, *arc*, winxpblue
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
    
    # [2020-04-13]\\
    """
    def create_label_frame(self, the_root): # {
        self.labelframe = ttk.Frame(the_root)
        self.labelframe.pack(anchor=tk.CENTER, fill=tk.BOTH, expand=True)
        
        ttk.Label(master=self.labelframe, text="I wish..."
                  ).pack(anchor=tk.CENTER, fill=tk.BOTH, expand=False)
        
    # }
    """
    
    def create_main_frame(self, the_root): # {
        # TRY THE FOLLOWING
        try: # {
            self.mainframe = ttk.Frame(the_root)
            # [2020-04-13]\\self.mainframe.pack(anchor=tk.CENTER, fill=tk.X, expand=True)
            self.mainframe.pack(anchor=tk.CENTER, fill=tk.BOTH, expand=True)
            
            # TKINTER VARS TO HOLD INPUT VALUES
            self.end_date = tk.StringVar(master=the_root, value=str(pd.Timestamp.now())[:10])
            self.start_date = tk.StringVar(master=the_root, value=None)
            
            # START/END DATE & ENTRY LABELS
            ttk.Label(master=self.mainframe, text="Enter START Date: \n(YYYY-MM-DD)"
                     ).pack(anchor=tk.NW, fill=tk.X, expand=True)
            ttk.Entry(master=self.mainframe, textvariable=self.start_date
                      ).pack(anchor=tk.NE, fill=tk.BOTH, expand=True)
            ttk.Label(master=self.mainframe, text="Enter END Date:\n(YYYY-MM-DD)"
                      ).pack(anchor=tk.SW, fill=tk.X, expand=True)
            ttk.Entry(master=self.mainframe, textvariable=self.end_date
                      ).pack(anchor=tk.SE, fill=tk.BOTH, expand=True)
            # .CSV FILE IMPORT BUTTON
            self.csv_import = ttk.Button(master=self.mainframe, text="Import MATERIALS .csv",
                                    command=self.import_materials_file)
            self.csv_import.pack(anchor=tk.S, fill=tk.BOTH, expand=False)
            #####################################
            # EXPORT FILE LOCATION BUTTON / RUN # 
            #####################################
            self.export_button = ttk.Button(master=self.mainframe, text="<< RUN >>",
                                       state=tk.DISABLED, command=self.select_export_path
                                      )
            self.export_button.pack(anchor=tk.S, fill=tk.BOTH, expand=False)
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
    
    def import_materials_file(self): # {
        # TRY THE FOLLOWING
        try: # {
            print("IMPORTING <<materials>> file...")
            self.materials_file_path = Path(filedialog.askopenfilename(master=self.root, 
                                                                       title="Select MATERIALS .csv:",
                                                                       filetypes=((".csv", "*.csv"), ("All Files", "*.*")))
                                            )
            # IMPORT FILEPATH INTO DATAFRAME
            self.df_infile = pd.read_csv(self.materials_file_path, header=0, dtype=np.str, engine='python')
            # CREATE SERIES off of DataFrame
            self.materials_file = pd.Series(data=self.df_infile['ProductNo'], copy=True)
            print("df_infile:\n" + str(self.df_infile.head()))
            print("SERIES:\n" + str(self.materials_file))
            # NOW MAKE OTHER BUTTON *ACTIVATED*
            self.export_button['state'] = tk.ACTIVE
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
        else: # {
            print("Operation Completed Successuflly...")
        # }
    # }
    
    def select_export_path_in_thread(self): # {
        # TRY THE FOLLOWING
        try: # {
            # START THREAD
            self.thread = Thread(None, self.select_export_path, None, (), {}, daemon=True)
            self.thread.start()
        # }
        except: # {
            pass
        # }
    # }
    
    def select_export_path(self): # {
        # TRY THE FOLLOWING
        try: # {
            print("Selecting EXPORT location...")
            self.export_file_path = Path(filedialog.askdirectory(master=self.root, title="Select EXPORT Location:"))
            # CREATE FILE PATH FOR THE export .csv
            """
            self.export_file_path = os.path.join(self.export_file_path, "TIS-Material-Merge-"
                                                + str(pd.Timestamp.now())[:10]
                                                + ".csv")
            """
            # CALL DETERMINE RANGE() (to begin run)
            self.determine_range()
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
    
    def determine_range(self): # {
        # TRY THE FOLLOWING
        try: # {
            print("DETERMINING RANGE....")
            # CREATE CLASS VARIABLES FOR START TIME
            self.the_end_date = pd.Timestamp(ts_input=str(self.end_date.get()))
            print("THE-END-DATE:\n\t\t" + str(self.end_date.get()))
            # CREATE CLASS VARIABLE FOR END TIME (off input)
            self.the_start_date = pd.Timestamp(ts_input=str(self.start_date.get()))
            print("THE-START-DATE:\n\t\t" + str(self.start_date.get()))
            # DETERMINE NUMBER OF DAYS
            self.num_of_days = pd.Timedelta(self.the_end_date - self.the_start_date)
            print("NUM OF DAYS:\n\t" + str(self.num_of_days))
            # CALL RUN
            self.run(date_input=self.the_end_date, day_range=self.num_of_days)
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
    
    def run(self, date_input, day_range): # {
        # TRY THE FOLLOWING
        try: # {
            # Create date (OFF INPUT)
            the_date = pd.Timestamp(ts_input=str(date_input))
            # create day range
            x_days_ago = the_date - pd.Timedelta(value=day_range, unit='D')
            # [2020-04-06]\\x_days_ago = the_date - timedelta(days = int(day_range))
            df_x_range = pd.date_range(start=x_days_ago, end=the_date, freq='D')
            print(str(df_x_range))
            # CREATE METRICS TABLE FROM CLASS METHOD
            # (returning only time-series we want??)
            self.df_metrics_table = self.create_metrics_table(
                time_start=x_days_ago, # "2019-11-01"
                time_end=the_date # "2020-03-01"
                )
            """
            <<< CREATE COPY OF DATAFRAME WITH **NO INDEX** >>
            """
            # [2020-04-06]\\df_metrics_no_idx = pd.DataFrame(data=self.df_metrics_table, copy=True)
            """
            <<< SET INDEX BUT ALSO KEEP AS COLUMN >>>
            """
            # [2020-04-06]\\self.df_metrics_table.set_index(['QCDate'], drop=False, inplace=True)
            """
            <<< CHANGE DATA-TYPES OF COLUMNS >>
            """
            # CREATE EMPTY DATAFRAME TO HOLD SPECIFIC TIS DATA
            df_TIS_metrics = pd.DataFrame(data=None, dtype=np.str, index=None) #index = df_x_range
            # ADD IN COLUMNS
            df_TIS_metrics['QCDate'] = self.df_metrics_table['QCDate']
            # [2020-04-10]\\df_TIS_metrics['QCDate'] = self.df_tblProdflow['QCDate']
            #df_TIS_metrics['QCDate'] = pd.to_datetime(df_TIS_metrics.index)
            df_TIS_metrics['OrderID'] = self.df_metrics_table['OrderID']
            df_TIS_metrics['ProductNo'] = self.df_metrics_table['ProductNo']
            df_TIS_metrics["Volume"] = self.df_metrics_table["Volume"]
            df_TIS_metrics["BuildByDate"] = self.df_metrics_table["BuildByDate"]
            df_TIS_metrics["OrderDate"] = self.df_metrics_table["OrderDate"]
            df_TIS_metrics["PrepDate"] = self.df_metrics_table["PrepDate"]
            df_TIS_metrics["PrepVolume"] = self.df_metrics_table["PrepVolume"]
            df_TIS_metrics["UnitizeNLT"] = self.df_metrics_table["UnitizeNLT"]
            df_TIS_metrics["ShipNLTDate"] = self.df_metrics_table["ShipNLTDate"]
            df_TIS_metrics["BulkQCDate"] = self.df_metrics_table["BulkQCDate"]
            df_TIS_metrics["AmpDate"] = self.df_metrics_table["AmpDate"]
            df_TIS_metrics["GreenSheet"] = self.df_metrics_table["GreenSheet"]
            df_TIS_metrics["SOLink"] = self.df_metrics_table["SOLink"]
            df_TIS_metrics["Notes"] = self.df_metrics_table["Notes"]
            # [2020-04-06]\\
            """
            df_TIS_metrics.to_csv(os.path.join(self.export_file_path, "df-TIS-metrics-"
                                               + str(pd.Timestamp.now())[:10]
                                               + ".csv"), index=True)
            """
            # MERGE WITH MATERIALS IN FILE
            df_merge = pd.merge(df_TIS_metrics, self.df_infile, on='ProductNo', how='inner')
            # CREATE MERGE ATTEMPT # 2
            merged = df_TIS_metrics.join(self.df_infile, how = 'right', lsuffix = '_x')
            # [2020-04-06]\\
            """
            merged.to_csv(os.path.join(self.export_file_path, "df-merged-"
                                       + str(pd.Timestamp.now())[:10]
                                       + ".csv"), index=True)
            """
            # SET INDEX OF "df_merge" to be that of QCDATE :)
            df_merge.set_index(['QCDate'], inplace=True)
            # SORT INDEX (in-place)
            df_merge.sort_index(inplace=True)
            print(str(df_merge.info()))
            # After-Index #############################################################
            # NARROW DOWN EVEN FURTHER (based off Order Date, not QCDATE this time )  #
            ###########################################################################
            df_merged = df_merge[(df_merge['OrderDate'] >= x_days_ago) & (df_merge['OrderDate'] <= the_date)]
            # create index variable with data set to "OrderID"
            idx_order_id = pd.Index(data=df_merged['OrderID'])
            """
            sample = df_merged.sample(15)
            sample.to_csv(os.path.join(self.export_file_path, "df-merged-"
                                                     + str(pd.Timestamp.now())[:10]
                                                     + ".csv"), 
                          index_label="INDEX:qcdate", 
                          index=True)
            """
            # RESET INDEX SO THERE IS NONE (on a copy)
            df_merged_no_idx = df_merged.reset_index()
            """
            sample_no_idx = df_merged_no_idx.sample(15)
            sample_no_idx.to_csv(os.path.join(self.export_file_path, "df-merged-no-idx-"
                                              + str(pd.Timestamp.now())[:10]
                                              + ".csv"),
                                 index_label="INDEX:num",
                                 index=True)
            """
            # CREATE * NUMERICAL INDEX * var
            num_idx = df_merged_no_idx.index
            df_merged_FINALE = pd.DataFrame(data=df_merged_no_idx, 
                                            index=num_idx,
                                            columns=['OrderID', 'ProductNo',
                                                     'Volume', 'PrepVolume',
                                                     'OrderDate', 'BuildByDate',
                                                     'PrepDate', 'BulkQCDate',
                                                     'UnitizeNLT', 'AmpDate',
                                                     'GreenSheet', 'QCDate',
                                                     'ShipNLTDate', 'SOLink', 'Notes'])
            ##############################
            # CREATE FILENAME FOR EXPORT #
            ##############################
            export_filename_dates = str(x_days_ago)[:10] + "-" + str(the_date)[:10]
            #################
            # EXPORT FINALE #
            #################
            df_merged_FINALE.to_csv(os.path.join(self.export_file_path, "TIS-Material-Merge-"
                                                + str(export_filename_dates) + ".csv"),
                             index=False)
            # MAKE THE RUN BUTTON LOCKED AGAIN SO USER MUST RE-IMPORT MATEIRALS FILE
            self.export_button['state'] = tk.DISABLED
            ##########################################################################
            ## ALL FAILURES BELOW #
            ###########################################################################
            """
            # CHANGE INDEX to "OrderID" FOR EXPORT
            # save index as value
            merge_idx = pd.Index(data=df_merged['OrderID'])
            csv_idx = pd.Index(data=df_merged['OrderID'])
            print("CSV-IDX:\n" + str(merge_idx))
            # CREATE NEW EMPTY DATAFRAME (specifically for exporting...)
            # df_merged_csv = pd.DataFrame(data=)
            # SET NEW INDEX BUT KEEP OLD INDEX AS COLUMN , DONT DROP
            # [2020-04-13]\\df_merged.set_index(['OrderID'], drop=False, inplace=True)
            df_merged.reindex(columns=['ProductNo', 'Volume',
                                       'PrepVolume', 'OrderDate',
                                       'BuildByDate', 'PrepDate',
                                       'BulkQCDate', 'UnitizeNLT',
                                       'AmpDate', 'GreenSheet',
                                       'QCDate', 'ShipNLTDate',
                                       'SOLink', 'Notes'],
                              index=num_idx,
                              copy=False)
            """
            # <<<<< USE RE-INDEX >>>> 
            """
            df_merged.reindex(index=merge_idx, 
                              columns=['ProductNo', 'Volume', 'PrepVolume', 
                                       'OrderDate', 'BuildByDate', 'PrepDate',
                                       'BulkQCDate', 'UnitizeNLT', 'AmpDate',
                                       'GreenSheet', 'QCDate', 'ShipNLTDate',
                                       'SOLink', 'Notes'], copy=False)
            """
            """
            <<< EXPORT >>>
            """
            # EXPORT .CSV TO LOCATION CHOSEN BY USER
            # [2020-04-13]\\
            """
            df_merge.to_csv(os.path.join(self.export_file_path, "TIS-Material-Merge-" 
                                         + str(pd.Timestamp.now())[:10]
                                         + ".csv"), index=True)
            """
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
        else: # {
            print("Operation Completed Successfully...")
        # }
    # }
    
    def calculate_month_mat_match(self): # {
        # TRY THE FOLLOWING
        try: # {
            pass
        # }
        except: # {
            pass
        # }
        else: # {
            pass
        # }
    # }
    
    """
    Referred to as "ProdflowII" in SQL-Server
    """
    def pull_ProdflowII_table(self, table_name): # {
        # TRY THE FOLLOWING
        try: # {
            # CREATE CONNECTION STRING
            conn_str = str(
                r'DRIVER={ODBC Driver 17 for SQL Server};'
                r'SERVER=wtkngappflow1.is.agilent.net;'
                r'DATABASE=ProdFlowII_Prod;'
                r'Trusted_Connection=yes;'
            )
            # CREATE PYODBC CONNECTION
            cnxn_ProdflowII = pyodbc.connect(conn_str)
            # [2020-02-028]\\crsr_ProdflowII = cnxn_ProdflowII.cursor()
            # PERFORM SQL QUERY AND SET AS DATAFRAME
            df_ProdflowII_table = pd.read_sql_query(sql='SELECT * FROM ' + str(table_name),
                                                    con=cnxn_ProdflowII
                                                    )
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
        # }
        else: # {
            print("Operation Completed Successfully...")
            return df_ProdflowII_table
        # }
    # }
    
    """
    Referred to as "Prodflow" in SQL-Server
    """
    def pull_ProdflowIII_table(self, table_name): # {
        # TRY THE FOLLOWING
        try: # {
            # CREATE CONNECTION STRING
            conn_str = str(
                r'DRIVER={ODBC Driver 17 for SQL Server};'
                r'SERVER=wtkngappflow1.is.agilent.net;'
                r'DATABASE=ProdFlow;'
                r'Trusted_Connection=yes;'
            )
            # CREATE PYODBC CONNECTION
            cnxn_ProdflowIII = pyodbc.connect(conn_str)
            # [2020-02-28]\\crsr_ProdflowIII = cnxn_ProdflowIII,cursor()
            # PERFORM SQL QUERY AND SET AS DATAFRAME
            df_ProdflowIII_table = pd.read_sql_query(sql='SELECT * FROM ' + str(table_name),
                                                     con=cnxn_ProdflowIII,
                                                     parse_dates=['QCDate', 
                                                                  'AmpDate',
                                                                  'OriginationDate', 
                                                                  'EntryDate'
                                                                  ]
                                                     )
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
        # }
        else: # {
            print("Operation Completed Successfully...")
            return df_ProdflowIII_table
        # }
    # }
    
    def create_metrics_table(self, time_start, time_end): # {
        # TRY THE FOLLOWING
        try: # {
            # pull ORDERS table
            self.df_orders = self.pull_ProdflowII_table(table_name='Orders')
            # RENAME ['Product#'] column to ['ProductNo']
            self.df_orders.rename(columns={'Product#':'ProductNo'},
                                  inplace=True)
            print(self.df_orders.info())
            # pull tblProdflow TABLE
            self.df_tblProdflow = self.pull_ProdflowIII_table(table_name='tblProdflow')
            print(self.df_tblProdflow.info())
            # CREATE METRICS TABLE
            df_metrics_table = pd.merge(self.df_orders, self.df_tblProdflow,
                                        on='ProductNo', how='right')
            # DROP ALL ROWS WITHOUT A 'QCDate' & 'ProductLevel'
            df_metrics_table.dropna(axis=0, subset=['QCDate'], how='any', inplace=True)
            # ONLY USE ROWS THAT ARE WITHIN SPECIFIED TIME FRAME
            # time_start, time_end
            df_TIS_metrics = df_metrics_table[(df_metrics_table['QCDate'] > time_start) & (df_metrics_table['QCDate'] < time_end)]
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
        # }
        else: # {
            print("Operation Completed Successfully...")
            return df_TIS_metrics
        # }
    # }
    
# }

def main(): # { 
    # TRY THE FOLLOWING
    try: # {
        window = tk.Tk()
        application = Agilent_TIS_Metrics(root = window, the_logger=None)
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
    else: # {
        print("Operation Completed Successfully...")
    # }
# }


if __name__ == "__main__": # {
    # call main function
    main()
# }