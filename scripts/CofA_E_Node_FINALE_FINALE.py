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
import datetime
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

class CofA_E_Node(): # {
    
    in_file = "C:/data/inbound/Agilent_CofA_Letterhead_03-21-19.pdf"
    # [2020-01-27]\\in_directory_1 = "F:/APPS/CofA/"
    # [2020-01-27]\\in_directory_2 = "G:/C of A's/Agilent/"
    # [2020-01-27]\\out_directory = "G:/C of A's/#Email Node/"
    f_drive_convention = "*[@]*.pdf"
    g_drive_convention = "[part]*[CofA]*[Lot]*[#]*.pdf"
    
    def __init__(self, in_directory, out_directory, ignore_list): # {
        self.in_directory = in_directory
        self.out_directory = out_directory
        self.ignore_list = ignore_list
        # <<< CALL MAIN FUNCTION >>>
        self.main()
    # }
    
    def pull_creation_timestamp(self, a_file_path): # {
        pass
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
    
    def dir_traverse(self, the_directory, ignore_dir_list, file_type_list): # {
        pass
    # }
    
    def send_email(self, send_from, send_to, subject, message, files=[],
                   server="cos.smtp.agilent.com", port=587, use_tls=True): # {
        pass
    # }
    
    def main(self): # {
        logging.info("\n\tIN_DIRECTORY == " + str(self.in_directory))
        logging.info("\n\tOUT_DIRECTORY == " + str(self.out_directory))
        logging.info("\n\tIGNORE_LIST == " + str(self.ignore_list))
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
    e_node = CofA_E_Node(in_directory="F:/APPS/CofA/",
                         out_directory="G:/C of A's/#Email Node/",
                         ignore_list=['Archive ERR',
                                      'Archive - For all archived CofA, see G Cofa Folder',
                                      'Instruction Sheets',
                                      'EXPORT ERRORS']
                         )
# }

