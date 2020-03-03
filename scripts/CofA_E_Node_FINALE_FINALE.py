# -*- coding: utf-8 -*-
"""
Created on Mon Jan 27 13:44:43 2020

CofA_E_Node_FINALE(_FINALE).py

USES: 
    - CofA_Nightly_Node_v2.py
    - CofA_Nightly_Node_FINALE.py
    - CofA_email_cathcup.ipynb
    - CofA_G_DRIVE_file name conv...ipynb

@author: derbates
"""

# IMPORT THE GOODS
import os, sys, time
from time import sleep
import pathlib, glob
from pathlib import Path
import fnmatch, shutil
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from pandas import Series, DataFrame
import logging
import tempfile, threading
from PyPDF2 import PdfFileReader, PdfFileWriter
from zipfile import ZipFile
import email, smtplib, ssl
import os.path as op
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox, filedialog 
from tkinter import constants, commondialog

class CofA_E_Node(): # {
    
    in_file = "C:/data/inbound/Agilent_CofA_Letterhead_03-21-19.pdf"
    # [2020-01-27]\\in_directory_1 = "F:/APPS/CofA/"
    # [2020-01-27]\\in_directory_2 = "G:/C of A's/Agilent/"
    # [2020-01-27]\\out_directory = "G:/C of A's/#Email Node/"
    f_drive_convention = "*[@]*.pdf"
    g_drive_convention = "[part]*[CofA]*[Lot]*[#]*.pdf"
    
    def __init__(self, in_directory, out_directory, ignore_list, check_start, check_end): # {
        ####################################
        # INSTANTIATE/SETUP MAIN VARIABLES #
        self.in_directory = in_directory
        self.out_directory = out_directory
        self.ignore_list = ignore_list
        self.check_start = check_start
        self.check_end = check_end
        # <<< CALL MAIN FUNCTION >>>
        self.main()
    # }
    
    """
    TAKES IN:
    (1) file_path to file 
    (2) integer to determine WHICH DIRECTION:
    [XXX-123@XXXXXXXXXX.pdf <or> part XXX-123 CofA Lot# XXXXXXXXXX.pdf]
    RETURNS: 
    The create time or modified time, whichever is older
    """
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
            # IF CREATE TIME IS OLDER...
            if ctime < mtime:  # {
                # FORMAT DATE VAR as str
                date_str = str(datetime.fromtimestamp(ctime))
            # }
            # ELSE.... MODIFIED TIME IS OLDER...
            else:  # {
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
            logging.error("\n" + typeE +
                          "\n" + fileE +
                          "\n" + lineE +
                          "\n" + messageE)
        # }
        else:  # {
            logging.info("Operation Completed Successfully...")
            # RETURN THE DATE WE PULLED AS STRING
            return date_str
        #}
        finally:  # {
            logging.info("FINISHED")
        #}
    # }
    
    def generate_naming_convention(self, the_pdf_path): # {
        pass
    # }
    
    def create_watermark(self, input_pdf, output, watermark): # {
        pass
    # }
    
    def get_all_file_paths(self, directory): # {
        pass
    # }
    
    def zip_the_directory(self, directory_to_zip): # {
        pass
    # }
    
    """
    TAKES IN:
    (1) the directory to scan
    (2) list of sub-directories TO NOT SCAN
    (3) list of file types that you are searching for
    (4a) uses self.start
    """
    def dir_traverse(self, the_directory, ignore_dir_list, file_type_list, 
                     check_start, check_end): # {
        pass
    # }
    
    def create_time_idx_frame(self, the_directory): # {
        x = 0
        counter = 0
        # TRY THE FOLLOWING
        try: # {
            # CREATE LIST VAR of DIRECTORY
            dir_list = os.listdir(the_directory)
            logging.info("\tLENGTH OF [dir_list]: " + str((len(dir_list))))
            # CREATE SERIES OFF LIST
            d1 = pd.Series(dir_list)
            d1.astype(dtype=np.str)
            # CREATE EMPTY DATAFRAME (TO BE FILLED)
            df_time_idx = pd.DataFrame(data=None, dtype=np.str)
            # ASSIGN PANDAS SERIES as first column
            df_time_idx['File'] = d1
            # CREATE COLUMN VARIABLE TO STORE DATA
            date_col = []
            x = 0  # counter
            # create Series from column
            d1 = pd.Series(df_time_idx['File'])
            d1.astype(dtype=np.str)
            # FOR EACH ROW IN THE COLUMN
            for row in d1: # {
                the_str = str(row)
                file_path = os.path.join(the_directory, the_str)
                # create date var
                the_date = self.pull_creation_timestamp(a_file_path=file_path)
                logging.info("THE_DATE == " + str(the_date))
                # APPEND TO LIST
                date_col.append(the_date)
                x += 1 # increment counter
            # }
            # CREATE COLUMN FROM LIST
            df_time_idx['Date'] = date_col
            # RE-ALIGN DATE AS INDEX
            df_time_idx.set_index(['Date'], inplace=True)
            # Display index
            logging.info("INDEX:\n" + str(df_time_idx.index))
            # SORT INDEX
            df_time_idx.sort_index(inplace=True)
            # EXPORT TO TEMP FOLDER (for meow)
            df_time_idx.to_csv("C:/data/outbound/CofA_E_Node_SORTED.csv", index=True)
        # }
        except: # {
            errorMessage = str(sys.exc_info()[0]) + "\n"
            errorMessage = errorMessage + str(sys.exc_info()[1]) + "\n"
            errorMessage = errorMessage + str(sys.exc_info()[2]) + "\n"
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            typeE = str("TYPE : " + str(exc_type))
            fileE = str("FILE : " + str(fname))
            lineE = str("LINE : " + str(exc_tb.tb_lineno))
            messageE = str("MESG : " + "\n" + str(errorMessage))
            print("\n" + typeE +
                  "\n" + fileE +
                  "\n" + lineE +
                  "\n" + messageE)
        # }
    # }
    
    def send_email(self, send_from, send_to, subject, message, files=[],
                   server="cos.smtp.agilent.com", port=587, use_tls=True): # {
        pass
    # }
    
    """
    << MAIN FUNCTION LOGIC >>
    """
    def main(self): # {
        logging.info("\n\tIN_DIRECTORY == " + str(self.in_directory))
        logging.info("\n\tOUT_DIRECTORY == " + str(self.out_directory))
        logging.info("\n\tIGNORE_LIST == " + str(self.ignore_list))
        # GET/SET ORIGINAL WORKING DIRECTORY
        self.og_wd = os.getcwd()
        logging.info("OG-WORKING-DIR == " + str(self.og_wd))
        self.file_list_f = [] # remove duplicate below!!
        self.time_list_f = []
        self.file_list_g = []
        self.time_list_g = []
        # CREATE INDEX FRAME
        self.create_time_idx_frame(the_directory=self.in_directory)
    # }
    
# }

def setup_logger(): # {
    # TRY THE FOLLOWING
    try: # {
        logging.basicConfig(level=logging.INFO,
                           format='%(asctime)s: %(message)s, FROM=%(funcName)s, LINENO=%(lineno)d',
                           datefmt='%Y-%m-%d-%H%M%S',
                           filemode='a')
    # }
    except: #{ 
        errorMessage = str(sys.exc_info()[0]) + "\n"
        errorMessage = errorMessage + str(sys.exc_info()[1]) + "\n"
        errorMessage = errorMessage + str(sys.exc_info()[2]) + "\n"
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        typeE = str("TYPE : " + str(exc_type))
        fileE = str("FILE : " + str(fname))
        lineE = str("LINE : " + str(exc_tb.tb_lineno))
        messageE = str("MESG : " + "\n" + str(errorMessage))
        print("\n" + typeE +
              "\n" + fileE +
              "\n" + lineE +
              "\n" + messageE)
    # }
    else: # {
        logging.info("Operation Completed Successfully...")
    # }
# }

if __name__ == "__main__": # {
    # SETUP LOGGER
    setup_logger()
    ################################
    # INSTANTIATE GLOBAL VARIABLES #
    in_directory_1 = ""
    in_directory_2 = ""
    # [2020-03-02]\\og_wd = os.getcwd() # GET/SET ORIGINAL WORKING DIRECTORY
    # [2020-03-02]\\file_list_f = []
    # [2020-03-02]\\time_list_f = []
    # [2020-03-02]\\file_list_g = []
    # [2020-03-02]\\time_list_g = []
    # CREATE TIMESTAMP FOR RIGHT NOW
    # [2020-03-02]\\ts_now = pd.Timestamp(year=2020, day=29, month=1, hour=5) # hard-coded for testing
    ts_now = pd.Timestamp.now()
    # USED TO DETERMINE THE CORRECT "start_time" (one day and five hours prior)
    # [2020-03-02]\\ts_start_delta = pd.Timedelta(days=1, hours=5)
    ts_start_delta = pd.Timedelta(days=1)
    # USED TO DETERMINE THE CORRECT "end_time" (five hours prior)
    # [2020-03-02]\\ts_end_delta = pd.Timedelta(hours=5)
    ts_end_delta = pd.Timedelta(hours=1)
    # SUTRACT and determine "start_time"
    time_start = ts_now - ts_start_delta
    logging.info("\n\t START OF SCAN-TIME: " + str(time_start))
    # SUBTRACT and determine "end_time"
    time_end = ts_now - ts_end_delta
    logging.info("\n\tEND OF SCAN-TIME == " + str(time_end))
    F_Drive_node = CofA_E_Node(in_directory="F:/APPS/CofA/",
                               out_directory="G:/C of A's/#Email Node/",
                               ignore_list=['Archive ERR',
                                            'Archive - For all archived CofA, see G Cofa Folder',
                                            'Instruction Sheets',
                                            'EXPORT ERRORS'],
                               check_start=time_start,
                               check_end=time_end)
    G_Drive_node = CofA_E_Node(in_directory="G:/C of A's/Agilent/",
                               out_directory="G:/C of A's/#Email Node/",
                               ignore_list=['#Archive'],
                               check_start=time_start,
                               check_end=time_end)
# }

