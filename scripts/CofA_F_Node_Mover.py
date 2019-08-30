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


"""
TAKES IN:
(1) DataFrame

"""
def iter_dataframe(the_dataframe): #{
    print("difference here")
#}

#################################################

def main(): #{
    test = 0
#}


###################################################################################################
# MAIN BOILERPLATE


if __name__ == "__main__":  # {
    # START TIME
    time_start = pd.Timestamp.now()
    # CREATE STR FOR TODAYS DATE
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
        print("\n" + typeE +
              "\n" + fileE +
              "\n" + lineE +
              "\n" + messageE)
    # }
    else:  # {
        print("[setup-Logger] SUCCESS! VERY NICE!")
    # }
    finally: #{
        print("[setup-Logger] FIN....")
    # }
    #############################################
    # INSTANTIATE GLOBAL VARIABLES
    in_file = "C:/data/inbound/Agilent_CofA_Letterhead_03-21-19.pdf"
    in_directory = "C:/data/outbound/CofA/"
    out_directory = "G:/C of A's/#Email Node/"
    file_conv_list = []  # EMPTY LIST TO HOLD NEWLY CREATED FILES (name conv)
    file_time_list = []  # EMPTY LIST TO HOLD TIMESTAMPS OF NEWLY ABOVE ^^
    print("TODAY == " + str(time_today))
    # SUBTRACTION DELTA
    subtraction_delta = pd.Timedelta(value=1, unit='days')
    print("\t\n SUTBRACTING... " + str(subtraction_delta))
    # AND GET YESTERDAYS DATE BY SUBTRACTING
    time_yesterday = time_start - subtraction_delta
    # SETUP STRING
    yesterstr = str(time_yesterday.date())
    print("YESTERDAY == " + str(yesterstr))
    print("\nTEST GLOB-STRING == " + str("C:/data/outbound/CofA/*_" + yesterstr + "_F_*"))
    print("\n\t\t GLOBBING DIR >>> " + str(os.listdir(in_directory)))
    # GLOB & PRELIMINARY SETUPS:
    glob_previous = sorted(glob.glob("C:/data/outbound/CofA/*_" + yesterstr + "_F_*"))
    print("\n\t GLOB_PREVIOUS >>> \n")
    for name in glob_previous: #{
        print(name)
    #}
    glob_current = sorted(glob.glob("C:/data/outbound/CofA/*_" + time_today + "_F_*"))
    print("\n\t GLOB_CURRENT >>> \n")
    for name in glob_current: #{
        print(name)
    #}
    #################
    # SETUP IMPORTS #
    #################
    # set as first element in returned list
    df1 = pd.read_csv(glob_previous[0])
    # set as first element in returned list
    df2 = pd.read_csv(glob_current[0])
    print("LEN_D1 == " + str(len(df1)))
    print("LEN_D2 == " + str(len(df2)))
    # SET DIFFERENCE OF TWO DATAFRAMES IN PANDAS PYTHON
    set_diff_df = pd.concat([df2, df1, df1]).drop_duplicates(keep=False)
    print("LENGTH OF DIFF_DF: " + str(len(set_diff_df)))
    print(set_diff_df)
    # COUNTER
    #x = 0
    ##############################################
    # ITERATE THRU TUPLES (using temp directory) #
    ##############################################
    # ITERATE THRU FIRST FRAME (F_DRIVE)
    # << WHILE INSIDE OF TEMP DIRECTORY
    with tempfile.TemporaryDirectory() as temporary_directory:  # {
        # COUNTER
        x = 0
        the_dir = Path(temporary_directory)
        print("TEMPORARY DIRECTORY >>> " + str(the_dir))
        # ITERATE THRU DATAFRAME
        for row in set_diff_df.itertuples(index=False, name='CofA'):  # {
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
            file_time_list.append(str(row[1]))
            ############################################################
            # CREATE NEW PATH VARIABLE TO CHECK IF FILE EXISTS....
            new_path = os.path.join(out_directory, file_name_conv)
            # CREATE 'temp_path'
            temp_path = os.path.join(the_dir, file_name_conv)
            # CREATE 'ds_path'
            dst_path = os.path.join(out_directory, file_name_conv)
            # WATERMARK A COPY TO G_DRIVE **WITH CORRECT NEW FILE NAME**
            create_watermark(input_pdf=str(row[0]),
                            output=dst_path, watermark=in_file)
            # WATERMARK A COPY INTO TEMP FOLDER **WITH CORRECT NEW FILE NAME**
            create_watermark(input_pdf=str(row[0]),
                             output=temp_path, watermark=in_file)
            # INCREASE COUNTER
            x += 1
            print("COUNT === " + str(x))
        #}
        # ZIP THE CURRENT TEMP FOLDER WE ARE INSIDE OF
        try: #{
            print("\n\n\nXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
            print("\nWORKING DIRECTORY ---BEFORE--- ZIP == " + str(os.getcwd()))
            # path to folder
            directory = "." # (the_dir)
            # CHANGE WORKING DIRECTORY TO THE TEMPORARY DIR
            # (IN ORDER TO PROPERLY ZIP FILES/FOLDER)
            os.chdir(the_dir)   # WAS: "C:/"
            print("\nWORKING DIRECTORY ---DURING--- ZIP == " + str(os.getcwd()))
            # calling function to get all file paths in the directory
            file_paths = get_all_file_paths(the_dir)
            # printing the list of all files to be zipped 
            print('\nFollowing files will be zipped:') 
            for file_name in file_paths: #{
                print(file_name) 
            #}
            # writing files to a zipfile 
            with ZipFile('CofA-' + str(pd.Timestamp.now())[:10] + ".zip",'w') as zip: #{
                # writing each file one by one 
                for file in file_paths: #{
                    zip.write(file) 
                #}
            #}
            print('All files zipped successfully!\n\nXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX' 
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
            print("\n" + typeE +
                "\n" + fileE +
                "\n" + lineE +
                "\n" + messageE)
        #}
        else: #{
            print("ALL FILES SUCCESSFULLY ZIPPED!")
        #}
        finally: #{
            ts = pd.Timestamp.now()
            run_time = ts - time_start
            print("[Zip-Files] RUN TIME == " + str(run_time))
        #}
        # TRY AND FINISH THIS SHIT OFF (email this shit!)
        try: #{
            print("\n\t\t\t GLOBBING FOR ZIP FILE !!!")
            for name in sorted(glob.glob(str(the_dir) + "/*.zip")): #{
                print("NAME OF FILE == "
                    + str(name))
                print("LENGTH OF GLOB == "
                    + str(len(sorted(glob.glob(str(the_dir))))))
                # GET & SET PATH_NAME
                zip_path = Path(name)
                print("ZIP_PATH == " + str(zip_path))
            #}
            #################################################
            # CREATE EMPTY DATAFRAME WITH FILE NAME CONV NAMES & TIMESTAMPS
            file_conv_df = pd.DataFrame(data=None, columns=None)
            # SET ONE *NEW* COLUMN OF DATAFRAME TO LIST (file_name_conv)
            file_conv_df["CofA"] = file_conv_list
            # SET ANOTHER *NEW* COLUMN OF DATAFRAME TO LIST (timestamps)
            file_conv_df["Timestamp"] = file_time_list
            # CREATE STR FOR PATH OF SAVE_DIFF_DATAFRAME
            df_save_str = str("CofA-" + str(pd.Timestamp.now())[:10] + ".csv")
            df_save_path = os.path.join(the_dir, df_save_str)
            print("\n\n\tSAVE-PATH FOR DATAFRAME == " + str(df_save_path))
            # SORT THE DATAFRAME BEFORE EXPORTING ????
            # CREATE FILE_LIST VAR
            file_list = [str(zip_path), str(df_save_path)]
            print(">>> FILE LIST :  \n\t" + str(file_list) + "\n")
            #####################################################
            # >>>>>>>>>>>>> SEND EMAIL HERE <<<<<<<<<<<<<<<<<<< #
            # >>>>>>>>>>>>> SEND EMAIL HERE <<<<<<<<<<<<<<<<<<< #
            #####################################################
            try: #{
                send_mail(send_from="derek.bates@non.agilent.com",
                            send_to="derek.bates@non.agilent.com", 
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
                print("\n" + typeE +
                                "\n" + fileE +
                                "\n" + lineE +
                                "\n" + messageE)
            #}
            else: #{
                print("EMAIL SUCCESSFULLY SENT! VERY NICE!")
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
            print("[Create-set-diff-df-F-DRIVE] SUCCESS! VERY NICE!")
        #}
        finally: #{
            ts = pd.Timestamp.now()
            run_time = ts - time_start
            print("[Email-Files] FIN...")
            observer.stop() #  WAS: sys.exit(69)
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
            (C) IF IT *DOES NOT* EXIST:     call "create_watermark()" into BOTH temp_dir and other
            *** SO THAT BOTH VERSIONS NOW DO EXIST ***
            """