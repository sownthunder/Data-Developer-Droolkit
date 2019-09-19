"""
Created on September 19 at 11:04 AM - Derek Bates
command-line program that checks to see **INPUT** time has passed
if has not yet passed it will loop EVERY MINUTE until it has.
Once the time has passed.... the specific function, or functions,
specified in the **SECOND** command-line agrument... will be called.


"""

# IMPORT THE GOODS
import os, sys, time
from time import sleep
from pathlib import Path
import logging
from threading import Timer
from subprocess import Popen
import pandas as pd
import numpy as np
from pandas import Series, DataFrame

# DEFINE CLASSE(S)
class taskScheduler(): #{

    def __init__(self, name, command_path, scheduled_time):  # {
        self.name = name
        self.command_path = command_path
        self.scheduled_time = scheduled_time
    # }

    def begin_loop(self):  # {
        logging.info("DESIRED HOUR (24 hour):\t" + str(self.scheduled_time))
        # GET/SET HOUR
        the_hour = int(self.scheduled_time)
        logging.info("DESIRED HOUR (12 hour):\t" + str(int(the_hour - 12)))
        while 1 == 1:  # {
            time_now = pd.Timestamp.now()
            logging.info("TIME NOW:\t\t\t" + str(time_now))
            # CHECK IF PASSED HOUR
            if time_now.hour >= the_hour:  # {
                logging.info("ITS PASSED " + str(the_hour) + "! !")
                # CREATER COUNTER
                x = 0
                # RUN EVERY COMMAND IN THE COMMAND LIST WITH 60 SECOND INTERVALS
                for cmd in self.command_path:  # {
                    logging.info("COMMAND #" + str(x))
                    # RUN PROCESS
                    proc = subprocess.Popen(str(cmd))
                    logging.info(str(cmd))
                    # SLEEP FOR A MINUTE
                    countdown(60)
                    proc_status = str(proc.returncode)
                    logging.info("RETURNCODE:\t" + str(proc_status))
                    # INCREMENT COUNTER
                    x += 1
                # }
                break
            # }
            else:  # {
                logging.info("ITS NOT PASSED " + str(the_hour) + ":")  # + str(the_min) + "! !")
                # SLEEP FOR A MIN
                countdown(60)
            # }
        # }
    # }

    def check_task_status(self): #{
        pass
    #}

#}

# DEFINE FUNCTIONS
def countdown(n): #{
    while n > 0 : #{
        logging.info(n)
        sleep(1) # sleep for 1 second
        n -= 1
    #}
    else: #{
        logging.info("BLAST OFF!")
    #}
#}

def main(): #{
    # RE-INSTANTIATE GLOBALS
    global cmd_list
    # TRY THE FOLLOWING:
    try: #{
        #######################
        # BEGIN INFINITE LOOP #
        #######################
        while 1 == 1: #{
            # GET CURRENT TIME
            ts_now = pd.Timestamp.now()
            logging.info("CURRENT TIME:\t\t" + str(ts_now))
            ##############################################
            # COMPARE THE TWO
            ###############################################
            # if the input time_stamp is greater than the current one right now..
            if (test_ts > ts_now): #{
                # that means it hasnt happened yet...
                logging.info("\n\n\t"
                             + str(test_ts)
                             + " HASN'T HAPPENED YET !! \n(it is: "
                             + str(ts_now)
                             + ")\n")
                # WAIT ANOTHER 60 SECONDS to check again...
                countdown(60)
            #}
            ###############################################
            # << HAS HAPPENED >>
            else: #{
                # that means it **HAS** happened...
                logging.info("\n\n\t"
                             + str(test_ts)
                             + " **HAS** HAPPENED !! \n(it is: "
                             + str(ts_now)
                             + ")\n")
                # CREATER COUNTER
                x = 0
                for command in cmd_list: #{
                    logging.info("COMMAND # " + str(x + 1) + "! !")
                    # RUN PROCESS
                    proc = Popen(str(command))
                    logging.info(str(command))
                    # SLEEP FOR A MINUTE
                    countdown(60)
                    proc_status = proc.returncode()
                    logging.info("RETURNCODE:\t" + str(proc_status))
                    # INCREMENT COUNTER
                    x +1
                #}
                break
            #}
        #}
        #####################
        # END INFINITE LOOP #
        #####################
    #}
    except SystemExit: #{
        print("noob")
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
    finally: #{
        # CALL AGAIN MAKING IT RECURSIVE
        main()
    #}
#}

if __name__ == "__main__": #{
    # SETUP LOGGER
    try: #{
        logging.basicConfig(level=logging.INFO,
                           format='%(asctime)s : %(message)s',
                           datefmt='%Y-%m-%d-%H:%M:%S',
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
        logging.error("\n" + typeE +
              "\n" + fileE +
              "\n" + lineE +
              "\n" + messageE)
    #}
    else: #{
        logging.info("[Setup-Logger] SUCCESS! VERY NICE!!")
    #}
    # INSTANTIATE GLOBAL VARIABLES
    logging.info("...checking arguments...")
    # IF THERE IS 1 OR MORE ARGUMENTS AT COMMAND-LINE:
    if len(sys.argv) > 1:  # {
        logging.info("ARGUMENTS ARE: \n")
        logging.info(str(sys.argv))
        # ASK FOR TIMESTAMP INPUT!
        test_input = input("enter timestamp please:\n")
        # CREATE TIMESTAMP FROM INPUT
        test_ts = pd.Timestamp(ts_input=str(test_input))
        logging.info("TIMESTAMP:\t\t" + str(test_ts))
        # SET COMMAND LIST TO BE EVERY ITEM IN LIST EXCEPT FOR FIRST SPOT (the script name)
        cmd_list = sys.argv[1:]
    # }
    # ELSE... no arguments!
    else:  # {
        logging.info("FAIL... will quit after ENTER...")
        end_str = input("press ENTER to end...")
        sys.exit(69)
    # }
    """
    # ASK FOR TIMESTAMP INPUT!
    test_input = input("enter timestamp please:\n")
    # CREATE TIMESTAMP FROM INPUT
    test_ts = pd.Timestamp(ts_input=str(test_input))
    logging.info("TIMESTAMP:\t\t" + str(test_ts))
    """
    # [2019-09-19]... ABOVE AND BELOW REMOVED for CofA
    """
    cmd_list = [
        "C:/EXE/CofA_F_Scanner.exe",
        "C:/EXE/CofA_G_Scanner.exe",
        "C:/EXE/CofA_Nightly_Node_v2.exe"
    ]
    """
    # CALL MAIN FUNCTION
    main()
# }