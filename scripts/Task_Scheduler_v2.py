"""
Created on September 18, 2019 at 01:40 PM - DB
Edited/Semi-Finalized on September 23, 2019 at 09:51 AM - DB
** NEEDS TO BE EDITED FOR ANY COMMAND INPUT !! **

"""

# IMPORT THE GOODS
import os, sys, time
from time import sleep
from pathlib import Path
import logging, subprocess
from threading import Timer
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk
import pandas as pd
import numpy as np
from pandas import Series, DataFrame

class Task_Scheduler(): #{

    def __init__(self, name, command_path, scheduled_time): #{
        self.name = name
        self.command_path = command_path
        self.scheduled_time = scheduled_time
    #}

    def begin_loop(self): #{
        logging.info("DESIRED HOUR (24 hour):\t" + str(self.scheduled_time))
        # GET/SET HOUR
        the_hour = int(self.scheduled_time)
        logging.info("DESIRED HOUR (12 hour):\t" + str(int(the_hour - 12)))
        while 1 == 1: #{
            time_now = pd.Timestamp.now()
            logging.info("TIME NOW:\t\t\t" + str(time_now))
            # CHECK IF PASSED (currently on) HOUR
            if time_now.hour == the_hour: #{
                logging.info("ITS PASSED " + str(the_hour) + "! !")
                # CREATER COUNTER
                x = 0
                # RUN EVERY COMMAND IN THE COMMAND LIST WITH 60 SECOND INTERVALS
                for cmd in self.command_path: #{
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
                #}
                logging.info("NUM OF CMDS:\t\t\t" + str(int(x)))
                break
            #}
            else: #{
                logging.info("ITS NOT PASSED " + str(the_hour) + ":") # + str(the_min) + "! !")
                # SLEEP FOR A MIN
                countdown(60)
            #}
        #}
	#}

    def check_task_status(self): #{
        pass
    #}
#}

def countdown(n): #{
    while n > 0: #{
        logging.info(n)
        sleep(1) # sleep for 1 second
        n -= 1
    #}
    else: #{
        logging.info("BLAST OFF!")
    #}
#}

def main(): #{
    # TRY THE FOLLOWING:
    try:  # {
        # Create list variable to hold COMMANDS & to insert into class function
        cmd_list = [
            Path("C:/EXE/CofA_F_Scanner.exe"),
            Path("C:/EXE/CofA_G_Scanner.exe"),
            Path("C:/EXE/CofA_Nightly_Node_v3.exe")
        ]
        # Create an object from the class
        CofA_Task = Task_Scheduler(name="CofA_Nightly_Node", command_path=cmd_list, scheduled_time=21)
        # Now we can work with the object
        logging.info(str(CofA_Task.name))
        CofA_Task.begin_loop()
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
    finally:  # {
        # WAIT ANOTHER HOUR THEN RECURSIVE CALL TO GO AGAIN!
        countdown(3600)
        main()
    # }
# }

if __name__ == "__main__": #{
    # SETUP LOGGER
    try:  # {
        logging.basicConfig(level=logging.INFO,
                            format="%(asctime)s : %(message)s",
                            datefmt='%Y-%d-%m-%H%M%S',
                            filemode='a')
    #
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
    else: #{
        logging.info("[Setup-Logger] SUCCESS! VERY NICE!")
    # }
    # INSTANTIATE GLOBAL VARIABLES
    if len(sys.argv) > 1:  # {
        print(str(sys.argv))
    # }
    # CALL MAIN FUNCTION
    main()
#}