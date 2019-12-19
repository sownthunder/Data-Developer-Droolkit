#!/usr/bin/env python
# coding: utf-8

# ### *insert date as `str` for the `END-DATE` of file creation*

# ### *insert date as `str` for the `START-DATE` of file creation*

# ---
# 
# loop thru `F:/APPS/CofA/` *as well as* `G:/C of A's/Agilent/` 
# 
# and pull each file creation stamp 
# 
# (code taken from "**CofA_Email_Node-LOOP-CHANGING-DATES**")

# In[1]:


import os, sys, time
from time import sleep
from datetime import datetime
from pathlib import Path
import pandas as pd
import numpy as np
from pandas import Series, DataFrame
import fnmatch, glob, shutil
import platform, logging
from zipfile import ZipFile

from docx import Document
from docx.shared import Inches
from docx.shared import Pt

from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.style import WD_STYLE_TYPE
# In[2]:


from PyPDF2 import PdfFileWriter, PdfFileReader


# ### *SETUP-LOGGER*

# In[3]:


# SETUP LOGGER
try: #{
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s:%(message)s',
                        datefmt='%Y-%m-%d-%H%M%S',
                        filemode='a'
                       )
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
    logging.info("[setup-logger] SUCCESS! VERY NICE!")
#}
finally: #{
    logging.info("[Setup-logger] FIN...")
#}


# ---

# ### *DEFINE FUNCTIONS*

# In[4]:


"""
TAKES IN:
(1) file_path to file 
RETURNS: 
The create time or modified time, whichever is older
"""
def pull_creation_timestamp(a_file_path):  # {
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
        logging.info("SUCCESS! VERY NICE!")
        # RETURN THE DATE WE PULLED AS STRING
        return date_time
    #}
    finally:  # {
        logging.info("[pull_creation_timestamp] FIN...")
    #}
# }


# In[5]:


def extract_information(pdf_path): #{
    with open(pdf_path, 'rb') as f: #{
        pdf = PdfFileReader(f)
        information = pdf.getDocumentInfo()
        number_of_pages = pdf.getNumPages()
    #}
    txt = f"""
    Information about {pdf_path}:
    
    Author: {information.author}
    Creator: {information.creator}
    Producer: {information.producer}
    Subject: {information.subject}
    Title: {information.title}
    Number of Pages: {number_of_pages}
    """
    
    logging.info(txt)
    return information
#}


# In[6]:


def creation_date(path_to_file): #{
    """
    Try to get the date that a file was created, falling back to when it was
    last modified if that isn't possible.
    """
    if platform.system() == 'Windows': #{
        return os.path.getctime(path_to_file)
    #}
    else: #{
        stat = os.stat(path_to_file)
        try: #{
            return stat.st_birthtime
        #}
        except AttributeError: #{
            # We're probably on Linux. No easy way to get creation dates here,
            # so we'll settle for when its content was last modified.
            return stat.st_mtime
        #}
    #}
    return 
#}


# In[7]:


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
    logging.debug("\t\t[*************************]")
    logging.debug("\t\t|>>> HALF 1 == " + half1)
    logging.debug("\t\t|>>> HALF 2 == " + half2)
    #  setup NEW FILE NAME (for copy)
    new_name = "part "
    new_name += str(half1)
    new_name += " CofA Lot# "
    new_name += str(half2)
    logging.info("\t\t|>>> NEW NAME == " + str(new_name))
    logging.debug("\t\t[*************************]")
    #################################
    return str(new_name)
#}


# In[8]:


def create_watermark(input_pdf, output, watermark): #{
    try: #{
        watermark_obj = PdfFileReader(watermark)
        watermark_page = watermark_obj.getPage(0)
        
        pdf_reader = PdfFileReader(input_pdf)
        pdf_writer = PdfFileWriter()
        
        # Watermark all the pages
        for page in range(pdf_reader.getNumPages()): #{
            page = pdf_reader.getPage(page)
            page.mergePage(watermark_page)
            pdf_writer.addPage(page)
        #}
        
        with open(output, 'wb') as out: #{
            pdf_writer.write(out)
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
        logging.error("\n" + typeE +
              "\n" + fileE +
              "\n" + lineE +
              "\n" + messageE)
    #}
    else: #{
        logging.debug("[Watermark-PDF] FIN...")
    #}
    return
#}


# In[9]:


def get_all_file_paths(directory): #{
    
    # initializing empty file paths list
    file_paths = []
    
    # crawling through directory and subdirectories
    for root, directories, files in os.walk(directory): #{
        for filename in files: #{
            # join the two strings in order to form the full filepath
            filepath = os.path.join(root, filename)
            file_paths.append(filepath)
        #}
    #}
    
    # returning all file paths
    return file_paths

#}


# In[10]:


def dir_traverse(the_directory, ignore_dir_list, file_type_list): #{
    # RE-INSTANTIATE GLOBALS
    global date_check, end_check
    global file_list, file_name_conv_list, ts_list, time_start
    global zip_dir_path, zip_dir_path_2
    # COUNTER
    x = 0 # number of PDFS matched
    count = 0 # total number of files
    # TRY THE FOLLOWING
    try: #{
        # SETUP VARIABLES
        scan_directory = Path(the_directory)
        # BEGIN OS.WALK
        for root, dirs, files in os.walk(scan_directory): #{
            # FOR EACH ITEM IN IGNORE LIST...
            for item in ignore_dir_list: #{
                # IF THAT ITEM IS IN FACT IN DIRECTORY...
                if str(item) in dirs: #{
                    # REMOVE FROM OS.WALK
                    dirs.remove(str(item))
                #}
            #}
            # OTHERWISE IF THERE ARE FILES IN DIRECTORY
            for f in files: #{
                # FOR EACH ITEM IN 'file_type_list'
                for item in file_type_list: #{
                    # CREATE FILE_MATCH VAR
                    file_match = str("*" + item)
                    # DO FNMATCH FOR THIS "item"
                    if fnmatch.fnmatch(f, file_match): #{
                        # <<< STRING OPERATIONS >>>
                        ###############################################
                        # ASSEMBLE!
                        file_path = os.path.join(root, f)
                        logging.info("\n\tFILE_PATH == " + str(file_path))
                        # RETURN DATETIME VAR 
                        test_date = pull_creation_timestamp(file_path)
                        logging.info("\n\tTEST_DATE == " + str(test_date))
                        # CONVERT TO pandas.Timestamp
                        timestamp = pd.Timestamp(test_date)  # WAS: readable_ts
                        # COMPARE TO CHECK_DATE VARIABLE
                        check_delta = pd.Timedelta(timestamp - date_check)
                        logging.debug("\n\tDELTA == " + str(check_delta))
                        # COMPARE TO CHECK_END_DATE VARIABLE
                        end_delta = pd.Timedelta(timestamp - end_check)
                        logging.debug("\n\tEND_DELTA ==" + str(end_delta))
                        # IF CHECK DELTA IS POSITIVE ** and END_DELTA is NEGATIVE
                        #(test_date occurred AFTER date_check)
                        if check_delta.days >= 0: #{
                            logging.info("\tCREATED AFTER " + str(time_start))
                            # IF END_DELTA IS NEGATIVE
                            if end_delta.days <=0: #{
                                logging.info("\tCREATED BEFORE " + str(end_check))
                                x += 1 # increase PDF-count
                                # CREATE FILE_NAME VARIABLE
                                file_name = os.path.basename(file_path)
                                # CREATE DIR NAME VARIABLE
                                dir_name = os.path.dirname(file_path)
                                # CHECK WHICH DIRECTORY WE ARE IN AND WHETHER OR NOT TO MAKE FILE_NAME_CONV
                                if str(os.path.dirname(file_path)) == "F:\APPS\CofA": #{
                                    # CREATE NEW NAMING CONVENTION
                                    file_name_conv = generate_naming_convention(file_name)
                                    # CREATE VARIABLE FOR (new) zip PATH
                                    new_path = os.path.join(zip_dir_path, file_name_conv)
                                    # CREATE VARIABLE FOR (new) non-zip PATH
                                    newer_path = os.path.join(outbound_directory, file_name_conv)
                                    # CREATE WATERMARK/COPY IN FOLDER TO BE ZIPPED
                                    create_watermark(input_pdf=file_path,
                                                     output=new_path,
                                                     watermark=watermark)
                                    # COPY TO OUTBOUND_DIRECTORY
                                    shutil.copy2(src=new_path, dst=newer_path)
                                    # GET METADATA OF OLD ORIGINAL FILE
                                    old_stinfo = os.stat(file_path)
                                    logging.info("OLD FILE STATS: \n" + str(old_stinfo))
                                    old_atime = old_stinfo.st_atime
                                    logging.info("OLD FILE A-TIME: \n" + str(old_atime))
                                    old_mtime = old_stinfo.st_mtime
                                    logging.info("OLD FILE M-TIME: \n" + str(old_mtime))
                                    # CHANGE METADATA OF COPIED FILE TO ORIGINAL
                                    os.utime(newer_path, (old_atime, old_mtime))
                                    # APPEND TO FILE LIST
                                    file_list.append(file_name_conv)
                                    # APPEND TO DIR LIST
                                    dir_list.append(dir_name)
                                    # APPEND TO TIMESTAMP_LIST
                                    ts_list.append(test_date)
                                #}
                                # ELSE... we are in "G:/C of A's/Agilent/" 
                                else: #{
                                    # CREATE VARIABLE FOR (new) zip PATH
                                    new_path = os.path.join(zip_dir_path_2, file_name)
                                    # CREATE VARIABLE FOR (new) non-zip PATH
                                    newer_path = os.path.join(outbound_directory, file_name)
                                    # COPY FILE TO FOLDER TO BE ZIPPED (no watermark)
                                    shutil.copy2(src=file_path, dst=new_path)
                                    """
                                    # CREATE WATERMARK/COPY IN FOLDER TO BE ZIPPED
                                    create_watermark(input_pdf=file_path,
                                                     output=new_path,
                                                     watermark=watermark)
                                    """
                                    # COPY TO OUTBOUND_DIRECTORY
                                    shutil.copy2(src=file_path, dst=newer_path)
                                    # APPEND TO FILE LIST
                                    file_list.append(file_name)
                                    # APPEND TO DIR LIST
                                    dir_list.append(dir_name)
                                    # APPEND TO TIMESTAMP_LIST
                                    ts_list.append(test_date)
                                #}
                                """
                                # APPEND TO FILE LIST
                                file_list.append(file_path)
                                # APPEND TO TIMESTAMP_LIST
                                ts_list.append(test_date)
                                """
                            #}
                            else: #{
                                logging.info("CREATED AFTER " + str(end_check))
                            #}
                        #}
                        else: #{
                            logging.info("CREATED BEFORE " + str(time_start))
                        #}
                    #}
                    else: #{
                        logging.debug("NOT A PDF : \t" + str(f))
                    #}
                    count += 1
                    logging.info("\nTOTAL # of PDFS : " + str(x))
                    logging.info("TOTAL # OF FILES : " + str(count))
                #}
            #}
        #}
        """
        # CREATE NEW DATAFRAME TO HOLD LIST
        df_filelist = pd.DataFrame(data=None, columns=None, dtype=np.str)
        # ASSIGN LIST TO COLUMN IN DATAFRAME
        df_filelist['CofA'] = file_list
        # EXPORT TO NECESSARY FOLDER
        export_path = os.path.join()
        """
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
        print("SUCCESS! VERY NICE!")
    #}
    finally: #{
        print("FIN...")
    #}
#}


# ## `BEGIN DIRECTORY TRAVERSAL`

# #### *DEFINE GLOBAL VARIABLES*

# In[11]:


# CREATE TIME STAMP FOR ZIP FOLDER
ts = pd.Timestamp.now()
ts_str = str(ts)[:10]
watermark = "C:/data/inbound/Agilent_CofA_Letterhead_03-21-19.pdf"
in_directory_1 = "F:/APPS/CofA/"
in_directory_2 = "G:/C of A's/Agilent/"
out_directory = "C:/data/outbound/CofA/"
outbound_directory = "G:/C of A's/#Email Node/"
zip_dir_path = os.path.join(out_directory, ts_str)
zip_dir_path_2 = zip_dir_path + "_2"
# if 'zip_folder' DOES NOT YET EXIST!
if not os.path.exists(zip_dir_path): #{
    # MAKE IT EXIST!
    os.makedirs(zip_dir_path)
#}
if not os.path.exists(zip_dir_path_2): #{
    # MAKE IT EXIST!
    os.makedirs(zip_dir_path_2)
#}
# RESET/RE-ESTABLISH 'out_directory'
#out_directory = Path(zip_dir_path)


# In[12]:


if __name__ == "__main__": #{
    # TAKE INPUT AND SET AS START TIME
    time_start = str(input("input start-date str..."))
    # TAKE INPUT AND SET AS END TIME
    time_end = str(input("input end-date str..."))
    # CREATE TIME STAMP VAR for filter requirements
    date_check = pd.Timestamp(time_start)
    logging.info("CHECK-DATE: \n" + str(date_check))
    logging.info(str(type(date_check)))
    end_check = pd.Timestamp(time_end)
    logging.info("CHECK-END-DATE: \n" + str(end_check))
    logging.debug(str(type(end_check)))
    # INSTANTIATE GLOBAL VARIABLES
    ignore_list = ['Archive ERR', 
                   'Archive - For all archived CofA, see G CofA folder', 
                   'Instruction Sheets']
    file_list = [] # LIST TO HOLD ALL PATHS FOR FILES (F_DRIVE)
    file_name_conv_list = [] # LIST HOLD ALL PATHS FOR NEW FILE NAME CONVENTIONS
    dir_list = [] # LIST TO HOLD ALL DIRECTORY NAMES
    ts_list = [] # LIST TO HOLD ALL TIMESTAMPS
    # CALL TRAVERSE FUNCTION ON (F:/APPS/CofA/) DIRECTORY
    dir_traverse(in_directory_1, ignore_list, [".pdf"])
    # CALL TRAVERSE FUNCTION ON (G:/C of A's/Agilent/) DIRECTORY
    dir_traverse(in_directory_2, [], [".pdf"])
    ##############################################################
    # CREATE DATAFRAME OF NEWLY CREATED COFA's AND ZIP AND EMAIL!
    df_filelist = pd.DataFrame(data=None, columns=None, dtype=np.str)
    # ASSIGN LIST TO COLUMN IN DATAFRAME
    df_filelist['CofA'] = file_list
    # ASSIGN LIST TO COLUMN IN DATAFRAME
    df_filelist['Directory'] = dir_list
    # ASSIGN TIMESTAMP TO COLUMN IN DATAFRAME
    df_filelist['Timestamp'] = ts_list
    # EXPORT TO PATH OF FOLDER WE ARE GOING TO ZIP (zip_dir_path)
    export_path = os.path.join(zip_dir_path, "CofA-" 
                               + str(pd.Timestamp.now())[:10] 
                               + ".csv")
    logging.info(export_path)
    df_filelist.to_csv(export_path, index=False)
#}


# In[13]:


logging.info(len(file_list))
for name in file_list: #{
    logging.info(name)
#}


# In[ ]:




