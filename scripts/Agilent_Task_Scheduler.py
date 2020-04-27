# -*- coding: utf-8 -*-
"""
Created on Wed Apr 22 11:17:54 2020

Agilent_Task_Scheduler

USES:
    - CofA_Task_Scheduler_FINALE.py
    - Task_Scheduler_v2.py
    - Task_Scheduler_v3.py (v2 just renamed to v3)

@author: derbates
"""

# IMPORT THE GOODS
import os, sys, time
from time import sleep
from pathlib import Path
import logging, subprocess
from threading import Thread, Timer
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog, messagebox
from ttkthemes import ThemedStyle
import pandas as pd
import numpy as np
from pandas import Series, DataFrame

class Logger(): # {
    
    def __init__(self): # {
        pass
    # }
# }

class Agilent_Task_Scheduler(): # {
    
    user_name = str(os.getlogin()) # get username
    outbound_dir = "C:/data/outbound/" + str(pd.Timestamp.now())[:10]
    desktop_dir = "OneDrive - Agilent Technologies/Desktop"
    
    def __init__(self, root, the_logger): # {
        self.root = root
        self.root.title("Agilent Task Scheduler")
        self.root.geometry('315x200+300+300')
        self.root.resizable(width=True, height=True)
        # Get/Set USERNAME & DESKTOP DIRECTORIES
        self.desktop_folder = os.path.join(self.desktop_dir, str(pd.Timestamp.now())[:10])
        print(self.desktop_folder)
        if not os.path.exists(self.desktop_folder): # {
            # MAKE IT EXIST
            os.makedirs(self.desktop_folder)
        # }
        # OVERWRITE DESKTOP VAR
        self.desktop_dir = self.desktop_folder
        # INITIALIZE UI
        self.create_gui(the_root = self.root)
    # }
    
    def create_gui(self, the_root): # {
        # TRY THE FOLLOWING
        try: # {
            self.create_ttk_themes(the_root=the_root)
            self.create_label_frame(the_root=the_root)
            self.create_main_frame(the_root=the_root)
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
    # }
    
    def create_ttk_themes(self, the_root): # {
        # TRY THE FOLLOWING
        try: # {
            self.style = ThemedStyle(the_root)
            # STYLE THEME
            self.style.set_theme("blue")  # equilux
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
    # }
    
    def create_label_frame(self, the_root): # {
        # TRY THE FOLLOWING
        try: # {
            self.label_frame = ttk.Frame(master=the_root)
            self.label_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
            # TK VARIABLE TO HOLD IF WANT OUTPUTTED RESULTS TO CSV
            self.output_csv = tk.IntVar(master=the_root, value=0)
            # LABEL
            ttk.Checkbutton(master=self.label_frame, text="Output to .csv", 
                            variable=self.output_csv).pack()
        # }
        except: # {
            pass
        # }
    # }
    
    def create_main_frame(self, the_root): # {
        # TRY THE FOLLOWING
        try: # {
            self.main_frame = ttk.Labelframe(master=the_root)
            self.main_frame.pack(anchor=tk.CENTER, fill=tk.BOTH, expand=True)
            
            # IMPORT COMMAND LIST TO run thruough and execute
            self.import_button = ttk.Button(master=self.main_frame, text="Import COMMAND list",
                       command=self.import_command_list
                       )
            self.import_button.pack()
            
            # BEGIN EXECUTING COMMANDS (disabled at first)
            self.run_commands = ttk.Button(master=self.main_frame, text="RUN",
                                           command=self.begin_loop_in_thread, state=tk.DISABLED
                                           )
            self.run_commands.pack()
        # }
        except: # {
            pass
        # }
    # }
    
    def countdown(self, n): # {
        # TRY THE FOLLOWING
        try: # {
            while n > 0: #{
                print(n)
                sleep(1) # sleep for 1 second
                n -= 1
                #}
            else: #{
                print("BLAST OFF!")
                #}
            # }
        except: # {
            pass
        # }
    # }
    
    """
    TAKES IN:
    (1) - dataframe containing scheduled times and scheduled commands
    (2) - timestamp of the CURRENT time (time of this functions call)
    """
    def check_status(self, command_dataframe_data, current_time): # {
        # TRY THE FOLLOWING
        try: # {
            # ITERATE THROUGH ENITRE COMMAND DATAFRAME
            # CHECKING CURRENT TIME AGAIN SCHEDULED TIME (in df)
            # [2020-04-23]\\print("DESIRED HOUR (24 hour):\t" + str(self.sched))
            pass
        # }
        except: # {
            pass
        # }
    # }
    
    def import_command_list(self): # {
        print("IMPORT")
        # TRY THE FOLLOWING
        try: # {
            print("importing...")
            # import infile to variable
            in_file = filedialog.askopenfilename(title="Browse for COMMANDS.csv")
            print("creating DATAFRAME...")
            # CREATE CLASS-WIDE DATAFRAME THAT HOLDS COMMANDS AND TIMES
            self.df_command_paths = pd.read_csv(in_file, index_col=0)
            print(self.df_command_paths.info())
            # set run button to active
            print("ACTIVATING RUN BUTTON")
            self.run_commands['state'] = tk.ACTIVE
            # DE ACTIVATE IMPORT BUTTON
            self.import_button['state'] = tk.DISABLED
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
    # }
    
    def begin_loop_in_thread(self): # {
        # START THREAD
        self.thread = Thread(None, self.begin_loop, None, (), {}, daemon=True)
        self.thread.start()
    # }
    
    def begin_loop(self): # {
        # TRY THE FOLLOWING
        try: # {
            # MAKE RUN BUTTON INACTIVE
            self.run_commands['state'] = tk.DISABLED
            #  BEGIN INFINITE LOOP
            while 1 == 1: # {
                print("\n=====================")
                # ITERATE THROUGH DATAFRAME
                for row in self.df_command_paths.itertuples(index=True, name='Command'): # {
                    print("==================")
                    print("IDX == " + str(row[0]))
                    print("==================\n")
                    print("COL == " + str(row[1]))
                    # PUSH TO RUN FUNCTION AND CHECK TIMES
                    self.run(scheduled_time=pd.Timestamp(ts_input=str(row[0])),
                             command_path=Path(row[1])
                             )
                # }
                # WAIT 59 SECONDS (1 minute)
                self.countdown(60)
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
    # }
    
    def run(self, scheduled_time, command_path): # {
        # TRY THE FOLLOWING
        try: # {
            time_now = pd.Timestamp.now()
            print("TIME NOW:\n\t" + str(time_now))
            print("SCHEDULED TIME:\n\t" + str(scheduled_time))
            # CREATE TIME OF THE TWO SUBTRACTED FROM ONE ANOTHER
            check_time = pd.Timedelta(time_now - scheduled_time)
            print("CHECK-TIME:\n\t" + str(check_time))
            # CHECK IF PASSED (currently on) TIMESTAMP
            if time_now.hour == scheduled_time.hour: # {
                # check if minutes are the same
                if time_now.minute == scheduled_time.minute: # {
                    print("\n<<<<<<< RUN >>>>>>>\n")
                    print("| CMD == " + str(command_path))
                    # RUN COMMAND (as process)
                    proc = subprocess.Popen(str(command_path))
                    proc_status = str(proc.returncode)
                    print("| RETURN-CODE == " + str(proc_status))
                # }
                else: # {
                    print("NOT PROPER MINUTE!")
                # }
            # }
            else: # {
                print("NOT PROPER HOUR!")
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
    # }
    
# }

def main(): # {
    # TRY THE FOLLOWING
    try: # {
        # SETUP LOGGER
        # [2020logger = Logger(logging_output_dir="C:/Temp/").logger
        window = tk.Tk()
        application = Agilent_Task_Scheduler(root=window, the_logger=None)
        window.config()
        window.mainloop()
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
# }

if __name__ == "__main__": # {
    # MAIN BOILERPLATE
    main()
# }