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

class Agilent_TIS_Metrics(): # {
    
    user_name = str(os.getlogin()) # get username
    outbound_dir = "C:/data/outbound/"
    desktop_dir = "OneDrive - Agilent Technologies/Desktop"
    
    def __init__(self, root, the_logger): # {
        self. root = root
        self.root.title("TIS Metrics")
        self.root.geometry('315x200+300+300')
        self.root.resizable(width=False, height=False)
    # }
    
# }