"""
taken from CofA_Custom_Crate.py in archive folder


"""

# IMPORT THE GOODS
import os, sys, time
from time import sleep
from pathlib import Path
import fnmatch, glob, shutil
import wmi, psutil
from PyPDF2 import PdfFileWriter, PdfFileReader
import tempfile
from zipfile import ZipFile
import pandas as pd
import numpy as np
from pandas import Series, DataFrame
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import logging

def clicked():  # {
    # RE-INSTANTIATE GLOBALS
    global label1

    label1.configure(text="AFTER... button was clicked", state=tk.DISABLED)
# }

def get_all_file_paths(directory):  # {

    # initalizing empty file paths list
    file_paths = []

    # crawling through directory and subdirectories
    for root, directories, files in os.walk(directory):  # {
        for filename in files:  # {
            # join the two strings in order to form the full filepath
            filepath = os.path.join(root, filename)
            file_paths.append(filepath)
        # }
    # }
    # returning all file paths
    return file_paths
# }

def select_batch_list():   # {
    # RE-INSTANTIATE GLOBALS
    global root, e1_var, selected_batch_list, b2
    logging.info("BATCH_LIST_SELECTED(bool)==" + str(selected_batch_list))
    # TRY THE FOLLOWING
    try:  # {
        root.filename = filedialog.askopenfilename(initialdir=".", title="Select 'BATCH LIST''",
                                                   filetypes=(("csv files", "*.csv"),
                                                              ("xlsx files", "*.xlsx"),
                                                              ("all files", "*.*")))
        logging.info(root.filename)
        e1_var.set(root.filename)
        # CREATE FILE_PATH FOR "BATCH_LIST"
        batch_path = Path(root.filename)
        # ENABLE ZIP DIR SELECTION BUTTON...WAS: CONFIRM BUTTON
        b2.configure(state=tk.ACTIVE)
        # CALL THE DISPLAY FUNCTION
        display_batch_list(batch_path)
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
        logging.info("[Select-Batch-List] SUCCESS! VERY NICE!")
    # }
    finally:  # {
        # SET BOOL TO TRUE
        selected_batch_list = True
        logging.info("BATCH_LIST_SELECTED(bool)=="  + str(selected_batch_list))
# }

def display_batch_list(file_path):  # {
    # TRY THE FOLLOWING:
    try:  # {
        # TOP LEVEL PROPERTIES
        top = tk.Toplevel(master=root)
        top.title('Crate-Batch-List:')
        top.geometry('300x450+550+300')
        top.minsize(width=300, height=450)
        top.maxsize(width=300, height=1050)
        top.resizable(width=False, height=True)

        # CREATE SCROLL BAR?
        scrollbar = tk.Scrollbar(master=top)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # CREATE LISTBOX
        Lb1 = tk.Listbox(master=top, width=300, yscrollcommand=scrollbar.set)

        ## CHECK FILE TYPE
        file_str = str(file_path)
        # IF EXCEL FILE
        global df_batch
        if fnmatch.fnmatch(file_str, "*.xlsx"):  # {
            logging.info(str(file_str) + " == .EXCEL FILE!")
            # GLOBAL VAR
            # global df_batch
            # READ IN AS .XLSX
            df_batch = pd.read_excel(file_path, sheetname=0)
            # FOR EACH PART_NO LISTED IN THE BATCH_FILE:
            for row in df_batch.itertuples(index=True, name="PART_NO"):  # {
                # INSERT PART_NO
                Lb1.insert(int(row[0] + 1), str(row[1]))
            # }
        # }
        # ELSE... IF CSV
        elif fnmatch.fnmatch(file_str, "*.csv"):  # {
            logging.info(str(file_str) + " == .CSV FILE!")
            # GLOBAL VAR
            # global df_batch
            # READ IN AS .CSV
            df_batch = pd.read_csv(file_path)
            # FOR EACH PART_NO LISTED IN BATCH_FILE:
            for row in df_batch.itertuples(index=True, name="PART_NO"):  # {
                # INSERT PART_NO
                Lb1.insert(int(row[0] + 1), str(row[1]))
            # }
        # }
        # PLACE COMPLETED LISTBOX
        Lb1.pack(side=tk.LEFT, fill=tk.BOTH)
        # Lb1.place(anchor=tk.CENTER, relx=0.5, rely=0.5)
        scrollbar.config(command=Lb1.yview)
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
        logging.info("[Display-Batch-List] SUCCESS! VERY NICE!")
    # }
# }

def select_zip_folder():  # {
    # RE-INSTANTIATE GLOBALS
    global out_directory, zip_folder, e2_var, R1, R2, b3
    global selected_batch_list, selected_zip_folder  # WAS: selected_batch_list, zip_folder_selected
    # TRY THE FOLLOWING:
    try:  # {
        root.directory = filedialog.askdirectory(initialdir=".", parent=root, title="SELECT ZIP FOLDER")
        out_directory = Path(root.directory)
        logging.info(root.directory)
        e2_var.set(root.directory)
        # TIME STAMP FOR FOLDER NAME
        time_now = pd.Timestamp.now()
        time_now_str = str(time_now)
        # SHORTEN STR
        time_now_str = time_now_str[:10]
        time_now_str += "-CofA-Custom-Crate"
        # CREATE NEW DIR IN SELECTED DIRECTORY
        # (for zipped files of watermarks)
        new_dir_path = os.path.join(out_directory, str(time_now_str))
        logging.info(new_dir_path)
        # IF 'NEW DIR' DOES NOT EXIST (it wont)
        if not os.path.exists(new_dir_path):  # {
            # MAKE IT EXIST!
            os.makedirs(new_dir_path)
        # }
        zip_folder = new_dir_path
        print(str(zip_folder))
        #return
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
        logging.info("[Select-Zip-Folder] SUCCESS! VERY NICE!")
        return
    # }
    finally:  # {
        # SET BOOL TO TRUE
        selected_zip_folder = True
        # [2019-09-23]... ENABLE "Most Recent" & "Return All" CofA option(s)
        R1.configure(state=tk.ACTIVE)
        R2.configure(state=tk.ACTIVE)
        # [2019-09-23]... SELECT "Return All" option specifically!
        R2.select()
        # [2019-09-20].... was: zip_folder_selected = True
        # ENABLE ZIP DIR SELECTION BUTTON...WAS: CONFIRM BUTTON
        b3.configure(state=tk.ACTIVE)
        logging.info("ZIP_FOLDER_SELECTED(bool)== "+ str(selected_zip_folder))
        if (selected_zip_folder is True) & (select_batch_list is True):  # {
            # SET GLOBAL VAR TO TRUE
            preliminaries_selected = True
        # }
    # }
    #return out_directory
# }

def create_watermark(input_pdf, output, watermark):  # {
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
        logging.info("\n" + typeE +
              "\n" + fileE +
              "\n" + lineE +
              "\n" + messageE)
        # }
    else:  # {
        logging.info("[WATERMARK-PDF] FIN...")
        # }
    return
# }

def pull_all_cofas():  # {
    logging.info("<<PULLING ALL COFAS>>")
# }


def pull_recent_cofas():   # {
    logging.info("<<PULLING RECENT COFAS>>")
# }

def zip_the_directory(directory_to_zip): #{
    # RE-INSTANTIATE GLOBALS
    global og_wd
    # TRY THE FOLLOWING
    try: #{
        logging.info("\n\n\nXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
        logging.info("\nWORKING DIRECTORY ---BEFORE--- ZIP==\n" + str(os.getcwd()))
        # CHANGE THE WORKING DIRECTORY TO DIRECTORY WE WISH TO ZIP
        os.chdir(directory_to_zip)
        # path to folder (NOW currently folder we want to zip)
        directory = "."
        logging.info("\nWORKING DIRECTORY ---DURING--- ZIP==\n" + str(os.getcwd()))
        # calling function to get all file paths we want to zip
        file_paths = get_all_file_paths(directory)
        # printing the list of all files to be zipped
        logging.info("\nFollowing files will be zipped:")
        for file_name in file_paths: #{
            logging.info(file_name)
        #}
        # writing files to a zipfile
        with ZipFile('CofA-'
                     + str(pd.Timestamp.now())[:10]
                     + ".zip", 'w') as zip: #{
            # writing each file one by one
            for file in file_paths: #{
                zip.write(file)
            #}
        #}
        logging.info("All files zipped successfully!\n\nXXXXXXXXXXXXXXXXXXXXXXXXXX")
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
        logging.info("[Zip-Files-" + str(directory_to_zip) + "] SUCCESS! VERY NICE!")
    #}
    finally: #{
        # CHANGE WORKING DIRECTORY BACK TO ORIGINAL
        os.chdir(og_wd)
    #}
#}

def cofa_crate(): #{
    # RE-INSTANTIATE GLOBALS
    global root, in_directory, out_directory, zip_folder, df_batch
    # setup infile variable
    in_file = root.filename
    print("BATCH_LIST: \n" + str(in_file))
    # CREATE DATAFRAME FROM BATCH LIST
    df_batch = pd.read_csv(in_file, header=None, names=["Lot_No"], enginge='python')
    # counter
    x = 0
    for lot_no in df_batch.itertuples(): #{
        print("============= \n" + str(lot_no[1]) + "\n=============")
        # CHECK AND CREATE NEW DIR PATH
        new_dir_path = os.path.join(zip_folder, str(lot_no[1]))  # WAS: root.directory
        # IF 'lot_no' DIRECTORY DOES NOT EXIST:
        if not os.path.exists(new_dir_path): #{
            # MAKE IT EXIST!
            os.makedirs(new_dir_path)
        #}
        # CREATE TEMP DIR/FOLDER TO WORK INSIDE OF:
        with tempfile.TemporaryDirectory() as directory_name: #{
            the_dir = Path(directory_name)
            print("TEMP_DIRECTORY == " + str(the_dir))
            # GLOB AND ITERATE THRU EACH FILE MATCHING NAME... etc
            for name in sorted(glob.glob(in_directory)
                               + "*"
                               + str(lot_no[1])
                               + "*"): #{
                # CREATE PATH VARIABLE
                pdf_path = Path(str(name))
                # GET BASE NAME (FILE NAME)
                file_name = os.path.basename(pdf_path)
                # CREATE TEMP PATH
                temp_path = os.path.join(the_dir, file_name)
                # COPY FILE TO NEW LOCATION
                shutil.copy2(pdf_path, temp_path)
                # CREATE WATERMARK ON NEW FILE
                create_watermark(input_pdf=temp_path,
                                 output=os.path.join(zip_folder, file_name),
                                 watermark=watermark_pdf)
                # GET METADATA OF OLD ORIGINAL FILE
                old_stinfo = os.stat(pdf_path)
                # INCREASE COUNT
                x += 1
            #}
        #}
        print("count == " + str(x))
        print("Directory exists after?", str(the_dir.exists()))
        print("Contents after: ", str(list(the_dir.glob("*"))))
        print("told you so")
    #}
    """
    # TRY AND ZIP FOLDER
    try: #{
        # path to folder which needs to be zipped
        directory = zip_dir_path
        """
#}


"""
Copy/move all files matching creteria into TEMP folder
Then we zip the contents inside the TEMP folder in out_directory
"""
def create_custom_crate(): #{
    # RE-INSTANTIATE GLOBALS
    global root, in_directory, out_directory, zip_folder, df_batch
    # setup infile variable
    in_file = root.filename
    print("BATCH_LIST: \n" + str(in_file))
    # CREATE DATAFRAME FROM BATCH LIST
    df_batch = pd.read_csv(in_file, header=None, names=['Lot_No'], engine='python')
    print(df_batch.head(5))
    # create REGEX variable
    regex_glob = str(in_directory + "*")
    print(regex_glob)
    # TOTAL counter
    x = 0
    for lot_no in df_batch.itertuples(): #{
        logging.info("=======" + str(lot_no[1]) + "========")
        # CHECK AND CREATE NEW DIR PATH
        # [2019-10-10]... new_dir_path = os.path.join(out_directory, str(lot_no[1]))
        new_dir_path = os.path.join(zip_folder, str(lot_no[1]))
        # IF 'lot_no' DIRECTORY DOES NOT EXIST:
        if not os.path.exists(new_dir_path): #{
            # MAKE IT EXIST!
            os.makedirs(new_dir_path)
        #}
        # CREATE TEMP DIR/FOLDER TO WORK INSIDE OF:
        with tempfile.TemporaryDirectory() as directory_name: #{
            # create TEMP DIR var
            the_dir = Path(directory_name)
            logging.info("TEMP_DIRECTORY == " + str(the_dir))
            # GLOB AND ITERATE THRU EACH FILE NAME MATCHING
            for name in sorted(glob.glob(in_directory + "*" + str(lot_no[1]) + "*")): #{
                # CREATE PATH VARIABLE
                pdf_path = Path(str(name))
                logging.info("PDF_EXISTS == " + str(os.path.exists(pdf_path)))
                # GET BASE NAME (file name)
                file_name = os.path.basename(pdf_path)
                # CREATE TEMP PATH
                temp_path = os.path.join(the_dir, file_name)
                # CREATE NEW PATH
                new_path = os.path.join(new_dir_path, file_name)
                logging.info("NEW_PATH == " + str(new_path))
                # COPY FILE TO NEW LOCATION
                shutil.copy2(pdf_path, temp_path)
                # CREATE WATERMARK ON NEW FILE
                create_watermark(input_pdf=temp_path,
                                 output=new_path,
                                 watermark=watermark_pdf)
                # GET METADATA OF OLD ORIGINAL FILE
                old_stinfo = os.stat(pdf_path)
                logging.info("OLD FILE STATS: \n" + str(old_stinfo))
                old_atime = old_stinfo.st_atime
                logging.info("OLD FILE A-TIME: \n" + str(old_atime))
                old_mtime = old_stinfo.st_mtime
                logging.info("OLD FILE M-TIME: \n" + str(old_mtime))
                # CHANGE METADATA OF COPIED FILE TO ORIGINAL
                os.utime(new_path, (old_atime, old_mtime))
                # increase count
                x += 1
        #}
    #}
    logging.info("count == " + str(x))
    logging.info("Directory exits after?", str(the_dir.exists()))
    logging.info("Contents After:", str(list(the_dir.glob("*"))))
    logging.info("told you so")
#}

# [2019-09-23]... commented out below for fixes
"""
def custom_cofa_crate():  # {
    global out_directory, df_batch, root
    logging.info("<<BEGIN CUSTOM_CRATE>>")
    # CREATE INDEX
    idx = pd.Index(df_batch[0])
    logging.info(idx)
    index_list = []
    # CREATE INDEX
    for row in df_batch.itertuples(name='CofA'):  #{
        # PDF NAME = PART_NO + LOT_NO
        logging.info(row[0])
        pdf_name = str(row[1] + "@" + row[2] + ".pdf")
        logging.info(pdf_name)
        # print(row[1])
        # print(row[2])
        # APPEND ITEM TO LIST
        index_list.append(row[1])  # WAS: pdf_name
    #}
    logging.info(index_list)
    # CREATE SERIES OFF OF LIST
    i1 = pd.Series(index_list)
    i1.astype(dtype=np.str)
    idx = pd.Index(i1)
    logging.info(idx)
    # DETERMINE IF WE ARE PULLING ALL CofAs OR MOST RECENT ONLY
    if check_var == 1:  # {
        logging.info("PULLING MOST RECENT CofA(s)")
        # CALL FUNCTION TO PULL MOST RECENT
        pull_recent_cofas()
    # }
    elif check_var == 2:  # {
        logging.info("PULL ALL APPLICABLE CofA(s)")
    # }
    # TRY THE FOLLOWING
    try:  # {
        # counter-baby
        x = 0 # number of PDFS matched
        count = 0 # total number of files
        ## CREATE TEMPORARY DIR TO WORK INSIDE OF ##
        with tempfile.TemporaryDirectory() as directory_name: #{
            the_dir = Path(directory_name)
            logging.info("TEMP_DIRECTORY == " + str(the_dir))
            # ITERATE THROUGH DIRECTORY/DIRECTORY
            for root, dirs, files in os.walk(in_directory): #{
                # DIRECTORY SKIP CONDITIONS
                if 'Archive ERR' in dirs: #{
                    dirs.remove('Archive ERR') # don't visit Archive ERR directories
                #}
                if 'Arhive - For all archive CofA, see G CofA folder' in dirs: #{
                    dirs.remove('Archive - For all archive CofA, see G CofA folder') # skip
                #}
                if 'Instruction Sheets' in dirs: #{
                    dirs.remove('Instruction Sheets') # skip
                #}
                # OTHERWISE IF THERE ARE FILES IN DIRECTORY
                for f in files: #{
                    # IF FILE IS OF TYPE .pdf
                    if fnmatch.fnmatch(f, "*.pdf"): #{
                        # ASSEMBLE!
                        file_path = os.path.join(root, f)
                        # << PERFORM STR OPERATIONS >>
                        test_path = Path(file_path)
                        the_str = str(file_path)
                        the_len = len(the_str)
                        idx_mrk = f.find('@', 0, len(f))
                        pn_str = str(f[idx_mrk:len(f)-4])
                        logging.info("PN-STR == " + str(pn_str))
                        ########################################
                        # COMPARE CURRENT FILE TO INDEX
                        if idx.contains(pn_str) is True: #{
                            logging.info("\n OMG TRUE! \n")
                            logging.info("old path == " + str(test_path))
                            logging.info("temp path == " + str(os.path.join(the_dir, f)))
                            logging.info("new path == " + str(os.path.join(out_directory, f)))
                            temp_path = os.path.join(the_dir, f)
                            new_path = os.path.join(out_directory, f)
                            # COPY FILE TO NEW LOCATION
                            shutil.copy2(test_path, temp_path)
                            # CREATE WATERMARK FILE
                            create_watermark(input_pdf=temp_path,
                                             output=new_path,
                                             watermark=watermark_pdf)
                            x += 1
                        #}
                    #}
                    # ELSE // NOT A PDF
                    else: #{
                        logging.info(str(f) + " NOT A .PDF!")
                    #}
                #}
            #}
        #}
        # BEGIN TO MOVE FILES INTO ZIP FOLDER
        for name in sorted(glob.glob(out_directory + "*")): #{
            logging.info(name)
            logging.info("FROM == " + (str(out_directory) + " TO == " + str(zip_folder)))
        #}
        # path to folder which needs to be zipped
        directory = Path(zip_folder) # WAS: directory = "."

        # calling function to get all file paths in the directory
        file_paths = get_all_file_paths(directory)

        # printing the list of all files to be zipped
        logging.info('Following files will be zipped:')
        for f_name in file_paths:
            logging.info(f_name)

            # writing files to a zipfile
        with ZipFile('my_python_files.zip', 'w') as zip:
            # writing each file one by one
            for file in file_paths:
                zip.write(file)

        logging.info('All files zipped successfully!')
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
        logging.info("\n" + typeE +
              "\n" + fileE +
              "\n" + lineE +
              "\n" + messageE)
    # }
    else:  # {
        logging.info("[CRATE-CREATION] FIN...")
    # }
# }
"""

def test_messagebox():  # {
    global out_directory
    messagebox.showinfo(title="test",
                        message="RADIO BUTTON VALUE == "
                                + str(check_var.get())
                                + "\nout_directory == "
                                + str(out_directory),
                        parent=root)
# }

if __name__ == "__main__": #{
    # SETUP LOGGER
    try: #{
        logging.basicConfig(level=logging.INFO,
                           format='%(asctime)s : %(message)s',
                           datefmt='%Y-%m-%d-%H%M%S',
                           filemode='a')  #stream=sys.stdout)
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
        logging.info("[SETUP-LOGGER] SUCCESS! VERY NICE! ")
    #}
    ##################################################
    # INSTANTIATE GLOBAL VARIABLES
    root = tk.Tk()
    selected_batch_list = False
    selected_zip_folder = False
    e1_var = tk.StringVar()
    e2_var = tk.StringVar()
    check_var = tk.IntVar()
    # GET/SET ORIGINAL WORKING DIRECTORY PATH
    og_wd = Path(os.getcwd())
    print("WD: \t" + str(og_wd))
    in_directory = "F:/APPS/CofA/"
    check_directory = "G:/C of A's/#Email Node/"
    watermark_pdf = "C:/data/inbound/02OTHER_Rohde Island_Agilent Quality_Digital Letterhead.pdf"
    zip_folder = "."
    out_directory = "."
    # create empty dataframe as placeholder
    df_batch = pd.DataFrame(data=None, columns=None)
    ##################################################
    # MAIN APP PROPERTIES
    # [2019-10-09]... root = tk.Tk()
    root.title('CofA_Custom_Crate')
    root.geometry('552x282+250+250')
    root.minsize(width=474, height=282)  # WAS: (width=375, height=275)
    root.maxsize(width=552, height=450)  # WAS: (width=False, height=False)
    root.resizable(width=True, height=True)
    b1 = tk.Button(master=root)
    ###########################################################################################
    # TOP FRAME
    topframe = tk.Frame(master=root)
    topframe.pack(expand=1, fill=tk.BOTH, side=tk.TOP)

    e1_str = "<<INSERT BATCH LIST FILE HERE>>"
    e1_var.set(e1_str)

    # E1
    e1 = tk.Entry(master=topframe,
                  width=35,
                  textvariable=e1_var,
                  relief=tk.GROOVE,
                  cursor="rightbutton")
    e1.place(x=50, y=5, height=25, width=200)  # WAS: (height=30, width=200, x=50, y=20)

    # B1
    b1 = tk.Button(master=topframe, width=30,
                   text="Browse for BATCH_LIST",
                   font=("Sourcecode Semibold", 10),
                   command=select_batch_list,
                   relief=tk.GROOVE, cursor="pirate")
    b1.place(x=300, y=5, height=25, width=150)  # WAS: (height=30, width=100, x=250, y=20)
    # b1.config(command=test_messagebox)

    ##########################################################################################3
    # BOTTOM FRAME
    bottomframe = tk.Frame(master=root)
    bottomframe.pack(expand=1, fill=tk.BOTH, side=tk.BOTTOM)

    e2_str = "<<INSERT (to) ZIP FOLDER HERE>>"  # WAS: "C:/"
    e2_var.set(e2_str)

    # E2
    e2 = tk.Entry(master=bottomframe, width=20, textvariable=e2_var)
    e2.place(x=50, y=5, height=25, width=200)  # WAS: (x=50, y=30, height=30, width=200)

    # B2
    b2 = tk.Button(master=bottomframe, width=30,
                   text="Browse for ZIP Dir",
                   state=tk.DISABLED,
                   font=("Sourcecode Semibold", 10),
                   command=select_zip_folder,
                   relief=tk.GROOVE, cursor="spider")
    b2.place(x=300, y=5, height=25, width=150)  # WAS: (x=250, y=30, height=30, width=100)

    # CONFIRM BUTTON /b3
    b3 = tk.Button(master=bottomframe,
                   text="Confirm",
                   width=10,
                   state=tk.DISABLED,  # if b1_var.get() == False else tk.ENABLED,
                   font=("Sourcecode Semibold", 12),
                   command=create_custom_crate,  # WAS: custom_cofa_crate
                   relief=tk.RAISED, cursor="sb_down_arrow")
    b3.place(x=50, y=50, height=25, width=100)

    # CANCEL BUTTON /b4
    b4 = tk.Button(master=bottomframe, text="Cancel", width=10,
                   font=("Sourcecode Semibold", 12), command=root.destroy,
                   relief=tk.RAISED, cursor="circle")

    b4.place(x=150, y=50, height=25, width=100)

    # CHECK BUTOTNS FOR ( most recent / all ) SELECTION TYPES
    # CheckVar1 = tk.IntVar()
    # CheckVar2 = tk.IntVar()
    R1 = tk.Radiobutton(master=bottomframe, text="Most Recent CofA(s)", font=("Sourcecode Light", 12),
                        variable=check_var, value=1, state=tk.DISABLED, command=test_messagebox)
    R1.place(x=250, y=35, height=50, width=200)
    R2 = tk.Radiobutton(master=bottomframe, text="Return All CofA(s)", font=("Sourcecode Light", 12),
                        variable=check_var, value=2, state=tk.DISABLED, command=test_messagebox)
    R2.place(x=250, y=85, height=50, width=200)

    root.config()
    root.mainloop()
    ##################################################
    """
    App()
    """
    ##################################################
#}