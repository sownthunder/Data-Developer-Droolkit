#!/usr/bin/env python
# coding: utf-8

# In[1]:


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


# In[2]:


#################################################################
# DEFINE FUNCTIONS

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


# In[3]:


#################################################
# MAIN BOILERPLATE


if __name__ == "__main__":  # {
    # START TIME
    time_start = pd.Timestamp.now()
    # CREATE STR FOR TODAYS DATE
    #[2019-09-04]... time_today = str(time_start)[:10]
    #[2019-09-05]... time_today = "2019-09-03"
    #[2019-09-05]... time_today = "2019-09-04"
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
    in_file = "C:/data/inbound/Agilent_CofA_Letterhead_03-21-19.pdf"
    in_directory = "C:/data/outbound/CofA/"
    out_directory = "G:/C of A's/#Email Node/"
    file_conv_list = []  # EMPTY LIST TO HOLD NEWLY CREATED FILES (name conv)
    file_time_list = []  # EMPTY LIST TO HOLD TIMESTAMPS OF NEWLY ABOVE ^^
    logging.info("TODAY == " + str(time_today))
    # SUBTRACTION DELTA
    subtraction_delta = pd.Timedelta(value=1, unit='days')
    logging.info("\t\n SUTBRACTING... " + str(subtraction_delta))
    # AND GET YESTERDAYS DATE BY SUBTRACTING
    time_yesterday = time_start - subtraction_delta
    # SETUP STRING
    #[2019-09-04]... yesterstr = str(time_yesterday.date())
    #[2019-09-05]... yesterstr = "2019-08-28"
    #[2019-09-05]... yesterstr = "2019-09-03"
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
    # SET DIFFERENCE OF TWO DATAFRAME FOR G_DRIVE IN PANDAS PYTHON
    g_set_diff_df = pd.concat([df4, df3, df3]).drop_duplicates(keep=False)
    logging.info("LENGTH OF G_DIFF_DF: " + str(len(g_set_diff_df)))
    logging.info(str(g_set_diff_df))
    logging.info("\n########################<>#########################\n")
    #################################################################
    # CREATE A COLUMN VARIABLE TO STORE DATA (file_names)
    fn_col = []
    # CREATE A COLUMN VARIABLE TO STORE DATA (timestamps)
    ts_col = []
    # CREATE A COLUMN VARIABLE TO STORE DATA (file_paths)
    path_col = []
    # GET TIME STAMPS / CREATE "FINAL" DATAFRAME FOR EACH DIRECTORY/DF
    # TRY THE FOLLOWING 
    try:  # {
        # COUNTER
        y = 0
        # CREATE SERIES FROM COLUMN
        f1 = pd.Series(data=f_set_diff_df['CofA File'], dtype=np.str)
        g1 = pd.Series(data=g_set_diff_df['CofA File'], dtype=np.str)
        # FOR EACH ROW IN THE COLUMN
        for row in f1:  # {
            # CREATE FILE PATH VAR
            the_file_path = os.path.join("F:/APPS/CofA/", str(row))#Path(row)
            logging.info("\nTHE FILE == " + str(the_file_path))
            file_name = os.path.basename(the_file_path)
            # CREATE FILE_NAME_CONV VARIABLE
            file_name_conv = generate_naming_convention(file_name)
            # APPEND FILE_NAME_CONV TO LIST/COLUMN
            fn_col.append(str(file_name_conv))
            logging.info("FILE NAME == " + str(file_name_conv))
            # APPEND FILE_PATH TO LIST/COLUMN
            path_col.append(str(the_file_path))
            # CREATE TIMESTAMP VARIABLE
            the_ts = pull_creation_timestamp(the_file_path)
            logging.info("THE TIME STAMP == " + str(the_ts))
            # APPEND TIMESTAMP TO LIST/COLUMN
            ts_col.append(str(the_ts))
            y += 1
        # }
        # FOR EACH ROW IN THE COLUMN
        for row in g1:  # {
            # CREATE FILE_PATH VAR
            the_file_path = os.path.join("G:/C of A's/Agilent/", row)#Path(row)
            logging.info("\nTHE FILE == " + str(the_file_path))
            file_name = os.path.basename(the_file_path)
            """ NOT USED FOR G DRIVE
            # CREATE FILE NAME CONV VARIABLE
            file_name_conv = generate_naming_convention(file_name)
            """
            # APPEND FILE_NAME TO LIST/COLUMN
            fn_col.append(str(file_name))
            logging.info("FILE NAME == " + str(file_name))
            # APPEND FILE_PATH TO LIST/COLUMN
            path_col.append(str(the_file_path))
            # CREATE TIMESTAMP VARIABLE
            the_ts = pull_creation_timestamp(the_file_path)
            logging.info("THE TIME STAMP == " + str(the_ts))
            # APPEND TIMESTAMP TO LIST/COLUMN
            ts_col.append(str(the_ts))
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
    ###########################
    # COMBINE BOTH DATAFRAMES #
    ###########################
    # SET_DIFF_DF (not export df)
    set_diff_df = pd.DataFrame(data=None, columns=None, dtype=np.str)
    set_diff_df['CofA File'] = path_col
    set_diff_df['Timestamp'] = ts_col
    set_diff_df.to_csv("set_diff_df.csv", index=False)
    # EXPORT DATAFRAME (the one we will email)
    export_df = pd.DataFrame(data=None, columns=None, dtype=np.str)
    export_df['CofA'] = fn_col
    export_df['Timestamp'] = ts_col
    export_df.to_csv("export_df.csv", index=False)
    ##############################################
    # ITERATE THRU TUPLES (using temp directory) #
    ##############################################
    # ITERATE THRU FIRST FRAME (F_DRIVE)
    # << WHILE INSIDE OF TEMP DIRECTORY
    with tempfile.TemporaryDirectory() as temporary_directory:  # {
        # COUNTER
        x = 0
        the_dir = Path(temporary_directory)
        logging.info("TEMPORARY DIRECTORY >>> " + str(the_dir))
        # ITERATE THRU DATAFRAME
        for row in set_diff_df.itertuples(index=False, name='CofA'):  # {
            logging.info("\n++++\t" + str(row[0]) + "\t++++\n")
            logging.info("\n\tDIR_NAME ==" + str(os.path.dirname(str(row[0]))) + "\n")
            # GET/CREATE FILE/BASE_NAME
            base_name = os.path.basename(str(row[0]))  # WAS: the_event_path
            # GET/CREATE OLD_PATH
            old_path = Path(str(row[0]))
            logging.info("OLD-PATH: \t" + str(old_path))
            file_name = os.path.basename(row[0])
            logging.info("FILE-NAME: \t" + str(file_name))
            # CREATE NEW FILE NAME CONV
            file_name_conv = generate_naming_convention(old_path)
            ############################################################
            """
            APPEND FILE NAME TO file_conv_list FOR exporting
            """
            file_conv_list.append(str(file_name_conv))
            """
            APPEND TIME STAMP TO file_time_list FOR exporting
            """
            # USE FUNCTION TO RETURN TIMESTAMP
            the_timestamp = pull_creation_timestamp(old_path)
            file_time_list.append(str(the_timestamp))  # WAS: str(row[1])
            #############################################################
            # CREATE NEW PATH VARIABLE TO CHECK IF FILE EXISTS....      #
            # ** ALSO DEPENDS ON WHAT THE OLD-DIRECTORY ORIGINALLY WAS !#
            #############################################################
            #new_path = os.path.join(out_directory, file_name_conv)
            # IF WE DO NEED FILE NAME CONVENTIONS....
            if str(os.path.dirname(str(row[0]))) == "F:\APPS\CofA": #{
                logging.info("needs convention name change")
                # CREATE 'temp_path'
                temp_path = os.path.join(the_dir, file_name_conv)
                # CREATE 'dst_path'
                dst_path = os.path.join(out_directory, file_name_conv)
            #}
            # ELSE THE FILE IS FROM "G:C of A's/Agilent/"...keep name
            else: #{
                # CREATE 'temp_path'
                temp_path = os.path.join(the_dir, base_name)
                # CREATE 'dst_path'
                dst_path = os.path.join(out_directory, base_name)
            #}
            #OLD# CREATE 'temp_path'
            #OLD# temp_path = os.path.join(the_dir, file_name_conv)
            #OLD# CREATE 'ds_path'
            #OLD# dst_path = os.path.join(out_directory, file_name_conv)
            """
            # WATERMARK A COPY TO G_DRIVE **WITH CORRECT NEW FILE NAME**
            create_watermark(input_pdf=str(row[0]),
                            output=dst_path, watermark=in_file)
            """
            logging.info("\n\t~~~~~~ <WATERMARK " 
                  + str(os.path.basename(row[0])) 
                  + "> ~~~~~~~~~~~~")
            logging.info("\t Create at==\n" + str(temp_path))
            logging.info("\t Copy to==" + str(dst_path))
            # WATERMARK A COPY INTO TEMP FOLDER **WITH CORRECT NEW FILE NAME**
            create_watermark(input_pdf=str(row[0]),
                             output=temp_path, watermark=in_file)
            # COPY FILE THAT IS IN TEMP FOLDER TO G_DRIVE
            shutil.copy2(src=temp_path, dst=dst_path)
            # INCREASE COUNTER
            x += 1
            logging.info("COUNT === " + str(x))
        #}
        # ZIP THE CURRENT TEMP FOLDER WE ARE INSIDE OF
        try: #{
            logging.info("\n\n\nXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
            logging.info("\nWORKING DIRECTORY ---BEFORE--- ZIP==\n" + str(os.getcwd()))
            # CHANGE WORKING DIRECTORY TO THE TEMPORARY DIR
            # (IN ORDER TO PROPERLY ZIP FILES/FOLDER)
            os.chdir(the_dir)   # WAS: "C:/"
            # path to folder (NOW currently the temp_folder)
            directory = "."  # the_dir
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
            logging.info("[Zip-Files] ALL FILES SUCCESSFULLY ZIPPED!")
        #}
        finally: #{
            ts = pd.Timestamp.now()
            run_time = ts - time_start
            logging.info("[Zip-Files] RUN TIME == " + str(run_time))
        #}
        # TRY AND FINISH THIS SHIT OFF (email this shit!)
        try: #{
            logging.info("\n\t\t\t GLOBBING FOR ZIP FILE !!!")
            logging.info(str(os.path.join(the_dir, "*.zip")))
            
            for name in sorted(glob.glob(str(the_dir) + "/*.zip")): #{
                logging.info("NAME OF FILE == "
                    + str(name))
                logging.info("LENGTH OF GLOB == "
                    + str(len(sorted(glob.glob(str(the_dir))))))
                # GET & SET PATH_NAME
                zip_path = Path(name)
                logging.info("ZIP_PATH == " + str(zip_path))
            #}
            #################################################################
            # CREATE EMPTY DATAFRAME WITH FILE NAME CONV NAMES & TIMESTAMPS #
            #################################################################
            file_conv_df = pd.DataFrame(data=None, columns=None)
            # SET ONE *NEW* COLUMN OF DATAFRAME TO LIST (file_name_conv)
            file_conv_df["CofA"] = file_conv_list
            # SET ANOTHER *NEW* COLUMN OF DATAFRAME TO LIST (timestamps)
            file_conv_df["Timestamp"] = file_time_list
            # CREATE STR FOR PATH OF SAVE_DIFF_DATAFRAME
            df_save_str = str("CofA-" + str(pd.Timestamp.now())[:10] + ".csv")
            df_save_path = os.path.join(the_dir, df_save_str)
            logging.info("\n\n\tSAVE-PATH FOR DATAFRAME == \n" + str(df_save_path))
            # CREATE THAT DATAFRAME IN THE PATH JUST CREATED 
            export_df.to_csv(df_save_path, index=False)
            # CREATE FILE_LIST VAR
            file_list = [str(zip_path), str(df_save_path)]
            file_str = ""
            for file_yo in file_list: #{
                file_str += str(file_yo + "\n") 
            #}
            logging.info(">>> FILE LIST :  \n\t" + str(file_str) + "\n")
            #####################################################
            # >>>>>>>>>>>>> SEND EMAIL HERE <<<<<<<<<<<<<<<<<<< #
            # >>>>>>>>>>>>> SEND EMAIL HERE <<<<<<<<<<<<<<<<<<< #
            #####################################################
            try: #{
                send_mail(send_from="derek.bates@non.agilent.com",
                            send_to=["derek.bates@non.agilent.com",
                                     "agilent_cofa@agilent.com"], 
                            subject=str(pd.Timestamp.now())[:10],
                            message="See File(s) attached",
                            files=file_list)
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
                logging.info("\n" + typeE +
                                "\n" + fileE +
                                "\n" + lineE +
                                "\n" + messageE)
            #}
            else: #{
                logging.info("[Email-Files] SUCCESS! VERY NICE!")
            #}
            finally: #{
                logging.info("[Email-Files] FIN...")
            #}
        #}
        except: #{
            errorMessage = str(sys.exc_info()[0]) + "\n\t\t"
            errorMessage = errorMessage + str(sys.exc_info()[1]) + "\n"
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
        #}
        else: #{
            logging.info("[Glob-Find-Email] SUCCESS! VERY NICE!")
        #}
        finally: #{
            ts = pd.Timestamp.now()
            run_time = ts - time_start
            logging.info("[Glob-Find-Email] FIN...")
        #}
    #}
    
#}

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