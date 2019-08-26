
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
(1) path-object to the directory to be scanned
RETURNS:
hard-coded file conditions
"""
def scan_directory(the_dir): #{
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
        for root, dirs, files in os.walk(the_dir): #{
            # DIRECTORY SKIP CONDITIONS
            if 'Archive ERR' in dirs: #{
                # REMOVE AND DON'T VISIT IN WALK
                dirs.remove('Archive ERR')
            #}
            if 'Archive - For all archived CofA, see G CofA folder' in dirs: #{
                # REMOVE AND DON't VISIT IN WALK
                dirs.remove('Archive - For all archived CofA, see G CofA folder')
            #}
            if 'Instruction Sheets' in dirs: #{
                dirs.remove('Instruction Sheets')
            #}
            # OTHERWISE IF THERE ARE FILES IN DIRECTORY
            for f in files: #{
                # IF FILE IS OF TYPE .pdf
                if fnmatch.fnmatch(f, "*.pdf"): #{
                    # ASSEMBLE!
                    file_path = os.path.join(root, f)
                    # GET CREATE TIME
                    create_time = os.path.getctime(file_path)
                    # GET MODIFIED TIME
                    mod_time = os.path.getmtime(file_path)
                    # MAKE 'ctime' INTO DATETIME / more readable
                    readable_c = datetime.datetime.fromtimestamp(create_time).isoformat()
                    # MAKE 'mtime' INTO DATETIME / more readable
                    readable_m = datetime.datetime.fromtimestamp(mod_time).isoformat()
                    # CONVERT TO pandas.Timestamp
                    timeStamp_c = pd.Timestamp(readable_c)
                    # AGAIN FOR MODIFIED TIME
                    timeStamp_m = pd.Timestamp(readable_m)
                    # APPEND TO FILE_LIST
                    file_list.append(file_path)
                    # INCREMENT COUNTER
                    x += 1
                #}
                else: #{
                    print("NOT A PDF : \t" + str(f))
                #}
            #}
        #}
        # CREATE NEW DATAFRAME TO HOLD LIST
        df_filelist = pd.DataFrame(data=None, columns=["CofA File"], dtype=np.str)
        # ASSIGN LIST TO COLUMN IN DATAFRAME
        df_filelist[0] = file_list
        # EXPORT TO NECCESSARY FOLDER
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
        print("[F_SCAN] FIN...")
    #}
#}



#################################################

if __name__ == "__main__": #{
    # INSTANTIATE GLOBAL VARIABLES
    time_start = pd.Timestamp.now()
    # CREATE STR OF TODAYS DATE
    time_today = str(time_start)[:10]
    in_directory = "F:/APPS/CofA/"
    in_file = ""
    out_file_dir = "C:/data/outbound/CofA/"  # WAS: "C:/data/inbound/"
    # CREATE FILE_NAME STR USING TODAYS DATE CONVENTION
    out_file_str = str("CofA_Email_Node_list_" + time_today + "_pull.csv")


#}