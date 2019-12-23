"""
Created on May 07, 10:07 AM - DB
Modified on May 28, 09:11 AM - DB # INCLUDE SQLITE3

USES:
(1) "single_directory_scanning_SDS.py"
(2) "pdf_cofa.ipynb" / "jupyter_multi_threads_SDS.ipynb"

<inbound>
(1) F:/APPS/CofA/
(2) J:/controlled_docs/CofA/
<outbound>
(1) C:/Temp/ (for logging)
(2) J:/controlled_docs/CofA/CofA Lists/
"""

# import the goodies
import xlrd
import os
import sys
import time
import datetime
from datetime import date
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

## Initalize VARS ######################
exitFlag = 0
inDirectory = "F:/APPS/CofA/"
inDirectory_2 = ""
outDirectory = "C:/Temp/"
outboundDirectory = "J:/controlled_docs/CofA/CofA Lists/"
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
            if self.name == "Scan-1":  # {
                # SCAN DIRECTORY CHOICE 1
                dfTest = scanDirectory(False, "F:/APPS/CofA/")
                # EXPORT TO .CSV
                dfTest.to_csv(outDirectory + str(time_object) + "_popFrame_CofA_F.csv", index=True)
                #  COPY TO OUTBOUND DIRECTORY
                shutil.copy(outDirectory + str(time_object) + "_popFrame_CofA_F.csv",
                            outboundDirectory + str(time_object) + "_CofA_F_Lists.csv")
                # INSERT INTO DATABASE
                insert_df_into_db(dfTest)
            # }
            else:  # {
                # SCAN DIRECTORY CHOICE 2
                dfTest = scanDirectory(False, "J:/controlled_docs/CofA/")
                # EXPORT TO .CSV
                dfTest.to_csv(outDirectory + str(time_object) + "_popFrame_CofA_J.csv", index=True)
                # COPY TO OUTBOUND DIRECTORY
                shutil.copy(outDirectory + str(time_object) + "_popFrame_CofA_J.csv",
                            outboundDirectory + str(time_object) + "_CofA_J_Lists.csv")
                # INSERT INTO DATABASE
                insert_df_into_db(dfTest)
            #}
            print("EXITING " + self.name + " > \n=============================\n")
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

#}

def print_time(threadName, delay, counter): #{
    try: #{
        while counter: #{
            if exitFlag: #{
                threadName.exit()
            #}
            time.sleep(delay)
            print("%s: %s" % (threadName, time.ctime(time.time())))
            counter -= 1
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
[RETURNS] : DataFrame containing list of:
>>>>> [File-Name] & [Date-Created]
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
    ########################### TRY #################################
    try: #{
        logStr += "BEGIN SCAN : < " + str(aDir) + " >"
        #inDirectory_1
        #inDirectory_2
        # initalize variables
        outDirectory = "C:/Temp/"
        outboundDirectory = "J:/controlled_docs/CofA/CofA Lists/"
        # CREATE TIME STAMP FOR FILE CREATION NAME
        date_object = datetime.date.today()
        time_object = str('{0:%m_%d_%Y-%H%M%S}'.format(datetime.datetime.now()))  # _%S <--- FOR SECONDS
        logStr += "file naming convention (today's example) : " + str(time_object) + "\n"
        ###########################
        ## LOG
        logStr += "outboundDirectory == " + str(outboundDirectory) + "\n"
        #inDirectory = Path("J:/controlled_docs/SDS/Agilent_SDS/")
        logStr += "inDirectory == " + str(inDirectory) + "\n"
        isDirectory = inDirectory.is_dir()
        logStr += "is A Dir == " + str(isDirectory) + "\n"
        # create list of String
        doc_list = os.listdir(inDirectory)
        ## LOG
        logStr += "length of [doc_list]: \n" + str(len(doc_list))
        # Create Series off list
        d1 = pd.Series(doc_list)
        d1.astype(dtype=np.str)
        # create a list to store the data
        fileList = []
        dateList = []
        ## LOG
        logStr += "...CREATING:[dataframe].... \n"
        testFrame = pd.DataFrame()
        print("=====LOG=====\n" + logStr)
        #######################################################
        destdir = Path(inDirectory)
        #######################################################
        # counter-baby
        x = 0
        # iteratre thru directory (SINGLE FOR CofA)
        for root, d_names, f_names in os.walk(inDirectory): #{
            print( "<BEGIN_LOOP # " + str(x) + "> ======================================<> \n|" )
            # if there are files in directory
            if len(f_names) >= 0: #{
                # for each file <<PERFORM THE FOLLOWING ACTIONS>>
                for f in f_names: #{
                    theStr = str(f)
                    theLen = len(theStr)
                    print(str(root) + "\\" + "_FILE_NAME_.PDF")
                    # SUB-STR OPERATIONS FOR FILE-NAME (CofA)
                    fileStr = str(root) + "\\" + theStr
                    print(str(root) + "\\" + theStr + "\n")
                    print("| FULL-PATH : " + str(root) + "\\" + theStr) #WAS: theStr
                    indexMrk = theStr.rfind('\\', 0, theLen)
                    print("| indexMrk (before shift): " + str(indexMrk))
                    indexMrk += 1  # add 1 to get proper index loc
                    fileStr = str(theStr[indexMrk:theLen])
                    print("| the file-name: " + fileStr)
                    fileList.append(fileStr)
                    ## CREATION DATE OPERATIONS
                    testPath = Path(str(root) + "\\" + str(f))
                    date = os.path.getctime(testPath)
                    dateStr = str(datetime.date.fromtimestamp(date))
                    print("C-DATE: " + dateStr + "\n")
                    dateList.append(dateStr)
                    print("{*} current count: " + str(x) + " {*} \n")
                    # OLD#print("string: " + theStr + "\n length: " + str(theLen) + "\n")
                    print("<END_LOOP #" + str(x) + "> =========================================<> \n")
                    # increment counter
                    x += 1
                #}
            #}
            else: #{
                print("\t NO-FILE!")
            #}
        #}
        # Creation Column(s) from list(s)
        testFrame['Creation'] = dateList
        testFrame['File'] = fileList

        print("LENGTHS: \n\n "
              + "dateList == "
              + str(len(dateList))
              + "\t fileList == "
              + str(len(fileList)))

        ###
        ## LOG
        logStr += "LENGTHS : \n\n "\
                  + "dateList =="\
                  + str(len(dateList))\
                  + "fileList == "\
                  + str(len(fileList))

        ######################################

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
        print("[CofA] : FIN...")
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
        # CONNECT  TO DATABASE
        cnxn = sqlite3.connect(outDirectory + 'CofA_scans.db')
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
        # Create new threads
        scan1 = myThread(1, "Scan-1", 1)
        scan2 = myThread(2, "Scan-2", 2)
        #testBool = single_or_multi_dir("")
        print("BEGIN SCRIPT : < CofA_scan.py >")
        # Start new Threads
        scan1.start()
        scan2.start()
        scan1.join()
        scan2.join()
        # call scan function returned as DataFrame
        #OLD#dfTest = scanDirectory(False, "F:/APPS/CofA/")
        # create DataFrame as .CSV
        #OLD#dfTest.to_csv(outDirectory + str(time_object) + ".csv", index=False)
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
        now_time = datetime.datetime.now()
        # RE-TIME-STAMP
        now_hour = str("%s" % now_time.hour)
        now_minute = str("%s" % now_time.minute)
        print("Current hour = " + str(now_hour))  # WAS: "Current hour = %s" %now_time.hour
        print("Current minute = " + str(now_minute))  # WAS: "Current minute = %s" %now_time.minute
        # END-TIME-TUPLE
        end = (now_hour, now_minute)
        print("END TIME: " + str(end))
        print("FIN...")

    #}


    print("<COUNTING DOWN>")
    countdown(3)
    return
#}

if __name__ == "__main__":
    main()