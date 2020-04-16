# -*- coding: utf-8 -*-
"""
Created on Thu Apr 16 10:39:57 2020

CofA_F_Scanner_FINALE

RUN AS 9PM
WHILE:
    SCANNING:    F:/APPS/CofA/
    EXPORT-2:    C:/data/outbound/CofA/
    FILENAME:    CofA_Email_Node_list_[*DATE*]_F_pull.csv

USES:
    (original) CofA_F_Scanner - one that creates .csv, not WATCHDOGGER

@author: derbates
"""


# IMPORT THE GOODS
import os, sys, time
from time import sleep
from datetime import datetime
from pathlib import Path
from os.path import join, getsize
import fnmatch, glob, shutil
from threading import Timer

class CofA_F_Scanner(): # {
    
    def __init__(self): # {
        pass
    # }
    
    def scan_directory(the_directory, ignore_dir_list, file_type_list): # {
        # CREATE COUNTER
        count = 0
        # TRY THE FOLLOWING
        try: # {
            # create path variable
            scan_directory = Path(the_directory)
        # }
        except: # {
            pass
        # }
    # }
# }