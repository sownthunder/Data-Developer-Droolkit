"""
Edited on August 16, 2019 at 02:05 PM
FINALIZED on August 23 at 09:45 AM
Renamed "CofA_Daily_Watch" 2019/08/23

- cleaner cut program taken from "CofA_IGNORE_DIRS.py"
- begins running at 05:00 AM every day
- creates a DataFrame object throughout day for new files in F:/APPS/CofA/
- scans the directory of "F:/APPS/CofA/" and ignores 3 dirs
- creates a DataFrame object that is then exported to .CSV

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
from os.path import join, getsize
import subprocess, logging
from threading import Timer
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

###################################################################################################
# DEFINE CLASSES

class CofA_Event_Handler(FileSystemEventHandler): #{

    def __init__(self, save_dataframe, the_directory): #{
        self.save_dataframe = save_dataframe
        self.the_directory = the_directory
    #}

    def on_created(self, event): #{
        # RE_INSTANTIATE GLOBALS
        global df_save_list
        # TRY THE FOLLOWING
        try: #{
            # CREATE TIME STAMP
            ts = pd.Timestamp.now()
            # CREATE EVENT PATH VAR
            the_event_path = Path(event.src_path)
            # CREATE 'file_name' VAR
            file_name = os.path.basename(the_event_path)
            # CHECK AND SEE IF FILE IS OF TYPE .PDF
            if fnmatch.fnmatch(file_name, "*.pdf"): #{
                # CREATE NEW FILE NAME CONVENTION
                file_name_conv = generate_naming_convention(file_name)
                # CREATE EVENT ITEM FOR LIST
                event_list = [str(file_name), str(ts)]
                df_save_list = append_to_dataframe(the_event_list=event_list,
                                                   dataframe_to_append=df_save_list)
            #}
            else: #{
                print("NON-PDF CREATED AT " + str(ts))
            #}


###################################################################################################
# DEFINE FUNCTIONS



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
(1) LIST-type obj containing:
    - basename (CofA etc)[*.pdf]
    - timestamp
    - "Created" **OR** "Modified category"
(2) DataFrame obj containing:
    - that the newest row will be appended too
RETURNS: 
DataFrame (not in-place) with newly
appended tuple row etc 
"""
def append_to_dataframe(the_event_list, dataframe_to_append): #{
    # TRY THE FOLLOWING
    try: #{
        # CHECK IF LIST
        if type(the_event_list) is list: #{  # WAS: (the_event_list is list)
            print("\t\tLIST check == PASS")
            # SEPERATE COLUMNS
            col_1 = str(the_event_list[0])
            col_2 = str(the_event_list[1])
            #col_3 = str(the_event_list[2])
            # CREATE APPENDAGE FRAME
            df_appendage = pd.DataFrame(data=[the_event_list],
                                        columns=['CofA', 'Timestamp'])
            # CREATE INSTANCE OF DATAFRAME WE ARE RETURNING
            return_df = dataframe_to_append.append(df_appendage, ignore_index=True, sort=False)
            print(return_df.tail(5))
        #}
        else: #{
            print("\t\tLIST check == FAIL")
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
        print("\t\t[Append-2-DataFrame] FIN...")
        return return_df
    #}
    finally: #{
        # CREATE END-TIME VAR
        time_end = pd.Timestamp.now()
        # DETERMINE OVERALL RUN-TIME
        run_time = pd.Timedelta(time_end - time_start)
        # PRINT TOTAL RUNTIME
        print("\t\t[Append-2-DataFrame] >>> time_alloted: "+ str(run_time))
    #}
#}

#################################################

def end_script(): #{
    # RE-INSTANTIATE GLOBALS
    global save_list
    global df_save_list
    # EXPORT NEWLY CREATED CofAs THAT HAVE BEEN COLLECTED THROUGHOUT THE DAY

    # CALL SCAN_DIRECTORY FUNCTION TO CREATE .CSV FOR next-step-exe
    scan_directory("F:/APPS/CofA/")
#}

#################################################

def scan_directory(the_directory): #{
    # RE-INSTANTIATE GLOBALS
    global time_start, time_now
    global path_list
    global x
    in_directory = Path(the_directory)
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
        #OLD# df_paths.to_csv("C:\CofA\log\lists\CofA_Email_Node_List_"
        df_paths.to_csv("C:/data/outbound/CofA/CofA_Email_Node_List"
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
        print("[scan_directory()] SUCCESS! VERY NICE!")
    #}
    finally: #{
        time_end = pd.Timestamp.now()
        run_time = (time_end - time_start)
        print("[scan_directory()] FIN...")
        print(run_time)
    #}
#}

###################################################################################################
# MAIN FUNCTION CALL

if __name__ == "__main__": #{
    # [SETUP-LOGGER]
    try:  #{
        logging.basicConfig(level=logging.INFO,
                            filename="C:/data/outbound/CofA//CofA-Daily-Watch-"
                                     + str(pd.Timestamp.now())[:10] + ".log",
                            format='%(asctime)s:%(message)s',
                            datefmt='%Y-%d-%m-%H%M%S',
                            filemode='a')
    #}
    except:  #{
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
    else:  #{
        print("[Setup-Logger] SUCCESS! VERY NICE!")
    #}
    """
    finally:  #{
        time_end = pd.Timestamp.now()
        run_time = (time_end - time_start)
        print("[main()] FIN...")
        print(run_time)
    #}
    """
    # INSTANTIATE GLOBAL VARIABLES
    in_directory = "C:/Temp/F/APPS/CofA/"  # "F:/APPS/CofA/"
    df_save_list = pd.DataFrame(data=None, columns=['CofA', 'Timestamp'], dtype=None)
    time_start = pd.Timestamp.now()
    time_now = str(time_start)[:10]
    path_list = []  # create list to hold clean data yo
    save_list = []  # create list to hold NEW CofA files
    x = 0  # counter
    # CREATE TIMER VAR
    t = Timer(60, end_script)
    # START TIMER
    t.start()
    # CREATE INSTANCE OF CUSTOM EVENT HANDLER
    event_handler = CofA_Event_Handler(df_save_list, in_directory)
    observer = Observer()
    observer.schedule(event_handler=event_handler,
                      path=in_directory,
                      recursive=True)
    observer.start()
    try: #{
        while True: #{
            sleep(1)
        #}
    #}
    except KeyboardInterrupt: #{
        observer.stop()
    #}
    observer.join()
#}