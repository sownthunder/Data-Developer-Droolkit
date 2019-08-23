"""
CofA_Monitor

Monitors the activity inside:
F:/APPS/CofA/
throughout the day creating a DF
until EOD is reached, when then
the DF is exported to a csv, and
the F:/APPS/CofA/ directory is
scanned and compared to the scan
of yesterday


"""

# IMPORT THE GOODS
#################################################
import os, sys, time
from time import sleep
from pathlib import Path
import fnmatch, glob, shutil
import wmi, psutil, subprocess
import tempfile, textwrap
from textwrap import wrap
from zipfile import ZipFile
import pandas as pd
import numpy as np
from pandas import Series, DataFrame
import email, smtplib, ssl
import os.path as op
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
import subprocess, threading, logging
from threading import Timer
from PyPDF2 import PdfFileReader, PdfFileWriter
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# GLOBAL VARIABLES
#################################################
in_file = "C:/data/inbound/Agilent_CofA_Letterhead_03-21-19.pdf"
in_directory = "C:/Temp/F/APPS/Cofa/"                               # F:/APPS/CofA/
out_directory = "C:/Temp/G/C of A's/#Email Node/"                   # G:/C of A's/#Email Node/
save_list = []
isEOD = False
time_start = pd.Timestamp.now()
df_save_list = pd.DataFrame()

# DEFINE CLASSES
#################################################
class CofA_Event_Handler(FileSystemEventHandler): #{

    def __init__(self, save_dataframe, in_directory, out_directory): #{
        self.save_dataframe = save_dataframe
        self.in_directory = in_directory
        self.out_directory = out_directory
    #}

    def on_created(self, event): #{
        global df_save_list
        # TRY THE FOLLOWING
        try:  # {
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            ts = pd.Timestamp.now()  # CREATE TIME STAMP
            print("| CREATED >>> " + str(ts))
            # CREATE EVENT PATH VAR
            the_event_path = Path(event.src_path)  # WAS: the_event_path
            # CREATE 'file_name' VAR
            file_name = os.path.basename(the_event_path)
            # CHECK AND SEE IF FILE IS OF TYPE .PDF
            if fnmatch.fnmatch(file_name, "*.pdf"):  # {
                # CREATE str TO HOLD FINAL COLUMN FOR TUPLE
                created_str = "Created"
                # CREATE EVENT LIST
                event_list = [str(file_name), str(ts), str(created_str)]
                df_save_list = append_to_dataframe(the_event_list=event_list,
                                                   dataframe_to_append=df_save_list)
            # }
            else:  # {
                print("NON-PDF CREATED AT " + str(ts))
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
            print("\n" + typeE +
                  "\n" + fileE +
                  "\n" + lineE +
                  "\n" + messageE)
        # }
        else:  # {
            print("\t [Created-Event] FIN..")
        # }
        finally:  # {
            # CREATE END-TIME VAR
            time_end = pd.Timestamp.now()
            # DETERMINE OVERALL RUN-TIME
            run_time = pd.Timedelta(time_end - time_start)
            # PRINT TOTAL RUNTIME
            print("\t [Created-Event] >>> time_alloted: " + str(run_time))
        # }
    #}

    def on_modified(self, event): #{
        global df_save_list
        # TRY THE FOLLOWING
        try:  # {
            # CREATE INDEX FROM CURRENT DATAFRAME
            idx = pd.Index(data=df_save_list['Basename'], dtype=np.str)
            # CREATE EVENT PATH VAR
            the_event_path = Path(event.src_path)
            # CREATE 'file_name' VAR
            file_name = os.path.basename(the_event_path)
            """
            # CREATE FILE NAME CONV GENERATOR
            file_name_conv = generate_naming_convention(str(event.src_path))
            """
            # IF **MODIFIED** SRC_PATH IS ALREADY IN THE DATAFRAME...
            print("\n\t CHECKING IF FILE ADDED IS ALREADY IN DATAFRAME..." + str(file_name))
            if idx.contains(file_name):  # {
                print(str(event.src_path) + " IS IN SAVE_DATAFRAME")
                # DONT ADD ANYTHING TO DATAFRAME
            # }
            # APPEND TO "df_save_list" WITH A MODIFIED TYPE
            else:  # {
                print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                ts = pd.Timestamp.now()  # CREATE TIME STAMP
                print("| MODIFIED >>> " + str(ts))
                # CREATE EVENT PATH VAR
                the_event_path = Path(event.src_path)  # WAS: the_event_path
                # CREATE 'file_name' VAR
                file_name = os.path.basename(the_event_path)
                # CHECK AND SEE IF FILE IS OF TYPE .PDF
                if fnmatch.fnmatch(file_name, "*.pdf"):  # {
                    # CREATE str TO HOLD FINAL COLUMN FOR TUPLE
                    modified_str = "Modified"
                    # CREATE EVENT LIST
                    event_list = [str(file_name), str(ts), str(modified_str)]
                    df_save_list = append_to_dataframe(the_event_list=event_list,
                                                       dataframe_to_append=df_save_list)
                # }
                else:  # {
                    print("NON-PDF CREATED AT " + str(ts))
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
            print("\n" + typeE +
                  "\n" + fileE +
                  "\n" + lineE +
                  "\n" + messageE)
        # }
        else:  # {
            print("\t [Modified-Event] VERY NICE GOOD JOB! ")
        # }
        finally:  # {
            # CREATE END-TIME VAR
            time_end = pd.Timestamp.now()
            # DETERMINE OVERALL RUN-TIME
            run_time = pd.Timedelta(time_end - time_start)
            # PRINT TOTAL RUNTIME
            print("\t [Modified-Event] >>> time_alloted: " + str(run_time))
        # }
    #}

    def on_deleted(self, event): #{
        ts = pd.Timestamp.now()
        print("DELETED : " + str(ts))
    #}
#}

# DEFINE FUNCTIONS
#################################################
"""
TAKES IN:
(1) path to pdf 
RETURNS: 
the STRING of that PDF to match the naming convention
in G:/C of A's/#Email Node/ from F:/APPS/CofA/
"""
def generate_naming_convention(the_pdf_path): #{
    # get/set filename to variable
    the_file_name = str(os.path.basename(the_pdf_path))
    # PERFORM STRING OPERATIONS
    #################################
    idx_mrk = the_file_name.rfind('@', 0, len(the_file_name))
    half1 = str(the_file_name[0:idx_mrk])
    half2 = str(the_file_name[idx_mrk + 1:len(the_file_name)])
    print("\t>>> HALF 1 == " + half1)
    print("\t>>> HALF 2 == " + half2)
    #  setup NEW FILE NAME (for copy)
    new_name = "part "
    new_name += str(half1)
    new_name += " CofA Lot# "
    new_name += str(half2)
    print("\t>>> NEW NAME == " + str(new_name))
    #################################
    return str(new_name)
#}

"""
TAKES IN: 
(1) LIST-type obj containing:
    - basename (*.pdf)
    - timestamp
    - "Created" **OR** "Modified category"
(2) DataFrame obj that the newest row will be appended too
RETURNS: DataFrame (not in-place) with newly
appended tuple row etc 
"""
def append_to_dataframe(the_event_list, dataframe_to_append): #{
    # TRY THE FOLLOWING
    try: #{
        # CHECK IF LIST
        if type(the_event_list) is list : #{  # WAS: (the_event_list is list)
            print("LIST check == PASS")
            # SEPERATE COLUMNS
            col_1 = str(the_event_list[0])
            col_2 = str(the_event_list[1])
            col_3 = str(the_event_list[2])
            # CREATE APPENDAGE FRAME
            df_appendage = pd.DataFrame(data=[the_event_list],
                                        columns=['Basename', 'Timestamp', 'Created/Modified'])
            # CREATE INSTANCE OF DATAFRAME WE ARE RETURNING
            return_df = dataframe_to_append.append(df_appendage, ignore_index=True, sort=False)
            print(return_df.tail(5))
        #}
        else: #{
            print("LIST check == FAIL")
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
        print("\t [Append-2-DataFrame] FIN...")
        return return_df
    #}
    finally: #{
        # CREATE END-TIME VAR
        time_end = pd.Timestamp.now()
        # DETERMINE OVERALL RUN-TIME
        run_time = pd.Timedelta(time_end - time_start)
        # PRINT TOTAL RUNTIME
        print("\t [Append-2-DataFrame] >>> time_alloted: "+ str(run_time))
    #}
#}

"""
TAKES IN:
(1) STR-type obj containing:
    - email address to send "from"
(2) STR-type obj containing:
    - email address to send "to"
(3) STR-type obj containing:
    - subject of email message
(4) STR-type obj containing:
    - contents of email message
(5) LIST-type obj containing:
    - list of files to send
"""
def send_mail(send_from, send_to, subject, message, files=[],
              server="cos.smtp.agilent.com", port=587, use_tls=True):  # {
    print("SENDING MAIL... " + str(pd.Timestamp.now()))
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
    return
# }