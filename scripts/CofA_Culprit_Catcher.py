# -*- coding: utf-8 -*-
"""
Created on Thu Dec 19 09:43:05 2019

Designed to catch the cuplrit who is definitely moving files around in:
- F:/APPS/CofA/
- G:/C of A's/Agilent/

<< USES SCRIPTS >>
CofA_Daily_Watch_v1.py
CofA_Daily_Launcher[FINALE].py

@author: derbates
"""

# IMPORT THE GOODS
import os, sys, time
from time import sleep
from pathlib import Path
import threading, logging
import pandas as pd
import numpy as np
from pandas import Series, DataFrame
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, LoggingEventHandler

class Logger():  # {
    
    def __init__(self):  # {
        # Initiating the Logger object
        self.logger = logging.getLogger(__name__)
        
        # Set the leel of the logger This is SUPER USEFUL since it enables
        # Explanation regarding the logger levels can be found here:
        # https://docs.python.org/3/howto/logging.html
        self.logger.setLevel(logging.DEBUG)
        
        # Create file handler which logs even debug messages
        fh = logging.FileHandler("C:/data/logs/CofA_Culprit_Catch.log")
        fh.setLevel(logging.DEBUG)
        
    # }
# }

class CofA_Culprit_Catcher(FileSystemEventHandler):  # {
    
    """
    takes in DATAFRAME to append csvs to 
    takes in DIRECTORY to move/copy pdfs to OUTBOUNDly
    """
    def __init__(self, save_dataframe, the_directory):  # {
        self.save_dataframe = save_dataframe
        self.the_directory = the_directory
    # }
    
    def dispatch(self, event): # {
        pass
    # }
    
    def on_created(self, event):  # {
        # TRY THE FOLLOWING
        try:  # {
            # CREATE TIMESTAMP
            ts_meow = pd.Timestamp.now()
            # CREATE EVENT PATH VAR
            the_event_path = Path(event.src_path)
            # CREATE 'file_name' VARIABLE
            the_file_name = os.path.basename(the_event_path)
        # }
        except: # {
            pass
        # }
        else:  # {
            pass
        # }
    # }
    
    def on_deleted(self, event): # {
        pass
    # }
    
    def on_modified(self, event): # {
        pass
    # }
    
    def on_moved(self, the_event): # {
        pass
    # }
    
#}

def main():  # {
    # RE-INSTANTIATE GLOBAL VARIABLES
    global logger
# }

if __name__ == "__main__":  # {
    # INSTANTIATE GLOBAL VARIABLES
    logger = Logger().logger
# }