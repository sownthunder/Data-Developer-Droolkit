
# IMPORT THE GOODS
import os, sys, time
from datetime import datetime
from time import sleep
from pathlib import Path
from os.path import join, getsize
import fnmatch, glob, shutil
from threading import Timer
import pandas as pd
import numpy as np
from pandas import Series, DataFrame
from PyPDF2 import PdfFileReader, PdfFileWriter

#################################################
# DEFINE FUNCTIONS

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
        print("FIN...")
    # }
    return
# }

########################

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

########################

"""
TAKES IN:
(1) file_path to file 
RETURNS: 
The create time or modified time, whichever is older
"""
def pull_creation_timestamp(a_file_path): #{
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
        date_str = str(datetime.fromtimestamp(ctime))
    # }
    # ELSE.... MODIFIED TIME IS OLDER...
    else:  # {
        # FORMAT DATE VAR as str
        date_str = str(datetime.fromtimestamp(mtime))
    # }
    # RETURN THE DATE WE PULLED AS STRING
    return date_str
#}

########################

"""
TAKES IN:
(1) FILE-PATH obj containing:
    - directory that needs to be scanned
(2) LIST-type obj containing:
    - list of STR (if any) of directories to skip/avoid
(3) LIST-type obj containing:
    - list of STR (more than one) of file type to return in scan
RETURNS:
DataFrame? of all scanned objects that might criteria etc
"""
def scan_directory(the_directory, ignore_dir_list, file_type_list): #{
    # RE-INSTANTIATE GLOBALS
    global out_file_dir, out_file_str
    # CREATE TIMESTAMP VARIABLE TO TRACK WHEN STARTED...
    time_start = pd.Timestamp.now()
    # CREATE LIST TO HOLD CLEAN DATA YO
    file_list = []
    # COUNTER
    x = 0
    # TRY THE FOLLOWING
    try: #{
        # VARIABLES
        scan_directory = Path(the_directory)
        # create list to hold clean data yp
        path_list = []
        # BEGIN << OS.WALK >>
        for root, dirs, files in os.walk(scan_directory):  # {
            #############################
            # DIRECTORY SKIP CONDITIONS #
            #############################
            # FOR EACH ITEM IN "ignore_dir_list":
            for item in ignore_dir_list:  # {
                if str(item) in dirs:  # {
                    dirs.remove(str(item))  # REMOVE THAT FROM OS.WALK
                # }
            # }
            # OTHERWISE IF THERE ARE FILES IN DIRECTORY
            for f in files:  # {
                ##############################
                # FILE MATCH-TYPE CONDITIONS #
                ##############################
                # FOR EACH ITEM IN "file_type_list":
                for item in file_type_list: #{
                    print("in list")
                #}
            #}
        #}
        # CREATE NEW DATAFRAME TO HOLD LIST
        df_filelist = pd.DataFrame(data=None, columns=["CofA File"], dtype=np.str)
        # ASSIGN LIST TO COLUMN IN DATAFRAME
        df_filelist[0] = file_list
        # EXPORT TO NECESSARY FOLDER
        export_path = os.path.join(out_file_dir, out_file_str)
        df_filelist.to_csv(export_path, index=False)
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
        print("SUCCESS ! VERY NICE!")
    #}
    finally: #{
        print("[G_SCAN] FIN...")
    #}
#}

########################

"""
def scan_directory(the_directory, ): #{
    # CREATE TIMESTAMP VARIABLE TO TRACK WHEN STARTED...
    time_start = pd.Timestamp.now()
    # CREATE LIST TO HOLD CLEAN DATA YO
    file_list = []
    # TRY THE FOLLOWING
    try: #{
        for root, dirs, files in os.walk(the_dir): #{
            # NO DIRECTORY SKIP CONDITIONS
"""


#################################################

if __name__ == "__main__":  #{
    # INSTANTIATE GLOBAL VARIABLES
    time_start = pd.Timestamp.now()
    # CREATE STR OF TODAYS DATE
    time_today = str(time_start)[:10]
    in_directory = "G:/C of A's/Agilent/"
    in_file = ""
    out_file_dir = "C:/data/outbound/CofA/"  # WAS: C:/data/inbound/"
    # CREATE FILE_NAME STR USING TODAYS DATE CONVENTION
    out_file_str = str("CofA_Email_Node_list_" + time_today + "_pull.csv")

#}