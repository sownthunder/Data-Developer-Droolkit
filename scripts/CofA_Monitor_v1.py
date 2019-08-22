"""
Restarted on August 22, 2019 at 03:30 PM

- Begins at 05:00 AM (MORNING!)
-


"""

# IMPORT THE GOODS
import os, sys, time
from time import sleep
from pathlib import Path
import fnmatch, glob, shutil
import wmi, psutil
import filecmp, tempfile, textwrap
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

# DEFINE CLASSES

class CofA_Event_Handler(FileSystemEventHandler): #{

    def __init__(self, save_dataframe, in_directory, out_directory): #{
        self.save_dataframe = save_dataframe
        self.in_directory = in_directory
        self.out_directory = out_directory
    #}

    def on_created(self, event): #{
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
                """
                # CREATE str TO HOLD FINAL COLUMN FOR TUPLE
                created_str = "Created"
                """
                # CREATE NEW FILE NAME CONV
                file_name_conv = generate_naming_convention(file_name)
                # CREATE EVENT ITEM FOR LIST
                event_list = [str(file_name_conv), str(ts)]  # WAS: (created_str)
                # APPEND EVENT ITEM TO "save_list"
                save_list.append(event_list)
                print("SAVE LIST == \n"
                      + str(save_list))
                """
                df_save_list = append_to_dataframe(the_event_list=event_list,
                                    dataframe_to_append=df_save_list)
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
            logging.error("\n" + typeE +
                          "\n" + fileE +
                          "\n" + lineE +
                          "\n" + messageE)
            # }
        else:  # {
            print("\t\t[Created-Event] FIN..")
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

    def on_modified(self, event): #{
        print("test")
    #}
#}


# DEFINE FUNCTIONS

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
        if type(the_event_list) is list : #{  # WAS: (the_event_list is list)
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

"""
EXPORTS DATAFRAME
TAKES IN:
(1) DATAFRAME OBJECT THAT HAS BEEN CREATED VIA WATCHODG
"""


def execute_staging():  # {
    # RE-INSTANTIATE GLOBALS
    global save_list
    # OLD# global df_save_list
    global in_directory
    global out_directory
    global today_date_str
    global isEOD
    # OLD# print("DATAFRAME IS OF TYPE ==\n\t\t" + str(type(df_save_list)))
    # OLD# print("AND IS EMPTY !?!?!? == \n" + str(df_save_list))
    print("\n\n\n >>>>> BUT THAT SEXY save_list == \n" + str(save_list))
    print("of type =====================" + str(type(save_list)))
    #################### CREATE [save_list] DATAFRAME #####################
    try:  # {
        # WE HAVE THE SAVE_LIST, NOW WE NEED TO FILL THAT DATA IN
        # TO THE MAIN DATAFRAME THAT IT BELONG TO
        df_saveframe = pd.DataFrame(data=save_list,
                                    columns=['CofA', 'Timestamp'],
                                    dtype=np.str)
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
        print("[Create-DataFrame] SUCCESS! VERY NICE!")
        print(str(df_saveframe))
    # }
    finally:  # {
        ts = pd.Timestamp.now()
        run_time = ts - time_start
        print("[Create-DataFrame] RUN TIME == " + str(run_time))
    # }
    #################################################
    try:  # {
        print("\n\n\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("TODAYS (FAKE) DATE == " + today_date_str)
        ###########################################
        # CREATE TODAY AND YESTERDAY STR
        today_str = str(pd.Timestamp.now())[:10]
        print("TODAYS (REAL) DATE == " + today_str)
        time_now = pd.Timestamp(year=2019, month=8, day=14)
        # CREATE SUTBRACTION DELTA
        subtraction_delta = pd.Timedelta(value=1, unit='days')
        print("SUBTRACTION DELTA == " + str(subtraction_delta))
        # CREATE "yesterdays date" BY SUTBRACTING
        yesterstr = str(time_now - subtraction_delta)[:10]
        print("YESTERSTR == " + str(yesterstr))
        print("\nTEST GLOB-STRING == " + str("C:/data/inbound/*_"
                                             + yesterstr
                                             + "_*"))
        ###########################################
        # BEGIN GLOBBING
        glob_previous = sorted(glob.glob("C:/data/inbound/*_"
                                         + yesterstr
                                         + "_*"))
        print("\n\t GLOB_PREVIOUS >>> \n")
        for name in glob_previous:  # {
            print(name)
        # }
        #####################################################################
        # < FOR RIGHT NOW WE IMPORT A .CSV FOR THE TODAY_FILE...
        # THIS IS CREATED MANUALLY EVERY TIME BY CREATING A LIST OF
        # "F:/APPS/CofA/" AND PUTTING INTO  A DATAFRAME
        # ==============[DIRECTORY CHANGE FOR FINAL VERISON]===========
        # "C:/data/inbound/*_" >>>> "C:/CofA/log/lists/*_"
        #####################################################################
        # RETURN LIST FROM FUNCTION
        #
        # OLD#glob_current = scan_directory("F:/APPS/CofA/")
        #
        ########################################################
        glob_current = sorted(glob.glob("C:/data/inbound/*_"
                                        + today_date_str
                                        + "_*"))
        print("\n\t GLOB_CURRENT >>> \n")
        for name in glob_current:  # {
            print(name)
        # }
        print("\n\n\n~~~~~~~~~~~~~~~~~~~8==D~~~~~~~~~~~~~~~~~~~~~~~~~~")
        #################
        # SETUP IMPORTS #
        #################
        df1 = pd.read_csv(glob_previous[0])
        df2 = pd.read_csv(glob_current[0])
        """
        # we dont use indeces because of LIST
        df2 = pd.DataFrame() # EMPTY AT FIRST
        # ASSIGN COLUMN OF DATAFRAME FROM LIST
        df2['CofA File'] = glob_current
        """
        print("LEN_D1 == " + str(len(df1)))
        print("LEN_D2 == " + str(len(df2)))
        # OLD#print(df1.info)
        # OLD#print(df2.info)
        # SET DIFFERENCE OF TWO DATAFRAMES IN PANDAS PYTHON
        set_diff_df = pd.concat([df2, df1, df1]).drop_duplicates(keep=False)
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("\n\tLENGTH OF DIFFERENCE == " + str(len(set_diff_df)))
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
        x = 0  # counter variable
        # CREATE TEMPORARY DIRECTORY (TO WORK INSIDE OF)
        ###################################################################
        with tempfile.TemporaryDirectory() as directory_name:  # {
            the_dir = Path(directory_name)
            print("| TEMPORARY DIRECTORY >>> " + str(the_dir) + "\n")
            # ITERATE THRU TUPLES...
            for row in set_diff_df.itertuples(index=False, name="CofA"):  # {
                # GET/CREATE BASE_NAME
                base_name = os.path.basename(str(row[0]))  # WAS: the_event_path
                # GET NEW FILE NAME CONVENTION
                file_name_conv = generate_naming_convention(base_name)
                # CREATE "temp_path"
                temp_path = os.path.join(the_dir, file_name_conv)
                # CREATE "dst_path"
                dst_path = os.path.join(out_directory, file_name_conv)
                # WATERMARK A COPY TO G_DRIVE **WITH CORRECT NE W FILE NAME**
                create_watermark(input_pdf=str(row[0]),
                                 output=dst_path, watermark=in_file)
                # WATERMARK A COPY INTO TEMP FOLDER ** WITH CORRECT NEW FILE NAME**
                create_watermark(input_pdf=str(row[0]),
                                 output=temp_path, watermark=in_file)
                # INCREASE COUNTER
                x += 1
                print("COUNT == " + str(x))
            # }
            ################################################################
            # ZIP THE CURRENT TEMP DIR (no need to create... just rename)
            try:  # {
                print("\n\n\nXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
                print("\nWORKING DIRECTORY ---BEFORE--- ZIP == " + str(os.getcwd()))
                # path to folder
                directory = "."  # (the_dir)
                # CHANGE WORKING DIRECTORY TO THE TEMPORARY DIR
                # (IN ORDER TO PROPERLY ZIP FILES/FOLDER)
                os.chdir(the_dir)  # WAS: "C:/"
                print("\nWORKING DIRECTORY ---DURING--- ZIP == " + str(os.getcwd()))
                # calling function to get all file paths in the directory
                file_paths = get_all_file_paths(the_dir)
                # printing the list of all files to be zipped
                print('\nFollowing files will be zipped:')
                for file_name in file_paths:  # {
                    print(file_name)
                    # }
                # writing files to a zipfile
                with ZipFile('CofA-' + str(pd.Timestamp.now())[:10] + ".zip", 'w') as zip:  # {
                    # writing each file one by one
                    for file in file_paths:  # {
                        zip.write(file)
                        # }
                # }
                print('All files zipped successfully!\n\nXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
                      + 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX\n')
                ###################################################
                # ....NOW ZIP THE NEWLY MADE FOLDER INSIDE TEMP FOLDER...
                # WAS#zip_directory = "./" + str(today_date_str)
                """
                zip_dir = Path("/" + str(today_str))
                print("\n MAKE-SHIFT ZIPPY_DIR == " + str(zip_dir) + "\n")
                # CREATE ZIP_DIRECTORY PATH VARIABLE
                zip_directory = os.path.join(".", zip_dir)
                print("\n ZIP_DIRECTORY == " + str(zip_directory) + "\n")
                # calling function to get all file paths in directory
                file_paths = get_all_file_paths(zip_directory)
                # printing the list of all files to be zipped
                print('Following files will be zipped:') 
                """
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
                print("ALL FILES SUCCESSFULLY ZIPPED!")
            # }
            finally:  # {
                ts = pd.Timestamp.now()
                run_time = ts - time_start
                print("[Zip-Files] RUN TIME == " + str(run_time))
            # }
            # TRY TO FINISH THIS SHIT OFF
            try:  # {
                print("\n\t\t\t GLOBBING FOR ZIP FILE !!!")
                for name in sorted(glob.glob(str(the_dir) + "/*.zip")):  # {
                    print("NAME OF FILE == "
                          + str(name))
                    # logging.info(name)
                    print("LENGTH OF GLOB == "
                          + str(len(sorted(glob.glob(str(the_dir))))))
                    # GET&SET PATH NAME
                    zip_path = Path(name)
                    print("ZIP_PATH == "
                          + str(zip_path))
                # }
                """
                # CREATE ZIP_DRIECTORY OFF SINGLE_GLOB_STR
                zip_path = Path(sorted(glob.glob(str(the_dir) + "/*.zip"))[0])
                """
                #################### EXPORT DATAFRAME #####################
                # ZIP FILE HAS BEE CREATED NOW WE CAN EXPORT DATAFRAME
                # AND NOT WORRY ABOUT IT ALSO BEING INCLUDE IN ZIP
                #########################################################
                # CREATE STR FOR PATH FOR (NEW/SAVE LIST) DATAFRAME
                df_save_str = str("CofA-"
                                  + str(pd.Timestamp.now())[:10]
                                  + ".csv")
                df_save_path = os.path.join(the_dir, df_save_str)
                print("\n\n\tSAVE-PATH FOR DATAFRAME == " + str(df_save_path))
                # NO NEED TO CREATE PATH FOR SAVE_DIFF_DATAFRAME
                """
                df_save_path = os.path.join(the_dir, 
                                            "CofA-" 
                                            + str(pd.Timestamp.now())[:10] 
                                            + ".csv")
                print("EXPORT-CSV-PATH == " + str(df__savepath))
                # CREATE PATH FOR (NEW/SAVE LIST) DATAFRAME
                df_diff_path = os.path.join(the_dir,
                                            "CofA-" 
                                            + str(pd.Timestamp.now())[:10]
                                            + ".csv")
                """
                # OLD# print("\n\t DF_SAVE_LIST == " + str(type(df_save_list)))
                # os.path.join(in_directory, )
                """
                if str(type(df_save_list)) == "NoneType": #{
                    sys.exit(69)
                #}
                """
                ####################################################
                # EXPORT DATAFRAME TO FILE IN TEMP FOLDER IN ORDER TO EMAIL
                # OLD# df_save_list.to_csv(str(df_save_path), index=False)
                ##################################################
                # EXPORT THE SET_DIFF_DF TO FILE  IN TEMP FOLDER IN ORDER TO EMAIL
                # OLD# set_diff_df.to_csv(str(df_save_path), index=False)
                break_input = input("Continue? Y\n")
                # CREATE FILE_LIST VAR
                file_list = [str(zip_path), str(df__save_path)]
                print("<<<<<< FILE LIST : \n\t\n\t\t"
                      + str(file_list)
                      + "\n")
                #####################################################
                # >>>>>>>>>>>>> SEND EMAIL HERE <<<<<<<<<<<<<<<<<<< #
                # >>>>>>>>>>>>> SEND EMAIL HERE <<<<<<<<<<<<<<<<<<< #
                #####################################################
                # CREATE PATH VAR and "Popen" via SUBPROCESS
                print("Opening Explorer Window...")
                the_dir = Path(directory_name)
                # open temp_folder in a new EXPLORER WINDOW
                subprocess.Popen('explorer ' + str(the_dir))
                if str(break_input) == "n":  # {
                    sys.exiit(69)
                # }
                else:  # {
                    print("CONT....")
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
                sys.exit(69)
            # }
            else:  # {
                print("[]")
            # }
            finally:  # {
                ts = pd.Timestamp.now()
                run_time = ts - time_start
                print("[Email-Files]")
            # }
        # }
        print('Directory exists after?' + str(the_dir.exists()))
        print('Contents after:' + str(list(the_dir.glob('*'))))
        ###################################################
        # OUTSIDE OF TEMP FOLDER
        # EXPORT THE .csv?
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
        isEOD = True
        # BECAUSE WE SET "isEOD" TO TRUE IT WILL STOP WATCHDOG LISTENER,
        # POST TIME STAMP, THEN EN

    # }
    finally:  # {
        ts = pd.Timestamp.now()
        run_time = ts - time_start
        print("RUN TIME == " + str(run_time))
        print("LINE 305 EXECUTE STAGING()")
    # }

# }

if __name__ == "__main__": #{
    # INSTANTIATE GLOBAL VARIABLES
    in_file = "C:/CofA/imp/Agilent_CofA_Letterhead_03-21-19.pdf"
    save_list = []
    isEOD = False
    in_directory = "C:/Temp/F/APPS/CofA/"
    out_directory = "C:/Temp/G/C of A's/#Email Node/"
    to_email = "agilent_cofa@agilent.com"
    from_email = "derek.bates@non.agilent.com"
    time_start = pd.Timestamp.now()
    print("[=================================================]")
    print("| SCANNING DIRECTORY >>> " + str(in_directory))
    print("| STORING IN DATAFRAME >>> " + str(save_list))  # WAS: str(df_save_list.head()))
    print("[=================================================]")
    print("| Initializing Time >>> " + str(pd.Timestamp.now()))
    print("[=================================================]\n\n\n")
    # CREATE TIMER VAR  // 12 HOURS... now 10.5 HOURS !! 08/07/2019
    # 37800
    t = Timer(25, execute_staging)  # WAS 2592000,3600,720,600,43200,300 & 120
    # START TIMER
    t.start()
    # CREATE INSTANCE OF CUSTOM EVENT HANDLER
    print("\n\n<><><><><><><><><><>BEFORE HANDLER START<><><><><><><><><><><>\n")
    print("<><><><><> save_list == \n")
    # PRINT OUT EVERY ITEM & COUNT #
    len_count = len(save_list)
    for save in save_list:  # {
        print("SAVE NAME === " + str(save))
        print("COUNT === " + str(len_count))
        # subtract one
        len_count -= 1
    # }
    # print("<><><><><> df_save_list == " + str(df_save_list))
    print("\n<><><><><><><><><><><><><><><><><><><><><><><><><><><>\n\n")
    event_handler = CofA_Event_Handler(save_list, in_directory, out_directory)
    observer = Observer()
    observer.schedule(event_handler=event_handler,
                      path=in_directory,
                      recursive=True)
    observer.start()
    # TRY THE FOLLOWING
    try:  # {
        sleep_counter = 0
        while isEOD is False:  # {
            # increase SLEEP COUNTEr & sleep...
            sleep_counter += 1
            sleep(1)
        # }
        else:  # {
            print("[EOD] REACHED !!! <CLOSING SCRIPT>>")
            ts = pd.Timestamp.now()
            run_time = ts - time_start
            print("RUN TIME == " + str(run_time))
            sys.exit(0)
        # }
    # }
    except KeyboardInterrupt:  # {
        observer.stop()
    # }
    observer.join()
    #}