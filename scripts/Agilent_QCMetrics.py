# -*- coding: utf-8 -*-
"""
Created on Mon Feb 24 16:16:13 2020

@author: derbates

TABLES INPUTEED:
    - tblProdflow
    - PRODUCTS

==========================================
DETERMINES NUMBER OF "PfBatchID" over 
last 30 days, in 3 level bins 
(L1, L2, L3)
==========================================

"""

# IMPORT THE GOODS
import os, sys, time
from time import sleep
from pathlib import Path
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from pandas import Series, DataFrame
import pyodbc
from openpyxl import Workbook, load_workbook
from openpyxl.drawing.image import Image
from openpyxl.utils.dataframe import dataframe_to_rows
import tempfile
from ttkthemes import ThemedStyle
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox, filedialog, commondialog


class AgilentQCMetrics(): # {
    
    outbound_dir = "C:/data/outbound/"
    
    def __init__(self, root, the_logger): # {
        self.root = root
        self.root.title("QC Metrics")
        self.root.geometry('250x250+300+300')
        self.root.resizable(width=True, height=False)
        self.create_gui(the_root = self.root)
    # }
    
    def create_gui(self, the_root): # {
        # TRY THE FOLLOWING
        try: # { 
            self.create_ttk_styles(the_root=the_root)
            self.create_label_frame(the_root=the_root)
            self.create_main_frame(the_root=the_root)
        # }
        except: # {
            pass
        # }
    # }
    
    def create_ttk_styles(self, the_root): # {
        # TRY THE FOLLOWING
        try: # {
            # CONFIGURE THE TTK STYLE
            self.style = ThemedStyle(the_root)
            # STYLE THEME
            self.style.set_theme("radiance")
        # }
        except:# { 
            pass
        # }
    # }
    
    def create_label_frame(self, the_root): # {
        self.labelframe = ttk.Frame(the_root)
        self.labelframe.pack(anchor=tk.CENTER, fill=tk.BOTH, expand=True)
    # }
    
    def create_main_frame(self, the_root): # {
        # TRY THE FOLLOWING
        try: # {
            ttk.Label(master=the_root, text="Select Start Date: "
                      ).grid(row=0, col=0, padx=10, pady=10, sticky='w')
            ttk.Label(master=the_root, text="Select End Date: "
                      ).grid(row=0, col=0, padx=10, pady=10, sticky='w')
        # }
        except: # {
            pass
        # }
        else: # {
            pass
        # }
    # }
    
    def run(self, day_range): # {
        # TRY THE FOLLOWING
        try: # {
            # [2020-02-28]\\self.time_unit = time_unit
            # [2020-02-28]\\self.time_value = time_value
            self.day_range = day_range
            # get/set current date variable
            the_date = pd.Timestamp.now()
            # create variable for a month ago
            one_month_ago = the_date - timedelta(days = int(day_range))
            # [2020-02-28]\\one_month_ago = the_date - pd.Timedelta(unit=str(self.time_unit), value=str(self.time_value))
            print(type(one_month_ago))
            # CREATE METRICS TABLE FROM CLASS METHOD
            self.df_metrics_table = self.create_metrics_table()
            #############################
            # create .csv with no drops #
            #############################
            self.df_metrics_table.to_csv(os.path.join(self.outbound_dir, "df_metrics_noDrop.csv"), index=True)
            # DROP ROWS WITH PRODUCT LEVEL && QCDATE = NONE
            self.df_metrics_table.dropna(axis=0, subset=['QCDate', 'ProductLevel'], how='any', inplace=True)
            # create .csv with DROPS
            self.df_metrics_table.to_csv(os.path.join(self.outbound_dir, "df_metrics_DROP.csv"), index=True)
            # Set index of METRICS
            self.df_metrics_table.set_index(['QCDate', 'ProductLevel'], inplace=True)
            print(self.df_metrics_table)
            # Display Index
            print(self.df_metrics_table.index)
            #############################
            # create .csv with UNSORTED #
            #############################
            self.df_metrics_table.to_csv(os.path.join(self.outbound_dir, "df_metrics_UNSORTED.csv"), index=True)
            # SORT INDEX
            self.df_metrics_table.sort_index(inplace=True)
            ###########################
            # create .csv with SORTED #
            ###########################
            self.df_metrics_table.to_csv(os.path.join(self.outbound_dir, "df_metrics_SORTED.csv"), index=True)
            print("SORTED:\n")
            print(self.df_metrics_table.index)
            # SLICE & DICE THE DATAFRAME
            self.df_level_1s = self.df_metrics_table.loc[('2017-01-02', float(1))]
            print(self.df_level_1s)
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
        # }
    # }
    
    """
    Referred to as "ProflowII" in SQL-Server
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
    Referred as "Prodflow" in SQL-Server
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
                                                     parse_dates=['QCDate']
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
    
    def create_metrics_table(self): # { 
        # TRY THE FOLLOWING
        try: # {
            # pull PRODUCTS TABLE
            self.df_products = self.pull_ProdflowII_table(table_name='Products')
            # RENAME ['Product#'] column to ["ProductNo']
            self.df_products.rename(columns={'Product#': 'ProductNo'}, inplace=True)
            print(self.df_products.info())
            # pull tblProdflow TABLE
            self.df_tblProdflow = self.pull_ProdflowIII_table(table_name='tblProdflow')
            print(self.df_tblProdflow.info())
            # CREATE METRICS TABLE
            df_metrics_table = pd.merge(self.df_products, self.df_tblProdflow, on='ProductNo', how='right')
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
            return df_metrics_table
        # } 
    # }
# }

if __name__ == "__main__": # {
    # logger = Logger(logging_output_dir="").loggger
    window = tk.Tk()
    application = AgilentQCMetrics(root= window, the_logger=None)
    window.config()
    window.mainloop()
    # CALL METRICS CLASS WITH A RANGE OF 1 MONTH
    # [2020-02-28]\\test_metrics = AgilentQCMetrics(time_unit='M', time_value=1)
    # [2020-03-04]\\test_metrics = AgilentQCMetrics(day_range=30)
# }