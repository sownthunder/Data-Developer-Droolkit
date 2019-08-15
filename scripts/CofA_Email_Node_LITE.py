"""
Created on July 03, 2019 at 09:15 PM - DB
Modified on July 09, 2019 at 01:51 PM - DB
Modified on July 22, 2019 at 11:25 AM - DB


"""

# IMPORT THE GOODS
import os, sys, time
from time import sleep
from pathlib import Path
import fnmatch, glob, shutil
import tempfile, threading
import logging
import pandas as pd
import numpy as np
from pandas import Series, DataFrame
from PyPDF2 import PdfFileWriter, PdfFileReader

# GLOBAL VARS
global time_now, time_start, time_end, run_time
global in_directory, out_directory, archive_dir
# INSTANTIATE
time_start = pd.Timestamp.now()
in_directory = "C:/CofA/log/lists/"
out_directory = "G:/C of A's/#Email Node/"
archive_dir = "C:/CofA/"

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
        print("FIN...")
    # }
    return
# }

def create_new_filename(input_str): #{
    # filename as STR var "f"
    f = str(input_str)
    # PERFORM STR OPERTIONS #
    #########################
    idxMrk = f.rfind('@', 0, len(f))
    half1 = str(f[0:idxMrk])
    half2 = str(f[idxMrk + 1:len(f)])
    print("HALF 1 == " + half1)
    print("HALF 2 == " + half2)
    # SETUP NEW FILE_NAME (for copy)
    new_name = "part "
    new_name += str(half1)
    new_name += "CofA Lot# "
    new_name += str(half2)
    print("NEW NAME == " + str(new_name))
    # RETURN STR
    return new_name
#}

def main(): #{
    # CREATE LOGGER
    try: #{
        logging.basicConfig(level=logging.INFO,
                        filename="C:/CofA/log/Node_Mover_LITE.log",
                        format='%(asctime)s - %(message)s - %(lineno)s',
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
        print("[SETUP-LOGGER] FIN...")
    #}
    # TRY THE FOLLOWING:
    try: #{
        # SETUP IMPORTS
        watermark_pdf = "C:/data/inbound/02OTHER_Rohde Island_Agilent Quality_Digital Letterhead.pdf"
        # CREATE TODAYS DATE & YESTERDAYS DATE
        time_now = pd.Timestamp.now()
        time_str = str(time_now)
        # TODAYS DATE
        time_str = time_str[:10]
        logging.info(time_str)
        # SUBTRACTION DELTA
        subtraction_delta = pd.Timedelta(value=1, unit='days')
        logging.info(subtraction_delta)
        # YESTERDAYS DATE
        time_yesterday = time_now - subtraction_delta
        logging.info(time_yesterday)
        # SETUP STRING
        yesterstr = str(time_yesterday.date())
        logging.info(yesterstr)
        logging.info("GLOB OF DIR : \n" + str(os.listdir(in_directory)))
        # GLOB & PRELIMINARY SETUPS:
        df_previous = glob.glob("*" + yesterstr + "*")
        logging.info(df_previous)
        df_current = glob.glob("*" + time_str + "*")
        logging.info(df_current)
        # IMPORT AS DATAFRAMES
        # set as first element in returned list
        df1 = pd.read_csv(df_previous[0])
        # set as first element in returned list
        df2 = pd.read_csv(df_current[0])
        # SET DIFFERENCE OF TWO DATAFRAMES IN PANDAS PYTHON
        set_diff_df = pd.concat([df2, df1, df1]).drop_duplicates(keep=False)
        logging.info("LENGTH OF DIFF_DF: " + str(len(set_diff_df)))
        logging.info(set_diff_df)
        # ITERATE THRU TUPLES (using temp directory)
        # << WHILE INSIDE TEMP DIRECTORY >>
        with tempfile.TemporaryDirectory() as directory_name:  # {
            x = 0
            the_dir = Path(directory_name)
            logging.info("TEMPORARY DIRECTORY >>> " + str(the_dir))
            # ITERATE THRU DATAFRAME
            for row in set_diff_df.itertuples(index=False, name='CofA'):  # {
                logging.info("OLD-PATH: \t" + str(row[0]))
                old_path = Path(row[0])
                file_name = os.path.basename(row[0])
                logging.info("FILE-NAME: \t" + str(file_name))
                # CREATE 'ARCHIVE_PATH'
                archive_path = os.path.join(archive_dir, file_name)
                logging.info("ARCHIVE: \t" + str(archive_path))
                # COPY TO ARCHIVE_PATH
                shutil.copy2(src=old_path, dst=archive_path)
                # CREATE 'TEMP_PATH' FROM TEMP_DIR
                temp_path = os.path.join(the_dir, file_name)
                logging.info("Temp-PATH: \t" + str(temp_path))
                # COPY TO TEMP_PATH
                shutil.copy2(src=old_path, dst=temp_path)
                # CALL FUNCTON TO CREATE "new_name"
                new_name = create_new_filename(file_name)
                # CREATE 'new_path' by using "new_name"
                new_path = os.path.join(out_directory, new_name)
                logging.info("NEW-PATH: \t" + str(new_path))
                ## CALL WATERMARKED .PDF FUNCTION
                create_watermark(input_pdf=temp_path, output=new_path, watermark=watermark_pdf)
                x += 1
                logging.info("<<< COUNT == [" + str(x) + "] >>>")
            # }
            sleep(1)
        # }
        logging.info("Name of temp directory:", str(the_dir))
        logging.info("Directory exists after?", the_dir.exists())
        logging.info("Contents after:", list(the_dir.glob('*')))
        time_end = pd.Timestamp.now()
        run_time = time_end - time_start
        logging.info("TOTAL RUNTIME == " + str(run_time))
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
        logging.info("FIN...")
    #}
#}

if __name__ == "__main__": #{
    main()
#}
