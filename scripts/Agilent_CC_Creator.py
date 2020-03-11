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
        # CREATE TEMP DIR/FOLDER TO WORK INSIDE OF;
        with tempfile.TemporaryDirectory() as directory_name: # {
            the_dir = Path(directory_name)
            print("TEMP_DIRECTORY == " + str(the_dir))
            # ITERATE THROUGH DATAFRAME RETURNED ABOVE
            for row in self.df_index.itertuples(): # {
                # CREATE "old_path"
                old_path = os.path.join(row[1], row[2])
                # CREATE "temp_path"
                temp_path = os.path.join(the_dir, row[2])
                # COPY FILE TO NEW LOCATION
                shutil.copy2(old_path, temp_path)
                
            # }
            # CALL FUNCTION TO ZIP DIRECTORY WHILE STILL INSIDE
            self.zip_the_directory(the_dir)
            # TRY AND FINISH THIS SHIT OFF (copy/move this shit!)
            print("GLOBBING FOR ZIP FILE !!!")
            print(str(os.path.join(the_dir, "*.zip")))
            for name in sorted(glob.glob(str(the_dir) + "/*.zip")): # {
                print("NAME OF FILE == " + str(name))
                print(len(sorted(glob.glob(str(the_dir)))))
                # GET AND SET PATH_NAME
                zip_path = Path(name)
                print("ZIP_PATH == " + str(zip_path))
            # }
            # COPY ZIP FILE FROM TEMP FOLDER TO TARGET FOLDER
            shutil.copy2(src=zip_path, dst=self.zip_dir_path)
        # }
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
    
    def get_all_file_paths(self, directory): # {
         # initializing empty file paths list
            file_paths = []
            
            # crawling through directory and subdirectories
            for root, directories, files in os.walk(directory): # {
                for filename in files: # {
                    # join the two strings in order to form the full filepath
                    filepath = os.path.join(root, filename)
                    file_paths.append(filepath)
                # }
            # }
            
            # returning all file paths
            return file_paths
    # }
    
    def zip_the_directory(self, directory_to_zip): # {
        # RE-INSTANTIATE GLOBALS
        global og_wd
        # TRY THE FOLLOWING
        try: # {
            print("\n\n\nXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
            print("\nWORKING DIRECTORY ---BEFORE--- ZIP ==\n" + str(os.getcwd()))
            # CHANGE WORKING DIRECTORY TO DIRECTORY WE WISH TO ZIP
            os.chdir(directory_to_zip)
            # path to folder (NOW currently folder we want to zip)
            directory = "."  #self.out_directory
            print("\nWORKING DIRECTORY ---DURING--- ZIP==\n" + str(os.getcwd()))
            # calling function to get all file paths in the directory
            file_paths = self.get_all_file_paths(directory)
            print("\nfollowing files will be zipped:")
            for file_name in file_paths: # {
                print(file_name)
            # }
            # writing files to a zipfile
            with ZipFile('Custom_Crate_'
                         + str(pd.Timestamp.now())[:10]
                         + ".zip", "w") as zip: # {
                # Writing each file one by one
                for file in file_paths: # {
                    zip.write(file)
                # }
            # }
            print("ALL FILES ZIPPED SUCCESSFULLY!\nXXXXXXXXXXXXXXXXXXXXXX")
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
        else: # {
            print("Operation Completed Successfully...")
        # }
        finally: # {
            # CHANGE WORKING DIRECTORY BACK TO ORIGINAL
            # [2020-03-10]\\os.chdir(self.out_directory)
            os.chdir(og_wd)
        # }
    # }
    
    def create_date_idx(self): # {
        # TRY THE FOLLOWING
        try: # {
            ###########################################################
            # CREATE EMPTY DATAFRAME TO HOLD FILE NAMES AND DATE INDEX
            df_index = pd.DataFrame(data=None, dtype=np.str)
            # READIN .CSV
            df_batch = pd.read_csv(self.in_file, header=None, names=['Lot_No'], dtype=np.str, engine='python')
            # COUNTER
            x = 0
            # FOR EACH PATH LISTED:
            for directory in self.list_of_directories: # {
                # SET "in_directory" to be one from LIST
                in_directory = Path(directory)
                print(in_directory)
                # EMPTY LISTS TO FILL WITH DATA
                filepath_col = [] # for FILE DIRECTORY
                filename_col = [] # for FILE NAME
                filedate_col = [] # creation DATE
                lot_num_col = [] # FOR CURRENT LOT #
                # CREATE REGEX VAR FOR DIR
                glob_path = str(directory + "**/*.pdf")
                # FOR EACH LOT_NO 
                for lot_no in df_batch.itertuples(): # {
                    the_lot_no = str(lot_no[1])
                    print(" << LOT # " + the_lot_no + " >>\n\n")
                    # GET A RECURSIVE LIST OF FILE PATHS THAT
                    # MATCHES FILE TYPE INCLUDING SUB-DIRS
                    file_list = glob.glob(glob_path, recursive=True)
                    # Iterate over the list of filepaths & perform on each file
                    for file_path in file_list: # {
                        # IF FILE CONTAINS 'our' LOT #
                        if (str(file_path).find(the_lot_no) != -1): # {
                            print("\t<<<<< FOUND >>>>>")
                            # CREATE PDF PATH
                            pdf_path = Path(file_path)
                            print("PDF:\n\t" + str(pdf_path))
                            print("exists: " + str(os.path.exists(pdf_path)))
                            # GET DIR NAME
                            dir_name = os.path.dirname(pdf_path)
                            print("DIR_NAME:\n\t" + str(dir_name))
                            # GET BASE NAME (FILE NAME)
                            file_name = os.path.basename(pdf_path)
                            print("FILE_NAME:\n\t" + str(file_name))
                            # GET FILE CREATION DATE
                            file_date = self.pull_creation_timestamp(pdf_path)
                            print("FILE_DATE:\n\t" + str(file_date))
                            #####################
                            # FILL LIST COLUMNS #
                            #####################
                            filepath_col.append(str(dir_name))
                            filename_col.append(str(file_name))
                            filedate_col.append(str(file_date))
                            lot_num_col.append(str(the_lot_no))
                            # INCREASE COUNT
                            x += 1
                        # }
                        else: # {
                            pass
                        # }
                        
                    # }
                    # << CONCAT DATAFRAME ?? >>
                    # [2020-03-11]\\df_test = pd.DataFrame(data=None, dtype=np.str)
                    # CREATE EMPTY DATAFRAME FOR EACH INDIVIDUAL DIRECTORY
                    df_dir = pd.DataFrame(data=None, dtype=np.str)
                    # CREATE COLUMNS
                    df_dir['Directory'] = filepath_col
                    df_dir['Filename'] = filename_col
                    df_dir['Creation'] = filedate_col
                    df_dir['Lot_No'] = lot_num_col
                    # EXPORT ??
                    df_dir.to_csv('df_dir_' + str(directory)[:1] + '_.csv',
                                  index=True)
                    
                # }
                ## << CONCAT DATAFRAME??? >>
                result = pd.concat([df_index, df_dir])
                # EXPORT ??
                result.to_csv('df_result_ ' + str(pd.Timestamp.now())[:10] + ",csv",
                              index=True, mode='a')
                
            # }
            # APPEND TO MAIN DATAFRAME
            # [2020-03-10]\\df_index = df_index.append(result)
            # APPEND TO MAIN DATAFRAME
            df_index = df_index.append(result)
            # EXPPORT?
            df_index.to_csv("df_index_test_" + str(pd.Timestamp.now())[:10] + ".csv",
                            index=True)
            """
            # CREATE DATAFRAME
            df_test= pd.DataFrame(data=None, dtype=np.str)
            # Create Columns?
            df_test['Directory'] = filepath_col
            df_test['Filename'] = filename_col
            df_test['Creation'] = filedate_col
            df_test['Lot_No'] = lot_num_col
            # SET INDEX OF DATAFRAME
            df_test.set_index(['Creation'], inplace=True)
            # SORT INDEX?
            df_test.sort_index(inplace=True)
            # EXPORT ??
            df_test.to_csv('df_test_' + str(directory)[:1] + "_.csv", index=True)
            # CONCAT/CREATE "result"
            result = pd.concat([df_index, df_test])
            # EXPORT ??
            result.to_csv('df_result_' + str(pd.Timestamp.now())[:10] + ".csv",
                          index=True, mode='a')
            # APPEND TO MAIN DATAFRAME
            df_index = df_index.append(result)
            # EXPORT ??
            df_index.to_csv("df_index_test_" + str(pd.Timestamp.now())[:10] + ".csv",
                            index=True)
            """
            # CREATE NEW DATAFRAME OF DROPPED DUPS
            df_dedupped = df_index.drop_duplicates(subset=['Lot_No'], keep='last')
            df_dedupped.to_csv("df_dedupped_test.csv", index=True)
            # RETURN DATAFRAME WITH UNIQUE ROWS etc
            return df_dedupped
            """
            # APPEND TO MAIN DATAFRAME
            df_index = df_index.append(result)
            print("COUNT == " + str(x))
            """
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
    
    def pull_creation_timestamp(self, a_file_path): # { 
        # TRY THE FOLLOWING
        try: # {
            # FORCE PATH VARIABLE
            the_path = Path(str(a_file_path))
            # GET MODIFIED TIME
            mtime = os.path.getmtime(the_path)
            # GET CREATE TIME
            ctime = os.path.getctime(the_path)
            # CREATE DATE VAR
            if ctime < mtime: # {
                # FORMAT DATE VAR AS str
                date_str = str(datetime.fromtimestamp(ctime))
            # }
            # ELSE.... MODIFIED TIME IS OLDER..
            else: # {
                # FORMAT DATE VAR as str
                date_str = str(datetime.fromtimestamp(mtime))
            # }
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
        #}
        else: # {
            print("Operation Completed Successfully...")
            return date_str
        # }
        finally: # {
            print("FIN...")
        # }
    # } 
    
# }

if __name__ == "__main__": # {
    # INSTANTIATE GLOBAL VARIABLES
    og_wd = os.getcwd() # GET/SET ORIGINAL WORKING DIRECTORy
    # CREATE TIMESTAMP FOR ZIP FOLDER
    ts = pd.Timestamp.now()
    ts_str = str(ts)[:10]
    print(ts_str)
    # CREATE / CALL MAIN CLASS FUNCTION
    create_crate = CustomCrate(the_date=ts_str, 
                               list_of_directories=['F:/APPS/CofA/'],
                                                    #"G:/C of A's/Agilent/",
                                                    #"J:/controlled_docs/SDS/Agilent_SDS/USA/"],
                               in_file="C:/data/inbound/2020-03-05-batch-list.csv"
                               )
# }


