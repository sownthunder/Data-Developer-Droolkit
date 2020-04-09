# -*- coding: utf-8 -*-
"""
Created on Wed Mar 25 16:21:03 2020

QC_Metrics (turn around time)

TABLES USED:
    - tblProdflow
    - PRODUCTS

===================================================
- Takes the INPUT OF USER (month?)
- pulls tables from Prodflow
- Returns the average turn around time (cycle-days) 
  PER PRODUCT LEVEL, PER WEEK RANGE (yayyyy)
===================================================

04/07/20 - began implementing PDF export feature...

@author: derbates
"""

# IMPORT THE GOODS
import os, sys, time
from time import sleep
from pathlib import Path
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import pandas as pd
import numpy as np
from pandas import Series, DataFrame
import logging
import pyodbc
from openpyxl import Workbook, load_workbook
from openpyxl.drawing.image import Image
from openpyxl.utils.dataframe import dataframe_to_rows
import tempfile
from ttkthemes import ThemedStyle
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox, filedialog, commondialog

class Logger(): # {
    
    def __init__(self): # {
        pass
    # }
# }

class Agilent_QC_TR_Metrics(): # {
    
    user_name = str(os.getlogin()) # get username
    outbound_dir = "C:/data/outbound/" + str(pd.Timestamp.now())[:10]
    desktop_dir = "OneDrive - Agilent Technologies/Desktop"
    
    def __init__(self, root, the_logger): # {
        self.root = root
        self.root.title("QC Metrics - Cycle Time")
        self.root.geometry('315x200+300+300')
        self.root.resizable(width=False, height=False)
        # Get/Set USERNAME & DESKTOP DIRECTORIES
        self.user_name_dir = os.path.join("C:/Users/", self.user_name)
        self.desktop_dir = os.path.join(self.user_name_dir, self.desktop_dir)
        print("USER_DIR == " + str(self.user_name_dir))
        print("DESKTOP == " + str(self.desktop_dir))
        # CHECK IF DIRECTORIES ABOVE EXIST, IF NOT... CREATE THEM...
        self.desktop_folder = os.path.join(self.desktop_dir, str(pd.Timestamp.now())[:10])
        print(self.desktop_folder)
        if not os.path.exists(self.desktop_folder): # {
            # MAKE IT EXIST!
            os.makedirs(self.desktop_folder)
        # }
        # OVERWRITE DESKTOP VAR
        self.desktop_dir = self.desktop_folder
        # INITITALIZE UI
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
            print("FAILED GUI")
        # }
    # }
    
    def create_ttk_styles(self, the_root): # {
        # TRY THE FOLLOWING
        try: # { 
            self.style = ThemedStyle(the_root)
            # STYLE THEME
            self.style.set_theme("blue")
        # }
        except: # {
            pass
        # }
    # }
    
    def create_label_frame(self, the_root): # {
        self.labelframe = ttk.Frame(the_root)
        self.labelframe.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    # }
    
    def create_main_frame(self, the_root): # {
        # TRY THE FOLLOWING
        try: # {
            self.mainframe = ttk.Frame(self.labelframe)
            self.mainframe.pack(anchor=tk.CENTER, fill=tk.BOTH, expand=True)
            # END DATE LABEL
            ttk.Label(master=self.mainframe, text="Enter Date: \n(YYYY-MM-DD)"
                      ).place(x=20, y=20) #.grid(row=0, col=0, padx=10, pady=10) 
            # CREATE END DATE TK VAR TO HOLD STR
            self.end_date = tk.StringVar(master=the_root)
            # ENTRY FOR END DATE
            ttk.Entry(master=self.mainframe, textvariable=self.end_date
                      ).place(x=140, y=20) #.grid(row=0, col=1, padx=10, pady=10)
            # NUM OF DAYS LABEL
            ttk.Label(master=self.mainframe, text="# of days back: "
                      ).place(x=20, y=65)# .grid(row=1, col=0, padx=10, pady=10) 
            self.num_of_days = tk.IntVar(master=the_root, value=1)
            # NUM OF DAYS SPINBOX
            ttk.Spinbox(master=self.mainframe, to=365, from_=0, textvariable=self.num_of_days
                        ).place(x=140, y=55) #.grid(row=1, col=1, padx=10, pady=10)
            # CREATE STRING TO HOLD POSSIBLE FILENAME
            # [2020-03-08]\\self.period_str = tk.StringVar(master=the_root, value="Day")
            self.filename_str = tk.StringVar(master=the_root, value=str(self.end_date.get()))
            # FILENAME LABELS AND ENTRY BOX
            ttk.Label(master=self.mainframe, text="Folder Name:\tQCMetrics_"
                      ).place(x=10, y= 100)
            ttk.Entry(master=self.mainframe, textvariable=self.end_date, state=tk.DISABLED,
                      width=16
                      ).place(x=170, y= 100)
            # [2020-04-07]\\
            """
            ttk.Label(master=self.mainframe, text=".xlsx"
                      ).place(x=270, y= 100)
            """
            # BROWSE FOR EXPORT LOCATION BUTTON
            self.export_button = ttk.Button(master=self.mainframe, text="EXPORT TO DESKTOP",
                       command=self.determine_range, width=20).place(x=20, y = 140)
            # KEY-TYPE (radio-button)
            self.key_type_var = tk.StringVar(master=self.mainframe, value="ProductLevel")
            radio_type_1 = ttk.Radiobutton(master=self.mainframe,
                                           variable=self.key_type_var,
                                           value="ProductLevel", text="ProductLevel")
            radio_type_1.place(x=190, y = 140)
            radio_type_2 = ttk.Radiobutton(master=self.mainframe,
                                           variable=self.key_type_var,
                                           value="QCValidation", text="QCValidation")
            radio_type_2.place(x=190, y = 165)
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
            print("DETERMINING...")
            print(self.end_date.get())
            print(self.num_of_days.get())
            print(self.key_type_var.get())
            # CALL RUN
            self.run(date_input=str(self.end_date.get()), day_range=self.num_of_days.get())
        # }
        except: # {
            pass
        # }
    # }
    
    def create_dashboard(self, cycle_time, n, date_range): # {
        # TRY THE FOLLOWING
        try: # {
            # CREATE DATAFRAME FROM IMPORT
            columns = ('Cycle Time(days)', 'n', 'Date Range')
            levels = pd.CategoricalIndex(['1', '2', '3'])
            self.df_dashboard = pd.DataFrame(data=None, index=levels, columns=columns)
            # CREATE COLUMN DATA
            self.df_dashboard['Cycle Time(days)'] = cycle_time
            self.df_dashboard['n'] = n
            self.df_dashboard['Date Range'] = date_range
            print(self.df_dashboard)
        # }
        except: # {
            print("FAILED CREATING DATAFRAME OF QC_DASHBOARD")
        # }
        else: # {
            print("Operation Completed Successfully...")
        # }
    # }
    
    def run(self, date_input, day_range): # {
        # TRY THE FOLLOWING
        try: # {
            # Create date (OFF INPUT)
            the_date = pd.Timestamp(ts_input=str(date_input))
            # create day range
            x_days_ago = the_date - timedelta(days = int(day_range))
            df_x_range = pd.date_range(start=x_days_ago, end=the_date, freq='D')
            print(list(df_x_range))
            # CREATE METRICS TABLE FROM CLASS METHOD
            # (returning only time-series we want??)
            self.df_metrics_table = self.create_metrics_table(
                time_start=x_days_ago, # 2019-11-01
                time_end=the_date) # 2020-03-01
            """
            << CHANGE DATA-TYPES OF COLUMNS >>
            """
            # change to 'DATETIME'
            self.df_metrics_table['AmpTimeIn'] = pd.to_datetime(self.df_metrics_table['AmpTimeIn'])
            self.df_metrics_table['AmpTimeOut'] = pd.to_datetime(self.df_metrics_table['AmpTimeOut'])
            # change to 'STRING'
            self.df_metrics_table['PfBatchID'] = self.df_metrics_table['PfBatchID'].astype('object')
            self.df_metrics_table['ProductID'] = self.df_metrics_table['ProductID'].astype('object')
            """
            << GRAB ONLY LEVELS 1, 2, and 3 >>
            """
            value_list= ['1.0', '2.0', '3.0']
            level_1 = ['1.0']
            level_2 = ['2.0']
            level_3 = ['3.0']
            # GRAB DATAFRAME ROWS where COLUMN contains certain values
            # >>> based on "self.key_type_var.get()"
            self.df_metrics_obv = self.df_metrics_table[self.df_metrics_table[str(self.key_type_var.get())].isin(value_list)]
            # EXPORT ??
            # [2020-03-30]\\self.df_metrics_obv.to_csv("c:/data/outbound/2020-03-30/df_metrics_obv.csv")
            # THEN GRAB DATAFRAME ROWS for EACH PRODUCT LEVEL
            self.df_level_1 = self.df_metrics_table[self.df_metrics_table[str(self.key_type_var.get())].isin(level_1)] # ProductLevel
            print(self.df_level_1.info())
            self.df_level_2 = self.df_metrics_table[self.df_metrics_table[str(self.key_type_var.get())].isin(level_2)] # ProductLevel
            print(self.df_level_2.info())
            self.df_level_3 = self.df_metrics_table[self.df_metrics_table[str(self.key_type_var.get())].isin(level_3)] # ProductLevel
            print(self.df_level_3.info())
            print("LEN OF (all levels) == " + str(len(self.df_metrics_obv)))
            print("LEN OF (#01 levels) == " + str(len(self.df_level_1)))
            print("LEN OF (#02 levels) == " + str(len(self.df_level_2)))
            print("LEN OF (#03 levels) == " + str(len(self.df_level_3)))
            # CREATE LIST TO HOLD NUMBERS (n)
            level_1_n = len(self.df_level_1)
            level_2_n = len(self.df_level_2)
            level_3_n = len(self.df_level_3)
            all_numbers = [level_1_n, level_2_n, level_3_n]
            # CREATE << GROUPBY >> DATAFRAME
            # [2020-03-30]\\self.df_groupby_levels = pd.DataFrame(data=self.df_total_levels.groupby(['QCDate', 'ProductLevel'])[['PfBatchID'].count()])
            self.ProdsPerDay = self.df_metrics_obv.groupby(['QCDate', str(self.key_type_var.get())])[['PfBatchID']].count()
            # RENAME COLUMNS
            self.ProdsPerDay.rename(columns={'PfBatchID':'Count'}, 
                                    inplace=True)
            """
            << PRODS PER DAY UNSTACK >>
            """
            self.ProdsPerDay = self.ProdsPerDay.unstack(level=-1)
            """
            <<< EXPORT TO DESKTOP >>>
            """
            filename_var = str("QC-ProdsPerDay-" + str(the_date)[:10] + ".csv")
            file_path = os.path.join(self.desktop_dir, str(filename_var))
            self.ProdsPerDay.to_csv(file_path)
            """
            <<< DETERMINE DAYS IN QC >>>
            """
            self.df_days_in_QC = pd.DataFrame(data=self.df_metrics_obv['PfBatchID'])
            # CREATE ANOTHA COLUMN
            self.df_days_in_QC['Date'] = self.df_metrics_obv['QCDate']
            # [2020-03-30]\\self.df_days_in_QC['ProductLevel'] = self.df_metrics_obv['ProductLevel']
            self.df_days_in_QC[str(self.key_type_var.get())] = self.df_metrics_obv[str(self.key_type_var.get())]
            self.df_days_in_QC['AmpDate'] = self.df_metrics_obv['AmpDate']
            ################
            # CALCULCATION #
            ################
            self.calculation = (self.df_days_in_QC['Date'] - self.df_days_in_QC['AmpDate'])
            # Assign Calculation COlumn
            self.df_days_in_QC['QC_days'] = self.calculation
            print(self.df_days_in_QC)
            #####################
            # CHANGE DATA-TYPES #
            #####################
            self.df_days_in_QC['QC_days'] = pd.to_timedelta(self.df_days_in_QC['QC_days'])
            ###########
            # DROP NA #
            ###########
            self.df_days_in_QC.dropna(subset=[str(self.key_type_var.get()), 'QC_days', 'AmpDate'],
                                      inplace=True)
            # CREATE COLUMN OF TYPE INT
            self.df_days_in_QC['Cycle_Time(days)'] = self.df_days_in_QC['QC_days'].dt.days
            print(self.df_days_in_QC)
            ################
            # CHANGE INDEX #
            ################
            self.df_days_in_QC.set_index(['Date'], drop=True, inplace=True)
            ##############
            # SORT INDEX #
            ##############
            self.df_days_in_QC.sort_index(inplace=True)
            """
            <<< ROLLING >>>
            """
            # Trail-rolling average transform [COLUMN]
            rolling = self.df_days_in_QC['Cycle_Time(days)'].rolling(window=1)
            rolling_mean = rolling.mean()
            # ASSIGN NEW COLUMN
            self.df_days_in_QC['rolling_avg'] = rolling_mean
            # [2020-03-31]\\
            """
            self.df_days_in_QC.to_csv(os.path.join(self.desktop_dir, "df_days_in_QC"
                                                   + str(pd.Timestamp.now())[:10]
                                                   + ".csv"))
            """
            """
            <<< GROUP-BY >>
            """
            # FORWARD_FILL
            # [2020-03-30]\\self.forward_fill = self.df_days_in_QC.groupby("ProductLevel")['Cycle_Time(days)'].resample("D").ffill()
            self.days_cycle = pd.DataFrame(data=self.df_days_in_QC.groupby(str(self.key_type_var.get()))['Cycle_Time(days)'].resample("D").mean()).reset_index()
            # EXPORT
            # [2020-03-31]\\
            """
            self.days_cycle.to_csv(os.path.join(self.desktop_dir, "QC-CycleTime-"
                                                + str(pd.Timestamp.now())[:10]
                                                + ".csv"))
            """
            # PLOT?
            names = self.df_days_in_QC[str(self.key_type_var.get())]
            values = self.days_cycle['Cycle_Time(days)']
            
            ########################
            # ['ProductLevel']
            ########################
            self.level_1s = self.days_cycle[self.days_cycle[str(self.key_type_var.get())].isin(level_1)]
            self.level_1s.dropna(axis=0, how='any', inplace=True)
            self.level_2s = self.days_cycle[self.days_cycle[str(self.key_type_var.get())].isin(level_2)]
            self.level_2s.dropna(axis=0, how='any', subset=['Cycle_Time(days)'], inplace=True)
            self.level_3s = self.days_cycle[self.days_cycle[str(self.key_type_var.get())].isin(level_3)]
            self.level_3s.dropna(axis=0, how='any', subset=['Cycle_Time(days)'], inplace=True)
            ########################
            # CALCULATE AVG AGAIN #
            ########################
            print("===========================\n\n")
            print("AVG OF level1 == " + str(self.level_1s['Cycle_Time(days)'].mean()))
            print("AVG OF level2 == " + str(self.level_2s['Cycle_Time(days)'].mean()))
            print("AVG of level3 == " + str(self.level_3s['Cycle_Time(days)'].mean()))
            level_1_avg = self.level_1s['Cycle_Time(days)'].mean()
            level_2_avg = self.level_2s['Cycle_Time(days)'].mean()
            level_3_avg = self.level_3s['Cycle_Time(days)'].mean()
            # CREATE LIST TO HOLD AVERAGES
            all_averages = [level_1_avg, level_2_avg, level_3_avg]
            print("ALL AVERAGES:\n\t" + str(all_averages))
            # PRINT ALL NUMBERS (generated above)
            print("ALL NUBMERS:\n\t" + str(all_numbers))
            # [2020-03-31]\\
            """
            # << EXPORT >>
            self.level_1s.to_csv(os.path.join(self.desktop_dir, "QC-CycleTime-Level1-"
                                              + str(pd.Timestamp.now())[:10]
                                              + ".csv"))
            self.level_2s.to_csv(os.path.join(self.desktop_dir, "QC-Cycle-Time-Level1-"
                                              + str(pd.Timestamp.now())[:10]
                                              + ".csv"))
            self.level_3s.to_csv(os.path.join(self.desktop_dir, "QC-CycleTime-Level3-"
                                              + str(pd.Timestamp.now())[:10]
                                              + ".csv"))
            """
            """
            [[[ CREATE DASHBOARD ]]]
            """
            self.create_dashboard(cycle_time=all_averages, n=all_numbers,
                                  date_range=str(x_days_ago) + " to " + str(the_date))
            """
            [[[ CREATE DASHBOARD ]]]
            """
            self.df_dashboard.to_csv(os.path.join(self.desktop_dir, "QC-Dashboard-"
                                                  + str(pd.Timestamp.now())[:10]
                                                  + ".csv"), index_label="Level")
            ###################################################################
            # WORK BOOK FUNCTION (sending to method)
            ###################################################################
            self.wb = self.create_excel_workbook
            #################################################################################
            # WORK BOOK FUNCTION >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
            #############################################################################
            
            print(self.desktop_dir)
            # CREATE STR VAR for filename convention
            ts_str = str(the_date)[:10]
            # CREATE FILENAME VAR
            filename_var = str("QC-Metrics-CycleTime-"
                               + str(self.key_type_var.get())
                               + "-" + str(ts_str) + ".xlsx")
            # CREATE FULL WORKBOOK PATH
            workbook_path = os.path.join(self.desktop_dir, str(filename_var))
            print("WORKBOOK PATH == " + str(workbook_path))
            # CREATE NEW WORKBOOK
            wb = Workbook()
            wb.save(workbook_path)
            # ADD SHEETS TO WORKBOOK
            # DESGINATE SHEET NAME AND POSITION
            sheet1 = wb.create_sheet('Table', 0)
            sheet2 = wb.create_sheet('Graphs', 1)
            # ACTIVATE WORKSHEET TO WRITE DATAFRAME
            active = wb['Table']
            # WRITE DATAFRAME TO ACTIVE WORKSHEET
            # df_daily_unstacked_1
            # df_days_cycle
            for x in dataframe_to_rows(self.df_days_in_QC): # {
                active.append(x)
            # }
            # SAVE
            wb.save(filename_var)
            # CREATE LINE PLOT VARIABLE
            plot = self.ProdsPerDay.plot()
            # CREATE AREA PLOT VARIABLE
            area_plot = self.ProdsPerDay.plot(kind='area')
            # MATPLOTLIB figure for "line_plot"
            line_fig = plot.get_figure()
            # MATPLOTLIB figure for "area_plot"
            area_fig = area_plot.get_figure()
            ###################
            # CREATE TEMP DIR #
            ###################
            with tempfile.TemporaryDirectory() as directory_name: # {
                the_dir = Path(directory_name)
                print("TEMPORARY DIR == " + str(the_dir))
                line_img_path = os.path.join(the_dir, str(ts_str) + "_line_plot.png")
                area_img_path = os.path.join(the_dir, str(ts_str) + "_area_plot.png")
                print("line_plot_path == " + str(line_img_path))
                print("area_plot_path == " + str(area_img_path))
                # SAVE LINE PLOT
                line_fig.savefig(line_img_path)
                # SAVE AREA PLOT
                area_fig.savefig(area_img_path)
                # ACTIVATE WORKSHEET
                active = wb['Graphs']
                # Insert Plot into Worksheet
                # Select active sheet and cell reference
                img_line = Image(line_img_path)
                active.add_image(img_line, 'A1')
                # Insert Plot into worksheet
                # Select active sheet and cell reference
                img_area = Image(area_img_path)
                active.add_image(img_area, 'H1')
                # SAVE WORKBOOK
                wb.save(workbook_path)
            # }
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
    TAKES IN: 
    (1) - date as string
    (2) - filename of OUTPUT file which will be saved at Desktop
    (3) - dataframe of *DATA* to put in sheet-1
    (4) - dataframe of *GRAPH* to put in sheet-2
    RETURNS: Nada, will have output an .xlsx file to location when complete
    """
    def create_excel_workbook(self, the_date, file_name, data_df, graph_df): # {
        # TRY THE FOLLOWING
        try: # {
            print(self.desktop_dir)
            # CREATE STR VAR FOR filename convention
            ts_str = str(the_date)[:10]
            # CREATE FILENAME VAR
            filename_var = str("QC_TR_Metrics_" + str(ts_str) + ".xlsx")
            # CREATE FULL WORKBOOK PATH
            workbook_path = os.path.join(self.desktop_dir, str(filename_var))
            print("WORKBOOK PATH == " + str(workbook_path))
        # }
        except: # {
            pass
        # }
    # }
    
    def calculate_moving_average(self, dataframe_to_avg, columns_to_avg): # {
        # TRY THE FOLLOWING
        try: # {
            weighted_avg = (
                dataframe_to_avg[str(columns_to_avg[0])] 
                * dataframe_to_avg[str(columns_to_avg[1])].sum() 
                / dataframe_to_avg(str(columns_to_avg[2])).sum()
                )
            print("\n\tWEIGHTED AVERAGE:\n\t" + str(weighted_avg))
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
            return weighted_avg
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
            # pull PRODUCTS TABLE
            self.df_products = self.pull_ProdflowII_table(table_name='Products')
            # RENAME ["Product#'] column to ["ProductNo"]
            self.df_products.rename(columns={'Product#':'ProductNo'}, 
                                    inplace=True)
            print(self.df_products.info())
            # pull ORDERS TABLE
            self.df_orders = self.pull_ProdflowII_table(table_name='Orders')
            print(self.df_orders.info())
            # pull tblProdflow TABLE
            self.df_tblProdflow = self.pull_ProdflowIII_table(table_name='tblProdflow')
            print(self.df_tblProdflow.info())
            # CREATE METRICS TABLE
            df_metrics_table = pd.merge(self.df_products, self.df_tblProdflow, 
                                        on='ProductNo', how='right')
            # DROP ALL ROWS WITHOUT A 'QCDate' & 'ProductLevel'
            df_metrics_table.dropna(axis=0, subset=['QCDate', str(self.key_type_var.get())], 
                                    how='any', inplace=True)
            # ONLY USE ROWS THAT ARE WITHIN SPECIFIED TIME FRAME
            # time_start, time_end
            df_QC_metrics = df_metrics_table[(df_metrics_table['QCDate'] > time_start) & (df_metrics_table['QCDate'] < time_end)] 
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
            # [2020-03-27]\\return df_metrics_table
            return df_QC_metrics
        # }
    # }
    
# }

def main(): # { 
    # TRY THE FOLLOWING
    try: # {
        window = tk.Tk()
        application = Agilent_QC_TR_Metrics(root = window, the_logger=None)
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
    # }
    else: # {
        print("Operation Completed Successfully...")
    # }
# }


if __name__ == "__main__": # {
    # call main function
    main()
# }