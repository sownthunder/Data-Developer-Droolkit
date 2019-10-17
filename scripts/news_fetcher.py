"""
FETCH DA NEWS


"""

# import the goodies
import os, sys, time
from time import sleep
import datetime
from datetime import date

import random

import tkinter as tk
from tkinter import filedialog
from tkinter import font
from tkinter import ttk
from tkinter import messagebox

import sqlite3
import pyautogui

# INCLUDE:
# ttk.Progressbar()

# importing requests package
import requests



class App(object): #{
    def __init__(self):  # {
        self.root = tk.Tk()
        self.root.geometry('400x300+250+250')
        self.style = ttk.Style()
        available_themes = self.style.theme_names()
        random_theme = random.choice(available_themes)
        self.style.theme_use(random_theme)
        self.root.title(random_theme)

        # TOP FRAME
        frm = ttk.Frame(master=self.root)
        frm.pack(expand=True, fill='both')
        # create a Combobox with themes to choose from
        self.combo = ttk.Combobox(frm, values=available_themes)
        self.combo.pack(padx=32, pady=8)
        # make the Enter key change the style
        self.combo.bind('<Return>', self.change_style)
        # make a Button to change the style
        button = ttk.Button(frm, text='OK')
        button['command'] = self.change_style
        button.pack(pady=8)

        # BOTTOM FRAME
        bottom_frm = ttk.Frame(master=frm)
        bottom_frm.pack(expand=True, fill='both', side=tk.BOTTOM)
        # LABEL
        labeltext = tk.StringVar()
        # set news to label?
        labeltext.set(str(news))
        # make a Label to display the news articles
        newslabel = ttk.Label(frm, textvariable=labeltext)

    # }

    def change_style(self, event=None):  # {
        """set the Style to the content of the Combobox"""
        content = self.combo.get()
        try:  # {
            self.style.theme_use(content)
        # }
        except tk.TclError as err:  # {
            messagebox.showerror('Error', err)
        # }
        else:  # {
            self.root.title(content)
        # }
    # }
#}

"""
BBB-NEWS-FEED

"""
def NewsFromBBC(): #{
    # BBC news api
    main_url = " https://newsapi.org/v1/articles?source=bbc-news&sortBy=top&apiKey=4dbc17e007ab436fb66416009dfb59a8"

    # fetching data in json format
    open_bbc_page = requests.get(main_url).json()

    # getting all articles in a string article
    article = open_bbc_page["articles"]

    # empty list which will
    # contain all trending news
    results = []

    for ar in article: #{
        results.append(ar["title"])
    #}

    for i in range(len(results)): #{
        # printing all trending news
        print(i + 1, results[i])
    #}

    print("RESULTS AS LIST : \n" + str(results))
    # Driver Code
    return results
#}

####################################
# GLOBALS
global root
global news
##################################################
root = tk.Tk()
# INITIALIZE VARS
news = NewsFromBBC()

def store_into_db(): #{
    # try the following
    try: #{
        # TIME STAMP
        time_object = str('{0:%Y-%m-%d}'.format(datetime.datetime.now()))
        print(str("file naming convention (today's example) :"), time_object)
        # ask for db file
        root.file = filedialog.askopenfilename(initialdir="/", title="Select file",
                                   filetypes=(("DB files", "*.db"), ("all files", "*.*")))
        # create database conn
        cnxn = sqlite3.connect(root.file)
        # create cursor
        crsr = cnxn.cursor()
        # Create table
        ## crsr.execute('''CREATE TABLE news (date text, article text)''') # TABLE CREATED 05/26/19

        ## INSERT THE NEWS
        for i in range(len(news)):#{
            # Insert a row of data
            crsr.execute("INSERT INTO news VALUES ('" + str(time_object) + "','" + str(news[i]) + "'" + ")")
        #}

        # Save (commit) the changes
        cnxn.commit()

        # We can also close the connection if we are done with it.
        # Just be sure any changes have been committed or they will be lost.
        cnxn.close()
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
        messageE = str("MESG : " + "\n" + str(errorMessage) + "\n")
        print("\n" + typeE +
              "\n" + fileE +
              "\n" + lineE +
              "\n" + messageE)
    #}
    else: #{
        print("FIN...[store_into_db]")
    #}
#}
def main(): #{
    #
    #  GUI call
    #app = App()
    #app.root.mainloop()
    ####################################
    try: #{
        root.title('top ten last news')
        root.geometry('450x550+300+300')
        root.resizable(width=True, height=False)

        # TOP FRAME
        topframe = tk.Frame(master=root, relief=tk.SUNKEN)
        topframe.pack(expand=True, fill=tk.X, side=tk.TOP)

        # function call
        bbc_snews = NewsFromBBC()
        bbc_str = "[APPENDING NEWS LIST]:\n"
        # seperate return from LIST-FORM
        for i in range(len(bbc_snews)):#{
            bbc_str += bbc_snews[i] + "\n"
            print(bbc_str)
        #}

        # SETUP STRING
        text1_var = tk.StringVar()
        # SET NEWS TO TK STR VAR
        text1_var.set(bbc_str) # WAS: bbcc_snews

        # LABEL
        l1 = tk.Label(master=topframe, textvariable=text1_var, font=("Source Code Pro", 8))
        l1.pack(expand=True, fill=tk.BOTH, anchor=tk.CENTER)

        # ATTACH STR VAR TO TEXT
        text1 = tk.Text(master=root,  fg="gold", bg="navy",
                        height=14, width=150,
                        font=("Courier New", 14))
        text1.setvar(bbc_str)
        text1.pack(anchor="center")

        # BOTTOM FRAME
        bottomframe = tk.Frame(master=topframe, relief=tk.RAISED)
        bottomframe.pack(expand=False, fill=tk.Y, side=tk.BOTTOM)

        b1 = tk.Button(master=bottomframe, text="STORE NEWS", command=store_into_db)
        b1.pack(expand=True, fill=tk.BOTH, anchor=tk.CENTER)

        root.config()
        root.mainloop()
    #}
    except: #P
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
        print("FIN...[main]")
    #}
#}

if __name__ == '__main__': #{
    main()
#}
