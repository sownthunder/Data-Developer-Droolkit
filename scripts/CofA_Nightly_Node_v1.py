"""
RUNS EVERY NIGHT AT ~ 9:01 PM

GLOBS in two files (todays and yesterdays)
<< INSIDE DIRECTORY: C:/data/outbound/CofA/ >>
of      SCAN OF F;/APPS/CofA/
then using tempfolders watermarks, pdfs & moves
to      DIR OF G:/C of A's/#Email Node/

*** AS WELL AS ***

creates a dir in C:/ drive with todays date
then copes all the same files THAT WERE JUST MOVED
TO G:/C of A's/#Email Node/ TO THE new folder in C:/

the folder is zipped, and then emailed, and then deleted

"""

###################################################################################################
# IMPORT THE GOODS
import os, sys, time
from time import sleep
from pathlib import Path
import fnmatch, glob, shutil
import pandas as pd
import numpy as np
from pandas import Series, DataFrame
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


#########################################################################################################
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
    print("\t\t[*************************]")
    print("\t\t|>>> HALF 1 == " + half1)
    print("\t\t|>>> HALF 2 == " + half2)
    #  setup NEW FILE NAME (for copy)
    new_name = "part "
    new_name += str(half1)
    new_name += " CofA Lot# "
    new_name += str(half2)
    print("\t\t|>>> NEW NAME == " + str(new_name))
    print("\t\t[*************************]")
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
        print("\n" + typeE +
              "\n" + fileE +
              "\n" + lineE +
              "\n" + messageE)
        # }
    else: # {
        print("\t\t[watermark-pdf] FIN...")
    # }
    finally: # {
        # CREATE END-TIME VAR
        time_end = pd.Timestamp.now()
        # DETERMINE OVERALL RUN-TIME
        run_time = pd.Timedelta(time_end - time_start)
        # PRINT TOTAL RUNTIME
        print("\t\t[watermark-pdf] >>> time_alloted: " + str(run_time))
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


def create_diff_dataframe(previous_df, current_df): #{
    print("difference here")
#}

###################################################################################################
# MAIN BOILERPLATE


if __name__ == "__main__":  # {
    # INSTANTIATE GLOBAL VARIABLES
    in_file = ""

    time_start = pd.Timestamp.now()
    # CREATE TODAYS DATE
    time_today = str(time_start)[:10]
    in_directory = "C:/data/outbound/CofA/"
    print("TODAY == " + str(time_today))
    # SUBTRACTION DELTA
    subtraction_delta = pd.Timedelta(value=1, unit='days')
    print("\t\n SUTBRACTING... " + str(subtraction_delta))
    # AND GET YESTERDAYS DATE
    time_yesterday = time_start - subtraction_delta
    # SETUP STRING
    yesterstr = str(time_yesterday.date())
    print("YESTERDAY == " + str(yesterstr))
    print("\n\t\t GLOBBING DIR >>> " + str(os.listdir(in_directory)))
    # GLOB & PRELIMINARY SETUPS:
    df_previous = glob.glob("*" + yesterstr + "*")
    print(df_previous)
    df_current = glob.glob("*" + time_today + "*")
    # IMPORT AS DATAFRAMES
    # set as first element in returned list
    df1 = pd.read_csv(df_previous[0])
    # set as first element in returned list
    df2 = pd.read_csv(df_current[0])
    # SET DIFFERENCE OF TWO DATAFRAMES IN PANDAS PYTHON
    set_diff_df = pd.concat([df2, df1, df1]).drop_duplicates(keep=False)
    print("LENGTH OF DIFF_DF: " + str(len(set_diff_df)))
    print(set_diff_df)
    # ITERATE THRU TUPLES (using temp directory)
    # << WHILE INSIDE OF TEMP DIRECTORY
    with tempfile.TemporaryDirectory() as temporary_directory:  # {
        # COUNTER
        x = 0
        the_dir = Path(temporary_directory)
        print("TEMPORARY DIRECTORY >>> " + str(the_dir))
        # ITERATE THRU DATAFRAME
        for row in set_diff_df.itertuples(index=False, name='CofA'): #{
            test = 0
            """
            NEED:
            (1) old_path = (F:/APPS/CofA/ or (G:/C of A's/Agilent/)
            (2) new_path = (G:/C of A's/#Email Node/) 
            (3) temp_path =  (C:/Users/derbates/AppData/Temp/...)
            (4) file_name_conv (part XXXXX CofA Lot # XXXXXXXXXX)
            STEPS:
            (A) check if a "create_watermark() version" exists for EVERY item
            (B) IF IT DOES EXIST:   copy that file into the temp directory
            (C) IF IT *DOES NOT* EXIST:     call "create_watermark()" into BOTH temp_dir and other
            *** SO THAT BOTH VERSIONS NOW DO EXIST ***
            """
        #}