"""
Created on July 09, at 09:51 AM - DB
Modified on July 17, 09:52 AM - DB
Modified on Sep 20, 11:15 AM - DB

- takes in input file of PART_NUMBERS
- returns zipped file of watermarked pdfs
( that were in "batch_list" of PART_NOs)

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

###################################################################################################
# GLOBAL VARS
"""
global root, e1_var, e2_var, check_var
global in_directory, check_directory
global watermark_pdf
# OUT_DIRECTORY IS INSTANTIATED IN "select_zip_folder"
"""
###################################################################################################

def get_all_file_paths(directory): #{

    # initalizing empty file paths list
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

def select_batch_list(): #{
    # RE-INSTANTIATE GLOBALS
    global e1_var
    root.filename = filedialog.askopenfilename(initialdir=".", title="Select 'BATCH LIST'",
                                               filetypes=(("csv files", "*.csv"),
                                                          ("xlsx files", "*.xlsx"),
                                                          ("all files", "*.*")))
    logging.info(root.filename)
    e1_var.set(root.filename)
    # CREATE FILE_PATH FOR "BATCH_LIST"
    batch_path = Path(root.filename)
    display_batch_list(batch_path)
#}


def display_batch_list(file_path): #{
    # TOP LEVEL PROPERTIES
    top = tk.Toplevel(master=root)
    top.title('Crate-Batch-List:')
    top.geometry('300x450+550+300')
    top.resizable(width=False, height=False)

    # CREATE SCROLL BAR?
    scrollbar = tk.Scrollbar(master=top)
    scrollbar.pack( side = tk.RIGHT, fill = tk.Y)

    # CREATE LISTBOX
    Lb1 = tk.Listbox(master=top, yscrollcommand=scrollbar.set)

    ## CHECK FILE TYPE
    file_str = str(file_path)
    # IF EXCEL FILE
    global batch_df
    if fnmatch.fnmatch(file_str, "*.xlsx"): #{
        logging.info(str(file_str) +  " == .EXCEL FILE!")
        # GLOBAL VAR
        #global batch_df
        # READ IN AS .XLSX
        batch_df = pd.read_excel(file_path, sheetname=0)
        # FOR EACH PART_NO LISTED IN THE BATCH_FILE:
        for row in batch_df.itertuples(index=True, name="PART_NO"): #{
            # INSERT PART_NO
            Lb1.insert(int(row[0]+1), str(row[1]))
        #}
    #}
    elif fnmatch.fnmatch(file_str, "*.csv"): #{
        logging.info(str(file_str) + " == .CSV FILE!")
        # GLOBAL VAR
        #global batch_df
        # READ IN AS .CSV
        batch_df = pd.read_csv(file_path)
        # FOR EACH PART_NO LISTED IN BATCH_FILE:
        for row in batch_df.itertuples(index=True, name="PART_NO"): #{
            # INSERT PART_NO
            Lb1.insert(int(row[0]+1), str(row[1]))
        #}
    #}
    # PLACE COMPLETED LISTBOX
    Lb1.pack(side = tk.LEFT, fill = tk.BOTH)
    #Lb1.place(anchor=tk.CENTER, relx=0.5, rely=0.5)
    scrollbar.config( command = Lb1.yview )
#}

def select_zip_folder(): #{
    # RE-INSTANTIATE GLOBALS
    global out_directory
    global zip_folder
    global e2_var
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
    if not os.path.exists(new_dir_path): #{
        # MAKE IT EXIST!
        os.makedirs(new_dir_path)
    #}
    zip_folder = new_dir_path
    return
#}

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


def custom_cofa_crate():  # {
    global out_directory
    logging.info("<<BEGIN CUSTOM_CRATE>>")
    # CREATE INDEX
    idx = pd.Index(batch_df[0])
    logging.info(idx)
    index_list = []
    # CREATE INDEX
    for row in batch_df.itertuples(name='CofA'):  # {
        # PDF NAME = PART_NO + LOT_NO
        logging.info(row[0])
        pdf_name = str(row[1] + "@" + row[2] + ".pdf")
        logging.info(pdf_name)
        # print(row[1])
        # print(row[2])
        # APPEND ITEM TO LIST
        index_list.append(row[1])  # WAS: pdf_name
    # }
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

def test_messagebox():  # {
    global out_directory
    messagebox.showinfo(title="test",
                        message="RADIO BUTTON VALUE == "
                                + str(check_var.get())
                                + "\nout_directory == "
                                + str(out_directory),
                        parent=root)
# }

def main():  # {
    # RE-INSTANTIATE GLOBALS
    global root, e1_var, e2_var
    global check_var, in_directory, check_directory
    global watermark_pdf
    # SETUP LOGGER
    try:  # {
        logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s : \n\t\t\t\t\t[MSG] : %(message)s \n\t\t\t\t\t[LINE] : %(lineno)d',
                            datefmt='%Y-%m-%d-%H%M%S')
        # INCLUDED PRIOR: %(pathname) - %(filename)s - %(module)s
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
        logging.info("[SETUP-LOGGER] FIN...")
    # }
    # TRY THE FOLLOWING:
    try:  # {
        # MAIN APP PROPERTIES
        # root = tk.Tk()
        root.title('CofA_Custom_Crate')
        root.geometry('552x282+250+250')# WAS: ('375x275+250+250')
        root.minsize(width=474, height=282) # WAS: (width=375, height=275)
        root.maxsize(width=552, height=450) # WAS: (width=False, height=False)

        ###########################################################################################
        # TOP FRAME
        topframe = tk.Frame(master=root)
        topframe.pack(expand=1, fill=tk.BOTH, side=tk.TOP)

        e1_str = "<<INSERT BATCH LIST FILE HERE>>"  # WAS: "C:/"
        e1_var.set(e1_str)

        # E1
        e1 = tk.Entry(master=topframe, width=20, textvariable=e1_var)
        e1.place(x=50, y=5, height=25, width=200)  # WAS: (height=30, width=200, x=50, y=20)

        # B1
        b1 = tk.Button(master=topframe, width=20, text="Browse for BATCH_LIST", command=select_batch_list)
        b1.place(x=300, y=5, height=25, width=150) # WAS: (height=30, width=100, x=250, y=20)

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
        b2 = tk.Button(master=bottomframe, width=20, text="Browse for ZIP Dir", command=select_zip_folder)
        b2.place(x=300, y=5, height=25, width=150)  # WAS: (x=250, y=30, height=30, width=100)

        # CONFIRM BUTTON /b3
        b3 = tk.Button(master=bottomframe, text="Confirm", width=10,
                       font=("Courier New", 14), command=custom_cofa_crate)
        b3.place(x=50, y=50, height=25, width=100)

        # CANCEL BUTTON /b4
        b4 = tk.Button(master=bottomframe, text="Cancel", width=10,
                       font=("Courier New", 14), command=root.destroy)
        b4.place(x=150, y=50, height=25, width=100)

        # CHECK BUTOTNS FOR ( most recent / all ) SELECTION TYPES
        #CheckVar1 = tk.IntVar()
        #CheckVar2 = tk.IntVar()
        R1 = tk.Radiobutton(master=bottomframe, text="Most Recent CofA(s)",
                            variable=check_var, value=1, state=tk.DISABLED, command=test_messagebox)
        R1.place(x=250,y=35, height=50, width=200)
        R2 = tk.Radiobutton(master=bottomframe, text="Return All CofA(s)",
                            variable=check_var, value=2, state=tk.DISABLED, command=test_messagebox)
        R2.place(x=250, y=85, height=50, width=200)

        root.config()
        root.mainloop()
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
        error_output = "\n" + typeE + "\n" + fileE + "\n" + lineE + "\n" + messageE
        logging.error(str(error_output))
        # SHOW ERROR MESSAGEBOX
        messagebox.showerror(title="ERRPR !", message=str(error_output))
    # }
    else:  # {
        logging.info("[tkinter] FIN...")
    # }

# }

if __name__ == "__main__": #{
    # INSTANTAITE GLOBALS
    root = tk.Tk()
    e1_var = tk.StringVar()
    e2_var = tk.StringVar()
    check_var = tk.IntVar()
    in_directory = "F:/APPS/CofA/"
    check_directory = "G:/C of A's/#Email Node/"
    watermark_pdf = "C:/data/inbound/02OTHER_Rohde Island_Agilent Quality_Digital Letterhead.pdf"
    zip_folder = "."
    out_directory = "."
    main()
#}