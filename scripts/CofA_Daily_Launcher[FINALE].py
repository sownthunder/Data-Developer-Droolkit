"""
Created on August 08, 2019

transfer from/finalization of:
"CofA_Daily_Launhcer_[Finale].ipynb"

Each day scans within:
F:/APPS/CofA/
AND ANY NEW FILE THAT COMES IN:

YOU KNOW THE REST

"""

# IMPORT THE GOODS
import os, sys, time
from time import sleep
from pathlib import Path
import fnmatch, glob, shutil
import wmi, psutil, subprocess
import tempfile, textwrap
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
import threading, logging
from threading import Timer
from PyPDF2 import PdfFileReader, PdfFileWriter
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
# GLOBAL VARS
in_file = "C:/CofA/imp/Agilent_CofA_Letterhead_03-21-19.pdf"
#in_directory = "F:/APPS/CofA/"
#out_directory = "G:/C of A's/#Email Node/"
in_directory = "C:/Temp/F/APPS/CofA/"
staging_directory = ""
out_directory = "C:/Temp/G/C of A's/#Email Node/"
save_list = []
isEOD = False
time_start = pd.Timestamp.now()
save_dataframe = pd.DataFrame()
# DEFINE CUSTOM CLASS(ES)
class Launcher_Event_Handler(FileNotFoundError):  # {

    #################### INIT #########################
    def __init__(self, save_list, staging_dir, out_dir):  # {
        self.save_list = save_list
        self.staging_dir = staging_dir
        self.out_dir = out_dir

    # }
    ###################################################

    def dispatch(self, event):  # {
        output_str = "EVENT >> " + str(event.event_type)  # + "\n"
        output_str += str("IS_DIR >> " + str(event.is_directory))  # + "\n"
        output_str += str("SRC_PATH >> " + str(event.src_path))  # + "\n"
        """
        x_out = wrap(output_str, 30)
        logging.info(x_out)
        """
        logging.info(textwrap.fill(output_str,
                                   initial_indent="",
                                   subsequent_indent="   " * 5,
                                   width=60))  # was 65
        event_str = str(event.event_type)
        event_path = Path(event.src_path)
        perform_on_event(the_event_type=event_str, the_event_path=event_path)
    # }

# }
# DEFINE FUNCTION(S)
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
        logging.info("[watermark-pdf] FIN...")
    # }
    return
# }
"""
TAKES IN path to pdf and edits the STRING
of that PDF to match the naming convention
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
    logging.debug("HALF 1 == " + half1)
    logging.debug("HALF 2 == " + half2)
    #  setup NEW FILE NAME (for copy)
    new_name = "part "
    new_name += str(half1)
    new_name += " CofA Lot# "
    new_name += str(half2)
    logging.debug("NEW NAME == " + str(new_name))
    #################################
    return str(new_name)
#}
def send_mail(send_from, send_to, subject, message, files=[],
              server="cos.smtp.agilent.com", port=587, use_tls=True):  # {
    logging.info("SENDING MAIL... " + str(pd.Timestamp.now()))
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
    return
# }
def extract_information(pdf_path):  # {
    with open(pdf_path, 'rb') as f:  # {
        pdf = PdfFileReader(f)
        information = pdf.getDocumentInfo()
        number_of_pages = pdf.getNumPages()
    # }
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
# }
def display_pdf_text(pdf_path):  # {
    read_pdf = PyPDF2.PdfFileReader(pdf_path)

    for i in range(read_pdf.getNumPages()):  # {
        page = read_pdf.getPage(i)
        print("Page No - " + str(1 + read_pdf.getPageNumber(page)))
    # }

# }
"""
WITHIN DISPATCH FUNCTION, FUNCTION CALLS WILL OCCUR **TWICE** IF DISPATCH &
THE SPECIFICED FUNCTION (ie "on_created") ARE IN THE "Launcher_Event_Handler" CLASS
SO DEPENDING ON THE STR INPUT (the_event_type) SPECIFIC PROCEDURES WILL OCCUR HERE
"""
def perform_on_event(the_event_type, the_event_path): #{
    global save_dataframe # OUR GLOBAL VARIABLE TO SAVE/WRITE ALL DATA TO
    event_str = str(the_event_type)
    event_path = Path(the_event_path)
    # SWITCH CASE
    if event_str == "created": #{
        ts = pd.Timestamp.now()
        print("| CREATED >>> " + str(ts))
        the_event_path = Path(the_event_path)
        # CREATE "file_name" VARIABLE
        file_name = os.path.basename(the_event_path)
        # IF INFACT IS CORRECT FILE-TYPE (PDF)
        if fnmatch.fnmatch(file_name, "*.pdf"): #{
            # CREATE "naming_convention" VARIABLE
            file_name_conv = generate_naming_convention(the_event_path)
            # CREATE TUPLE
            event_tuple = (str(file_name), str(file_name_conv), str(ts))
            # APPEND (tuple) to "save_list"
            save_list.append(event_tuple)
            # COPY/PREPARE TO MOVE IN "staging_dir"
            prepare_staging(the_pdf_path=the_event_path,
                            the_staging_directory=staging_dir,
                            the_naming_conv=file_name_conv)
        #}
        else: #{
            print(str(file_name) + " != (.pdf)")
        #}
        """
        # APPEND TO SAVE-LIST
        save_list.append(str(event_path))
        print(str(save_list))
        """
    #}
    elif event_str == "modified": #{
        ts = pd.Timestamp.now()
        print("| MODIFIED >>> " + str(ts))
        the_event_path = Path(the_event_path)
        # CREATE "file_name" VARIABLE
        file_name = os.path.basename(the_event_path)
        # IF INFACT IS CORRECT FILE-TYPE (PDF)
        if fnmatch.fnmatch(file_name, "*.pdf"): #{
            # CREATE "naming_convention" VARIABLE
            file_name_conv = generate_naming_convention(the_event_path)
            # CREATE TUPLE
            event_tuple = (str(file_name), str(file_name_conv), str(ts))
            # APPEND (tuple) to "save_list"
            save_list.append(event_tuple)
            """
            # COPY/PREPARE TO MOVE IN "staging_dir"
            prepare_staging(the_pdf_path=the_event_path, 
                            the_staging_directory=staging_dir,
                            the_naming_conv=file_name_conv)
            """
        #}
        else: #{
            print(str(file_name) + " != (.pdf)")
        #}
    #}
    elif event_str == "deleted": #{
        ts = pd.Timestamp.now()
        print("| DELETED >>> " + str(the_event_path) + " " + str(ts)) # WAS: event.src_path
        the_event_path = Path(the_event_path)
        # CREATE "file_name" VARIABLE
        file_name = os.path.basename(the_event_path)
        # CREATE 'naming_convention' VARIABLE
        file_name_conv = generate_naming_convention(the_event_path)
        # IF INFACT IS CORRECT FILE-TYPE (PDF)
        if fnmatch.fnmatch(file_name, "*.pdf"): #{
            # GET FILE NAME FROM DELETED FILE
            del_name = os.path.basename(file_name_conv) # WAS: the_event_path
            # CREATE PATH VAR AND LIKEWISE DELETE
            del_path = os.path.join(out_directory, del_name) # WAS: out_dir
            # CHECK IF ALREADY DELETED:
            if os.path.exists(del_path): #{
                # EXISTS SO DELETE!
                os.remove(del_path)
                print("| " + str(del_path) + " DELETED !")
            #}
            else: #{
                # ALREADY DELETED
                print("| " + str(del_path) + " already deleted!")
            #}
        #}
    #}
#}
"""
TAKES IN path to pdf and copies to desired directory with desired file name
"""
def prepare_staging(the_pdf_path, the_staging_directory, the_naming_conv): #{
    logging.info("PREPARING STAGING")
    logging.info("PDF_PATH >> " + str(the_pdf_path))
    logging.info("STAGING_DIR >> " + str(os.path.basename(the_staging_directory)))
    logging.info("NAMING_CON >> " + str(the_naming_conv))
    # CREATE "new_file_path" VARIABLE
    new_file_path = os.path.join(the_staging_directory, the_naming_conv)
    logging.info("NEW_FILE_PATH >> " + str(new_file_path))
    # COPY/MOVE to "staging_directory"
    shutil.copy2(src=the_pdf_path, dst=new_file_path)
    logging.info("Does exist? " + str(os.path.exists(new_file_path)))
    return
#}
"""
USING GLOBAL var (path to directory) (should be the temp one) that will be looped thru
and worked on/in in order to send CofA emails out at END OF THE DAY
"""
def execute_staging(): #{
    global staging_directory, isEOD, save_list
    print("=================================================")
    print("EXECUTING STAGING >>> " + str(pd.Timestamp.now()))
    print("=================================================")
    print("| DIR >> " + str(staging_directory))
    pdf_list = os.listdir(staging_directory)
    print("| LENGTH OF TEMPORARY DIRECTORY: " + str(len(pdf_list)))
    ##############################################################
    # LOOP THRU AND WATERMARK / MOVE INTO G:/C of A's/#Email Node/
    # ** AND THEN EMAIL FOR EACH PDF OR CLUMP TOGETHER IN ZIP **
    for item in pdf_list: #{
        print("| PDF >> " + str(item))
        # CREATE TEMP_DIR PATH VARIABLE
        current_path = os.path.join(staging_directory, item)
        print("| (path) >> " + str(os.path.dirname(current_path)))  # WAS: str(Path(item)), current_path
        # CREATE "outbound" VARIABLE
        outbound_path = os.path.join(out_directory, item)
        print("| WATERMARKING >>> ")
        # CREATE WATERMARK AND MOVE FILES OUT OF TEMP_DIR
        create_watermark(input_pdf=current_path,
                        output=outbound_path,
                        watermark=in_file)
        # 08/08/2019 - WE NOW DELETE/REMOVE TEMP AT **END** OF SCRIPT
        """
        # DELETE/REMOVE FILE FROM TEMP_DIR
        os.remove(current_path)  # WAS: Path(item)
        """
    #}
    # CREATE DATAFRAME FROM "save_list" DATA
    df_save_list = pd.DataFrame(data=save_list,
                                columns=['CofA_Name', 'Node_Name', 'Time_Created/Modified']
                               )
    print("==================================================")
    print(str(df_save_list.describe))
    print("==================================================")
    # create time_stamp for filename
    ts_meow = pd.Timestamp.now()
    timestamp_str = str(ts_meow)
    timestamp_str = timestamp_str[:10]
    # SAVE "save_list" to .CSV
    df_save_list.to_csv("C:/CofA/log/CofA-Launcher-" + timestamp_str + ".csv",
                        header=None, index=False, mode='a')
    # SET isEOD to be True (end script)
    isEOD = True
    print("| (isEOD) ? " + str(isEOD))
    return
#}
if __name__ == "__main__":  # {
    # SETUP LOGGER
    try:  # {
        logging.basicConfig(level=logging.INFO,
                            filename='C:/CofA/log/CofA_Email_Node.log',
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
                            # format='%(asctime)s:\n\t\t\t\t%(message)s\n\t\t\t\t<%(threadName)s-ID:%(thread)d>\n<FUNC=%(funcName)s>\n<LINE:%(lineno)s>',
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
        logging.error("\n" + typeE +
                      "\n" + fileE +
                      "\n" + lineE +
                      "\n" + messageE)
    # }
    else:  # {
        logging.debug("[Setup-Logger] FIN...")
    # }
    ########################################################
    global in_file, save_list, staging_directory
    global in_directory, out_directory
    global isEOD
    ########################################################
    # DETERMINE IF CALLED FROM COMMAND-LINE OR NOT...
    """
    if len(sys.argv) > 2: #{
        logging.info(">>> CLI call")
    #}
    """
    if 1:  # {
        logging.info("GUI call")
        logging.info("CREATING <<STAGING_DIRECTORY>>...")
        # BOOL VAR to make sure we open **ONE** EXPLORER WINDOW
        hasOpened = False
        # CREATE TEMP_DIR TO ACT AS "STAGING_DIRECTORY"
        with tempfile.TemporaryDirectory() as temporary_directory:  # {
            logging.info("<Successfully created STAGING_DIRECTORY>")
            # IF WE HAVE YET TO OPEN EXPLORER WINDOW OF NEW TEMP_DIR
            if hasOpened is False:  # {
                print("Opening Explorer Window...")
                # create Path var and "Popen" via SUBPROCESS
                temp_folder = Path(temporary_directory)
                # open temp_folder in a new EXPLORER WINDOW
                subprocess.Popen('explorer ' + str(temp_folder))
                # SET BOOL TO TRUE SO THIS DOES NOT OCCUR EVERYTIME
                hasOpen = True
            # }
            # ELSE...
            else:  # {
                print("ALREADY OPENED TEMP DIR!")
            # }
            # CREATE "staging_dir" VAR
            staging_dir = str(temporary_directory)
            # SET OUR GLOBAL VAR
            staging_directory = staging_dir
            print("[Staging_Directory] == " + str(staging_dir))
            print(str(os.path.basename(staging_dir)))
            print("=================================================")
            print("Initializing Timer >>> " + str(pd.Timestamp.now()))
            print("=================================================")
            # CREATE TIMER VAR  // 12 HOURS... now 10.5 HOURS !! 08/07/2019
            # 37800
            t = Timer(30, execute_staging)  # WAS 2592000,3600,720,600,43200,300 & 120
            # START TIMER
            t.start()
            # create event handler
            event_handler = Launcher_Event_Handler(save_list=save_list,
                                                   staging_dir=staging_dir,
                                                   out_dir=out_directory)
            observer = Observer()
            observer.schedule(event_handler=event_handler,
                              path=in_directory,
                              recursive=True)
            observer.start()
            # TRY THE FOLLOWING:
            try:  # {
                sleep_counter = 0
                # mod_counter = 0
                while isEOD is False:  # { # WAS: while True:
                    sleep_counter += 1
                    # mod_counter += 1
                    print("<EOD=FALSE>...sleeping..." + str(sleep_counter))
                    sleep(1)
                    """
                    #print(str(sleep_counter % 10))
                    if (sleep_counter % 9) == mod_counter: #{
                        print(str(mod_counter))
                        mod_counter += 4
                    #}
                    print("sleep==" + str(sleep_counter))
                    print("mod==" + str(mod_counter))
                    """
                # }
                else:  # {
                    print("[END] DELETING.... " + str(staging_directory))
                    # TRY THE FOLLOWNG:
                    try:  # {
                        # DELETE TEMP DIRECTORY / CONTENTS
                        os.remove(staging_directory)
                    # }
                    # HOWEVER, IF USER IS ACCIDENTLY STILL IN FOLDER...
                    except PermissionError:  # {
                        print("User still in directory " + str(staging_directory))
                        print("THEREFORE: deleting individual contents via loop")
                        # TRY THE FOLLOWING (again):
                        try:  # {
                            # CREATE LIST VAR OF ALL FILES IN TEMP_DIR
                            del_list = os.listdir(staging_directory)
                            # LOOP THRU EVERY ITEM IN THAT LIST
                            for item in del_list:  # {
                                print("ITEM:\n" + str(item) + "...deleting...")
                                os.remove(os.path.join(staging_directory, item))
                                print("DELETED!!!")
                            # }
                        # }
                        # HOWEVER< IF FILE IS ALREADY DELETED FOR SOME REASON...
                        except FileNotFoundError:  # {
                            print("\n\tactually tho... files already gone...")
                        # }
                        else:  # {
                            print("[delete-files] FIN...")
                            print("SUCCESSFULLY REMOVED! STOPPING OBSERVER...")
                            observer.stop()
                        # }
                    # }
                    # IF FINISHED SUCCESSFULLY:
                    else:  # {
                        print("[delete-directory] FIN...")
                        # print("SUCCESSFULLY REMOVED! SYS-EXIT-BABY!")
                        # sys.exit(69)
                        print("SUCCESSFULLY REMOVED! STOPPING OBSERVER...")
                        # STOP OBSERVER
                        observer.stop()
                    # }
                    #####################################
                    # EXIT OUT OF FUNCTION/PROGRAM HERE #
                    #####################################

                # }
            # }
            except KeyboardInterrupt:  # {
                observer.stop()
            # }
            observer.join()
        # }
        logging.info("Name of temp_dir: " + str(temporary_directory))  # WAS: the_dir
        logging.info("Directory exists after? " + str(os.path.exists(temporary_directory)))  # WAS: the_dir
        #logging.info("Contents after:" + str(list(temporary_directory.glob('*'))))  # WAS: the_dir
        logging.info("Contents after:" + str(list(glob.glob(str(temporary_directory) + "/*"))))
        print("===========================================")
        temporary_directory = Path(temporary_directory)
        print(str(os.path.basename(temporary_directory)) + " NO LONGER EXISTS !!")
    # }

# }