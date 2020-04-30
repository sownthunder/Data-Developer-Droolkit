# -*- coding: utf-8 -*-
"""
Created on Fri Apr 17 11:09:00 2020

CofA_Nightly_Node_v4

USES:
    CofA_Nightly_Node_v3 (FINALE).py

@author: derbates
"""

# IMPORT THE GOODS
import os, sys, time
import os.path as op
from time import sleep
from pathlib import Path
import glob, shutil, fnmatch
import tempfile, logging
from threading import Timer
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk
import pandas as pd
import numpy as np
from pandas import Series, DataFrame
from PyPDF2 import PdfFileReader, PdfFileWriter
from zipfile import ZipFile
import email, smtplib, ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate

class Logger(): # {
    
    def __init__(self, logging_output_dir): # {
        self.logging_output_dir = logging_output_dir
        self.logger = logging.getLogger(__name__)
        
        # set the level of the logger (THIS IS SUPER USEFUL since it enables)
        # Explanation regarding the logger levels can be found here:
        # https://docs.python.org/3/howto/logging.html
    # }
# }

class CofA_Nightly_Node(): # {
    
    def __init__(self, in_directory, out_directory): # {
        self.in_directory = in_directory
        self.out_directory = out_directory
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
    
    def send_mail(self, send_from, send_to, subject, message, files=[],
                  server="cos.smtp.agilent.com", port=587, use_tls=True): # {
        print("SENDING MAIL... DATE == " + str(pd.Timestamp.now())[:10])
        # TRY THE FOLLOWING
        try: # {
            msg = MIMEMultipart()
            msg['From'] = send_from
            msg['To'] = COMMASPACE.join(send_to)
            msg['Date'] = formatdate(localtime=True)
            msg['Subject'] = subject
            
            msg.attach(MIMEText(message))
            
            for path in files: # {
                part = MIMEBase('application', 'octet-stream')
                with open(path, 'rb') as file: # {
                    part.set_payload(file.read())
                # }
                encoders.encode_base64(part)
                part.add_header('Content-Disposition',
                                'attachment; filename="{}"'.format(op.basename(path)))
                msg.attach(part)
            # }
            
            smtp = smtplib.SMTP(server, port)
            if use_tls: # {
                smtp.starttls()
            # }
            smtp.sendmail(send_from, send_to, msg.as_string())
            smtp.quit()
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
    # }
    
    def pull_creation_timestamp(self, a_file_path): # {
        # TRY THE FOLLOWING
        try: # {
            # FORCE PATH VARIABLE
            the_path = Path(a_file_path)
            # GET MODIFIED TIME
            mtime = os.path.getmtime(the_path)
            # GET CREATE TIME
            ctime = os.path.getctime(the_path)
            # CREATE DATE VARIABLE
            if ctime < mtime: # {
                # FORMAT DATE VAR as str
                date_str = str(datetime.fromtimestamp(ctime))
            # }
            
        # }
        except: # {
            pass
        # }
        else: # {
            pass
        # }
    # }
    
    def zip_the_directory(self, directory_to_zip): # {
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
    
    def run(self): # {
        # START TIME
        time_start = pd.Timestamp.now()
        # create str off TIMESTAMP
        time_today = str(time_start)[:10]
        # GET/SET ORIGINAL WORKING DIRECTORY
        og_wd = os.getcwd()
        in_file = "C:/data/inbound/Agilent_CofA_Letterhead_03-21-19.pdf"
        in_directory = "C:/data/outbound/CofA/"
        out_directory = "F:/APPS/G Drive/C of A's/#Email Node/"
        #######################
        f_file_conv_list = [] #
        f_file_time_list = [] #
        #######################
        g_file_conv_list = [] #
        g_file_time_list = [] #
        #######################
        print("TODAY == " + str(time_today))
        # SUBTRACTION DELTA
        subtraction_delta = pd.Timedelta(value=1, unit='days')
        # AND GET YESTERDAYS DATE BY SUBTRACTING
        time_yesterday = time_start - subtraction_delta
        yesterstr = str(time_yesterday.date())
        print("YESTERDAY == " + str(yesterstr))
        """
        CREATE GLOB STRINGS
        """
        f_glob_str = str("C:/data/outbound/CofA/*_" + yesterstr + "_F_")
        g_glob_str = str("C:/data/outbound/CofA/*_" + yesterstr + "_G_")
        print("\n F-GLOB-STRING == " + f_glob_str)
        print("\n G-GLOB-STRING == " + g_glob_str)
        """
        CREATE GLOBBER VARIABLE FROM ABOVE
        """
        the_globber = os.listdir(self.in_directory)
        for globski in the_globber: # {
            print(globski)
        # }
        # GLOB & PRELIMINARY STEPS
        glob_f_prev = sorted(glob.glob("C:/data/outbound/CofA/*_"
                                       + yesterstr
                                       + "_F_*"))
        print("\n\t GLOB_F_PREVIOUS >>> \n")
        for name in glob_f_prev: # {
            print(name)
        # }
        glob_f_cur = sorted(glob.glob("C:/data/outbound/CofA/*_"
                                      + time_today
                                      + "_F_*"))
        print("\n\t GLOB_F_CURRENT >>> \n")
        for name in glob_f_cur: # {
            print(name)
        # }
        glob_g_prev = sorted(glob.glob("C:/data/outbound/CofA/*_"
                                       + yesterstr
                                       + "_G_*"))
        print("\n\t GLOB_F_PREVIOUS >>> \n")
        for name in glob_g_prev: # {
            print(name)
        # }
        glob_g_cur = sorted(glob.glob("C:/data/outbound/CofA/*_"
                                          + time_today
                                          + "_G_*"))
        print("\n\t GLOB_G_CURRENT >>> \n")
        for name in glob_g_cur: # {
            print(name)
        # }
        #################
        # SETUP IMPORTS #
        #################
        # set as first element in returned list
        df1 = pd.read_csv(glob_f_prev[0])
        # set as first element in returned list
        df2 = pd.read_csv(glob_f_cur[0])
        # set as first element in returned list
        df3 = pd.read_csv(glob_g_prev[0])
        # set as first element in returned list
        df4 = pd.read_csv(glob_g_cur[0])
        print("LEN_D1 == " + str(len(df1)))
        print("LEN_D2 == " + str(len(df2)))
        print("LEN_D3 == " + str(len(df3)))
        print("LEN_D4 == " + str(len(df4)))
        # SET DIFFERENCE OF TWO DATAFRAMES FOR F_DRIVE IN PANDAS PYTHON
        f_set_diff_df = pd.concat([df2, df1, df1]).drop_duplicates(keep=False)
        print("LENGTH OF F_DIFF_DF == " + str(len(f_set_diff_df)))
        # SET DIFFERENCE OF TWO DATAFRAMES FOR G DRIVE IN PANDAS PYTHON
        g_set_diff_df = pd.concat([df2, df1, df1]).drop_duplicates(keep=False)
        print("LENGTH OF G_DIFF_DF == " + str(len(g_set_diff_df)))
    # }
# }

def main(): # {
    # TRY THE FOLLOWING
    try: # {
        print('THERE IS NOTHING WRONG')
    # }
    except: # {
        pass
    # }
# }

if __name__ == "__main__": # {
    # MAIN BOILERPLATE
    main()
# }