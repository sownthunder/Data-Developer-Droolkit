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
    
    def __init__(self, the_date, list_of_directories, in_file): # {
        self.the_date = the_date
        self.list_of_directories = list_of_directories
        self.in_file = str(in_file)
        # CREATE ZIP FOLDER 
        self.zip_dir_path = os.path.join(self.out_directory, self.the_date)
        # if 'zip_folder' DOES NOT YET EXIST!
        if not os.path.exists(self.zip_dir_path): #{
            # MAKE IT EXIST!
            os.makedirs(self.zip_dir_path)
        #}
        # RESET/RE-ESTABLISH 'out_directory'
        self.out_directory = Path(self.zip_dir_path)
        # CALL FUNCTION TO CREATE DATE IDX
        self.df_index = self.create_date_idx()
    # }
    
    def create_watermark(self, input_pdf, output, watermark): # {
        # TRY THE FOLLOWING
        try: #{
            watermark_obj = PdfFileReader(watermark)
            watermark_page = watermark_obj.getPage(0)
            
            pdf_reader = PdfFileReader(input_pdf)
            pdf_writer = PdfFileWriter()
            
            # Watermark all the pages
            for page in range(pdf_reader.getNumPages()): #{
                page = pdf_reader.getPage(page)
                page.mergePage(watermark_page)
                pdf_writer.addPage(page)
            #}
            
            with open(output, 'wb') as out: #{
                pdf_writer.write(out)
            #}
        #}
        except: #{
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
        #}
        else: #{
            print("[Watermark-PDF] FIN...")
        #}
        return
    # }
    
    def create_date_idx(self): # {
        # TRY THE FOLLOWING
        try: # {
            ###########################################################
            # CREATE EMPTY DATAFRAME TO HOLD FILE NAMES AND DATE INDEX
            df_index = pd.DataFrame(data=None, dtype=np.str)
            # READIN .CSV
            df_batch = pd.read_csv(self.in_file, header=None, names=['Lot_No'], dtype=np.str, engine='python')
            # FOR EACH PATH LISTED:
            for a_list in self.list_of_directories: # {
                print(Path(a_list))
                in_directory = Path(a_list)
                # EMPTY LISTS TO FILL WITH DATA
                thedir_col = []
                filename_col = []
                thedate_col = []
                lotno_col = []
                
                test_glob = str(a_list + "*")
                print(test_glob)
                # COUNTER
                x = 0
                for lot_no in df_batch.itertuples(): # {
                    # GLOB-ITERATE THRU EACH FILE MATCHING NAME ETC
                    for name in sorted(glob.glob(in_directory
                                                 + "*"
                                                 + str(lot_no[1])
                                                 + "*")): # {
                        # CREATE PATH VARIABLE
                        pdf_path = Path(str(name))
                        print(os.path.exists(pdf_path))
                    # }
                    print("==================== \n" + str(lot_no[1]) + "\n==============")
                    # CHECK AND CREATE NEW DIR PATH
                    new_dir_path = os.path.join(self.out_directory, str(lot_no[1]))
                    # IF 'lot_no' DIRECTORY DOES NOT EXIST:
                    if not os.path.exists(new_dir_path): # {
                        # MAKE IT EXIST!
                        os.makedirs(new_dir_path)
                    # }
                    # CREATE TEMP DIR/FOLDER TO WORK INSIDE OF:
                    with tempfile.TemporaryDirectory() as directory_name: # {
                        # was: most_recent = ""
                        the_dir = Path(directory_name)
                        print("TEMP DIRECTORY == " + str(the_dir))
                        # GLOB-ITERATE THRU EACH FILE MATCHING NAME ETC
                        for name in sorted(glob.glob(in_directory
                                                     + "*"
                                                     + str(lot_no[1])
                                                     + "*")): # {
                            # CREATE PATH VARIABLE
                            pdf_path = Path(str(name))
                            print(os.path.exists(pdf_path))
                            # << COPY/WATERMARK/MOVE PDF >>
                            """
                            # GET BASE NAME (FILE NAME)
                            file_name = os.path.basename(pdf_path)
                            # CREATE TEMP PATH
                            temp_path = os.path.join(the_dir, file_name)
                            # COPY FILE TO NEW LOCATION
                            shutil.copy2(pdf_path, temp_path)
                            # CREATE WATERMARK ON NEW FILE
                            self.create_watermark(input_pdf=temp_path,
                                             output=os.path.join(new_dir_path, file_name),
                                             watermark=self.watermark)
                            """
                            # increase count
                            x += 1
                        # }
                        sub_glob = os.path.join(in_directory, "*")
                        # GLOB SUB FOLDERS
                        for name in sorted(glob.glob(sub_glob + "/*")): # {
                            print(name)
                        # }
                    # }
                    print("count == " + str(x))
                    print("Directory exists after?", str(the_dir.exists()))
                    print("Contents after:", str(list(the_dir.glob("*"))))
                    print("told you so")
                # }
                # create 'result' DataFrame
                result = pd.concat([])
            # }
        # }
        except: # {
            print("FAIL!")
        # }
    # }
    
    def pull_creation_timestamp(self, a_file_path): # { 
        # TRY THE FOLLOWING
        try: #{ 
            pass
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
                                                    "J:/controlled_docs/SDS/Agilent_SDS/USA/"],
                               in_file="2020-03-04-batch-list.csv"
                               )
# }


