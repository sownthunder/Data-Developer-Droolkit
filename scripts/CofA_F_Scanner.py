"""
BEGINS RUNNING AT 5 AM
WHILE:
    SCANNING:   F:/APPS/CofA/
    INTO:       G:/C of A's/#Email Node/
RUNS FOR 14 HOURS UNTIL 9 PM
THEN:
    EXPORTS DATAFRME OF ALL 
    NEW CREATED FILES THAT
    WERE MADE THROUGHOUT DAY
"""


################################################################################
# IMPORT THE GOODS
################################################################################
import os, sys, time
from datetime import datetime
from time import sleep
from pathlib import Path
from os.path import join, getsize
import fnmatch, glob, shutil
from threading import Timer
import textwrap, logging
import pandas as pd
import numpy as np
from pandas import Series, DataFrame
from PyPDF2 import PdfFileReader, PdfFileWriter
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

################################################################################
# DEFINE CLASSES
################################################################################


class CofA_Event_Handler(FileSystemEventHandler):  # {

    def __init__(self, save_dataframe, out_directory, observer):  # {

        self.save_dataframe = save_dataframe
        self.out_directory = out_directory
        self.observer = observer

    # }

    def dispatch(self, event):  # {
        # RE-INSTANTIATE GLOBALS
        global isEOD
        # TRY THE FOLLOWING:
        try:  # {
            # CHECK IF END OF DAY HAS ARRIVED
            if isEOD is True:  # {
                # STOP OBSERVER
                self.observer.stop()
                print("TRUE! ENDING SCRIPT!")
                sys.exit(0)
            # }
            else:  # {
                print("FALSE! \n STILL RUNNING AT "
                      + str(pd.Timestamp.now())
                      + "\n")
            # }
            #OLD# output_str = "EVENT >> " + str(event.event_type)  # + "\n"
            #OLD# output_str += str("IS_DIR >> " + str(event.is_directory))  # + "\n"
            #OLD# output_str += str("SRC_PATH >> " + str(event.src_path))  # + "\n"
            """
            x_out = wrap(output_str, 30)
            logging.info(x_out)
            logging.info(textwrap.fill(output_str,
                initial_indent="",
                subsequent_indent="   " * 5,
                width=60))  # was 65
            """
            #OLD# event_str = str(event.event_type)
            #OLD# event_path = Path(event.src_path)
            #OLD# perform_on_event(the_event_type=event_str, the_event_path=event_path)
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
            error_output = str("\n" + typeE + "\n" + fileE + "\n" + lineE + "\n" + messageE)
            print(error_output)
        # }
        else:  # {
            print("SUCCESS! VERY NICE!")
        # }
        finally:  # {
            print("[Dispatch] FIN...")
    # }

    def on_created(self, event):  # {
        # RE-INSTANTIATE GLOBALS
        global isEOD
        # TRY THE FOLlOWING:
        try:  # {
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            ts = pd.Timestamp.now()  # CREATE TIME STAMP
            print("| CREATED >>> " + str(ts))
            # CREATE EVENT PATH VAR
            the_event_path = Path(event.src_path)  # WAS: the_event_path
            # CREATE 'file_name' VAR
            file_name = os.path.basename(the_event_path)
            # CHECK AND SEE IF FILE IS OF TYPE .PDF
            if fnmatch.fnmatch(file_name, "*.pdf"): #{
                # CREATE NEW FILE NAME CONV
                file_name_conv = generate_naming_convention(file_name)
                # CREATE EVENT ITEM FOR LIST
                event_list = [str(file_name_conv), str(ts)]  # WAS: (created_str)
                # APPEND TO DATAFRAME
                self.save_dataframe = append_to_dataframe(the_event_list=event_list,
                                                          dataframe_to_append=self.save_dataframe)
                # PRINT DATAFRAME
                print(self.save_dataframe)
                # CREATE PATH VARIABLES FOR FILE MOVING PROCEDURES
                new_path = os.path.join(self.out_directory, file_name_conv)
                # CREATE/COPY WATERMARK TO DESTINATION FOLDER
                create_watermark(input_pdf=the_event_path,
                                 output=new_path,
                                 watermark=in_file)
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
            print("SUCCESS! VERY NICE!")
        # }
        finally:  # {
            # CREATE END-TIME VAR
            time_end = pd.Timestamp.now()
            # DETERMINE OVERALL RUN-TIME
            run_time = pd.Timedelta(time_end - time_start)
            # PRINT TOTAL RUNTIME
            print("\t\t[Created-Event] >>> time_alloted: " + str(run_time))
        # }
    # }

    def on_modified(self, event):  # {
        # RE-INSTANTIATE GLOBALS
        global isEOD
        # TRY THE FOLLOWING
        try:  # {
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            ts = pd.Timestamp.now()  # CREATE TIME STAMP
            print("| MODIFIED >>> " + str(ts))
            # CREATE EVENT PATH VAR
            the_event_path = Path(event.src_path)  # WAS: the_event_path
            # CREATE 'file_name' VAR
            file_name = os.path.basename(the_event_path)
            # CHECK AND SEE IF FILE IS OF TYPE .PDF
            if fnmatch.fnmatch(file_name, "*.pdf"): #{
                # CREATE NEW FILE NAME CONV
                file_name_conv = generate_naming_convention(file_name)
                # CREATE EVENT ITEM FOR LIST
                event_list = [str(file_name_conv), str(ts)]  # WAS: (created_str)
                # APPEND TO DATAFRAME
                self.save_dataframe = append_to_dataframe(the_event_list=event_list,
                                                          dataframe_to_append=self.save_dataframe)
                # PRINT DATAFRAME
                print(self.save_dataframe)
                # CREATE PATH VARIABLES FOR FILE MOVING PROCEDURES
                new_path = os.path.join(self.out_directory, file_name_conv)
                # 08/28/2019 - REMOVED BECAUSE WE DONT NEED TO WATERMARK SO MANY TIMES
                # JUST KEEPING THE MODIFIED TIMESTAMP AND APPENDING TO DATAFRAME
                """
                # CREATE/COPY WATERMARK TO DESTINATION FOLDER
                create_watermark(input_pdf=the_event_path,
                                 output=new_path,
                                 watermark=in_file)
                """
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
            print("SUCCESS! VERY NICE!")
        # }
        finally:  # {
            # CREATE END-TIME VAR
            time_end = pd.Timestamp.now()
            # DETERMINE OVERALL RUN-TIME
            run_time = pd.Timedelta(time_end - time_start)
            # PRINT TOTAL RUNTIME
            print("\t\t[Created-Event] >>> time_alloted: " + str(run_time))
        # }
    #}

# }

################################################################################
# DEFINE FUNCTIONS
################################################################################
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
        print("SUCCESS! VERY NICE!")
    # }
    finally:  # {
        print("[Watermark-PDF " + str(input_pdf) + "] FIN...")
    return
# }

#################################################

"""
TAKES IN:
(1) path to pdf 
RETURNS: 
the STRING of that PDF to match the naming convention
in G:/C of A's/#Email Node/ from F:/APPS/CofA/
"""
def generate_naming_convention(the_pdf_path):  # {
    # TRY THE FOLLOWING
    try:  # {
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
    else: # {
        print("SUCCESS! VERY NICE!")
        return str(new_name)
    # }
    finally: # {
        print("[generate-naming convention] FIN...")
    # }
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
    # RE-INSTANTIATE GLOBALS
    global df_save_list
    # TRY THE FOLLOWING
    try: #{
        # CHECK IF LIST
        if type(the_event_list) is list : #{  # WAS: (the_event_list is list)
            print("\t\tLIST check == PASS")
            # SEPERATE COLUMNS
            col_1 = str(the_event_list[0])
            col_2 = str(the_event_list[1])
            # CREATE APPENDAGE FRAME
            df_appendage = pd.DataFrame(data=[the_event_list],
                                        columns=['CofA', 'Timestamp'])
            # CREATE INSTANCE OF DATAFRAME WE ARE RETURNING
            return_df = dataframe_to_append.append(df_appendage, ignore_index=True, sort=False)
            #OLD# print(return_df.tail(5))
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
        print("\n" + typeE +
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
        print("\t\t[Append-2-DataFrame] >>> time_alloted: " + str(run_time))
    #}
#}

#################################################

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
        print("\n" + typeE +
              "\n" + fileE +
              "\n" + lineE +
              "\n" + messageE)
    #}
    else:  # {
        print("SUCCESS! VERY NICE!")
        # RETURN THE DATE WE PULLED AS STRING
        return date_str
    #}
    finally:  # {
        print("[pull_creation_timestamp] FIN...")
    #}
# }

#################################################

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
        # VARIABLES
        scan_directory = Path(the_dir)
        for root, dirs, files in os.walk(scan_directory): #{
            # DIRECTORY SKIP CONDITIONS
            if "Archive ERR" in dirs: #{
                # REMOVE AND DON'T VISIT IN WALK
                dirs.remove('Archive ERR')
            #}
            if "Archive - For all archived CofA, see G CofA folder" in dirs: #{
                # REMOVE AND DON't VISIT IN WALK
                dirs.remove("Archive - For all archived CofA, see G CofA folder")
            #}
            if "Instruction Sheets" in dirs: #{
                dirs.remove("Instruction Sheets")
            #}
            # OTHERWISE IF THERE ARE FILES IN DIRECTORY
            for f in files: #{
                # IF FILE IS OF TYPE .pdf
                if fnmatch.fnmatch(f, "*.pdf"): #{
                    # ASSEMBLE!
                    file_path = os.path.join(root, f)
                    """
                    # GET CREATE TIME
                    create_time = os.path.getctime(file_path)
                    # GET MODIFIED TIME
                    mod_time = os.path.getmtime(file_path)
                    # MAKE 'ctime' INTO DATETIME / more readable
                    # WAS: datetime.datetime
                    readable_c = datetime.fromtimestamp(create_time).isoformat()  
                    # MAKE 'mtime' INTO DATETIME / more readable
                    # WAS: datetime.datetime
                    readable_m = datetime.fromtimestamp(mod_time).isoformat()
                    # CONVERT TO pandas.Timestamp
                    timeStamp_c = pd.Timestamp(readable_c)
                    # AGAIN FOR MODIFIED TIME
                    timeStamp_m = pd.Timestamp(readable_m)
                    """
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
        df_filelist["CofA File"] = file_list
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
"""
def perform_on_event(the_event_type, the_event_path): #{
    # RE-INSTANTIATE GLOBALS
    global df_save_list
    # CREATE EVENT TYPE VAR
    event_str = str(the_event_type)
    # CREATE EVENT PATH VAR
    event_path = Path(the_event_path)
    ####################
    # TRY THE FOLLOWING
    try:  # {
        # IF EVENT TYPE == "CREATED":
        if event_str == "created":  # {
            ts = pd.Timestamp.now()
            print("| CREATED >>> " + str(ts))
            # CREATE /FILE_NAME/ VAR
            file_name = os.path.basename(event_path)
            # CHECK AND SEE IF FILE IS OF TYPE .PDF
            if fnmatch.fnmatch(file_name, "*.pdf"):  # {
                # CREATE NEW FILE NAME CONV
                file_name_conv = generate_naming_convention(event_path)
                # CREATE TUPLE
                event_tuple = (str(file_name_conv), str(ts))  # WAS: str(file_name)
                # APPEND TUPLE TO DATAFRAME VIA FUNCTION
                df_save_list= append_to_dataframe(the_event_list=event_tuple,
                                                     dataframe_to_append=df_save_list)
                # CREATE PATH VARIABLES FOR FILE MOVING PROCEDURES
                new_path = os.path.join(out_directory, file_name_conv)
                # CREATE/COPY WATERMARK TO DESTINATION FOLDER
                create_watermark(input_pdf=event_path,
                                output=new_path,
                                watermark=in_file)
            # }
            else:  # {
                print("NON-PDF CREATED ON " + str(ts))
            # }
        # }
        elif event_str == "modified":  # {
            ts = pd.Timestamp.now()
            print("| MODIFIED >>> " + str(ts))
            # CREATE /FILE_NAME/ VAR
            file_name = os.path.basename(event_path)
            # CHECK AND SEE IF FILE IS OF TYPE .PDF
            if fnmatch.fnmatch(file_name, "*.pdf"):  # {
                # CREATED NEW FILE NAME CONV
                file_name_conv = generate_naming_convention(event_path)
                ## CREATE TUPLE
                event_tuple = (str(file_name_conv), str(ts))  # WAS: str(file_name)
                # APPEND TUPLE TO DATAFRAME VIA FUNCTION
                df_save_list = append_to_dataframe(the_event_list=event_tuple,
                                                     dataframe_to_append=df_save_list)
            # }
            else:  # {
                print("NON-PDF MODIFIED ON " + str(ts))
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
        print("\t\t[Event-Processed] SUCCESS! VERY NICE!")
    # }
    finally:  # {
        # CREATE END-TIME VAR
        time_end = pd.Timestamp.now()
        # DETERMINE OVERALL RUN-TIME
        run_time = pd.Timedelta(time_end - time_start)
        # PRINT TOTAL RUNTIME
        print("\t\t[Event-Processed] >>> time_alloted: " + str(run_time))
    # }
# }
"""
#################################################

"""
[called at 5 pm by threading.timer]
EXPORTS:
(1) the dataframe that had been saved up
throughout the day 
"""
def end_of_day():  # {
    # RE-INSTANTIATE GLOBALS
    global df_save_list, in_directory
    # CALL MAIN SCAN FUNCTION
    scan_directory(the_dir=in_directory)
# }

#################################################

def main():  # {
    test = 0
#}

####################################################################################
# MAIN BOILERPLATE / INSTANTIATE GLOBAL VARIABLES
####################################################################################
if __name__ == "__main__": #{
    #############################################
    # START TIME
    time_start = pd.Timestamp.now()
    # CREATE STR OF TODAYS DATE
    time_today = str(time_start)[:10]
    #############################################
    # SETUP-LOGGER
    try: #{
        logging.basicConfig(level=logging.INFO,
                            filename="C:/data/outbound/CofA_F_Scanner_" 
                            + str(time_today)[:10] 
                            + ".log",
                            format='%(asctime)s:'
                            + '\n\t\t\t\t'
                            + '<MESG:%(message)s>'
                            + '\n\t\t\t\t'
                            + '<%(threadName)s-ID:%(thread)d>'
                            + '\n\t\t\t\t'
                            + '<%(processName)s-ID:%(process)d>'
                            + '\n\t\t\t\t'
                            + '<FUNC=%(funcName)s>'
                            + '\n\t\t\t\t'
                            + '<LINE:%(lineno)s>'
                            + '\n\t\t\t\t'
                            + '<PATH:%(pathname)s>'
                            + '\n\t\t\t\t'
                            + '<NAME:%(name)s>',
                            datefmt='%Y-%m-%d-%H%M%S',
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
        print("[Setup-Logger] FIN...")
    #}
    #############################################
    # INSTANTIATE GLOBAL VARIABLES
    in_directory = "F:/APPS/CofA/"
    out_directory = "G:/C of A's/#Email Node/"
    outbound_directory = "C:/data/outbound/CofA/"
    in_file = "C:/data/inbound/Agilent_CofA_Letterhead_03-21-19.pdf"
    # CREATE FILE_NAME STR USING TODAYS DATE CONVENTION
    out_file_dir = "C:/data/outbound/CofA/"  # WAS: "C:/data/inbound/"
    out_file_str = str("CofA_Email_Node_list_" + time_today + "_F_pull.csv")
    df_save_list = pd.DataFrame(data=None, columns=['CofA File'])
    isEOD = False
    # CREATE OBSERVER VARIABLE FOR WATCHDOG EVENT HANDLER
    observer = Observer()
    # CREATE TIMER VARIABLE
    t = Timer(10, end_of_day)
    # START TIMER
    t.start()
    # CREATE INSTANCE OF CUSTOM EVENT HANDLER
    event_handler = CofA_Event_Handler(df_save_list, out_directory, observer)
    observer.schedule(event_handler=event_handler,
                      path=in_directory,
                      recursive=True)
    observer.start()
    # TRY THE FOLLOWING
    try:  # {
        while True:  # {
            sleep(1)
        # }
    # }
    except KeyboardInterrupt:  # {
        observer.stop()
    # }
    observer.join()
    #############################################

    
#}