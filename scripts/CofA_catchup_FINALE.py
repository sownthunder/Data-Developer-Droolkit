"""
Created on Dec 16, 09:00 AM - DB

To be used whenever CofA_Nightly_Node Fails to catchup and scan between:
(1) START-DATE
(2) END-DATE

<< USES SCRIPTS >>>
Data-Developer-Droolkit/AGILENT/[2019_12_15]_CofA_Email_Node_catchup_date_FIX

()-------------------------------------------------------()
A) Grabs all CofAs created in-between the TWO GIVEN DATES
B) In the two Directories:
- F:/APPS/CofA/
- G:/C of A's/Agilent/
C) Watermarks, copies, and moves into TWO seperate folders
D) ZIPS ALL FILES INTO ONE and creates .CSV listing
"""

# IMPORT THE GOODS
import os, sys, time
from time import sleep
from pathlib import Path
from datetime import datetime
import pandas as pd
import numpy as np
from pandas import Series, DataFrame
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import platform, logging
import fnmatch, glob, shutil
from zipfile import ZipFile
from PyPDF2 import PdfFileWriter, PdfFileReader
import email, smtplib, ssl
import os.path as op
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate

class CofACatchup:  # {

    def __init__(self, root, the_timestamp, in_directory_1, in_directory_2, 
                 the_watermark, the_outbound_dir):  # {
        self.root = root
        self.the_timestamp = the_timestamp
        self.in_directory_1 = in_directory_1
        self.in_directory_2 = in_directory_2
        self.the_watermark = the_watermark
        self.the_outbound_dir = the_outbound_dir
        self.root.title("CofA Catchup: " + self.the_timestamp)  # str(self.the_timestamp)[:16])
        self.root.geometry('350x200+250+250')
        self.root.resizable(width=True, height=False)
        self.root.minsize(width=350, height=200)
        self.root.maxsize(width=400, height=200)
        self.create_gui()
    # }

    def create_gui(self):  # {
        self.create_label_frame()
        self.create_buttons()
    # }

    def create_label_frame(self):  # {
        # CREATE FRAME CONTAINER
        labelframe = ttk.LabelFrame(master=self.root, text='Enter in Date Range:')
        labelframe.pack(side=tk.TOP, fill=tk.BOTH, expand=True)  #.grid(row=0, column=1, padx=8, pady=8, sticky='ew')
        ttk.Label(master=labelframe, text='Start Date: ').pack(anchor=tk.W, fill=tk.BOTH, expand=True)  #.grid(row=1, column=1, sticky=tk.W, pady=2)
        self.start_datefield = ttk.Entry(master=labelframe)
        self.start_datefield.pack(anchor=tk.E, fill=tk.BOTH, expand=True)
        ttk.Label(master=labelframe, text="End Date: ").pack(anchor=tk.W, fill=tk.BOTH, expand=True)
        self.end_datefield = ttk.Entry(master=labelframe)
        self.end_datefield.pack(anchor=tk.E, fill=tk.BOTH, expand=True)
    # }

    def create_buttons(self):  # {
        self.begin_button = ttk.Button(master=self.root, text='<<BEGIN>>', command=self.run)
        self.begin_button.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
    # }
    
    """
    {runs the __main__: function that were originally part of [2019_12_15]_CofA_Email_Catchup_fix]}
    """
    def run(self):  # {
        if self.entry_dates_validated():  # {
            # TRY THE FOLLOWING
            try: #{ 
                # ASK FOR DIRECTORY TO SAVE FOLDERS CONTAINING ZIPS YALL
                self.out_directory = filedialog.askdirectory(parent=None, title="select OUTPUT folder:", initialdir="C:/")
                # CREATE TIME STAMP FOR ZIP FOLDER (from class variable)
                zip_ts = str(self.the_timestamp)[:10]
                # CREATE ZIP PATHS AT RUN_TIME:
                self.zip_dir_path = os.path.join(str(self.out_directory), "CofA-F-DRIVE-" + zip_ts)
                self.zip_dir_path_2 = os.path.join(str(self.out_directory), "CofA-G-DRIVE-" + zip_ts)
                # IF 'zip_folder' DOES NOT YET EXIST!
                if not os.path.exists(self.zip_dir_path):  # {
                    # MAKE IT EXIST!
                    os.makedirs(self.zip_dir_path)
                # }
                if not os.path.exists(self.zip_dir_path_2): # {
                    # MAKE IT EXIST!
                    os.makedirs(self.zip_dir_path_2)
                # }
                # TAKE INPUT FROM ENTRY BOXES AND SET AS START TIME / END TIME
                time_start = str(self.start_datefield.get())
                time_end = str(self.end_datefield.get())
                # CREATE TIME STAMP VAR for filter requirements
                self.start_check = pd.Timestamp(time_start)
                logging.info("\n\t\t CHECK-START-DATE:\t" + str(self.start_check))
                logging.info("\n\t\t" + str(type(start_check)))
                self.end_check = pd.Timestamp(time_end)
                logging.info("\n\t\t CHECK-END-DATE:\t" + str(self.end_check))
                logging.info("\n\t\t" + str(type(end_check)))
                # INSTANTIATE (class-wide) VARIABLES
                ignore_list = ['Archive ERR',
                               'Archive - For all archived CofA, see G CofA folder',
                               'Instruction Sheets']
                # LIST TO HOLD ALL PATHS FOR FILES (F_DRIVE)
                self.file_list = []
                # LIST TO HOLD ALL PATHS FOR NEW FILE NAME CONVENTIONS
                self.file_name_conv_list = []
                # LIST TO HOLD ALL DIRECTORY NAMES
                self.dir_list = []
                # LIST TO HOLD ALL TIMESTAMPS
                self.ts_list = []
                # CALL TRAVERSE/SCAN FUNCTION ON (F:/APPS/CofA/) DIRECTORY
                self.directory_scan(the_directory=self.in_directory_1, 
                                    the_ignore_list=ignore_list, 
                                    file_type_list=[".pdf"])
                # CALL TRAVERSE/SCAN FUNCTION ON (G:/C of A's/Agilent/) DIRECTORY
                self.directory_scan(the_directory=self.in_directory_2,
                                    the_ignore_list=ignore_list,
                                    file_type_list=[".pdf"])
                ###############################################
                # CREATE DATAFRAME ETC (line 518 in original) #
                ###############################################
                self.filelist_df = pd.DataFrame(data=None, columns=None, dtype=np.str)
                # ASSIGN LISTS TO **NEW** COLUMNS IN DATAFRAME
                self.filelist_df["CofA"] = self.file_list
                self.filelist_df["Directory"] = self.dir_list
                self.filelist_df["Timestamp"] = self.ts_list
                # EXPORT TO PATH OF FOLDER WE ARE GOING TO ZIP TO
                self.export_path = os.path.join(self.zip_dir_path, )
            # }
            except:  # {
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
            # }
        # }
        else:  # {
            messagebox.showwarning(title="WARNING!", message="Date(s) entrys are blank!", parent=self.root) 
        # } 
    # }
        
    
    def entry_dates_validated(self):  # {
        return len(self.start_datefield.get()) !=0 and len(self.end_datefield.get()) != 0
    # }
    
    def directory_scan(self, the_directory, the_ignore_list, file_type_list):  # {
        # TRY THE FOLLOWING
        try:  # {
            # COUNTER
            x = 0  # number of PDFS matched
            count = 0  # possible total number of matches (files)
            # SETUP VARIABLES
            scan_directory = Path(the_directory)
            # <<<<< BEGIN OS.WALK >>>>>
            for root, dirs, files in os.walk(scan_directory):  # {
                # FOR EACH ITEM IN IGNORE LIST...
                for item in the_ignore_list:  # {
                    # CREATE FILE_MATCH VAR
                    file_match = str("*" + item)
                    # DO FNMATCH FOR THIS 'item'
                    if fnmatch.fnmatch(f, file_match):  # {
                        # <<< STRING OPERATIONS >>>
                        ############################
                        # ASSEMBLE!
                        file_path = os.path.join(root, f)
                        logging.info("FILE_PATH == " + str(file_path))
                        # RETURN DATETIME VAR
                        file_date = self.pull_creation_timestamp(file_path)
                        logging.info("FILE_DATE == " + str(file_date))
                        ###################################################
                        #
                        #
                        #
                        # << FINISH DIRECTORY SCAN >> (dir_traverse)
                        #
                        #
                        #
                        #
                        #
                        ###################################################
                    # }
                    else:  # {
                        logging.info("\t" + str(f) + " NOT A PDF !")
                    # }
                # }
            # }
        # }
        except:  # {
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
        # }
    # }
    
    def pull_creation_timestamp(self, a_file_path):  # {
        # TRY THE FOLLOWING:
        try: #{
            # FORCE PATH VARIABLE
            the_path = Path(a_file_path)
            # GET MODIFIED TIME
            mtime = os.path.getmtime(the_path)
            # GET CREATE TIME
            ctime = os.path.getctime(the_path)
            # CREATE DATE VAR
            # IF CREATE TIME IS OLDER...
            if ctime < mtime:  # {
                # FORMAT DATE VAR as str
                date_time = datetime.fromtimestamp(ctime)
            # }
            # ELSE.... MODIFIED TIME IS OLDER...
            else:  # {
                # FORMAT DATE VAR as str
                date_time = datetime.fromtimestamp(mtime)
            # }
        # }
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
            logging.error("\n" + typeE +
                          "\n" + fileE +
                          "\n" + lineE +
                          "\n" + messageE)
        # }
        else:  # {
            logging.info("SUCCESS! VERY NICE!")
            # RETURN THE DATE WE PULLED AS STRING
            return date_time
        # }
        finally:  # {
            logging.info("[pull_creation_timestamp] FIN...")
        # }
    # }
    
    def generate_naming_convention(self, the_pdf_path):  # {
        pass
    # }
    
    def create_watermark(self, input_pdf, output, watermark):  # {
        pass
    # }
    
    def get_all_file_paths(self, directory): # {
        pass
    # }
    
    def zip_the_directory(self, directory_to_zip):  # {
        pass
    # }
    
    def send_mail(self, send_from, send_to, subject, message, files=[],
                  server="cos.smtp.agilent.com", port=587, use_tls=True):  # {
        logging.info("SENDING MAIL... DATE: \t" + str(pd.Timestamp.now())[:10])
        msg = MIMEMultipart()
        msg['From'] = send_from
        msg['To'] = COMMASPACE.join(send_to)
        msg['Date'] = formatdate(localtime=True)
        msg['Subject'] = subject
        
        msg.attach(MIMEText(message))
        
        for path in files:  # {
            part = MIMEBase('application', "octet-stream")
            with open(path, 'rb') as file:  # {
                part.set_payload(file.read())
            # }
            encoders.encode_base64(part)
            part.add_header('Content-Disposition',
                            'attachment; filename="{}"'.format(op.basename(path)))
            msg.attach(part)
        # }
        
        smtp = smtplib.SMTP(server, port)
        if use_tls:  # {
            smtp.starttls()
        # }
        smtp.sendmail(send_from, send_to, msg.as_string())
        smtp.quit()
    # }

# }

def setup_logger():  # {
    # TRY THE FOLLOWING
    try:  # {
        logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s: %(message)s, FROM=%(funcName)s, LINENO=%(lineno)d',
                            datefmt='%Y-%m-%d-%H%M%S',
                            filemode='a')
    # }
    except:  # {
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
        messagebox.showerror(title="ERROR!",
                             message=typeE +
                                     "\n" + fileE +
                                     "\n" + lineE +
                                     "\n" + messageE)
    # }
    else: # {
        logging.info("Operation Completed Successfully...")
    # }
# }

"""
{runs the "In[11]" that were originally part of [2019_12_15]_CofA_Email_Catchup_fix]}
"""
def main():  # {
    ################################
    # INSTANTIATE GLOBAL VARIABLES #
    ################################
    ts_now = pd.Timestamp.now()
    ts_str = str(ts_now)[:16]  # WAS: 10
    watermark = "C:/data/inbound/Agilent_CofA_Letterhead_03-21-19.pdf"
    in_directory_1 = "F:/APPS/CofA/"
    in_directory_2 = "G:/C of A's/Agilent/"
    # [2019-12-19]\\out_directory = filedialog.askdirectory(parent=None, title="select OUTPUT folder:", initialdir="C:/")
    outbound_directory = "G:/C of A's/#Email Node/"
    ###################################################
    # INSTANTIATE GUI AND FEED IN VARIABLE PARAMETERS #
    ###################################################
    root=tk.Tk()
    application = CofACatchup(root=root, the_timestamp=ts_str,
                              in_directory_1=in_directory_1,
                              in_directory_2=in_directory_2,
                              the_watermark=watermark,
                              the_outbound_dir=outbound_directory)
    root.config()
    root.mainloop()
# }

# MAIN BOILERPLATE
if __name__ == "__main__":  # {
    # SETUP LOGGER
    setup_logger()
    main()
# }