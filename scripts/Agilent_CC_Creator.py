# -*- coding: utf-8 -*-
"""
Created on Wed Mar  4 14:45:56 2020

Agilent_CC_Creator.py

CREATES **CUSTOM CRATE** OF:
    - CofA (both directories)
    - SDS (all countries or any country)

ALLOWS OPTIONS OF:
    - Most recent
    - All copies

USES:
    - CofA_Custom_Crate_Creator_v1.py
    - CofA_Custom_Crate_Creator_v2.py
    - .../AGILENT/CUSTOM_CRATES/2020_03_04/CC_2020_03_04.ipynb
    
==================================
1) take in list of directories
2) for each item in list... OS.WALK
3) create an IDX dataframe of FILE NAMES
    (with FILE-DATE as index)
4) pull out and create crate by PART_NUMBER
5) drop duplicates by FILE-DATE (recents only))

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
import fnmatch, glob, shutil
import tempfile, logging
from zipfile import ZipFile
from PyPDF2 import PdfFileWriter, PdfFileReader


class CustomCrate(): # {
    
    out_directory = "."
    watermark = "C:/data/inbound/Agilent_CofA_Letterhead_03-21-19.pdf"
    
    def __init__(self, the_date, list_of_directories): # {
        self.the_date = the_date
        self.list_of_directories = list_of_directories
        # CREATE ZIP FOLDER 
        self.zip_dir_path = os.path.join(self.out_directory, self.the_date)
        # if 'zip_folder' DOES NOT YET EXIST!
        if not os.path.exists(self.zip_dir_path): #{
            # MAKE IT EXIST!
            os.makedirs(self.zip_dir_path)
        #}
        # RESET/RE-ESTABLISH 'out_directory'
        self.out_directory = Path(self.zip_dir_path)
        # CALL MAIN
        self.main()
    # }
    
    def main(self): # {
        # TRY THE FOLLOWING
        try: # {
            # FOR EACH PATH LISTED:
            for a_list in self.list_of_directories: # {
                print(Path(a_list))
            # }
        # }
        except: # {
            pass
        # }
    # }
    
# }

if __name__ == "__main__": # {
    # CREATE TIMESTAMP FOR ZIP FOLDER
    ts = pd.Timestamp.now()
    ts_str = str(ts)[:10]
    print(ts_str)
    # CREATE / CALL MAIN CLASS FUNCTION
    create_crate = CustomCrate(the_date=ts_str, 
                               list_of_directories=['F:/APPS/CofA/',
                                                    "G:/C of A's/Agilent/",
                                                    "J:/controlled_docs/SDS/Agilent_SDS/USA/"]
                               )
# }


