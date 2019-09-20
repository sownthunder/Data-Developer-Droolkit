"""
Created on May 29, 2019 at 01:51 PM - DB

We need your help on another project.
F:\APPS\CofA folder contains all CofAs in PDF. For any CofA’s that’s created after 03/23/2019, the following needs to be done.
	1. Copy these CofAs to G:\C of A's\#Email Node with the file name <part number>@<lot number>
	        (for example, DWM-580-1@0001234567 or DWM-580-1@CT-1234) as “part <part number> CofA Lot# <lot number”
	        (for example, part DWM-580-1 CofA Lot# 00012345677 or part DWM-580-1 CofA Lot# CT-1234)
	2. Apply the letterhead background to each CofA and save. The letterhead background is saved at:
	        G:\C of A's\#Templates\Agilent CofA Letterhead_03-21-19.pdf
	3. Email each separately with the subject as same as file name to agilent_cofa@agilent.com
	4. Next, we need this to be automated if possible for any created each day.

"""

# import the goodies
import os, sys, time
import datetime
from datetime import date
import platform
import xlrd
import shutil
import pandas as pd
import numpy as np
from pandas import Series, DataFrame
from pathlib import Path
from docx import Document
from docx.shared import Inches
from docx.shared import Pt
#from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.style import WD_STYLE_TYPE
import logging
import smtplib
from PyPDF2 import PdfFileWriter, PdfFileReader

########################################################
# GLOBAL VARS
global date_object, time_object
global inFile, inDirectory, outDirectory, outboundDirectory
# INSTANTIATE
date_object = datetime.date.today()
time_object = str('{0:%m_%d_%Y-%H%M%S}'.format(datetime.datetime.now()))
print("TIME-STAMP: " + str(time_object))
# PDF we will use for watermarking other PDFs
inFile = "C:/Temp/Agilent_CofA_Letterhead_03-21-19.pdf"
# WHERE WE WILL BE SCANNING FILES
inDirectory = "F:/APPS/CofA"
# (TESTING) WHERE COPIED FILES WILL MOVE TO
outDirectory = "C:/Temp/Cofa_Email_Node/"
# WHERE COPIED FILES WILL MOVE TO
outboundDirectory = "G:/C of A's/#Email Node/"
# TIME STAMP VAR for filter requirements
dateCheck = pd.Timestamp(year=2019, month=3, day=23, hour=0)
# FOR FUTURE USE
todayCheck = dateCheck.today()
print("date-check: " + str(dateCheck))
print("today-check: " + str(todayCheck))
#######################################################

def extract_information(pdf_path): #{
    with open(pdf_path, 'rb') as f:  #{
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

    print(txt)
    return information
#}

def create_watermark(input_pdf, output, watermark): #{
    try:  #{
        watermark_obj = PdfFileReader(watermark)
        watermark_page = watermark_obj.getPage(0)

        pdf_reader = PdfFileReader(input_pdf)
        pdf_writer = PdfFileWriter()

        # Watermark all the pages
        for page in range(pdf_reader.getNumPages()):  #{
            page = pdf_reader.getPage(page)
            page.mergePage(watermark_page)
            pdf_writer.addPage(page)
        #}

        with open(output, 'wb') as out:  #{
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
        print("\n" + typeE +
              "\n" + fileE +
              "\n" + lineE +
              "\n" + messageE)
        #}
    else: #{
        print("FIN...")
    #}
    return
#}

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

def scan_and_watermark(aDir): #{
    try: #{
        # counter-baby
        x = 0
        count = 0
        # iterate thru directory/directories
        for root, d_names, f_names in os.walk(aDir):  #{
            # if there are files in directory
            if len(f_names) >= 0:  # {
                # for each file <<PERFORM THE FOLLOWING ACTIONS>>
                for f in f_names:  # {
                    filepath = str(root) + "\\" + str(f)
                    testPath = Path(filepath)
                    theStr = str(filepath)
                    theLen = len(theStr)
                    # IF CURRENT FILE IS A .PDF
                    if theStr.rfind('.pdf', 0, theLen) != -1:  #{
                        createDate = creation_date(testPath)

                        # GET CREATE TIME
                        createTime = os.path.getctime(testPath)
                        # GET MODIFIED TIME
                        modifiedTime = os.path.getmtime(testPath)
                        # MAKE 'ctime' INTO DATETIME / more readable
                        readable_c = datetime.datetime.fromtimestamp(createTime).isoformat()
                        # MAKE 'mtime' INTO DATETIME / more readable
                        readable_m = datetime.datetime.fromtimestamp(modifiedTime).isoformat()
                        # CONVERT TO pandas.Timestamp
                        timeStamp_c = pd.Timestamp(readable_c)
                        # AGAIN FOR MODIFIED TIME
                        timeStamp_m = pd.Timestamp(readable_m)
                        # PRINT
                        print("\n\t F == " + str(f))
                        print("\t FILE-PATH == " + str(filepath))
                        print("\t C-TIME == " + str(createTime))
                        print("\n\t TIME-STAMP == " + str(timeStamp_c))
                        print("\t DATE-CHECK == " + str(dateCheck))
                        ## SUTBRACT TIME STAMPS / CREATE TIME-DELTA
                        td_c = pd.Timedelta(timeStamp_c - dateCheck)
                        print("\n\t T-C-DELTA == " + str(td_c.delta))
                        # create var that holds 'delta-C-days'
                        days_created = int(td_c.days)
                        ## SUTBRACT TIME STAMPS / CREATE TIME DELTA
                        td_m = pd.Timedelta(timeStamp_m - dateCheck)
                        print("\n\t T-M-DELTA == " + str(td_m.delta))
                        # create var that holds 'delta-M-days'
                        days_modified = int(td_m.days)
                        # TEST BY INDIVIDUAL VALS
                        print("\n" + "CREATION DATE " + str(timeStamp_c.month)
                              + "/"
                              + str(timeStamp_c.day)
                              + "/"
                              + str(timeStamp_c.year))
                        print("\n" + "MODIFIED DATE " + str(timeStamp_m.month)
                              + "/"
                              + str(timeStamp_m.day)
                              + "/"
                              + str(timeStamp_m.year))
                        ### SET BOOLEAN?
                        if int(td_c.days) > 0:  #{
                            if days_modified > 0: #{
                                print("CREATED AFTER 03/23/2019")
                                x += 1  # increase PDF-count
                                # PERFORM STRING OPERATIONS
                                #################################
                                idxMrk = f.rfind('@', 0, len(f))
                                half1 = str(f[0:idxMrk])
                                half2 = str(f[idxMrk+1:len(f)])
                                print("HALF 1 == " + half1)
                                print("HALF 2 == " + half2)
                                #  setup NEW FILE NAME (for copy)
                                newName = "part "
                                newName += str(half1)
                                newName += " CofA Lot# "
                                newName += str(half2)
                                print("NEW NAME == " + str(newName))
                                #################################
                                # PERFORM COPY SHIT ETC
                                # copy to outboundfolder
                                shutil.copy2(testPath, outDirectory + str(f))
                                # EXTRACT PDF INFORMATION
                                extract_information(testPath)
                                #################################
                                # CREATE WATERMARK ON NEW FILES
                                # (created in **desired** dir)
                                create_watermark(input_pdf=outDirectory + str(f),
                                                 output=outboundDirectory + str(newName),
                                                 watermark=inFile)
                                print("WATERMARKED!")
                            #}
                        #}
                        else:  #{
                            print("CREATED BEFORE 03/23/2019")
                        #}

                    #}
                    else:  #{
                        print("\t XXXX NOT A .PDF XXXX")
                    #}
                    # OLD#x += 1
                    # OLD#print("MOVED == " + str(x))
                    count += 1
                    print("\nTOTAL # of PDFS : " + str(x))
                    print("TOTAL # OF FILES : " + str(count))
                #}
            #}
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
        print("FIN...")
    #}
#}


def main(): #{
    print(str(time_object) + " BEGAN << CofA_Email_Node >>")
    scan_and_watermark(inDirectory)
    return
#}

if __name__ == "__main__":
    main()