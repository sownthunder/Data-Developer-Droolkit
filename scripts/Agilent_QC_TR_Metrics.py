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

class Agilent_TIS_Metrics(): # {
    
    user_name = str(os.getlogin()) # get username
    outbound_dir = "C:/data/outbound/" + str(pd.Timestamp.now())[:10]
    desktop_dir = "OneDrive - Agilent Technologies/Desktop"
    
    def __init__(self, root, the_logger): # {
        self. root = root
        self.root.title("TIS Metrics")
        self.root.geometry('315x200+300+300')
        self.root.resizable(width=False, height=False)
        # Get/Set USERNAME & DESKTOP DIRECTORIES
        self.user_name_dir = os.path.join("C:/Users/", self.user_name)
        self.desktop_dir = os.path.join(self.user_name_dir, self.desktop_dir)
        print(self.user_name_dir)
        print(self.desktop_dir)
        
    # }
    
    def run(self): # {
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
    Referred to as "Prodflow" in SQL-Server
    """
    def pull_ProdflowIII_table(self, table_name): # {
        # TRY THE FOLLOWING
        try: # {
            pass
        # }
        except: # {
            pass
        # }
    # }
    
    def create_metrics_table(self): # {
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
    
# }

def main(): # { 
    # TRY THE FOLLOWING
    try: # {
        pass
    # }
    except: # {
        pass
    # }
# }


if __name__ == "__main__": # {
    # call main function
    main()
# }