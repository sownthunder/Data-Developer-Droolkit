# -*- coding: utf-8 -*-
"""
Created on Fri Nov 22 12:05:28 2019

@author: derbates
"""

# IMPORT THE GOODS
import os, sys, time
from time import sleep
from pathlib import Path
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import sqlite3, logging, random
import pyodbc
from threading import Thread, Timer
import pandas as pd
import numpy as np
from pandas import Series, DataFrame
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref


class QuotesBook: #{
    
    db_filename = "test_quotes.db"
    time1 = ""
    
    def __init__(self, root): #{
        self.root = root
        self.root.title('AGILENT Quotes')
        #self.root.geometry('1050x1250+250+250') # (WIDTH x HEIGHT + x + y)
        self.root.resizable(width=True, height=True)
        self.root.minsize(height=1250)
        ###############################################
        # CREATE / START THREAD FOR "timestamp puller"
        # [2019-11-21]\\my_thread = MyThread
        #
        #
        #
        ################################################
        # SETUP GUI CALL
        self.create_gui()
    #}
    
    def execute_db_query(self, query, parameters=()): #{
        with sqlite3.connect(self.db_filename) as conn: #{
            cursor = conn.cursor()
            query_result = cursor.execute(query, parameters)
            conn.commit()
        #}
        return query_result
    #}
    
    """
    Import data from ACCESS;
    clean & merge dataframes
    """
    def execute_access_query(self, query, the_conn): #{
        # TRY THE FOLLOWING:
        try: #{
            df = pd.read_sql_query(sql=str(query), 
                                   con=the_conn)
        #}
        except: #{
            errorMessage = str(sys.exc_info()[0]) + "\n"
            errorMessage += str(sys.exc_info()[1]) + "\n"
            errorMessage += str(sys.exc_info()[2]) + "\n"
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            typeE = str("TYPE : " + str(exc_type))
            fileE = str("FILE : " + str(fname))
            lineE = str("LINE : " + str(exc_tb.tb_lineno))
            messageE = str("MESG : " + "\n" + str(errorMessage))
            logging.critical("\n" + typeE +
                             "\n" + fileE +
                             "\n" + lineE +
                             "\n" + messageE)
            messagebox.showerror(title="ERROR!", 
                                 message=typeE +
                                 "\n" + fileE + 
                                 "\n" + lineE + 
                                 "\n" + messageE)
        #}
        else: #{
            print("[execute_ACCESS_query] Operation completed successfully")
        #}
    #}
    
    """
    def pull_timestamp(self): #{
        return str(pd.Timestamp.now())
    #}
    """
    
    def tick(self): #{
        # get the current local time from the PC
        self.time2 = time.strftime('%H:%M:%S')
        # if time string has changed, update it
        if self.time2 != self.time1: #{
            self.time1 = self.time2
            self.clock.config(text=self.time2)
        #}
        # calls itself every 200 milliseconds
        # to update the time display as needed
        # could use > 200 ms, but display gets jerky  
        self.clock.after(200, self.tick)
    #}
    
    #############################################################
    def create_gui(self): #{
        # TRY THE FOLLOWING:
        try: #{
            self.create_ttk_styles()
            # [2019-11-20]\\self.create_menu_bar()
            # [2019-11-18]\\self.create_left_icon()
            self.create_left_side()
            # [2019-11-13]\\self.create_tab_control()
            self.create_tab_control()
            # [2019-11-18]\\self.create_lblframe_create()
            self.create_tab_containers()
            self.create_tab_contents()
            self.create_right_side()
            self.create_tree_view()
            self.view_records()
        #}
        except: #{
            errorMessage = str(sys.exc_info()[0]) + "\n"
            errorMessage += str(sys.exc_info()[1]) + "\n"
            errorMessage += str(sys.exc_info()[2]) + "\n"
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            typeE = str("TYPE : " + str(exc_type))
            fileE = str("FILE : " + str(fname))
            lineE = str("LINE : " + str(exc_tb.tb_lineno))
            messageE = str("MESG : " + "\n" + str(errorMessage))
            logging.critical("\n" + typeE +
                             "\n" + fileE +
                             "\n" + lineE +
                             "\n" + messageE)
            messagebox.showerror(title="ERROR!", 
                                 message=typeE +
                                 "\n" + fileE + 
                                 "\n" + lineE + 
                                 "\n" + messageE)
            # SLEEP FOR 30 SECONDS BEFORE ENDING
            #USE# sleep(30)
            # EXIT PROGRAM
            #USE# sys.exit(0)
        #}
        else: #{
            print("[create_gui] Operation completed successfully")
        #}
    #}
    #############################################################
    
    def import_2_table(self): #{
        messagebox.showwarning(title="WARNING:", message="import 2 table")
    #}
    
    def export_2_table(self): #{
        messagebox.showwarning(title="WARNING:", message="export 2 table")
    #}
    
    """
    def create_menu_bar(self): #{
        # TRY THE FOLLOWING:
        try: #{
            self.menubar = tk.Menu(self.root)
            self.filemenu = tk.Menu(master = self.menubar,
                                    borderwidth = 4,
                                    background = "#0C85CE",
                                    font = ("Comfortaa", 12),
                                    tearoff = 0)
            self.filemenu.add_command(label = "Import", command = self.import_2_table)
            self.filemenu.add_command(label = "Export", command = self.export_2_table)
            
            self.filemenu.add_separator()
            
            self.filemenu.add_command(label = "Exit", command = self.root.quit)
            self.menubar.add_cascade(label = "File", menu = self.filemenu)
            self.editmenu = tk.Menu(master = self.root,
                                    borderwidth = 4,
                                    background = "#9e0ccf",
                                    font = ("Impact", 24),
                                    tearoff = 0)
            self.editmenu.add_command(label = "Filter Table", command = "")
            
            self.editmenu.add_separator()
            
            self.editmenu.add_command(label = "Copy Cell", command = "")
            self.editmenu.add_command(label = "Select All", command = "")
            
            self.menubar.add_cascade(label = "Edit", menu = self.editmenu)
            self.helpmenu = tk.Menu(master = self.menubar, 
                                    background = "#ffbf00",
                                    font = ("Courier New", 48),
                                    relief = tk.GROOVE,
                                    tearoff = 0)
            self.helpmenu.add_command(label = "Help Index", command = "")
            self.helpmenu.add_command(label =  "About...", command = "")
            self.menubar.add_cascade(label = "Help", menu = self.helpmenu)
        #}
        except: #{
            errorMessage = str(sys.exc_info()[0]) + "\n"
            errorMessage = errorMessage + str(sys.exc_info()[1]) + "\n"
            errorMessage = errorMessage + str(sys.exc_info()[2]) + "\n"
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            typeE = str("TYPE : " + str(exc_type))
            fileE = str("FILE : " + str(fname))
            lineE = str("LINE : " + str(exc_tb.tb_lineno))
            messageE = str("MESG : " + "\n" + str(errorMessage))
            logging.critical("\n" + typeE +
                             "\n" + fileE +
                             "\n" + lineE +
                             "\n" + messageE)
        #}
        else: #{
            print("[create_menu_bar] Operation completed successfully")
        #}
    #}
    """
    
    def create_ttk_styles(self): #{
        # TRY THE FOLLOWING:
        try: #{
            themes = sorted(ttk.Style().theme_names())
            for t in themes: #{
                print(str(t))
                #OLD# ttk.Style().theme_use(t)
            #}
            """
            # CONFIGURE STYLE
            self.ttk.Style().configure("TButton", padding=6, relief="flat",
            background='#ccc')
            """
            self.style = ttk.Style()
            # Modify the font of the body
            self.style.configure("mystyle.Treeview", highlightthickness=4, bd=4, font=('Calibri', 11))
            # Modify the font of the headings
            self.style.configure("mystyle.Treeview.Heading", font=('Calibri', 12, 'bold')) 
            # REMOVE THE BORDERS
            self.style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})])
            # BUTTON STYLE
            self.button_style = ttk.Style().configure("TButton", padding=4, 
                                                      relief="groove", background="#96A853",
                                                      font=('Calibri', 8, 'bold'), foreground="#600080")
            # ENTRY BOX STYLE
            self.entry_style = ttk.Style().configure("TEntry", padding=4, 
                                                     relief="ridge", font=('Calibri', 8, 'bold'))
            # SPIN BOX STYLE
            self.spinbox_style = ttk.Style().configure("TSpinbox", padding=4,
                                                       relief="groove", font=('Calibri', 8, 'bold'))
            # RADIO BUTTON STYLE
            self.radio_style = ttk.Style().configure("TRadio", padding=1,
                                                     relief="sunken", font=('Calibri', 8, 'bold'))
            """
            # LABEL STYLE
            self.label_style = ttk.Style().configure("TLabel", padding=6,
                                                     relief="sunken", font=('Wingdings', 8, 'bold'))
            """
            # [2019-11-20]\\ttk.Style().theme_use("vista")
        #}
        except: #{
            errorMessage = str(sys.exc_info()[0]) + "\n"
            errorMessage += str(sys.exc_info()[1]) + "\n"
            errorMessage += str(sys.exc_info()[2]) + "\n"
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            typeE = str("TYPE : " + str(exc_type))
            fileE = str("FILE : " + str(fname))
            lineE = str("LINE : " + str(exc_tb.tb_lineno))
            messageE = str("MESG : " + "\n" + str(errorMessage))
            logging.critical("\n" + typeE +
                             "\n" + fileE +
                             "\n" + lineE +
                             "\n" + messageE)
        #}
        else: #{
            print("[create_styles] Operation completed successfully")
        #}
    #}
    
    def create_left_icon(self): #{
        photo = tk.PhotoImage(file='icons/agilent_logo-Copy1.png')
        label = ttk.Label(image=photo)
        label.image = photo
        label.grid(row=0, column=0, columnspan=2, sticky='SW')
    #}
    
    def create_left_side(self): #{
        # Create a Frame Container
        self.leftframe = tk.Frame(self.root)
        self.leftframe.pack(side = tk.LEFT, fill = tk.BOTH, expand = True)
    #}
    
    def create_tab_control(self): #{
        # CREATE MESSGE AREA
        self.message = ttk.Label(master = self.leftframe, text='', 
                                 font=("Sourcecode Pro", 18), foreground='red')
        self.message.pack(side = tk.TOP, expand = True, fill = tk.BOTH)
        
        # NOTEBOOK WIDGET
        self.tab_control = ttk.Notebook(self.leftframe)
        
        # TAB-1
        self.tab1 = ttk.Frame(master = self.tab_control)
        self.tab_control.add(self.tab1, text = 'CREATE')
        self.tab_control.pack(expand = 2, fill = tk.BOTH)
        
        # TAB-2
        self.tab2 = ttk.Frame(master = self.tab_control)
        self.tab_control.add(self.tab2, text = 'READ')
        self.tab_control.pack(expand = 2, fill = tk.BOTH)
        
        # TAB-3
        self.tab3 = ttk.Frame(master = self.tab_control)
        self.tab_control.add(self.tab3, text = 'UPDATE')
        self.tab_control.pack(expand = 2, fill = tk.BOTH)
        
        # TAB-4
        self.tab4 = ttk.Frame(master = self.tab_control)
        self.tab_control.add(self.tab4, text = "DELETE")
        self.tab_control.pack(expand = 2, fill = tk.BOTH)
        
    #}
    
    """
    CREATE ALL THE "lblframe" objects to then fill with "tab_contents"
    """
    def create_tab_containers(self): #{
        # TRY THE FOLLOWING:
        try: #{
            # Create the Tab Container
            self.lblframe_create=ttk.LabelFrame(master=self.tab1, text="CREATE")
            self.lblframe_create.pack(anchor=tk.CENTER, fill=tk.BOTH, expand=False)
            
            # Create the READ Tab Container
            self.lblframe_read=ttk.LabelFrame(master=self.tab2, text="READ")
            self.lblframe_read.pack(anchor=tk.CENTER, fill=tk.BOTH, expand=False)
            
            # Create the UPDATE Tab Container
            self.lblframe_update=ttk.LabelFrame(master=self.tab3, text="UPDATE")
            self.lblframe_update.pack(anchor=tk.CENTER, fill=tk.BOTH, expand=False)
            
            # Create the DELETE Tab COntainer
            self.lblframe_delete=ttk.LabelFrame(master=self.tab4, text="DELETE")

            self.lblframe_delete.pack(anchor=tk.CENTER, fill=tk.BOTH, expand=False)
        #}
        except: #{
            errorMessage = str(sys.exc_info()[0]) + "\n"
            errorMessage = errorMessage + str(sys.exc_info()[1]) + "\n"
            errorMessage = errorMessage + str(sys.exc_info()[2]) + "\n"
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            typeE = str("TYPE : " + str(exc_type))
            fileE = str("FILE : " + str(fname))
            lineE = str("LINE : " + str(exc_tb.tb_lineno))
            messageE = str("MESG : " + "\n" + str(errorMessage))
            logging.critical("\n" + typeE +
                             "\n" + fileE +
                             "\n" + lineE +
                             "\n" + messageE)
        #}
        else: #{
            print("[create_tab_containers] Operation completed Succesfully")
        #}
        finally: #{
            print("[create_tab_containers]\\FIN")
        #}
        
    #}
    
    def create_tab_contents(self): #{
        # TRY THE FOLLOWING
        try: #{
            # ()()()()()()()()()()()()()()()()()()()()()()()()()()(()()()()())
            # () CREATE TAB CONTENTS () #
            # ()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()() #
            # Name Input
            ttk.Label(master = self.lblframe_create, text = 'Name: ').grid(row=0, column=0, padx=5,
                                                                           pady=5, sticky='w')
            self.name = ttk.Entry(master=self.lblframe_create, width=24) # [2019-11-18]\\ borderwidth=3)
            self.name.grid(row=0, column=1, sticky='w', padx=5, pady=5)
            
            # xXxXxXxXxXxXxXxXx
            # Email Input
            ttk.Label(master=self.lblframe_create, text='Email: ').grid(row=1, column=0, padx=5,
                                                                        pady=5, sticky='w')
            self.email=ttk.Entry(master=self.lblframe_create, width=24) # [2019-11-18]\\ borderwidth=3)
            self.email.grid(row=1, column=1, sticky='w', padx=5, pady=5)
            
            # xXxXxXxXxXxXxXxXx
            # Type Input
            ttk.Label(master=self.lblframe_create, text='Type: ').grid(row=2, column=0, padx=5,
                                                                       pady=5, sticky='w')
            ############################
            # RADIO-VARIABLE == STRING #
            self.radio_type_var = tk.StringVar(master=self.lblframe_create, value="email")
            ################################################################################
            self.radio_type_1 = ttk.Radiobutton(master=self.lblframe_create, variable=self.radio_type_var,
                                                value="web", text="Web", width=12) #, style="TButton")
            self.radio_type_1.grid(row=2, column=1, sticky='w', padx=1, pady=1)
            self.radio_type_2 = ttk.Radiobutton(master=self.lblframe_create, variable=self.radio_type_var,
                                          value="email", text="Email", width=12) #, style="TButton")
            self.radio_type_2.grid(row=2, column=1, sticky='e', padx=1, pady=1)
            
            # xXxXxXxXxXxXxXxXx
            # Sent Input
            ttk.Label(master=self.lblframe_create, text='Sent: ').grid(row=3, column=0, padx=5,
                                                                       pady=5, stick='w')
            ##########################
            # RADIO-VARIABLE == BOOL #
            self.radio_sent_var = tk.BooleanVar(master=self.lblframe_create, value=False)
            ################################################################################
            self.radio_sent_1 = ttk.Radiobutton(master=self.lblframe_create, variable=self.radio_sent_var, 
                                                value=True, text="Yes", width=12, style="TButton")
            self.radio_sent_1.grid(row=3, column=1, sticky='w', padx=1, pady=1)
            self.radio_sent_2 = ttk.Radiobutton(master=self.lblframe_create, variable=self.radio_sent_var,
                                                value=False, text="No", width=12, style="TButton")
            self.radio_sent_2.grid(row=3, column=1, sticky='e', padx=1, pady=1)
            
            # Tracking #
            ttk.Label(master = self.lblframe_create, text = 'Tracking#: ').grid(row=5, column=0,
                                                                                 padx=5, pady=5, sticky='w')
            self.tracking_num = ttk.Entry(master=self.lblframe_create, width=24)
            self.tracking_num.grid(row=5, column=1, sticky='w', padx=5, pady=5)
            
            # Quote #
            ttk.Label(master = self.lblframe_create, text = 'Quote#: ').grid(row=6, column=0,
                                                                              padx=5, pady=5, sticky='w')
            self.quote_num = ttk.Entry(master = self.lblframe_create, width=24)
            self.quote_num.grid(row=6, column=1, sticky='w', padx=5, pady=5)
            
            # Timestamp TKinter variable...
            self.timestamp_var = tk.StringVar(master=self.lblframe_create) #value=str(self.pull_timestamp))
            ttk.Label(master = self.lblframe_create, text = 'Timestamp: ').grid(row=7, column=0, padx=5, pady=5, sticky='w')
            
            # <<< CLOCK (timestamp_test) >>>
            self.clock = ttk.Label(master = self.lblframe_create, font = ("Calibri", 20, 'bold'), 
                                   background='#2b303b', foreground="#bbc0c9")
            self.clock.grid(row=7, column=1, columnspan=2, padx=5, pady=5, stick='w')
            
            """
            self.timestamp = ttk.Entry(master = self.lblframe_create, 
            width=24, 
            textvariable=self.timestamp_var)
            self.timestamp.grid(row=7, column=1, sticky='w', padx=5, pady=5)
            """
            
            # xXxXxXxXxXxXxXxXx
            # Notes Section
            self.notes = ttk.Notebook(master=self.lblframe_create, height=200, width=200, padding = (1, 1))
            # Create the pages
            self.note_tab = tk.Text(master=self.lblframe_create, height=15, width=15, 
                                    background="#96A853") #ttk.Frame(master = self.notes)
            self.trackingnum_tab = tk.Text(master=self.lblframe_create, height=15, width=15, 
                                           background="#2D323C")
            self.quotenum_tab = tk.Text(master=self.lblframe_create, height=15, width=15, 
                                        background="#96A853")
            self.timestamp_tab = tk.Text(master=self.lblframe_create, height=15, width=15)
            # Add them to the notebook
            self.notes.add(self.note_tab, text="NOTES", )
            # [2019-11-26]\\self.notes.add(self.trackingnum_tab, text="TRACKING #")
            # [2019--11-26]\\self.notes.add(self.quotenum_tab, text="QUOTE #")
            # [2019-11-26]\\self.notes.add(self.timestamp_tab, text="TIMESTAMP")
            
            #keep_em_seperated = ttk.Separator(master=self.lblframe_create, orient=tk.HORIZONTAL)
            #keep_em_seperated.grid(row=6, column=0, columnspan=4)
            
            # [2019-11-20]\\self.notes.grid(row=5, column=0, columnspan=2, padx=5, sticky='n')
            self.notes.grid(row=8, column=0, columnspan=2, padx=5, pady=5, sticky='n')
            # row = 6, column = 0, columnspan = 2 AND NO STICK OR PADX
            
            # xXxXXxXxXxXXXXXX
            # SUBMIT "CREATE" BUTTON
            ttk.Button(master=self.lblframe_create, text = 'SUBMIT', width=24, command=self.insert_record).grid(row=9, column=0,
                                                                                    rowspan=1, columnspan=2,
                                                                                    padx=5, pady=5, sticky='nesw')
            # ()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()
            # () READ TAB CONTENTS () #
            # ()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()
            # Filter input
            ttk.Label(master=self.lblframe_read, text = 'Filter: ' ).grid(row=0, column=0, padx=5,
                                                                          pady=5, sticky='w')
            self.read_filter_var = tk.StringVar(master=self.lblframe_read, value="Tracking #")
            self.read_filter = ttk.Entry(master=self.lblframe_update, textvariable=self.read_filter_var, state='readonly')
            self.read_filter.grid(row=0, column=1, sticky='w', padx=5, pady=5)
            """[2019-12-09]"""
            """
            self.read_filter = ttk.Spinbox(master=self.lblframe_read, values=['Tracking #','Name', 
                                                                              'Email','Type', 
                                                                              'Timestamp','Sent', 
                                                                              'Quote #','Product #'],
                                           textvariable=self.read_filter_var, 
                                           style="TSpinbox")
            self.read_filter.grid(row=0, column=1, sticky='w', padx=5, pady=5)
            """
            
            # Filter KEYWORDS
            ttk.Label(master=self.lblframe_read, text='Keywords: ').grid(row=1, column=0, padx=5,
                                                                         pady=5, sticky='w')
            self.read_keywords = ttk.Entry(master = self.lblframe_read, width=24) # [2019-11-19]\\ borderwidth=3)
            self.read_keywords.grid(row = 1, column = 1, sticky = 'w', padx=5, pady=5)

            
            ttk.Button(master=self.lblframe_read, text = 'READ NOTES', width=24).grid(row=2, column=0, 
                                                                                  rowspan=1, columnspan=2, 
                                                                                  padx=5, pady=5, sticky='nesw')
            
            # ()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()
            # () UPDATE TAB CONTENTS () #
            # ()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()
            # Filter input
            ttk.Label(master=self.lblframe_update, text = 'Tracking #: ').grid(row=0, column=0, padx=5,
                                                                           pady=5, sticky='w')
            self.update_filter_var = tk.StringVar(master=self.lblframe_update, value="Tracking #")
            self.update_filter = ttk.Entry(master=self.lblframe_update, textvariable=self.update_filter_var, state='readonly')
            self.update_filter.grid(row=0, column=1, sticky='w', padx=5, pady=5)
            """
            self.update_filter = ttk.Spinbox(master=self.lblframe_update, values=['Tracking #', 'Name',
                                                                                  'Email','Type',
                                                                                  'Timestamp','Sent',
                                                                                  'Quote #','Product #'],
                                             textvariable=self.update_filter_var)
            self.update_filter.grid(row=0, column=1, sticky='w', padx=5, pady=5)
            """
            
            # Filter KEYWORDS
            ttk.Label(master=self.lblframe_update, text='Keywords: ').grid(row=1, column=0, padx=5,
                                                                           pady=5, sticky='w')
            self.update_keywords = ttk.Entry(master = self.lblframe_update, width=24)
            self.update_keywords.grid(row = 1, column = 1, sticky = 'w', padx=5, pady=5)
            
            ttk.Button(master=self.lblframe_update, text = 'UPDATE', width=24, command=self.on_modify_selected_button_clicked).grid(row=2, column=0,
                                                                                    rowspan=1, columnspan=2,
                                                                                    padx=5, pady=5, sticky='nesw')
            
            # ()()()()()()()()()()()()()()
            # () DELETE TAB CONTENTS () #
            # ()()()()()()()()()()()()()()
            # Popout Button
            ttk.Button(master=self.lblframe_delete, text = "POPOUT: ", 
                       style = 'TButton', command=self.open_modify_window).grid(row=0, column=0, padx=5,
                                                                                pady=5, sticky='w')
        #}
        except: #{
            errorMessage = str(sys.exc_info()[0]) + "\n"
            errorMessage = errorMessage + str(sys.exc_info()[1]) + "\n"
            errorMessage = errorMessage + str(sys.exc_info()[2]) + "\n"
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            typeE = str("TYPE : " + str(exc_type))
            fileE = str("FILE : " + str(fname))
            lineE = str("LINE : " + str(exc_tb.tb_lineno))
            messageE = str("MESG : " + "\n" + str(errorMessage))
            logging.critical("\n" + typeE +
                             "\n" + fileE +
                             "\n" + lineE +
                             "\n" + messageE)
            messagebox.showerror(title="ERROR!", 
                                 message=typeE +
                                 "\n" + fileE + 
                                 "\n" + lineE + 
                                 "\n" + messageE)
        #}
        else: #{
            print("[create_tab_contents] Operation Completed Successfully...")
        #}
    #}
    
    """
    def create_lblframe_read(self): #{
        # Create the Tab Container
        self.lblframe_read=tk.LabelFrame(master=self.tab2, text="")
        self.lblframe_read.pack(anchor=tk.CENTER, fill=tk.BOTH, expand=False)
        
        # Filter Input
        ttk.Label(master = self.lblframe_create, text = 'Filter: ').grid(row=0, column=0, padx=5,
                                                                         pady=5, sticky='w')
        #self.filter = ttk.Listbox(master=self.tab2, )
        self.spinval = tk.StringVar()
        self.s = ttk.Spinbox(self.tab2, from_=1.0, to=100.0, textvariable=self.spinval)
        self.s.grid(row=0, column=1, sticky='w', padx=5, pady=5)
    #}
    """
    
    def confirm_message(self): #{
        pass
    #}
        
    def create_right_side(self): #{
        # Create a Frame Container
        self.rightframe = ttk.Frame(master = self.root)
        self.rightframe.pack(side = tk.RIGHT, fill = tk.BOTH, expand = True)
    #}
    
    def create_tree_view(self): #{
        # TABLE
        self.tree = ttk. Treeview(master = self.rightframe, style="mystyle.Treeview", 
                                  height = 30, columns = 8)  # height = 20
        self.tree["columns"] = ("one","two","three","four","five","six","seven")
        self.tree.column('#0', width=100, minwidth=90, stretch=tk.NO)
        self.tree.column("one", width=125, minwidth=125, stretch=tk.NO)
        self.tree.column("two", width=150, minwidth=150, stretch=tk.NO)
        self.tree.column("three", width=50, minwidth=50, stretch=tk.NO)
        self.tree.column("four", width=128, minwidth=128, stretch=tk.NO)
        self.tree.column("five", width=45, minwidth=45, stretch=tk.NO)
        self.tree.column("six", width=100, minwidth=90, stretch=tk.NO)
        self.tree.column("seven", width=100, minwidth=90, stretch=tk.YES)
        
        # Definitions of Headings
        # [2019-12-05]\\self.tree.grid(row = 1, column = 0, columnspan = 8, sticky = 'S')
        self.tree.pack(side = tk.TOP, fill = tk.BOTH, expand = True)
        self.tree.heading('#0', text = 'Tracking #', anchor = tk.CENTER)
        self.tree.heading('#1', text = 'Name', anchor = tk.CENTER)
        self.tree.heading('#2', text = 'Email', anchor = tk.CENTER)
        self.tree.heading('#3', text = 'Type', anchor = tk.CENTER)
        self.tree.heading('#4', text = 'Timestamp', anchor = tk.CENTER)
        self.tree.heading('#5', text = 'Sent', anchor = tk.CENTER)
        self.tree.heading('#6', text = 'Quote #', anchor = tk.CENTER)
        self.tree.heading('#7', text = 'Product #', anchor = tk.CENTER)

        # BIND CLICK ACTIONS/EVENTS
        self.tree.bind("<Double-1>", self.on_double_click)
    #}
    
    def on_add_record_button_clicked(self): #{
        self.add_new_record()
    #}

    def on_double_click(self, event): #{
        item = self.tree.selection()[0]
        #"you clicked on", self.tree.item(item, "text")
        messagebox.showinfo(title="test:", message="you clicked on" + str(self.tree.item(item, "text")))
    #}
    
    def on_delete_selected_button_clicked(self): #{
        self.message['text'] = ''
        try: #{
            self.tree.item(self.tree.selection())['values'][0]
        #}
        except: #{
            self.message['text'] = 'No item selected to delete'
            return
        #}
        self.delete_record()
    #}
    
    def on_modify_selected_button_clicked(self): #{
        self.message['text'] = ''
        try: #{
            self.tree.item(self.tree.selection())['values'][3]
            print(str(self.tree.item(self.tree.selection())['values'][3]))
        #}
        except IndexError as e: #{
            self.message['text'] = 'No Item selected to modify\n[' + str(e) +']'
            return
        #}
        test_name = str(self.tree.item(self.tree.selection())['values'][0])
        test_two = str(self.tree.item(self.tree.selection())['values'][1])
        print(str(self.tree.item(self.tree.selection())['values'][3]))
        print(str(self.tree.item(self.tree.selection())['values'][4]))
        #print(str(self.tree.item(self.tree.selection())['values'][5]))
        #print(str(self.tree.item(self.tree.selection())['values'][6]))
        #print(str(self.tree.item(self.tree.selection())['values'][7]))
        #print(str(self.tree.item(self.tree.selection())['values'][8]))
        the_timestamp = str(self.tree.item(self.tree.selection())['values'][3])
        self.open_modify_window_test(tracking_num="", the_name=test_name, 
                                     the_email=test_two, the_type="", 
                                     the_ts=the_timestamp, the_sent="",
                                     quote_num="", product_num="", the_notes="")
    #}
    
    def open_modify_window_test(self, tracking_num, the_name, 
                                the_email, the_type, the_ts, the_sent, 
                                quote_num, product_num, the_notes): #{
        print("[open_modify_window] BEGIN..." )
        print(tracking_num)
        print(the_name)
        print(the_email)
        print(the_type)
        print(the_ts)
        print(the_sent)
        print(quote_num)
        print(product_num)
        print(the_notes)
        # CREATE TKINTER TOPLEVEL
        self.transient = tk.Toplevel(master=self.root)
        # CREATE TKINTER STRING/BOOL/VARS
        self.old_name_var = tk.StringVar(master=self.transient, value=str(the_name))
        self.old_email_var = tk.StringVar(master=self.transient, value=str(the_email))
        self.old_type_var = tk.StringVar(master=self.transient, value=str(the_type))
        self.old_sent_var = tk.StringVar(master=self.transient, value=str(the_sent))
        self.old_ts_var = tk.StringVar(master=self.transient, value=str(the_ts))
        self.old_track_var = tk.StringVar(master=self.transient, value=str(tracking_num))
        self.old_quote_var = tk.StringVar(master=self.transient, value=str(quote_num))
        self.old_product_var = tk.StringVar(master=self.transient, value=str(product_num))
        self.old_notes_var = tk.StringVar(master=self.transient, value=(str(the_notes)))
        # CREATE TKINTER LABELS & ENTRY BOXES
        ttk.Label(self.transient, text='Name:').grid(row=0, column=1)
        self.new_name = ttk.Entry(self.transient, textvariable=self.old_name_var).grid(row=0, column=2)
        ttk.Label(self.transient, text='Email:').grid(row=1, column=1)
        self.new_email = ttk.Entry(self.transient, textvariable=self.old_email_var).grid(row=1, column=2)
        ttk.Label(self.transient, text='Type:').grid(row=2, column=1)
        self.new_type = ttk.Entry(self.transient, textvariable=self.old_type_var).grid(row=2, column=2)
        ttk.Label(self.transient, text='Sent:').grid(row=3, column=1)
        self.new_sent = ttk.Entry(self.transient, textvariable=self.old_sent_var).grid(row=3, column=2)
        ttk.Label(self.transient, text='Timestamp:').grid(row=4, column=1)
        self.new_ts = ttk.Entry(self.transient, textvariable=self.old_ts_var, state='readonly').grid(row=4, column=2)
        ttk.Label(self.transient, text='Tracking #:').grid(row=5, column=1)
        self.new_track = ttk.Entry(self.transient, textvariable=self.old_track_var, state='readonly').grid(row=5, column=2)
        ttk.Label(self.transient, text='Quote #:').grid(row=6, column=1)
        self.new_quote = ttk.Entry(self.transient, textvariable=self.old_quote_var, state='readonly').grid(row=6, column=2)
        ttk.Label(self.transient, text='Product #:').grid(row=7, column=1)
        self.new_product = ttk.Entry(self.transient, textvariable=self.old_product_var, state='readonly').grid(row=7, column=2)
        ttk.Button(self.transient, text='Update Record', command=self.modify_record).grid(row=8, column=2)
    #}
    
    def modify_record(self): #{
        # TRY THE FOLLOWING
        try: #{
            # CHECK AND MAKE SURE USER IS SURE
            confirm_bool = messagebox.askokcancel(title="ARE YOU SURE??", message="Last Chance!\nThis will overwrite record. Do you wish to continue?")
            print(confirm_bool)
            # IF USER WANTS... OVERWRITE RECORD
            if confirm_bool is True: #{
                print("CONFIRMED!")
                print(self.new_name.get())
                print(self.new_email.get())
                print(self.new_type.get())
                print(self.new_sent.get())
                print(self.new_ts.get())
                print(self.new_track.get())
                print(self.new_quote.get())
                print(self.new_product.get())
            #}
            # ELSE... let them edit it some more
            else: #{
                print("NOPE!")
            #}
        #}
        except: #{
            errorMessage = str(sys.exc_info()[0]) + "\n"
            errorMessage = errorMessage + str(sys.exc_info()[1]) + "\n"
            errorMessage = errorMessage + str(sys.exc_info()[2]) + "\n"
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            typeE = str("TYPE : " + str(exc_type))
            fileE = str("FILE : " + str(fname))
            lineE = str("LINE : " + str(exc_tb.tb_lineno))
            messageE = str("MESG : " + "\n" + str(errorMessage))
            logging.critical("\n" + typeE +
                  "\n" + fileE +
                  "\n" + lineE +
                  "\n" + messageE)
            messagebox.showerror(title="ERROR!", 
                                 message=typeE +
                                 "\n" + fileE + 
                                 "\n" + lineE + 
                                 "\n" + messageE)
        #}
        else: #{
            print("[modify_record] Operation completed successfully...")
        #}
    #}
    
    """
    ###########################################################################
    """
    
    def insert_record(self): #{
        # TRY THE FOLLOWING
        try: #{
            print("...INSERTING RECORD...")
            #print("timestamp == " + str(self.clock.get()))
            print("timestamp == " + str(pd.Timestamp(self.time2)))
            print("name == " + str(self.name.get()))
            print("email == " + str(self.email.get()))
            print("web/email == " + str(self.radio_type_var.get()))
            print("sent == " + str(self.radio_sent_var.get()))
            # CREATE SEPERATE LIST FOR EACH COLUMN
            track_num = [str(self.tracking_num.get())]
            name = [str(self.name.get())]
            email = [str(self.email.get())]
            the_type = [str(self.radio_type_var.get())]
            # [2019-11-26]\\ts = [str(self.timestamp_var.get())]
            ts = [str(pd.Timestamp(self.time2))]
            sent = [str(self.radio_sent_var.get())]
            # DICTIONARY OF LISTS
            dict = {'Tracking#': track_num,
                    'Name': name,
                    'Email': email,
                    'Type': the_type,
                    'Timestamp': ts,
                    'Sent': sent}
            create_record_df = pd.DataFrame(data=dict)
            # CREATE ENGINE (for sendning to Database)
            engine = create_engine('sqlite:///test_quotes.db')
            # SEND DATAFRAME TO DATABASE
            create_record_df.to_sql(name="quotes", con=engine, if_exists="append", index=False)
            self.view_records()
        #}
        except: #{
            errorMessage = str(sys.exc_info()[0]) + "\n"
            errorMessage = errorMessage + str(sys.exc_info()[1]) + "\n"
            errorMessage = errorMessage + str(sys.exc_info()[2]) + "\n"
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            typeE = str("TYPE : " + str(exc_type))
            fileE = str("FILE : " + str(fname))
            lineE = str("LINE : " + str(exc_tb.tb_lineno))
            messageE = str("MESG : " + "\n" + str(errorMessage))
            logging.critical("\n" + typeE +
                  "\n" + fileE +
                  "\n" + lineE +
                  "\n" + messageE)
            messagebox.showerror(title="ERROR!", 
                                 message=typeE +
                                 "\n" + fileE + 
                                 "\n" + lineE + 
                                 "\n" + messageE)
        #}\
        else: #{
            print("[insert_record] Operation Completed Successfully...")
        #}
    #}
    
    def add_new_record(self): #{
        if self.new_records_validated(): #{
            query = 'INSERT INTO quotes VALUES(NULL,?, ?, ?, ?, ?)'
            parameters = (self.name.get(), self.email.get(), self.radio_type_var.get(),
                          self.radio_sent_var.get(), self.notes.get()) 
            self.execute_db_query(query, parameters)
            self.message['text'] = 'Quote record of {} added'.format(
                self.name.get())
            self.name.delete(0, tk.END)
            self.email.delete(0, tk.END)
            self.radio_type_var.delete(0, tk.END)
            self.radio_sent_var.delete(0, tk.END)
            self.notes.delete(0, tk.END)
        #}
        else: #{
            self.message['text'] = 'name and email etc cannot be blank'
        #}
        self.view_records()
    #}
    
    def new_records_validated(self): #{
        return len(self.name.get()) !=0 and len(self.email.get()) !=0 and len(self.radio_type_var.get()) !=0 and len(self.radio_sent_var.get()) !=0 and len(self.notes.get()) !=0
    #}
    
    def view_records(self): #{
        print("[view_records] BEGIN READING IN RECORDS...")
        # TRY THE FOLLOWING
        try: #{
            items = self.tree.get_children()
            for item in items: #{
                self.tree.delete(item)
            #}
            query = 'SELECT * FROM quotes ORDER BY TIMESTAMP desc'
            quote_book_entries = self.execute_db_query(query)
            for row in quote_book_entries: #{
                logging.info("TRACKING # == " + str(row[0]))
                logging.info("NAME === " + str(row[1]))
                logging.info("Email == " + str(row[2]))
                logging.info("Type == " + str(row[3]))
                logging.info("Timestamp == " + str(row[4]))
                logging.info("Sent == " + str(row[5]))
                # CREATE LIST
                test_lst = [str(row[1]), str(row[2]), str(row[3]), str(row[4]), str(row[5])]
                # INSERT INTO TREE
                self.tree.insert('', 0, text=str(row[0]), values=test_lst)
            #}
        #}
        except: #{
            errorMessage = str(sys.exc_info()[0]) + "\n"
            errorMessage = errorMessage + str(sys.exc_info()[1]) + "\n"
            errorMessage = errorMessage + str(sys.exc_info()[2]) + "\n"
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            typeE = str("TYPE : " + str(exc_type))
            fileE = str("FILE : " + str(fname))
            lineE = str("LINE : " + str(exc_tb.tb_lineno))
            messageE = str("MESG : " + "\n" + str(errorMessage))
            logging.critical("\n" + typeE +
                  "\n" + fileE +
                  "\n" + lineE +
                  "\n" + messageE)
            messagebox.showerror(title="ERROR!", 
                                 message=typeE +
                                 "\n" + fileE + 
                                 "\n" + lineE + 
                                 "\n" + messageE)
        #}
        else: #{
            print("[view_records] Operation done successfully")
        #}
        
    #}
    
    def delete_record(self): #{
        self.message['text'] = ''
        name = self.tree.item(self.tree.selection())['text']
        query = 'DELETE FROM contacts WHERE name = ?'
        self.execute_db_query(query, (name,))
        self.message['text'] = 'Phone record for {} deleted'.format(name)
        self.view_records()
    #}
    
    def open_modify_window(self, record_to_modify): #{
        print("[open_modify_window]..BEGIN...")
        print(record_to_modify)
        # TRY THE FOLLOWING
        try: #{
            # [2019-11-26]\name = self.tree.item(self.tree.selection())['text']
            name = str(record_to_modify)
            # [2019-11-19]\\old_phone_number = self.tree.item(self.tree.selection())['values'][0]
            # [2019-11-26]old_time_stamp = self.tree.item(self.tree.selection())['values'][3] # Timestamp
            old_time_stamp = str(record_to_modify)
            self.transient = tk.Toplevel()
            ttk.Label(self.transient, text='Name:').grid(row=0, column=1)
            ttk.Entry(self.transient, textvariable=tk.StringVar(
                self.transient, value=name), state='readonly').grid(row=0, column=2)
            ttk.Label(self.transient, text='Old Timestamp:').grid(row=1, column=1)
            ttk.Entry(self.transient, textvariable=tk.StringVar(
                self.transient, value=old_time_stamp), state='readonly').grid(row=1, column=2)
            ttk.Label(self.transient, text='New Timestamp:').grid(
                row=2, column=1)
            new_phone_number_entry_widget = ttk.Entry(self.transient)
            new_phone_number_entry_widget.grid(row=2, column=2)
            ttk.Button(self.transient, text='Update Record', command=lambda: self.update_record(
                new_phone_number_entry_widget.get(), old_time_stamp, name)).grid(row=3, column=2, sticky=tk.E)
            self.transient.mainloop()
        #}
        except: #{
            errorMessage = str(sys.exc_info()[0]) + "\n"
            errorMessage = errorMessage + str(sys.exc_info()[1]) + "\n"
            errorMessage = errorMessage + str(sys.exc_info()[2]) + "\n"
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            typeE = str("TYPE : " + str(exc_type))
            fileE = str("FILE : " + str(fname))
            lineE = str("LINE : " + str(exc_tb.tb_lineno))
            messageE = str("MESG : " + "\n" + str(errorMessage))
            logging.critical("\n" + typeE +
                  "\n" + fileE +
                  "\n" + lineE +
                  "\n" + messageE)
            messagebox.showerror(title="ERROR!", 
                                 message=typeE +
                                 "\n" + fileE + 
                                 "\n" + lineE + 
                                 "\n" + messageE)
        #}
        else: #{
            print("[open_modify_window] Operation completed successfully")
        #}
    #}
    
    def update_record(self, newtimestamp, old_time_stamp, tracking_num): #{
        query = 'UPDATE quotes SET Timestamp=? WHERE Timestamp=? AND Tracking#=?'
        parameters = (newtimestamp, old_time_stamp, tracking_num)
        self.execute_db_query(query, parameters)
        self.transient.destroy()
        self.message['text'] = 'Quotes of {} modified'.format(self.name)
        self.view_records()
    #}
    
#}

def setup_logger(): #{
    # TRY THE FOLLOWING
    try: #{
        logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s: %(message)s, FROM=%(funcName)s, LINENO=%(lineno)d',
                            datefmt='%Y-%m-%d-%H%M%S',
                            filemode='a')
    #}
    except: #{
        errorMessage = str(sys.exc_info()[0]) + "\n"
        errorMessage = errorMessage + str(sys.exc_info()[1]) + "\n"
        errorMessage = errorMessage + str(sys.exc_info()[2]) + "\n"
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        typeE = str("TYPE : " + str(exc_type))
        fileE = str("FILE : " + str(fname))
        lineE = str("LINE : " + str(exc_tb.tb_lineno))
        messageE = str("MESG : " + "\n" + str(errorMessage))
        print("\n" + typeE +
              "\n" + fileE +
              "\n" + lineE +
              "\n" + messageE)
        messagebox.showerror(title="ERROR!", 
                                 message=typeE +
                                 "\n" + fileE + 
                                 "\n" + lineE + 
                                 "\n" + messageE)
    #}
    else: #{
        print("[setup_logger] Logger setup successfully")
    #}
#}

if __name__ == "__main__": #{
    # LOGGER
    setup_logger()
    # TRY THE FOLLOWING
    try: #{
        window = tk.Tk()
        application = QuotesBook(window)
        application.tick()
        window.mainloop()
    #}
    except: #{
        errorMessage = str(sys.exc_info()[0]) + "\n"
        errorMessage = errorMessage + str(sys.exc_info()[1]) + "\n"
        errorMessage = errorMessage + str(sys.exc_info()[2]) + "\n"
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        typeE = str("TYPE : " + str(exc_type))
        fileE = str("FILE : " + str(fname))
        lineE = str("LINE : " + str(exc_tb.tb_lineno))
        messageE = str("MESG : " + "\n" + str(errorMessage))
        logging.critical("\n" + typeE +
              "\n" + fileE +
              "\n" + lineE +
              "\n" + messageE)
        messagebox.showerror(title="ERROR!", 
                                 message=typeE +
                                 "\n" + fileE + 
                                 "\n" + lineE + 
                                 "\n" + messageE)
    #}
    else: #{
        print("[main] Operation done successfully")
    #}
#}