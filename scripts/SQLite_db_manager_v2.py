# -*- coding: utf-8 -*-
"""
Created on Tue Oct 15 13:54:52 2019

@author: derbates

Utilizing:
SQLite3
SQLalchemy

This script performs the following:
1) used PYAUTOGUI to create "CONFIRM" COMMANDS
2) ASK FOR LOAD IN--MEMORY SQLITE.db, INPUT .db FILE, or CREATE NEW
3) once input, then allows pop up box for SQL command entry

"""

# import the goodies
import os, sys, time
from pathlib import Path

import pyautogui
import pyodbc
import re

import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

import sqlite3
from sqlalchemy import create_engine

####################################################################
# GLOBALS
#global root
global logDirectory

####################################################################
#OLD#root = tk.Tk()
logDirectory = "C:/Temp/"

"""
Called based on user
creates selected Database 
opnes "App" (GUI) accordingly...
"""
def in_memory_launcher(): #{
    print("<IN-MEMORY .db>")
    root = tk.Tk()
    # try the following
    try: #{
        # CREATE CONNECTION to SQLITE in-memory database
        conn = sqlite3.connect(':memory:')
        #OLD#engine = create_engine('sqlite://')
        # Create CuRSOR
        ##crsr = conn.cursor()
        ## #EXECUTRE CREATE TABLE SCRIPT?
        ##crsr.execute("create table people (name_last, age)")
        ## OPEN UP GUI APPLICATION AND SEND OVER PARAMS
        App("IN-MEMORY-DATABASE", conn, root)
    #}
    except: #{
        errorMessage = str(sys.exc_info()[0]) + "\n"
        errorMessage = errorMessage + str(sys.exc_info()[1]) + "\n\t\t"
        errorMessage = errorMessage + str(sys.exc_info()[2]) + "\n"
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        typeE = str("TYPE : " + str(exc_type))
        fileE = str("FILE : " + str(fname))
        lineE = str("LINE : " + str(exc_tb.tb_lineno))
        messageE = str("MESG : " + "\n\n" + str(errorMessage) + "\n")
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

"""
Called based on user
creates selected Database 
opnes "App" (GUI) accordingly...
"""
def open_db_launcher(): #{
    print("<OPENING UP .db>")
    root = tk.Tk()
    # try the following
    try: #{
        # ASK FOR FILE LOCATION OF .db
        root.file = filedialog.askopenfilename(initialdir = "/",
                                           title = "Select file",
                                           filetypes = (("db files","*.db"),("all files","*.*")))
        # CREATE CONNECTION BASED ON FILE LOCATION
        conn = sqlite3.connect(root.file)
        # OPEN UP GUI APPLICATION AND SEND OVER PARAMS
        App("OPENED-DATABASE", conn, root)
    #}
    except: #{
        errorMessage = str(sys.exc_info()[0]) + "\n"
        errorMessage = errorMessage + str(sys.exc_info()[1]) + "\n\t\t"
        errorMessage = errorMessage + str(sys.exc_info()[2]) + "\n"
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        typeE = str("TYPE : " + str(exc_type))
        fileE = str("FILE : " + str(fname))
        lineE = str("LINE : " + str(exc_tb.tb_lineno))
        messageE = str("MESG : " + "\n\n" + str(errorMessage) + "\n")
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

"""
Called based on user
creates selected Database 
opnes "App" (GUI) accordingly...
"""
def create_db_launcher(): #{
    print("<CREATING NEW .db>")
    root = tk.Tk()
    # try the following
    try: #{
        # ASK FOR "save_fille_name" TO CREATE .db
        root.filename = filedialog.asksaveasfilename(initialdir = "/",title = "Select file",filetypes = (("db files","*.db"),("all files","*.*")))
        print(str(root.filename))
        """
        root.directory = filedialog.askdirectory()
        ## ASK USER FOR DATABASE FILENAME
        dbName = pyautogui.prompt(text="Enter Desired Datebase Name:", title="Name .db")
        print("DESIRED NAME == " + str(dbName))
        print("DATABASE PATH ==" + str(root.directory + "/" + dbName))
        ## APPEND PROPER STR TO MAKE FILE PATH WORK CORRECTLY
        dbPath = Path(root.directory + "/" + dbName + ".db")
        # CREATE NEW CONN / DATABASE BASED ON LOCATION & NAME
        """
        conn = sqlite3.connect(str(root.filename)) # WAS: dbPath
        # GET DATABASE NAME SPECIFICALLY
        db_str = str(root.filename)
        str_len = len(db_str)
        db_name = db_str.rfind("/", 0, str_len)
        # OPEN UP GUI APPLICATION AND SEND OVER PARAMS
        App("-NEW-DATABASE", conn, root)
    #}
    except: #{
        errorMessage = str(sys.exc_info()[0]) + "\n"
        errorMessage = errorMessage + str(sys.exc_info()[1]) + "\n\t\t"
        errorMessage = errorMessage + str(sys.exc_info()[2]) + "\n"
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        typeE = str("TYPE : " + str(exc_type))
        fileE = str("FILE : " + str(fname))
        lineE = str("LINE : " + str(exc_tb.tb_lineno))
        messageE = str("MESG : " + "\n\n" + str(errorMessage) + "\n")
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

"""
CRUD
"""
#######################################################################################
"""
TAKES IN A STRING TO **FINALLY** RUN SQL_QUERY INTO DB
CALLED FROM ONE OF THE FOUR "COMMAND" FUNCTIONS
"""
def sql_command(theCommand): #{
    print("ATTEMPTING TO RUN QUERY")
    ## IF SELECT
    """
    # Do this instead
    t = ('RHAT',)
    c.execute('SELECT * FROM stocks WHERE symbol=?', t)
    print(c.fetchone())
    """
#}

"""
ADD "theConn" as PARAM
"""
def read(): #{
    top = tk.Toplevel()
    top.title("READ")
    top.geometry('750x750+350+350')
    top.resizable(width=True, height=False)
    top.transient(master=None)
    #### DROP DOWN BOXES
    # USE CNXN.EXECUTE()
    print("READ")
    # Do this instead
    #t = ('RHAT',)
    # c.execute('SELECT * FROM stocks WHERE symbol=?', t)
    #print(c.fetchone())
    """
    ## TESTING
    cursor = theConn.cursor()
    cursor.execute("SELECT * from dummy")
    for row in cursor: #{
        print(f'row= {row}')
    #}
    print()
    """
    top.mainloop()
#}

"""
ADD "theConn" as PARAM
"""
def create(): #{
    create_top = tk.Toplevel()
    create_top.title("CREATE")
    create_top.geometry('750x750+350+350')
    create_top.resizable(width=True, height=False)
    #### DROP DOWN BOXES
    # USE CNXN.EXECUTE()
    print("CREATE")
    """
    ## TESTING
    cursor = theConn.cursor()
    cursor.execute(
        'insert into dummy(a,b) values(?,?);',
        (3232, 'catzzz')
    )
    theConn.commit()
    read(theConn)
    """
    create_top.mainloop()
#}

"""
ADD "theConn" as PARAM
"""
def update(): #{
    update_top = tk.Toplevel()
    update_top.title("UPDATE")
    update_top.geometry('750x750+350+350')
    update_top.resizable(width=True, height=False)
    update_top.transient(master=None)
    #### DROP DOWN BOXES
    # USE CNXN.EXECUTE()
    print("UPDATE")
    """
    ## TESTING
    cursor = theConn.cursor()
    cursor.execute(
        'update dummy set b = ? where a = ?;',
        ('dogzzz', 3232)
    )
    theConn.commit()
    read(theConn)
    """
    update_top.mainloop()
#}

"""
ADD "theConn" as PARAM
"""
def delete(): #{
    delete_top = tk.Toplevel()
    delete_top.title("DELETE")
    delete_top.geometry('750x750+350+350')
    delete_top.resizable(width=True, height=False)
    delete_top.transient(master=None)
    #### DROP DOWN BOXES
    # USE CNXN.EXECUTE()
    print("DELETE")
    """
    ## TESTING
    cursor = theConn.cursor()
    cursor.execute(
        'delete from dummy where a > 5'
    )
    theConn.commit()
    read(theConn)
    """
    delete_top.mainloop()
#}

"""
: param :
STR title to append to GUI 
CONN to database that was setup in "launcher"
"""
def App(theTitle, theConn, theRoot): #{
    try: #{
        #rooty = theRoot
        #top = tk.Tk(rooty)
        theRoot.title('SQLite_' + str(theTitle) + '_manager')
        theRoot.geometry('400x200+200+200')
        theRoot.resizable(width=True, height=False)

        ## CREATE BUTTON
        ##################

        c1 = tk.Checkbutton(master=theRoot)

        b1 = tk.Button(master=theRoot, text='READ', bg="green", fg="white", relief=tk.RIDGE, height=4, command=read)
        b1.pack(expand=True, fill=tk.BOTH, side=tk.LEFT)

        ## READ BUTTON
        ##################

        b2 = tk.Button(master=theRoot, text='CREATE', bg="gold", fg="purple", relief=tk.RIDGE, height=4, command=create)
        b2.pack(expand=False, fill=tk.X, anchor=tk.CENTER)

        ## UPDATE BUTTON
        ##################

        b3 = tk.Button(master=theRoot, text='UPDATE', bg="orange", fg="black", relief=tk.RIDGE, height=4, command=update)
        b3.pack(expand=False, fill=tk.X, anchor=tk.CENTER)

        ## DELETE BUTTON

        b4 = tk.Button(master=theRoot, text='DELETE', bg="red", fg="navy", relief=tk.RIDGE, height=4, command=delete)
        b4.pack(expand=False, fill=tk.X, anchor=tk.CENTER)

        theRoot.config()
        theRoot.mainloop()
    #}
    except: #{
        errorMessage = str(sys.exc_info()[0]) + "\n"
        errorMessage = errorMessage + str(sys.exc_info()[1]) + "\n\t\t"
        errorMessage = errorMessage + str(sys.exc_info()[2]) + "\n"
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        typeE = str("TYPE : " + str(exc_type))
        fileE = str("FILE : " + str(fname))
        lineE = str("LINE : " + str(exc_tb.tb_lineno))
        messageE = str("MESG : " + "\n\n" + str(errorMessage) + "\n")
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
    # try the following
    try: #{
        ## ASK USER THEIR DESIRED OPTION
        confirmStr = pyautogui.confirm(text='Yo whats good:',
                                       title='SQLite-Navigator',
                                       buttons=['In-Memory .db', 'Open Old .db', 'Create New .db'])
        if confirmStr == 'In-Memory .db': #{
            ## Call in-memory launcher function
            in_memory_launcher()
        #}
        elif confirmStr == 'Open Old .db': #{
            open_db_launcher()
        #}
        elif confirmStr == "Create New .db": #{
            create_db_launcher()
        #}
        ###############################################
        ## LAUNCHER
        ##
        ##
        """
        To use a SQLite :memory: database, specify an empty URL:
        engine = create_engine('sqlite://')
        """
        ################################################

    #}
    except: #{
        errorMessage = str(sys.exc_info()[0]) + "\n"
        errorMessage = errorMessage + str(sys.exc_info()[1]) + "\n\t\t"
        errorMessage = errorMessage + str(sys.exc_info()[2]) + "\n"
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        typeE = str("TYPE : " + str(exc_type))
        fileE = str("FILE : " + str(fname))
        lineE = str("LINE : " + str(exc_tb.tb_lineno))
        messageE = str("MESG : " + "\n\n" + str(errorMessage) + "\n")
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

if __name__ == "__main__": #{
    main()
#}

