"""
Created on May 07, 10:07 AM - DB
Modified on May 28, 09:11 AM - DB # INCLUDE SQLITE3
Modified on Nov 13, 02:46 PM - DB

USES:
(1) "multi_directory_scanning_SDS.py"
(2) "jupyter_multi_threads_SDS.ipynb"

<inbound>
(1) J:/controlled_docs/SDS/Agilent_SDS/
(2) J:/controlled_docs/SDS/ALL SDS's/
<outbound>
(1) C:/Temp/ (for logging)
(2) J:/controlled_docs/SDS/SDS Lists/
"""

# import the goodies
import xlrd
import os
import sys
import time
import datetime
# [2019-11-14]\\from datetime import date
from pathlib import Path
import pandas as pd
import numpy as np
from pandas import Series, DataFrame
import shutil
import re
import logging
import threading

import sqlite3

# GLOBAL variables
global start, end, logFile, logStr, exitFlag, time_object
global inDirectory, inDirectory_2, outDirectory, outboundDirectory

## Initialize VARS #####################
exitFlag = 0
inDirectory = "J:/controlled_docs/SDS/Agilent_SDS/"
inDirectory_2 = ""
outDirectory = "C:/Temp/"
outboundDirectory = "J:/controlled_docs/SDS/SDS Lists/"
date_object = datetime.date.today()
time_object = str('{0:%m_%d_%Y-%H%M%S}'.format(datetime.datetime.now()))
# CREATE TIME-STAMPS
print(str("START TIME:"), time_object)
now_time = datetime.datetime.now()
now_hour = str("%s" %now_time.hour )
now_minute = str("%s" %now_time.minute )
print("Current hour = " + str(now_hour))  # WAS: "Current hour = %s" %now_time.hour
print("Current minute = " + str(now_minute))  # WAS: "Current minute = %s" %now_time.minute
# START-TIME-TUPLE
start = (now_hour, now_minute)
############################################################################
############################################################################

class myThread (threading.Thread): #{
    def __init__(self, threadID, name, counter): #{
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
    #}
    def run(self): #{
        try: #{
            print("\n==================\n < Starting " + self.name + " > \n============================\n")
            print_time(self.name, self.counter, 5)
            # CHECK THREAD TYPE
            if self.name == "Scan-1": #{
                # SCAN DIRECTORY CHOICE 1
                dfTest = scanDirectory(False, "J:/controlled_docs/SDS/Agilent_SDS/")
                # EXPORT TO .CSV
                dfTest.to_csv(outDirectory + str(time_object) + "_popFrame_Agilent_SDS.csv", index=True)
                # COPY TO OUTBOUND DIRECTORY
                shutil.copy(outDirectory + str(time_object) + "_popFrame_Agilent_SDS.csv",
                            outboundDirectory + str(time_object) + "_SDS_Agilent_SDS.csv")
                # INSERT INTO DATABASE
                insert_df_into_db(dfTest)
            #}
            else: #{
                # SCAN DIRECTORY CHOICE 2
                dfTest = scanDirectory(False, "J:/controlled_docs/SDS/ALL SDS's/")
                # EXPORT TO .CSV
                dfTest.to_csv(outDirectory + str(time_object) + "_popFrame_ALL_SDS.csv", index=True)
                # COPY TO OUTBOUND DIRECTORY
                shutil.copy(outDirectory + str(time_object) + "_popFrame_ALL_SDS.csv",
                            outboundDirectory + str(time_object) + "_SDS_ALL_SDS_.csv")
                # INSERT INTO DATABASE
                insert_df_into_db(dfTest)
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
        print("EXITING " + self.name + " > \n=============================\n")
    #}

#}

def print_time(threadName, delay, counter): #{
    try: #{
        while counter:
            if exitFlag:  # {
                threadName.exit()
            # }
            time.sleep(delay)
            print("%s: %s" % (threadName, time.ctime(time.time)))
            counter -= 1
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
        print("[Print_Time] \t FIN...")
    #}
#}

"""
[RETURNS] : bool value:
>>>>> TRUE = is_single
>>>>> FALSE = is_multi
"""
def single_or_multi_dir(aDir):  # {

    # use OS module to determine if there are GREATER THAN 0 ROOTS (sub-folders)
    # IF SO: then this is a MULTi-DIR
    # IF NOT: then this is a single DIR

    # BOOL var for returning at end of function
    isSingle = False

    inDirectory = Path(aDir)
    # IF INPUT **IS** a dir
    if inDirectory.is_dir() is True:
        print("VERY NICE!! \t WORKING PATH! SUCCESS!")
        # get number of DIRS (if any)
        for root, d_names, f_names in os.walk(inDirectory):
            # if there is *AT LEAST* ONE directory
            if len(d_names) > 0:
                print("\t YES : **DOES** have multiple_dirs")
                isSingle = False
                print("DIR(s) : " + str(len(d_names)))
            else:
                print("\t NO : **DOES NOT** have multiple_dirs")
                isSingle = True
            # if there are files in directory
            if len(f_names) >= 0:
                print("FILES : " + str(len(f_names)))
                break
    else:
        print("NAUGHTY NAUGHTY! \t TRY AGAIN")
        # force loop that asks for input until CORRECT is given
        while inDirectory.is_dir is not True:
            inputty = input()
            inDirectory = Path(inputty)
            # RECURSIVE_CALL
            single_or_multi_dir(inDirectory)
            break
        ## FINALLY NOW HAVE A CORRECT DIR
        for root, d_names, f_names in os.walk(inDirectory):
            # if there is *AT LEAST* ONE directory
            if len(d_names) > 0:
                print("\t YES : **DOES** have multiple_dirs")
                isSingle = False
                print("DIR(s) : " + str(len(d_names)))
            else:
                print("\t NO : **DOES NOT** have multiple_dirs")
                isSingle = True
            # if there are files in directory
            if len(f_names) >= 0:
                print("FILES : " + str(len(f_names)))
                break

    return isSingle

# }

"""
gets the ORIGINAL META DATA OF FILE CREATION
"""
def get_creation_time(the_file_path): #{
    pass
#}
    
def setup_logger(): #{
    # TRY THE FOLLOWING
    try: #{
        logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s: %(message)s)',
                        filename='C:/data/outbound/SDS_SCAN_TEST.log',
                        filemode='w')
    #}
    except: #{
        pass
    #}
#}

"""
[RETURNS] : DataFrame containing list of:
>>>>> [File-Name], [Date-Created], [Language], [SDS-PN], MAYBE [Country]
***** NOT AUTOMATED OR UNIVERSAL RIGHT MEOW; FILE-PATH MUST BE HARD CODED
# CALLED LIKE:
# inDirectory == "J:/controlled_docs/SDS/Agilent_SDS/"
# dfFrame = scanDirectory( single_or_multi_dir(inDirectory), inDirectory)
"""
def scanDirectory(aBool, aDir): #{
    # set parameters
    isSingle = bool(aBool)
    inDirectory = Path(aDir)
    logStr = ""
    ########################### TRY #########################################
    try:  # {
        logStr += "BEGIN SCRIPT: < " + str(aDir) + " > "
        ##inDirectory_1 = Path("J:/controlled_docs/SDS/Agilent_SDS/")
        ##inDirectory_2 = Path("J:/controlled_docs/SDS/ALL SDS's/")
        # initalize variables
        outDirectory = "C:/Temp/"
        outboundDirectory = "J:/controlled_docs/SDS/SDS Lists/"
        # CREATE TIME STAMP FOR FILE CREATION NAME
        date_object = datetime.date.today()
        time_object = str('{0:%m_%d_%Y-%H%M%S}'.format(datetime.datetime.now()))  # _%S <--- FOR SECONDS
        logStr += "file naming convention (today's example) : " + str(time_object)
        ###########################
        ## LOG
        logStr += "outboundDirectory == " + str(outboundDirectory)
        #inDirectory = Path("J:/controlled_docs/SDS/Agilent_SDS/")
        logStr += "inDirectory == " + str(inDirectory) + "\n"
        isDirectory = inDirectory.is_dir()
        logStr += "is A Dir == " + str(isDirectory)
        # create list of String
        doc_list = os.listdir(inDirectory)
        ## LOG
        logStr += "length of [doc_list]: \n" + str(len(doc_list))
        # Create Series off list
        d1 = pd.Series(doc_list)
        d1.astype(dtype=np.str)
        # create a list to store the data
        pnList = []
        langList = []
        countryList = []
        fileList = []
        dateList = []
        ## LOG
        logStr += "...CREATING:[dataframe]...."
        testFrame = pd.DataFrame()
        #######################################################
        # counter-baby
        x = 0
        # iterate thru directory (SINGLE --OR-- MULTI)
        for root, d_names, f_names in os.walk(inDirectory):  # {
            print("<BEGIN_LOOP # " + str(x) + "> ======================================<> \n|")
            # if there are files in directory
            if len(f_names) >= 0:  # {
                # for each file <<PERFORM THE FOLLOWING ACTIONS>>
                for f in f_names:  # {
                    theStr = str(f)
                    theLen = len(theStr)
                    logging.info(str(root) + "\\" + "_PART_NO_.PDF")
                    print(str(root) + "\\" + "_PART_NO_.PDF")
                    # SUB-STR OPERATIONS FOR SDS-PN
                    logging.info(str(root) + "\\" + theStr + "\n")
                    print(str(root) + "\\" + theStr + "\n")
                    indexMrk = theStr.find('_', 0, theLen)  # first _ underscore
                    logging.info("\t ROOT == " + str(root))
                    print("\t ROOT == " + str(root))
                    pnStr = str(theStr[0:indexMrk])
                    print("| SDS-PN == " + pnStr)
                    logging.info("| SDS-PN == " + pnStr)
                    pnList.append(pnStr)
                    ################################################
                    ##   SUB STR OPERATIONS FOR LANGUAGE & LANG   ##
                    # == GET COUNTRY STR BY SEARCHING "rFind" from #
                    # == starting point of SDS-PN index location   #
                    ################################################
                    countryIndexMrk = root.rfind('\\', 0, len(root))
                    logging.info(("* indexMark == " + str(countryIndexMrk)))
                    print("* indexMark == " + str(countryIndexMrk))
                    countryStr = str(root[countryIndexMrk + 1:len(root)])
                    logging.info("| COUNTRY == " + countryStr)
                    print("| COUNTRY == " + countryStr)
                    countryList.append(countryStr)
                    ## SUB STR OPERATIONS FOR LANGUAGE & LANG
                    ########## REGULAR EXPRESSIONS ###########
                    searchObj = re.search(r'_\D\D\D\D\D\D_', theStr, re.M | re.I)
                    if searchObj is not None:  # {
                        langStr = str(searchObj.group())
                        print("| Country (lang) == " + langStr)
                        langList.append(langStr)
                        ## CREATION DATE OPERATIONS
                        # [2019-11-13]\\testPath = Path(str(root) + "\\" + str(f))
                        testPath = os.path.join(root, f)
                        # [2019-11-14]\\the_date = os.path.getctime(testPath)
                        the_date = os.path.getmtime(testPath)
                        # FORMAT DATE & SET AS STR
                        dateStr = str(datetime.date.fromtimestamp(the_date))
                        logging.info("M-DATE: " + dateStr)
                        print("M-DATE: " + dateStr)
                        dateList.append(dateStr)
                        # increment counter ??
                        x = x + 1
                    # }
                    else:  # {
                        # NO LANGUAGE FOUND
                        print("\t NO-LANGUAGE-FOUND-AT: " + str(x) + " ! \n")
                        print("\t <= TRYING AGAIN => \n")
                        # trying again with *LONGER* regex search
                        searchObj = re.search(r'_\D\D\D\D\D\D\D\D\D_', theStr, re.M | re.I)
                        if searchObj is not None:  # {
                            print("\t ==FOUND== \n")
                            # re-initialize
                            langStr = str(searchObj.group())
                            print("| Country (lang) == " + langStr)
                            langList.append(langStr)
                            ## CREATION DATE OPERATIONS
                            # [2019-11-13]\\testPath = Path(str(root) + "\\" + str(f))
                            testPath = os.path.join(root, f)
                            # [2019-11-14]\\the_date = os.path.getctime(testPath)
                            the_date = os.path.getmtime(testPath)
                            # FORMAT DATE & SET AS STR
                            dateStr = str(datetime.date.fromtimestamp(the_date))
                            logging.info("M-DATE: " + dateStr + "\n")
                            print("M-DATE: " + dateStr + "\n")
                            dateList.append(dateStr)
                            # increment counter ??
                            x = x + 1
                        # }
                        else:  # {
                            # NO LANGUAGE FOUND
                            print("\t AGAIN! NO-LANGUAGE-FOUND-AT: " + str(x) + " ! \n")
                            print("\t <== TRYING (2ndToLast) TIME => \n")
                            # trying again with "shorter" regex search
                            searchObj = re.search(r'_\D\D\D\D\D\D\D_', theStr, re.M | re.I)
                            if searchObj is not None:  # {
                                print("\t ==FOUND== \n")
                                # re-initialize
                                langStr = str(searchObj.group())
                                print("| Country (lang) == " + langStr)
                                langList.append(langStr)
                                ## CREATION DATE OPERATIONS
                                # [2019-11-13]\\testPath = Path(str(root) + "\\" + str(f))
                                testPath = os.path.join(root, f)
                                # [2019-11-14]\\the_date = os.path.getctime(testPath)
                                the_date = os.path.getmtime(testPath)
                                # FORMAT DATE & SET AS STR
                                dateStr = str(datetime.date.fromtimestamp(the_date))
                                logging.info("M-DATE: " + dateStr + "\n")
                                print("M-DATE: " + dateStr + "\n")
                                dateList.append(dateStr)
                                # increment counter ??
                                x = x + 1
                            # }
                            else:  # {
                                # NO LANGUAGE FOUND
                                print("\t NO-LANGUAGE-FOUND-AT: " + str(x) + " ! \n")
                                print("\t <=== TRYING LAST TIME => \n")
                                # trying again with "longer" regex search
                                searchObj = re.search(r'_\D\D\D\D\D\D\D\D_', theStr, re.M | re.I)
                                if searchObj is not None:  # {
                                    print("\t ==FOUND== \n")
                                    # re-initialize
                                    langStr = str(searchObj.group())
                                    print("| Country (lang) == " + langStr)
                                    langList.append(langStr)
                                    ## CREATION DATE OPERATIONS
                                    # [2019-11-13]\\testPath = Path(str(root) + "\\" + str(f))
                                    testPath = os.path.join(root, f)
                                    # [2019-11-14]\\the_date = os.path.getctime(testPath)
                                    the_date = os.path.getmtime(testPath)
                                    # FORMAT DATE & SET AS STR
                                    dateStr = str(datetime.fromtimestamp(date))
                                    print("M-DATE: " + dateStr + "\n")
                                    logging.info("M-DATE: " + dateStr + "\n")
                                    dateList.append(dateStr)
                                    # increment counter ??
                                    x = x + 1
                                # }
                                else:  # {
                                    # NO LANGUAGE FOUND (gave up)
                                    print("\t *** NOT FOUND ***")
                                    langStr = "ERROR"
                                    langList.append(langStr)
                                    ## CREATION DATE OPERATIONS
                                    # [2019-11-13]\\testPath = Path(str(root) + "\\" + str(f))
                                    testPath = os.path.join(root, f)
                                    # [2019-11-14]\\the_date = os.path.getctime(testPath)
                                    the_date = os.path.getmtime(testPath)
                                    # FORMAT DATE & SET AS STR
                                    dateStr = str(datetime.date.fromtimestamp(the_date))
                                    logging.info("M-DATE: " + dateStr + "\n")
                                    print("M-DATE: " + dateStr + "\n")
                                    dateList.append(dateStr)
                                    x = x + 1
                                # }
                            # }
                        # }
                    # append file NAME (root + f?)
                    file_name = os.path.join(root, f)
                    fileList.append(str(file_name))
                    # [2019-11-13]\\fileList.append(str(root) + "\\" + str(f))
                    # }
                # }
            # }
            else:
                # no files
                print("\t NO-FILE!")

        # }
        # Creation Column(s) from list(s)
        testFrame['SDS-PN'] = pnList
        testFrame['Country'] = countryList
        testFrame['Langauge'] = langList
        testFrame['Creation'] = dateList
        testFrame['File'] = fileList

        print("LENGTHS: \n\n "
              + "pnList == "
              + str(len(pnList))
              + "\t countryList == "
              + str(len(countryList))
              + "\t\n\n langList == "
              + str(len(langList))
              + "\t\t dateList == "
              + str(len(dateList))
              + "\t\n\n DOC_LIST == "
              + str(len(doc_list))
              + "\t\t fileList == "
              + str(len(fileList)))

        ###
        ## LOG
        logStr += "LENGTHS: \n\n " \
                  + "pnList == " \
                  + str(len(pnList)) \
                  + "\t countryList == " \
                  + str(len(countryList)) \
                  + "\t\n\n langList == " \
                  + str(len(langList)) \
                  + "\t\t dateList == " \
                  + str(len(dateList)) \
                  + "\t\n\n DOC_LIST == " \
                  + str(len(doc_list)) \
                  + "\t\t fileList == " \
                  + str(len(fileList))
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
        print("[SDS-PN] : FIN...")
        return testFrame  # RETURN DATAFRAME TO BE CREATED AS CSV IN main()
    #}

#}

def countdown(n): #{
    while n > 0: #{
        print(n)
        time.sleep(1) # sleep for 1 second
        n = n - 1
        if n == 0: #{
            print("BLAST OFF!")
            break;
        #}
    #}
    return
#}

def insert_df_into_db(aDataFrame): #{
    try: #{
        print("TESTING database insert")
        # CONNECT TO DATABASE
        cnxn = sqlite3.connect(outDirectory + 'SDS_scans.db')
        aDataFrame.to_sql(name="Scans", con=cnxn, if_exists="append",
                          index=False, chunksize=1000)
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

def main(): #{
    countdown(3)
    # initiate log string
    logStr = ""
    try: #{
        """
        # is DIR alone or many ?
        testBool = single_or_multi_dir("J:/controlled_docs/SDS/Agilent_SDS/")
        print("BEGIN SCRIPT : < SDS_scan.py >")
        # call scan function returned as DataFrame
        dfTest = scanDirectory(testBool, "J:/controlled_docs/SDS/Agilent_SDS/")
        # create DataFrame as .CSV
        dfTest.to_csv(outDirectory + str(time_object) + ".csv")
        """
        # Create new threads
        scan1 = myThread(1, "Scan-1", 1)
        scan2 = myThread(2, "Scan-2", 2)
        # testBool = single_or_multi_dir("")
        print("BEGIN SCRIPT : < SDS_scan.py >")
        # Start new Threads
        scan1.start()
        scan2.start()
        scan1.join()
        scan2.join()
        # call scan function returned as DataFrame
        # OLD#dfTest = scanDirectory(False, "J:/controlled_docs/SDS/Agilent_SDS/")
        # create DataFrame as .CSV
        # OLD#dfTest.to_csv(outDirectory + str(time_object) + ".csv", index=False)
        print("Exiting Main Thread")
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
        # RE-TIME-STAMP
        now_time = datetime.datetime.now()
        now_hour = str("%s" % now_time.hour)
        now_minute = str("%s" % now_time.minute)
        print("Current hour = " + str(now_hour))  # WAS: "Current hour = %s" %now_time.hour
        print("Current minute = " + str(now_minute))  # WAS: "Current minute = %s" %now_time.minute
        end = (now_hour, now_minute)
        print("END TIME: " + str(end))
        print("FIN...")
    #}


    print("<COUNTING DOWN>")
    countdown(3)
    return
#}

if __name__ == "__main__":
    setup_logger()
    main()