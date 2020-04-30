# -*- coding: utf-8 -*-
"""
Created on Mon Apr 09 16:47:43 2020

Agilent_CC_Creator_ttk.py

USES: 
    - Agilent_CC_Creator
    - Custom_Create_v1
    - Custom_Crate_v2
    
PURPOSE:
    - to be used whenever CofA_Nighly_Node_fails...
    - can choose between two dates
    - creates *nested* list of CofAs for BOTH:
        - EACH INDIVIDUAL DAY WITHIN RANGE
        - The # of CofAs at EOD for EACH DAY
    (pretty much a histogram of each day between )
    (the two dates the user picks and shows the )
    (new CofAs that were made for EACH EVERY DAY )

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
from ttkthemes import ThemedStyle
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox, filedialog 
from tkinter import constants, commondialog

class Logger(): # {
    
    def __init__(self, logging_output_dir): # {
        self.logging_output_dir = logging_output_dir
        #### INITITATING THE LOGGER OBJECT
        self.logger = logging.getLogger(__name__)
        
        # set the level of the logger (THIS IS SUPER USEFUL since it enables)
        # Explanation regarding the logger levels can be found here:
        # https://docs.python.org/3/howto/logging.html
        self.logger.setLevel(logging.DEBUG)
        
        # Create the logs.log file
        user_name = str(os.getlogin()) # get username 
        log_file_name = user_name + "-" + str(pd.Timestamp.now())[:10] + "-CofA-E-Node-Wizard-use-"
        log_file_path = os.path.join(self.logging_output_dir, str(log_file_name) + ".log")
        file_handler = logging.FileHandler(log_file_path)
        
        # Create the console handler with a higher log level
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.ERROR)
        
        # Format the logs structure so that every line would incude:
        # the time, the message, the function, the line #, script and level name
        formatter = logging.Formatter('%(asctime)s: %(message)s, FROM=%(funcName)s, LINENO=%(lineno)d, %(name)s - %(levelname)s')
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        # Adding the formater handlers
        self.logger.addHandler(console_handler)
        self.logger.addHandler(file_handler)
        
        # and printing the logs to the console as well
        self.logger.addHandler(logging.StreamHandler(sys.stdout))
    # }
# }

"""
IF SCRIPT IS BEING CALLED ON THE DAILY BASIS (ie scan last night and today)
*** THEN USE THE OLD ALGORITHIM OF SCANNING ENTIRE DIRECTORY AND CHECK AGAINST
 EACH INDIVIDUAL FILE SEPERATELY AND CHECK IF WITHIN TIME RANGE... ***
 
 IF SCRIPT IS BEING CALLED AND WANTS >> A SPECIFIC DATE RANGE << THEN 
 ** CREATE THE IDX FRAME AND SORT INDEX AND FILTER ON TIMESTAMP **
"""
class Agilent_CC_Creator(): # {
    
    in_file = "C:/data/inbound/Agilent_CofA_Letterhead_03-21-19.pdf"
    # [2020-01-27]\\in_directory_1 = "F:/APPS/CofA/"
    # [2020-01-27]\\in_directory_2 = "G:/C of A's/Agilent/"
    # [2020-01-27]\\out_directory = "G:/C of A's/#Email Node/"
    f_drive_convention = "*[@]*.pdf"
    g_drive_convention = "[part]*[CofA]*[Lot]*[#]*.pdf"
    
    def __init__(self, root, the_logger): # {
        self.root = root
        self.the_logger = the_logger
        self.root.title("Agilent CC Creator")
        self.root.geometry('427x207+300+300')  # was 275x400
        self.root.resizable(width=True, height=True)
        # [2020-04-27]\\self.root.minsize(width=275, height=275)
        self.root.minsize(width=275, height=125)
        self.root.maxsize(width=500, height=400)
        # Get/Set USERNAME & DESKTOP DIRECTORIES
        
        
        self.create_gui(the_root = self.root)
        ####################################
        # INSTANTIATE/SETUP MAIN VARIABLES #
        # [2020-04-07]\\
        """
        self.in_directory = in_directory
        self.out_directory = out_directory
        self.ignore_list = ignore_list
        self.check_start = check_start
        self.check_end = check_end
        """
        # <<< CALL MAIN FUNCTION >>>
        #self.main(self.in_directory, self.out_directory, self.ignore_list,
        #          self.check_start, self.check_end)
        """
        in_directory, out_directory, ignore_list, check_start, check_end
        """
    # }
    
    def create_gui(self, the_root): # {
        # TRY THE FOLLOWING
        try: # {
            self.create_ttk_styles(the_root=the_root)
            self.create_main_frame(the_root=the_root)
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
    # }
    
    def create_ttk_styles(self, the_root): # {
        # TRY THE FOLLOWING
        try: # {
            self.style = ThemedStyle(the_root)
            # STYLE THEME
            self.style.set_theme("kroc") # clearlooks, arc
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
    # }
    
    def create_main_frame(self, the_root): # {
        # TRY THE FOLLOWING
        try: # {
            self.mainframe = ttk.Frame(the_root)
            self.mainframe.pack(anchor=tk.CENTER, fill=tk.BOTH, expand=True)
            
            # [2020-04-27]\\
            """
            # START/END DATE ENTRY/LABELS
            ttk.Label(master=self.mainframe, text="Start-Date:\t"
                      ).pack(anchor=tk.NW, fill=tk.BOTH, expand=True)
            ttk.Entry(master=self.mainframe
                      ).pack(anchor=tk.NE, fill=tk.BOTH, expand=True)
            ttk.Label(master=self.mainframe, text="End-Date:\t"
                      ).pack(anchor=tk.SW, fill=tk.BOTH, expand=True)
            ttk.Entry(master=self.mainframe
                      ).pack(anchor=tk.SE, fill=tk.BOTH, expand=True)
            """
            
            # IMPORT [PRODUCT_NO] LIST
            self.import_product_nos = ttk.Button(master=self.mainframe, text="Import Product #s")
            self.import_product_nos.pack(anchor=tk.SW, fill=tk.BOTH, expand=True)
            
            # TK VAR for check button selection(s)
            # [2020-04-14]\\self.check_1 = tk.IntVar(master=self.mainframe)
            self.check_cofa = tk.IntVar(master=self.mainframe)
            self.check_sds = tk.IntVar(master=self.mainframe)
            
            # CHECK BUTTON FOR PROGRAM OPTIONS/SETTINGS
            ttk.Checkbutton(master=self.mainframe, text="CofA", 
                            variable=self.check_cofa
                            ).pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            
            ttk.Checkbutton(master=self.mainframe, text="SDS",
                            variable=self.check_sds
                            ).pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
            
            # IMPORT-WATERMARK BUTTON
            self.import_watermark = ttk.Button(master=self.mainframe, text="Import WATERMARK.pdf",
                                               command=self.import_product_nos, state=tk.DISABLED)
            self.import_watermark.pack(anchor=tk.NW, fill=tk.BOTH, expand=True)
            
            # EXPORT-LOCATION BUTTON
            self.export_button = ttk.Button(master=self.mainframe, text="Select EXPORT Location",
                                            state=tk.DISABLED)
            self.export_button.pack(anchor=tk.NW, fill=tk.BOTH, expand=True)
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
    # }
    
    def import_product_nos(self): # {
        # TRY THE FOLLOWING
        try: # {
            logger.info("IMPORTY")
        # }
        except: # {
            pass
        # }
        else: # {
            pass
        # }
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
        # TRY THE FOLLOWING
        try: # {
            pass
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
        else: # {
            logging.info("Operation Completed Successfully...")
        # }
    # }
    
    def send_email(self, send_from, send_to, subject, message, files=[],
                   server="cos.smtp.agilent.com", port=587, use_tls=True): # {
        pass
    # }
    
    """
    << MAIN FUNCTION LOGIC >>
    """
    def run(self): # {
        # TRY THE FOLLOWING
        try: # {
            pass
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
        # TRY THE FOLLOWING
        try: # {
            pass
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
    # }
    
# }

def main(): # {
    # TRY THE FOLLOWING
    try: # {
        # SETUP LOGGER
        logger = Logger(logging_output_dir="C:/Temp/").logger
        window = tk.Tk()
        application = Agilent_CC_Creator(root=window, the_logger=logger)
        window.config()
        window.mainloop()
    # }
    except: # {
        errorMessage = str(sys.exc_info()[0]) + "\n"
        errorMessage = errorMessage + str(sys.exc_info()[1]) + "\n\t\t"
        errorMessage = errorMessage + str(sys.exc_info()[2]) + "\n"
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        typeE = str("TYPE : " + str(exc_type))
        fileE = str("FILE : " + str(fname))
        lineE = str("LINE : " + str(exc_tb.tb_lineno))
        messageE = str("MESG : " + "\n\n" + str(errorMessage) + "\n")
        print("\n" + typeE + 
              "\n" + fileE + 
              "\n" + lineE + 
              "\n" + messageE)
        messagebox.showerror(title="ERROR!",
                             message=typeE +
                             "\n" + fileE +
                             "\n" + lineE +
                             "\n" + messageE)
    # }
# }

if __name__ == "__main__": # {
    # SETUP LOGGER
    # [2020-04-07]\\setup_logger()
    main()
# }

