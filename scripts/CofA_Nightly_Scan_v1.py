"""
Finalized on August 16, 2019 at 02:05 PM

- cleaner cut program taken from "CofA_IGNORE_DIRS.py"
- scans the directory of "F:/APPS/CofA/" and ignores 3 dirs
- creates a DATAFRAME object that is then exported to .CSV

"""

# IMPORT THE GOODS
import os, sys, time
from time import sleep
from pathlib import Path
import fnmatch, glob, shutil
import pandas as pd
import numpy as np
from pandas import Series, DataFrame
from os.path import join, getsize
import logging

# INSTANTIATE GLOBAL VARIABLES
in_directory = "F:/APPS/CofA/"
time_start = pd.Timestamp.now()
time_now = str(time_start)[:10]

# create list to hold clean data yo
path_list = []

# counter
x = 0

# [SETUP-LOGGER]
try: #{
    logging.basicConfig(level=logging.INFO,
                        filename="C:/CofA/log/lists/CofA-List-Counts.log",
                        format='%(asctime)s:%(message)s',
                        datefmt='%Y-%d-%m-%H%M%S',
                        filemode='a')
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
    print("[Setup-Logger] SUCCESS! VERY NICE!")
#}
finally: #{
    time_end = pd.Timestamp.now()
    run_time = (time_end - time_start)
    print("[main()] FIN...")
    print(run_time)
#}

def main(): #{
    # GLOBAL VAR REFERENCES
    global in_directory
    global time_start, time_now
    global path_list
    global x
    # TRY THE FOLLOWING
    try: #{
        for root, dirs, files in os.walk(in_directory):  # {
            # DIRECTORY SKIP CONDITIONS
            if 'Archive ERR' in dirs:  # {
                dirs.remove('Archive ERR')  # don't visit Archive ERR directories
            # }
            if 'Archive - For all archived CofA, see G CofA folder' in dirs:  # {
                dirs.remove('Archive - For all archived CofA, see G CofA folder')  # skip
            # }
            if 'Instruction Sheets' in dirs:  # {
                dirs.remove('Instruction Sheets')  # skip
            # }
            # OTHERWISE IF THERE ARE FILES IN DIRECTORY
            for f in files:  # {
                # IF FILE IS OF TYPE .pdf
                if fnmatch.fnmatch(f, "*.pdf"):  # {
                    # ASSEMBLE!
                    file_path = os.path.join(root, f)
                    """
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
                    """
                    path_list.append(file_path)
                    x += 1
                # }
                else:  # {
                    print("NOT A PDF : \t" + str(f))
                # }
            # }
        # }
        # CREATE NEW DATAFRAME TO HOLD LIST
        df_paths = pd.DataFrame()
        # ASSIGN LIST TO COLUMN IN DATAFRAME
        df_paths['CofA File'] = path_list
        df_paths.to_csv("C:\CofA\log\lists\CofA_Email_Node_List_"
                        + time_now
                        + "_pull.csv",
                        index=False)
        print("\n COUNT == " + str(x))
        logging.info("COUNT == " + str(x))
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
        print("[main()] SUCCESS! VERY NICE!")
    #}
    finally: #{
        time_end = pd.Timestamp.now()
        run_time = (time_end - time_start)
        print("[main()] FIN...")
        print(run_time)
    #}
#}

if __name__ == "__main__": #{
    main()
#}