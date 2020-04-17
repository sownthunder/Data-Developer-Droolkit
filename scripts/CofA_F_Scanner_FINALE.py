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
import pandas as pd
import numpy as np
from pandas import Series, DataFrame
from PyPDF2 import PdfFileReader, PdfFileWriter

class CofA_F_Scanner(): # {
    
    def __init__(self, inbound_dir, outbound_dir): # {
        self.inbound_dir = inbound_dir
        self.outbound_dir = outbound_dir
    # }
    
    def scan_directory(self, the_directory, ignore_dir_list, file_type_list): # {
        # CREATE COUNTER
        count = 0
        # TRY THE FOLLOWING
        try: # {
            # create path variable
            scan_directory = Path(the_directory)
            # create list to hold clean data yo
            path_list = []
            # << BEGIN OS.WALK >>
            for root, dirs, files in os.walk(scan_directory): # {
                # For each item in "ignore_dir_list"
                for item in ignore_dir_list: # {
                    if str(item) in dirs: # {
                        # REMOVE FROM OS.WALK
                        dirs.remove(str(item))
                    # }
                # }
                # OTHERWISE IF THERE ARE FILES IN DIRECTORY
                for f in files: # {
                    # FOR EACH ITEM IN "file_type_list":
                    for item in file_type_list: # {
                        ########################
                        # PERFORM ACTIONS HERE #
                        ########################
                        if fnmatch.fnmatch(f, "*" + str(item)): # {
                            # ASSEMBLE FILE PATH VAR
                            file_path = os.path.join(root, f)
                            # APPEND TO LIST
                            path_list.append(file_path)
                            # INCREMENT COUNTER
                            count += 1
                        # }
                    # }
                    else: # {
                        print("NOT PROPER FILE ! ")
                    # }
                # }
            # }
            # CREATE SERIES OFF LIST
            p1 = pd.Series(data=path_list, name='CofA File')
            # CREATE EMPTY DATAFRAME AND FILL WITH SERIES
            df_f_drive = pd.DataFrame(data=p1)
            # CREATE PATH VAR FOR FILENAME
            outfile_path = os.path.join(self.outbound_dir, 
                                        "CofA_Email_Node_list_"
                                        + str(pd.Timestamp.now())[:10]
                                        + "_F_pull.csv")
            # EXPORT DATAFRAME TO EXPORT LOCATION
            df_f_drive.to_csv(outfile_path, index=False)
        # }
        except: # {
            errorMessage = str(sys.exc_info()[0]) + "\n\t\t"
            errorMessage = errorMessage + str(sys.exc_info()[1]) + "\n\t\t"
            errorMessage = errorMessage + str(sys.exc_info()[2]) + "\n"
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            typeE = str("TYPE : " + str(exc_type))
            fileE = str("FILE : " + str(fname))
            lineE = str("LINE : " + str(exc_tb.tb_lineno))
            messageE = str("MESG : " + "\n" + str(errorMessage) + "\n")
            print("\n" + typeE +
                  "\n" + fileE +
                  "\n" + lineE +
                  "\n" + messageE)
        # }
    # }
# }

def main(): # {
    # TRY THE FOLLOWING
    try: # {
        # create PATH variable for scanning
        scan_directory = "F:/APPS/CofA/"
        # Create PATH variable for output
        out_directory = "C:/data/outbound/CofA/"
        # create class instance
        F_Scan = CofA_F_Scanner(inbound_dir=scan_directory, outbound_dir=out_directory)
        # CALL SCAN FUNCTION/METHOD
        F_Scan.scan_directory(the_directory=F_Scan.inbound_dir,
                              ignore_dir_list=['Archive ERR',
                                               'Archive - For all archived CofA, see G CofA folder',
                                               'Instruction Sheets'],
                              file_type_list=['.pdf'])
    # }
    except: # {
        errorMessage = str(sys.exc_info()[0]) + "\n\t\t"
        errorMessage = errorMessage + str(sys.exc_info()[1]) + "\n\t\t"
        errorMessage = errorMessage + str(sys.exc_info()[2]) + "\n"
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        typeE = str("TYPE : " + str(exc_type))
        fileE = str("FILE : " + str(fname))
        lineE = str("LINE : " + str(exc_tb.tb_lineno))
        messageE = str("MESG : " + "\n" + str(errorMessage) + "\n")
        print("\n" + typeE +
              "\n" + fileE +
              "\n" + lineE +
              "\n" + messageE)
    # }
# }

if __name__ == "__main__": # {
    # MAIN BOILERPLATE
    main()
# }