# -*- coding: utf-8 -*-
"""
Created on Wed Mar 18 14:48:03 2020

TIS_Metrics

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
import pyodbc
from openpyxl import Workbook, load_workbook
from openpyxl.drawing.image import Image
from openpyxl.utils.dataframe import dataframe_to_rows
import tempfile
from ttkthemes import ThemedStyle
import tkinter.ttk as ttk
from tkinter import messagebox, filedialog, commondialog
import wx

class MyPanel(wx.Panel): # { 
    
    def __init__(self, parent): # {
        super(MyPanel, self).__init__(parent)
        
        b = wx.Button(self, label = 'Greensheet ORDERS', pos = (100,100))
        b.Bind(wx.EVT_BUTTON, self.btnclk)
        self.Bind(wx.EVT_BUTTON, self.OnButtonClicked)
    # }
    
    def OnButtonClicked(self, e): # {
        print("Panel Received click event. propgated to Frame Class")
        e.Skip()
    # }
    
    def btnclk(self, e): #{
        print("Button recieved click event. propogated to Panel Class")
        e.Skip()
    # }
# }

class Agilent_TIS_Metrics(wx.Frame): # {
    
    user_name = str(os.getlogin()) # get username
    outbound_dir = "C:/data/outbound/" + str(pd.Timestamp.now())[:10]
    desktop_dir = "OneDrive - Agilent Technologies/Desktop"
    
    def __init__(self, parent): # {
        super(Agilent_TIS_Metrics, self).__init__(parent)
        #self.root.title("TIS Metrics")
        #self.root.geometry('315x200+300+300')
        #self.root.resizable(width=False, height=False)
        # Get/Set USERNAME & DESKTOP DIRECTORIES
        self.user_name_dir = os.path.join("C:/Users/", self.user_name)
        self.desktop_dir = os.path.join(self.user_name_dir, self.desktop_dir)
        print(self.user_name_dir)
        print(self.desktop_dir)
        # INITALIZE UI
        self.InitUI()
    # }
    
    def InitUI(self): # {
        
        mpn1 = MyPanel(self)
        self.Bind(wx.EVT_BUTTON, self.OnButtonClicked)
        self.SetTitle("Agilent TIS Custom Metrics")
        self.Centre()
        self.Show(True)
        """
        frm1 = MyFrame(self)
        self.SetTitle("TIS Metrics")
        self.Centre()
        self.frame.Show(True)
        """
        
    # }
    
    def OnButtonClicked(self, e): # {
        # TRY THE FOLLOWING
        try: # {
            print("click event recieved by frame class")
            print("attempting to run...")
            self.run()
            e.Skip()
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
    # }
    
    def run(self): # {
        # TRY THE FOLLOWING
        try: # {
            # Create date
            the_date = pd.Timestamp.now()
            # CREATE METRICS TABLE FROM CLASS METHOD
            # (returning only time-series we want??)
            self.df_metrics_table = self.create_metrics_table(
                time_start="2019-11-01",
                time_end="2020-03-01"
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
            df_metrics_table.dropna(axis=0, subset=['QCDate', 'ProductLevel'],
                                    how='any', inplace=True)
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
        app = wx.App()
        Agilent_TIS_Metrics(None)
        app.MainLoop()
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


if __name__ == "__main__": # {
    # call main function
    main()
# }