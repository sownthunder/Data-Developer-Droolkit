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
        pass
    # }
    
    def pull_creation_timestamp(self, a_file_path): # {
        pass
    # }
    
    def zip_the_directory(self, directory_to_zip): # {
        pass
    # }
    
    def run(self): # {
        # START TIME
        time_start = pd.Timestamp.now()
        # create str off TIMESTAMP
        time_today = str(time_start)[:10]
        # GET/SET ORIGINAL WORKING DIRECTORY
        og_wd = os.getcwd()
        
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