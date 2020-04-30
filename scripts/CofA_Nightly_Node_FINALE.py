# -*- coding: utf-8 -*-
"""
Created on Mon Dec 23 14:36:56 2019

CofA_Nightly_Node_FINALE

USES:
    CofA_Nightly_Node_v2.py


and ensures to check for "F:/APPS/G Drive/C of A's/Agilent/"
WAS: "G:/C of A's/Agilent/*" 
PROPER NAMING CONVENTION

-- 2020-04-06: edited for directory changes
-- 2020-04-30: edited for email changes

@author: derbates
"""

#!/usr/bin/env python
# coding: utf-8

# In[2]:


# IMPORT THE GOODS
import os, sys, time
from time import sleep
from datetime import datetime
from pathlib import Path
import fnmatch, glob, shutil
import pandas as pd
import numpy as np
from pandas import Series, DataFrame
import logging
import tempfile, subprocess
from PyPDF2 import PdfFileReader, PdfFileWriter
from zipfile import ZipFile
import email, smtplib, ssl
import os.path as op
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate


# In[3]:


#################################################################
# DEFINE FUNCTIONS

"""
TAKES IN:
(1) path to pdf 
RETURNS: 
the STRING of that PDF to match the naming convention
in F:/APPS/G Drive/C of A's/#Email Node/ from F:/APPS/CofA/
## in G:/C of A's/#Email Node/ from F:/APPS/CofA/
"""
def generate_naming_convention(the_pdf_path): #{
    # get/set filename to variable
    the_file_name = str(os.path.basename(the_pdf_path))
    # PERFORM STRING OPERATIONS
    #################################
    idx_mrk = the_file_name.rfind('@', 0, len(the_file_name))
    half1 = str(the_file_name[0:idx_mrk])
    half2 = str(the_file_name[idx_mrk + 1:len(the_file_name)])
    logging.info("\t\t[*************************]")
    logging.info("\t\t|>>> HALF 1 == " + half1)
    logging.info("\t\t|>>> HALF 2 == " + half2)
    #  setup NEW FILE NAME (for copy)
    new_name = "part "
    new_name += str(half1)
    new_name += " CofA Lot# "
    new_name += str(half2)
    logging.info("\t\t|>>> NEW NAME == " + str(new_name))
    logging.info("\t\t[*************************]")
    #################################
    return str(new_name)
#}

#################################################


"""
TAKES IN:
PDF TO WATERMARK,
"""
def create_watermark(input_pdf, output, watermark): # {
    try:  # {
        watermark_obj = PdfFileReader(watermark)
        watermark_page = watermark_obj.getPage(0)

        pdf_reader = PdfFileReader(input_pdf)
        pdf_writer = PdfFileWriter()

        # Watermark all the pages
        for page in range(pdf_reader.getNumPages()):  # {
            page = pdf_reader.getPage(page)
            page.mergePage(watermark_page)
            pdf_writer.addPage(page)
        # }

        with open(output, 'wb') as out:  # {
            pdf_writer.write(out)
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
    else: # {
        logging.info("\t\t[watermark-pdf] FIN...")
    # }
    finally: # {
        # CREATE END-TIME VAR
        time_end = pd.Timestamp.now()
        # DETERMINE OVERALL RUN-TIME
        run_time = pd.Timedelta(time_end - time_start)
        # PRINT TOTAL RUNTIME
        logging.info("\t\t[watermark-pdf] >>> time_alloted: " + str(run_time))
    # }
    return
# }

#################################################


def get_all_file_paths(directory):  # {

    # initializing empty file paths list
    file_paths = []

    # crawling through directory and subdirectories
    for root, directories, files in os.walk(directory):  # {
        for filename in files:  # {
            # join the two strings in order to form the full filepath.
            filepath = os.path.join(root, filename)
            file_paths.append(filepath)
        # }
    # }

    # returning all file paths
    return file_paths
# }

#################################################


def send_mail(send_from, send_to, subject, message, files=[],
              server="cos.smtp.agilent.com", port=587, use_tls=True):  # {
    print("SENDING MAIL... DATE == " + str(pd.Timestamp.now())[:10])
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

#################################################

"""
TAKES IN:
(1) file_path to file 
(2) integer to determine WHICH DIRECTION:
[XXX-123@XXXXXXXXXX.pdf <or> part XXX-123 CofA Lot# XXXXXXXXXX.pdf]
RETURNS: 
The create time or modified time, whichever is older
"""
def pull_creation_timestamp(a_file_path):  # {
    # TRY THE FOLLOWING:
    try: #{
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
        logging.error("\n" + typeE +
              "\n" + fileE +
              "\n" + lineE +
              "\n" + messageE)
    #}
    else:  # {
        logging.info("[pull_creation_timestamp] SUCCESS! VERY NICE!")
        # RETURN THE DATE WE PULLED AS STRING
        return date_str
    #}
    finally:  # {
        logging.info("[pull_creation_timestamp] FIN...")
    #}
# }

#################################################


# In[4]:


def zip_the_directory(directory_to_zip): #{
    # RE-INSTANTIATE GLOBALS
    global og_wd
    # TRY THE FOLLOWING
    try: #{
        logging.info("\n\n\nXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
        logging.info("\nWORKING DIRECTORY ---BEFORE--- ZIP==\n" + str(os.getcwd()))
        # CHANGE WORKING DIRECTORY TO DIRECTORY WE WISH TO ZIP
        os.chdir(directory_to_zip)
        # path to folder (NOW currently folder we want to zip)
        directory = "."
        logging.info("\nWORKING DIRECTORY ---DURING--- ZIP==\n" + str(os.getcwd()))
        # calling function to get all file paths in the directory
        file_paths = get_all_file_paths(directory)
        # printing the list of all files to be zipped 
        logging.info('\nFollowing files will be zipped:') 
        for file_name in file_paths: #{
            logging.info(file_name) 
        #}
        # writing files to a zipfile 
        with ZipFile('CofA-' 
                     + str(pd.Timestamp.now())[:10] 
                     + ".zip",'w') as zip: #{
            # writing each file one by one 
            for file in file_paths: #{
                zip.write(file) 
            #}
        #}
        logging.info('All files zipped successfully!\n\nXXXXXXXXXXXXXXXXXXXXXXXXX' 
                     + 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX\n')
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
        logging.error("\n" + typeE +
                      "\n" + fileE +
                      "\n" + lineE +
                      "\n" + messageE)
    #}
    else: #{
        logging.info("[Zip-Files-" + str(directory_to_zip) + "] SUCCESS! VERY NICE!")
    #}
    finally: #{
        # CHANGE WORKING DIRECTORY BACK TO ORIGINAL
        os.chdir(og_wd)
    #}
#}


# In[ ]:


#################################################
# MAIN BOILERPLATE


if __name__ == "__main__":  # {
    # START TIME
    time_start = pd.Timestamp.now()
    # CREATE STR FOR TODAYS DATE
    #[2019-09-04]... time_today = str(time_start)[:10]
    #[2019-09-05]... time_today = "2019-09-03"
    #[2019-09-05]... time_today = "2019-09-04"
    #[2019-09-05]... time_today = str(time_start)[:10]
    #[2019-09-11]... time_today = "2019-09-05"
    #[2019-09-11]... time_today = "2019-09-10"
    #[2019-09-12]... time_today = "2019-09-11"
    time_today = str(time_start)[:10]
    #############################################
    # SETUP-LOGGER
    try:  # {
        logging.basicConfig(level=logging.INFO,
                            filename="C:/data/outbound/CofA_Nightly_Node_"
                                     + str(time_today)
                                     + ".log",
                            format='%(asctime)s-%(message)s',
                            datefmt='%Y-%m-%d-%H%M%S',
                            filemode='a')
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
        logging.info("\n" + typeE +
              "\n" + fileE +
              "\n" + lineE +
              "\n" + messageE)
    # }
    else:  # {
        logging.info("[setup-Logger] SUCCESS! VERY NICE!")
    # }
    finally: #{
        logging.info("[setup-Logger] FIN....")
    # }
    #############################################
    # INSTANTIATE GLOBAL VARIABLES
    og_wd = os.getcwd() # GET/SET ORIGINAL WORKING DIRECTORY
    in_file = "C:/data/inbound/Agilent_CofA_Letterhead_03-21-19.pdf"
    in_directory = "C:/data/outbound/CofA/"
    out_directory = "F:/APPS/G Drive/C of A's/#Email Node/"
    # [2020-04-06]\\out_directory = "G:/C of A's/#Email Node/"
    f_file_conv_list = []  # EMPTY LIST TO HOLD NEWLY CREATED FILES (name conv)
    f_file_time_list = []  # EMPTY LIST TO HOLD TIMESTAMPS OF NEWLY ABOVE ^^
    #####################
    g_file_conv_list = []  # same as above but for G_DRIVE
    g_file_time_list = []
    logging.info("TODAY == " + str(time_today))
    # SUBTRACTION DELTA
    subtraction_delta = pd.Timedelta(value=1, unit='days')
    logging.info("\t\n SUTBRACTING... " + str(subtraction_delta))
    # AND GET YESTERDAYS DATE BY SUBTRACTING
    time_yesterday = time_start - subtraction_delta
    # SETUP STRING
    # [2019-09-04]... yesterstr = str(time_yesterday.date())
    # [2019-09-05]... yesterstr = "2019-08-28"
    # [2019-09-05]... yesterstr = "2019-09-03"
    # [2019-09-05]... yesterstr = str(time_yesterday.date())
    # [2019-09-11]... yesterstr = "2019-09-04"
    # [2019-09-11]... yesterstr = "2019-09-09"
    # [2019-09-12]... yesterstr = "2019-09-10"
    yesterstr = str(time_yesterday.date())
    logging.info("YESTERDAY == " 
          + str(yesterstr))
    logging.info("\nTEST F_GLOB-STRING == " 
          + str("C:/data/outbound/CofA/*_" + yesterstr + "_F_*"))
    logging.info("\nTEST G_GLOB_STRING == " 
          + str("C:/data/outbound/CofA/*_" + yesterstr + "_G_"))
    logging.info("\n\t\t GLOBBING DIR F >>> ")  # str(os.listdir(in_directory))
    f_globber = os.listdir(in_directory)
    for globski in f_globber: #{
        logging.info(globski)
    #}
    #########################################################################
    # GLOB & PRELIMINARY SETUPS:
    glob_f_previous = sorted(glob.glob("C:/data/outbound/CofA/*_" 
                                       + yesterstr 
                                       + "_F_*"))
    logging.info("\n\t GLOB_F_PREVIOUS >>> \n")
    for name in glob_f_previous: #{
        logging.info(name)
    #}
    glob_f_current = sorted(glob.glob("C:/data/outbound/CofA/*_" 
                                      + time_today 
                                      + "_F_*"))
    logging.info("\n\t GLOB_F_CURRENT >>> \n")
    for name in glob_f_current: #{
        logging.info(name)
    #}
    glob_g_previous = sorted(glob.glob("C:/data/outbound/CofA/*_" 
                                       + yesterstr 
                                       + "_G_*"))
    logging.info("\n\t GLOB_G_PREVIOUS >>> \n")
    for name in glob_g_previous: #{
        logging.info(name)
    #}
    glob_g_current = sorted(glob.glob("C:/data/outbound/CofA/*_" 
                                      + time_today 
                                      + "_G_*"))
    logging.info("\n\t GLOB_G_CURRENT >>> \n")
    for name in glob_g_current: #{
        logging.info(name)
    #}
    #################
    # SETUP IMPORTS #
    #################
    # set as first element in returned list
    df1 = pd.read_csv(glob_f_previous[0])
    # set as first element in returned list
    df2 = pd.read_csv(glob_f_current[0])
    # set as first element in returned list
    df3 = pd.read_csv(glob_g_previous[0])
    # set as first element in returned list
    df4 = pd.read_csv(glob_g_current[0])
    logging.info("LEN_D1 == " + str(len(df1)))
    logging.info("LEN_D2 == " + str(len(df2)))
    logging.info("LEN_D3 == " + str(len(df3)))
    logging.info("LEN_D4 == " + str(len(df4)))
    # SET DIFFERENCE OF TWO DATAFRAMES FOR F_DRIVE IN PANDAS PYTHON
    f_set_diff_df = pd.concat([df2, df1, df1]).drop_duplicates(keep=False)
    logging.info("LENGTH OF F_DIFF_DF: " + str(len(f_set_diff_df)))
    logging.info(str(f_set_diff_df))
    f_set_diff_df.to_csv("f_set_diff_df-" + str(pd.Timestamp.now())[:10] + ".csv", index=False)
    # SET DIFFERENCE OF TWO DATAFRAME FOR G_DRIVE IN PANDAS PYTHON
    g_set_diff_df = pd.concat([df4, df3, df3]).drop_duplicates(keep=False)
    logging.info("LENGTH OF G_DIFF_DF: " + str(len(g_set_diff_df)))
    logging.info(str(g_set_diff_df))
    g_set_diff_df.to_csv("g_set_diff_df-" + str(pd.Timestamp.now())[:10] + ".csv", index=False)
    logging.info("\n########################<>#########################\n")
    ###################################################################
    # [2019-09-09] ADD IN FAIL-SAFE IF THERE WERE NO COFAS CREATED TODAY
    # [2019-09-18] REMOVED CHECK FROM THIS SECITON
    """
    if (len(f_set_diff_df) == 0) & (len(g_set_diff_df) == 0):  # {
        logging.info("NO COFAS CREATED TODAY... EXCITING AND EXIT!")
        sys.exit(88)
    # }
    """
    # CREATE A COLUMN VARIABLE TO STORE DATA (file_names) [F_DRIVE]
    f_fn_col = []
    # CREATE A COLUMN VARIABLE TO STORE DATA (timestamps) [F_DRIVE]
    f_ts_col = []
    # CREATE A COLUMN VARIABLE TO STORE DATA (file_paths) [F_DRIVE]
    f_path_col = []
    ############################
    # CREATE A COLUMN VARIABLE TO STORE DATA (file_names) [G_DRIVE]
    g_fn_col = []
    # CREATE A COLUMN VARIABLE TO STORE DATA (timestamps) [G_DRIVE]
    g_ts_col = []
    # CREATE A COLUMN VARIABLE TO STORE DATA (file_paths) [G_DIRVE]
    g_path_col = []
    ############################
    # TRAVERSE BOTH DATAFRAMES #
    ############################
    # CREATE SERIESES FROM COLUMN
    f1 = pd.Series(data=f_set_diff_df['CofA File'], dtype=np.str)
    g1 = pd.Series(data=g_set_diff_df['CofA File'], dtype=np.str)
    ####################################################################
    # GET TIME STAMPS / CREATE "FINAL" DATAFRAME FOR EACH DIRECTORY/DF #
    ####################################################################
    # TRY THE FOLLOWING 
    try:  # {
        # COUNTER
        y = 0
        
        # FOR EACH ROW IN THE COLUMN
        for row in f1:  # {
            # CREATE FILE PATH VAR
            the_file_path = os.path.join("F:/APPS/CofA/", str(row))#Path(row)
            logging.info("\nTHE FILE == " + str(the_file_path))
            file_name = os.path.basename(the_file_path)
            # CREATE FILE_NAME_CONV VARIABLE
            file_name_conv = generate_naming_convention(file_name)
            # APPEND FILE_NAME_CONV TO LIST/COLUMN
            f_fn_col.append(str(file_name_conv))
            logging.info("FILE NAME == " + str(file_name_conv))
            # APPEND FILE_PATH TO LIST/COLUMN
            f_path_col.append(str(the_file_path))
            # CREATE TIMESTAMP VARIABLE
            the_ts = pull_creation_timestamp(the_file_path)
            logging.info("THE TIME STAMP == " + str(the_ts))
            # APPEND TIMESTAMP TO LIST/COLUMN
            f_ts_col.append(str(the_ts))
            y += 1
        # }
        # FOR EACH ROW IN THE COLUMN
        for row in g1:  # {
            # CREATE FILE_PATH VAR
            the_file_path = os.path.join("F:/APPS/G Drive/C of A's/Agilent/", row)
            # [2020-04-06]\\the_file_path = os.path.join("G:/C of A's/Agilent/", row)#Path(row)
            logging.info("\nTHE FILE == " + str(the_file_path))
            file_name = os.path.basename(the_file_path)
            """ NOT USED FOR G DRIVE
            # CREATE FILE NAME CONV VARIABLE
            file_name_conv = generate_naming_convention(file_name)
            """
            # APPEND FILE_NAME TO LIST/COLUMN
            g_fn_col.append(str(file_name))
            logging.info("FILE NAME == " + str(file_name))
            # APPEND FILE_PATH TO LIST/COLUMN
            g_path_col.append(str(the_file_path))
            # CREATE TIMESTAMP VARIABLE
            the_ts = pull_creation_timestamp(the_file_path)
            logging.info("THE TIME STAMP == " + str(the_ts))
            # APPEND TIMESTAMP TO LIST/COLUMN
            g_ts_col.append(str(the_ts))
            y += 1
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
        logging.info("{Timestamp-Filename-Table} SUCCESS! VERY NICE!")
    # }
    finally:  # {
        logging.info("{Timestamp-Filename-Table} FIN...")
    # }
    # TRY THE FOLLOWING:
    try: #{
        ##############################
        # CREATE SEPERATE DATAFRAMES #
        ##############################
        # SET_DIFF_DFS (the ones we will NOT be emailling)
        f_paths_df = pd.DataFrame(data=None, columns=None, dtype=np.str)
        f_paths_df['CofA File'] = f_path_col
        f_paths_df['Timestamp'] = f_ts_col
        g_paths_df = pd.DataFrame(data=None, columns=None, dtype=np.str)
        g_paths_df['CofA File'] = g_path_col
        g_paths_df['Timestamp'] = g_ts_col
        # EXPORT (for meow)
        f_paths_df.to_csv("f_paths_df_" + str(pd.Timestamp.now())[:10] + ".csv", index=False)
        g_paths_df.to_csv("g_paths_df_" + str(pd.Timestamp.now())[:10] + ".csv", index=False)
        # EXPORT DATAFRAMES (the ones we will email)
        f_export_df = pd.DataFrame(data=None, columns=None, dtype=np.str)
        f_export_df['CofA'] = f_fn_col
        f_export_df['Timestamp'] = f_ts_col
        g_export_df = pd.DataFrame(data=None, columns=None, dtype=np.str)
        g_export_df['CofA'] = g_fn_col
        g_export_df['Timestamp'] = g_ts_col
        # EXPORT (for meow)
        f_export_df.to_csv("f_export_df_" + str(pd.Timestamp.now())[:10] + ".csv", index=False)
        g_export_df.to_csv("g_export_df_" + str(pd.Timestamp.now())[:10] + ".csv", index=False)
        ###########################
        # [2019-09-11]... break_input = input("DO YOU WANT TO CONTINUE Y/N?")
        # [2019-09-11]... break_input = input("DO YOU WANT TO CONTINUE Y/N?")
        ###########################
        # COMBINE BOTH DATAFRAMES #
        ###########################
        """
        # SET_DIFF_DF (the one we will NOT be emailling)
        set_diff_df = pd.DataFrame(data=None, columns=None, dtype=np.str)
        set_diff_df['CofA File'] = path_col
        set_diff_df['Timestamp'] = ts_col
        #[2019-09-06]... set_diff_df.to_csv("set_diff_df.csv", index=False)
        # EXPORT DATAFRAME (the one we will email)
        export_df = pd.DataFrame(data=None, columns=None, dtype=np.str)
        export_df['CofA'] = fn_col
        export_df['Timestamp'] = ts_col
        """
        # [2019-09-11]... converted from one dataframe traversal to TWO
        # [2019-09-18]... ADDED check to make sure only FULL zips are created/sent
        #####################################################################
        # F_DRIVE #
        #####################################################################
        # ONLY IF THE LEN IS GREATER THAN ZERO
        if len(f_set_diff_df) > 0:  # {
            # ZIP AND SEND EMAIL
            with tempfile.TemporaryDirectory() as temporary_directory:  # {
                # COUNTER
                x1 = 0
                the_dir = Path(temporary_directory)
                logging.info("TEMPORARY DIRECTORY >>> " + str(the_dir))
                # ITERATE THRU DATAFRAME
                for row in f_paths_df.itertuples(index=False, name='F_DRIVE'):  # {
                    logging.info("\n++++\t" + str(row[0]) + "\t++++\n")
                    logging.info("\n\tDIR_NAME ==" + str(os.path.dirname(str(row[0]))) + "\n")
                    # GET/CREATE OLD_PATH
                    old_path = Path(str(row[0]))
                    logging.info("OLD-PATH: \t" + str(old_path))
                    # GET/CREATE FILE/BASE_NAME
                    file_name = os.path.basename(row[0])
                    logging.info("FILE-NAME: \t" + str(file_name))
                    # CREATE NEW FILE NAME CONV
                    file_name_conv = generate_naming_convention(old_path)
                    ############################################################
                    """
                    APPEND FILE NAME TO f_file_conv_list FOR exporting
                    """
                    f_file_conv_list.append(str(file_name_conv))
                    """
                    APPEND TIME STAMP TO f_file_time_list FOR exporting
                    """
                    # USE FUNCTION TO RETURN TIMESTAMP
                    the_timestamp = pull_creation_timestamp(old_path)
                    f_file_time_list.append(str(the_timestamp))  # WAS: str(row[1])
                    ############################################################
                    # CREATE 'temp_path'
                    temp_path = os.path.join(the_dir, file_name_conv)
                    # CREATE 'dst_path'
                    dst_path = os.path.join(out_directory, file_name_conv)
                    logging.info("\n\t~~~~~~ <WATERMARK "
                                 + str(os.path.basename(row[0]))
                                 + "> ~~~~~~~~~~~~")
                    logging.info("\t Create at==\n" + str(temp_path))
                    logging.info("\t Copy to==" + str(dst_path))
                    # WATERMARK A COPY INTO TEMP FOLDER **WITH CORRECT NEW FILE NAME**
                    create_watermark(input_pdf=str(row[0]),
                                     output=temp_path, watermark=in_file)
                    # COPY FILE THAT IS IN TEMP FOLDER TO F_DRIVE
                    shutil.copy2(src=temp_path, dst=dst_path)
                    # GET METADATA OF OLD ORIGINAL FILE
                    old_stinfo = os.stat(old_path)
                    logging.info("OLD FILE STATS: \n" + str(old_stinfo))
                    old_atime = old_stinfo.st_atime
                    logging.info("OLD FILE A-TIME: \n" + str(old_atime))
                    old_mtime = old_stinfo.st_mtime
                    logging.info("OLD FILE M-TIME: \n" + str(old_mtime))
                    # CHANGE METADATA OF COPIED FILE TO ORIGINAL
                    os.utime(dst_path, (old_atime, old_mtime))
                    # INCREASE COUNTER
                    x1 += 1
                    logging.info("COUNT === " + str(x1))
                # }
                # ZIP THE DIRECTORY
                zip_the_directory(directory_to_zip=the_dir)
                # TRY AND FINISH THIS SHIT OFF (email this shit!)
                logging.info("\n\t\t\t GLOBBING FOR ZIP FILE !!!")
                logging.info(str(os.path.join(the_dir, "*.zip")))
                for name in sorted(glob.glob(str(the_dir) + "/*.zip")):  # {
                    logging.info("NAME OF FILE == "
                                 + str(name))
                    logging.info(len(sorted(glob.glob(str(the_dir)))))
                    # GET & SET PATH_NAME
                    zip_path = Path(name)
                    logging.info("ZIP_PATH == " + str(zip_path))
                # }
                #################################################################
                # CREATE EMPTY DATAFRAME WITH FILE NAME CONV NAMES & TIMESTAMPS #
                #################################################################
                f_file_conv_df = pd.DataFrame(data=None, columns=None)
                # SET ONE *NEW* COLUMN OF DATAFRAME TO LIST (f_file_name_conv)
                f_file_conv_df["CofA"] = f_file_conv_list
                # SET ANOTHER *NEW* COLUMN OF DATAFRAME TO LIST (f_timestamps)
                f_file_conv_df["Timestamp"] = f_file_time_list
                # CREATE STR FOR PATH OF F_SAVE_DIFF_DATAFRAME
                f_df_save_str = str("CofA-" + str(pd.Timestamp.now())[:10] + ".csv")
                f_df_save_path = os.path.join(the_dir, f_df_save_str)
                logging.info("\n\n\tSAVE-PATH FOR DATAFRAME == \n" + str(f_df_save_path))
                # CREATE THAT DATAFRAME IN THE PATH JUST CREATED
                f_export_df.to_csv(f_df_save_path, index=False)
                # CREATE FILE LIST VAR
                f_file_list = [str(zip_path), str(f_df_save_path)]
                f_file_str = ""
                for f_file_yo in f_file_list:  # {
                    f_file_str += str(f_file_yo + "\n")
                # }
                logging.info(">>> F-FILE LIST :  \n\t" + str(f_file_str) + "\n")
                #####################################################
                # >>>>>>>>>>>>> SEND EMAIL HERE <<<<<<<<<<<<<<<<<<< #
                # [2019-09-12]... agilent_cofa@agilent.com
                # [2019-09-23]... removed penny & diluka from email
                # [2020-04-30]... removed myself :( ... goodbye
                send_mail(send_from="michael.labreche@agilent.com",
                          send_to=["agilent_cofa@agilent.com",
                                   "michael.labreche@agilent.com"],
                          subject=str(time_today) + "-F-APPS-CofAs-List",
                          message="See File(s) attached. \n Taken from: \n" + str(Path("F:/APPS/CofAs/")),
                          files=f_file_list)
                # >>>>>>>>>>>>> SEND EMAIL HERE <<<<<<<<<<<<<<<<<<< #
                #####################################################

            # }
        # }
        else:  # {
            logging.warning("NO COFAS FOR F:/APPS/COFA/")
        # }
        ####################################################################
        # G_DRIVE #
        ####################################################################
        # ONLY IF LENGTH IS GREATER THAN ZERO
        if len(g_set_diff_df) > 0:  # {
            # ZIP AND SEND EMAIL
            with tempfile.TemporaryDirectory() as temporary_directory:  # {
                # COUNTER
                x2 = 0
                the_dir = Path(temporary_directory)
                logging.info("TEMPORARY DIRECTORY >>> " + str(the_dir))
                # ITERATE THRU DATAFRAME
                for row in g_paths_df.itertuples(index=False, name='G_DRIVE'):  # {
                    logging.info("\n++++\t" + str(row[0]) + "\t++++\n")
                    logging.info("\n\tDIR_NAME == " + str(row[0]) + "\t++++\n")
                    # GET/CREATE OLD_PATH
                    old_path = Path(str(row[0]))
                    logging.info("OLD_PATH: \t" + str(old_path))
                    # GET/CREATE FILE/BASE_NAME
                    file_name = os.path.basename(row[0])
                    logging.info("FILE-NAME: \t" + str(file_name))
                    # NO NEED TO CREATE FILE NAME CONVENTION, so we set as og
                    file_name_conv = file_name
                    ######################################################
                    """
                    APPEND FILE NAME TO g_file_conv_list FOR exporting
                    """
                    g_file_conv_list.append(str(file_name_conv))
                    """
                    APPEND TIME STAMP TO file_time_list FOR exporting
                    """
                    # USE FUNCTION TO RETURN TIMESTAMP
                    the_timestamp = pull_creation_timestamp(old_path)
                    g_file_time_list.append(str(the_timestamp))  # WAS: str(row[1])
                    ############################################################
                    # CREATE 'temp_path'
                    temp_path = os.path.join(the_dir, file_name_conv)
                    # CREATE 'dst_path'
                    dst_path = os.path.join(out_directory, file_name_conv)
                    # COPY A COPY INTO TEMP FOLDER **WITH CORRECT NEW FILE NAME**
                    shutil.copy2(src=str(row[0]), dst=temp_path)
                    # COPY FILE THAT IS IN TEMP FOLDER TO G_DRIVE
                    shutil.copy2(src=temp_path, dst=dst_path)
                    # INCREASE COUNTER
                    x2 += 1
                    logging.info("COUNT === " + str(x2))
                # }
                # ZIP THE DIRECTORY
                zip_the_directory(directory_to_zip=the_dir)
                # TRY AND FINISH THIS SHIT OFF (email this shit!)
                logging.info("\n\t\t\t GLOBBING FOR ZIP FILE !!!")
                logging.info(str(os.path.join(the_dir, "*.zip")))
                for name in sorted(glob.glob(str(the_dir) + "/*.zip")):  # {
                    logging.info("NAME OF FILE == "
                                 + str(name))
                    logging.info(len(sorted(glob.glob(str(the_dir)))))
                    # GET & SET PATH_NAME
                    zip_path = Path(name)
                    logging.info("ZIP_PATH == " + str(zip_path))
                # }
                #################################################################
                # CREATE EMPTY DATAFRAME WITH FILE NAME CONV NAMES & TIMESTAMPS #
                #################################################################
                g_file_conv_df = pd.DataFrame(data=None, columns=None)
                # SET ONE *NEW* COLUMN OF DATAFRAME TO LIST (g_file_name_conv)
                g_file_conv_df["CofA"] = g_file_conv_list
                # SET ANOTHER *NEW* COLUMN OF DATAFRAME TO LIST (g_timestamps)
                g_file_conv_df["Timestamps"] = g_file_time_list
                # CREATE STR FOR PATH OF G_SAVE_DIFF_DATAFRAME
                g_df_save_str = str("CofA-" + str(pd.Timestamp.now())[:10] + ".csv")
                g_df_save_path = os.path.join(the_dir, g_df_save_str)
                logging.info("\n\n\tSAVE-PATH FOR DATAFRAME == \n" + str(g_df_save_path))
                # CREATE THAT DATAFRAME IN THE PATH JUST CREATED
                g_export_df.to_csv(g_df_save_path, index=False)
                # CREATE FILE LIST VAR
                g_file_list = [str(zip_path), str(g_df_save_path)]
                g_file_str = ""
                for g_file_yo in g_file_list:  # {
                    g_file_str += str(g_file_yo + "\n")
                # }
                logging.info(">>> G-FILE- LIST :  \n\t" + str(g_file_str) + "\n")
                #####################################################
                # >>>>>>>>>>>>> SEND EMAIL HERE <<<<<<<<<<<<<<<<<<< #
                # [2019-09-12]... agilent_cofa@agilent.com
                # [2019-09-23]... removed penny & diluka from email
                send_mail(send_from="derek.bates@non.agilent.com",
                          send_to=["agilent_cofa@agilent.com",
                                   "derek.bates@non.agilent.com"],
                          subject=str(time_today) + "-G-CofA's-Agilent-List",
                          message="See File(s) attached. \n Taken from: \n" + str(Path("F:/APPS/G Drive/C of A's/Agilent/")),
                          # [2020-04-06]\\message="See File(s) attached. \n Taken from: \n" + str(Path("G:/C of A's/Agilent/")),
                          files=g_file_list)
                # >>>>>>>>>>>>> SEND EMAIL HERE <<<<<<<<<<<<<<<<<<< #
                #####################################################
            # }
        # }
        else:  # {
            logging.warning("NO COFAS FOR F:/APPS/G DRIVE/C OF A'S/AGILENT/")
            # [2020-04-06]\\logging.warning("NO COFAS FOR G:/C OF A'S/AGILENT/")
        # }
        # [2019-09-06]... export_df.to_csv("export_df.csv", index=False)
        ##############################################
        # ITERATE THRU TUPLES (using temp directory) #
        ##############################################
        # ITERATE THRU FIRST FRAME (F_DRIVE)
    # }
    except PermissionError:  # {
        pass
    # }
    else:  # {
        print("[CofA_Nightly_Node_v2] done...")
    # }
# }

"""
##############################################
# CHECK IF NEW FILE ALREADY EXISTS......
if os.path.exists(new_path) is True: #{
print("FILE EXISTS! NO NEED TO CREATE WATERMARKED PDF !")
# BUT WE STILL NEED TO COPY THAT NEW PDF INTO TEMP FOLDER
# CREATE TEMP PATH TO DO THAT...
temp_path = os.path.join(the_dir, file_name_conv)
shutil.copy2(new_path, temp_path)
#}
# IF IT DOES NOT EXIST... CREATE WATERMARK PDF in G_DRIVE AND TEMP_DRIVE
# OFF OF METADATA (os.stats()) ACQUIRED FROM F_DRIVE
else: #{
print("FILE DOES NOT EXIST!!! CREATING WATERMARK")
# CREATE PATH VARIABLE FOR og file SO WE CAN GET METADATA
test_stat = os.stat(old_path)
print(str(test_stat[8]))
# WATERMARK A COPY TO G_DRIVE *WITH CORRECT FILE NAME*
create_watermark(input_pdf=str(row[0]),
output=new_path, watermark=in_file)
#}
"""

"""
NEED:
(1) old_path = (F:/APPS/CofA/ or (G:/C of A's/Agilent/)
(2) new_path/dst_path = (G:/C of A's/#Email Node/) 
(3) temp_path =  (C:/Users/derbates/AppData/Temp/...)
(4) file_name_conv (part XXXXX CofA Lot # XXXXXXXXXX)
STEPS:
(A) check if a "create_watermark() version" exists for EVERY item
(B) IF IT DOES EXIST:   copy that file into the temp directory
(C) IF IT *DOES NOT* EXIST:     call "create_watermark()" into BOTH temp_dir 
and other
*** SO THAT BOTH VERSIONS NOW DO EXIST ***
"""