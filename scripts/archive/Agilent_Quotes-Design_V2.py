#!/usr/bin/env python
# coding: utf-8

# In[1]:


import tkinter as tk
from tkinter import ttk


# In[2]:


import sqlite3


# In[3]:


class Quote: #{
    
    db_filename = "data/test_quotes.db"
    
    def __init__(self, root): #{
        self.root = root
        self.root.title('Quotes Application')
        # [2019-11-11]\\ 1150x505+250+50
        # [2019-11-11]\\self.wind.geometry('865x750+250+50')  # (WIDTH x HEIGHT + XPOS + YPOS) 
        self.root.resizable(width=True, height=True)
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
    
    def create_gui(self): #{
        self.create_menubar()
        # [2019-11-11]\\self.create_top_icon()
        #self.create_paned_window()
        self.create_label_frame()
        self.create_message_area()
        self.create_tree_view()
        # [2019-11-12]\\self.create_side_buttons()
        self.view_records()
        self.create_side_pane()
        #self.create_bottom_buttons()
        #self.create_bottom_icon()
        #self.create_notes_area()
        # CONFIGURE MENUBAR
        self.root.config(menu=self.menubar)
    #}
    
    def create_menubar(self): #{
        self.menubar = tk.Menu(self.root)
        self.filemenu = tk.Menu(master = self.menubar,
                                borderwidth = 4,
                                background = "#0C85CE", 
                                font = ("Comfortaa", 12),
                                tearoff = 0)
        self.filemenu.add_command(label = "Import", command = "")
        self.filemenu.add_command(label = "Export", command = "")
        
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
    
    """
    def create_paned_window(self): #{
        # Create a PANED WINDOW Container
        panedwindow = tk.PanedWindow(master=self.root)  #, orient=tk.VERTICAL)
        panedwindow.grid(row = 0, column = 1, columnspan = 4, padx = 0, pady = 0)
        # test label
        tk.Label(master=panedwindow, text = " Test: ").grid(row = 1, column = 3)
        self.name = tk.Entry(panedwindow)
        self.name.focus()
        self.name.grid(row = 1, column = 3)
    #}
    """
    
    def create_label_frame(self): #{
        """
        labelframe = tk.LabelFrame(self.root, text='Register A New Quote')
        labelframe.grid(row=0, column=1, padx=8, pady=8, sticky='ew')
        tk.Label(labelframe, text='Name:').grid(row=1, column=1, sticky=tk.W, pady=2)
        """
        # Create a Frame Container
        frame = tk.LabelFrame(master = self.root, text = 'Register A New Quote')
        # [2019-11-11]\\frame.grid(row = 0, column = 1, rowspan = 2, padx = 8, pady = 8, sticky = 'ew')  #, padx = 20, pady = 20)
        # (row = 2, column = 0, columnspan = 3, padx = 8, pady = 8, sticky = 'ew')
        #frame.grid(row = 0, column = 0, columnspan = 3, padx = 8, pady = 1, sticky = 'ew')
        # [2019-11-11]\\frame.grid(row = 2, column = 0, rowspan = 1, columnspan = 8, )
        frame.grid(row = 0, column = 0, padx = 8, pady = 8, sticky=tk.W)
        
        # Name Input
        tk.Label(master = frame, text = 'Name: ').grid(row = 1, column = 0, sticky = tk.W, pady = 2)
        self.name = tk.Entry(master = frame)
        #self.namefocus()
        self.name.grid(row = 1, column = 1, sticky = tk.W, padx = 5, pady = 2)
        # [2019-11-13]\\^^^^^^^^^^^^ LOOK ABOVE FOR THE PADX AND THE PADY 
        
        # Email Input
        tk.Label(master = frame, text = 'Email: ').grid(row = 2, column = 0)
        self.email = tk.Entry(master = frame)
        self.email.grid(row = 2, column = 1)
        
        # Type Input
        tk.Label(master = frame, text = 'Type: ').grid(row = 1, column = 3)
        type_var = tk.StringVar()
        self.type = tk.Entry(master = frame, textvariable = type_var)
        self.type.grid(row = 1, column = 4)
        
        # Timestamp Input
        tk.Label(master = frame, text = 'Timetamp: ').grid(row = 2, column = 3)
        self.time = tk.Entry(master = frame)
        self.time.grid(row = 2, column = 4)
        
        # Sent Input
        tk.Label(master = frame, text = 'Sent: ').grid(row = 1, column = 5)
        self.sent = tk.Entry(master = frame)
        self.sent.grid(row = 1, column = 6) # row = 1, column = 6, 3, 0
        
        # Tracking Input
        tk.Label(master = frame, text = 'Tracking #: ').grid(row = 2, column = 5)
        self.tracking = tk.Entry(master = frame)
        self.tracking.grid(row = 2, column = 6)  # row = 2, column = 6, 3, 1
        
        # Button Add Quote
        ttk.Button(master = frame, text = 'Save Quote').grid(
            row = 3, columnspan = 2, sticky = tk.W + tk.E
        )
        
    #}
    
    def create_side_pane(self): #{
        self.notes_frame = tk.LabelFrame(master = self.root, text = "Notes:")
        #test_frame.grid(row = 2, column = 0, rowspan = 2, columnspan = 8, sticky = tk.W)
        self.notes_frame.grid(row = 2, column = 1, padx = 8, pady = 8, sticky = 'ew')
        
        self.m1 = tk.PanedWindow(master = self.notes_frame)
        self.m1.pack(fill = tk.BOTH, expand = 1)
        
        self.left = tk.Entry(master = self.m1, bd = 2)
        self.m1.add(self.left)
        
        self.m2 = tk.PanedWindow(master = self.m1, orient = tk.VERTICAL)
        self.m1.add(self.m2)
        
        self.top = tk.Scale(master = self.m2, orient = tk.HORIZONTAL)
        self.m2.add(self.top)
        
        self.bottom = ttk.Button(master = self.m2, text = "OK")
        self.m2.add(self.bottom)
    #}
    
    def create_message_area(self): #{
        self.message = tk.Label(text = 'roshambo', fg = 'red', padx = 8, pady = 8, relief = tk.RIDGE)
        # [2019-11-11]\\self.message.grid(row = 3, column = 1, sticky = tk.N)
        # [2019-11-12]\\self.message.grid(row = 0, column = 6, columnspan = 2, sticky = tk.N)
        self.message.grid(row = 3, column = 0, sticky = tk.N)  # tk.N
    #}
    
    def create_tree_view(self): #{
        """
        # Scrollbar
        scrollbar = tk.Scrollbar(self.root)
        scrollbar.pack(side = tk.RIGHT, fill = tk.Y)
        """
        
        # Table
        self.tree = ttk.Treeview(height = 20, columns = 8)
        self.tree["columns"]=("one","two","three","four","five","six","seven")
        self.tree.column('#0', width=80, minwidth=80, stretch=tk.NO)
        self.tree.column("one", width=125, minwidth=125, stretch=tk.NO)
        self.tree.column("two", width=150, minwidth=150, stretch=tk.NO)
        self.tree.column("three", width=40, minwidth=40, stretch=tk.NO)
        self.tree.column("four", width=150, minwidth=150, stretch=tk.NO)
        self.tree.column("five", width=40, minwidth=35, stretch=tk.NO)
        self.tree.column("six", width=80, minwidth=75, stretch=tk.NO)
        self.tree.column("seven", width=80, minwidth=75, stretch=tk.NO)
        # [2019-11-12]\\self.tree.column("eight", width=100, minwidth=25)
        
        # Definitions of Headings
        self.tree.grid(row = 1, column = 0, columnspan = 8)   # (4, 0, 8) THEN (0, 3, 4) THEN (3, 0, 8)
        self.tree.heading('#0', text = 'Tracking #', anchor = tk.CENTER)
        self.tree.heading('#1', text = 'Name', anchor = tk.CENTER)
        self.tree.heading('#2', text = 'Email', anchor = tk.CENTER)
        self.tree.heading('#3', text = 'Type', anchor = tk.CENTER)
        self.tree.heading('#4', text = 'Timestamp', anchor = tk.CENTER)
        self.tree.heading('#5', text = 'Sent', anchor = tk.CENTER)
        self.tree.heading('#6', text = 'Quote #', anchor = tk.CENTER)
        self.tree.heading('#7', text = 'Product #', anchor = tk.CENTER)
        # [2019-11-12]\\self.tree.heading('#8', text = 'Notes: ', anchor = tk.CENTER)
    #}
    
    def create_bottom_buttons(self): #{
        ttk.Button(text="Delete Selected", width=16, command=self.on_delete_selected_button_clicked).grid(
            row = 4, column = 0, sticky=tk.E)  # row = 2, column = 6
        ttk.Button(text="Modify Selected", width=16, command=self.on_modify_selected_button_clicked).grid(
            row = 4, column = 1, sticky=tk.W)  # row = 2, column = 7
    #}
    
    def create_bottom_icon(self): #{
        photo = tk.PhotoImage(file = "icons/agilent_logo-Copy1.png")
        label = tk.Label(background = "#0C85CE", image = photo)
        #label = tk.Label(background="#9e0ccf", image=photo)
        label.image = photo
        # [2019-11-11]\\  # rowspan = 3, then 4, NOW 0
        # [2019-11-11]\\label.grid(row = 0, column = 0, columnspan = 3) 
        # [2019-11-11]\\label.grid(row = 0, column = 0, sticky='ew') #( columnspan = 8)
        label.grid(row = 3, column = 3, sticky = tk.W)
    #}
    
    def create_notes_area(self): #{
        self.notes = tk.Text(background = 'tan', relief = tk.GROOVE, width = 60, height = 10)
        ###############################
        # PULL FROM SELECTED CELL ()
        try: #{
            query = "SELECT [Notes] FROM quotes WHERE [Tracking#] = '" 
            + str() 
            + "''"
        #}
        except: #{
            print("FAIL!")
        #}
        else: #{
            print("SUCCESS! Very Nice!")
        #}
        ###############################
        self.notes.grid(row = 2, column = 0, columnspan = 8, sticky = tk.W)
    #}
    
    """
    def populate_tree_view(self, the_tree): #{
        # VIEW RECORDS ######
        items = the_tree.get_children()
    #}
    """
    
    def on_add_record_button_clicked(self): #{
        pass
    #}
    
    def on_delete_selected_button_clicked(self): #{
        pass
    #}
    
    def on_modify_selected_button_clicked(self): #{
        pass
    #}
    
    def add_new_record(self): #{
        if self.new_records_validated(): #{
            query = 'INSERT INTO contacts VALUES(NULL,?, ?)'
            parameters = (self.namefield.get(), self.numfield.get())
            self.execute_db_query(query, parameters)
            self.message['text'] = 'Qutote record of {} added'.format(
                self.namefield.get())
            self.namefield.delete(0, tk.END)
            self.numfield.delete(0, tk.END)
        #}
        else: #{
            self.message['text'] = 'name and phone number cannot be blank'
        #}
        self.view_records()
    #}
    
    def new_records_validated(self): #{
        return len(self.namefield.get()) != 0 and len(self.numfield.get()) != 0
    #}
    
    def view_records(self): #{
        print("...BEGIN READING IN RECORDS...")
        # TRY THE FOLLOWING:
        try: #{
            items = self.tree.get_children()
            for item in items: #{
                self.tree.delete(item)
            #}
            query = 'SELECT * FROM quotes ORDER BY name desc'
            quote_book_entries = self.execute_db_query(query)
            for row in quote_book_entries: #{
                print("Tracking # == " + str(row[0]))
                print("Name == " + str(row[1]))
                print("Email == " + str(row[2]))
                print("Type == " + str(row[3]))
                print("Timestamp == " + str(row[4]))
                print("Sent == " + str(row[5]))
                # CREATE LIST
                test_lst = [str(row[1]), str(row[2]), str(row[3]), str(row[4]), str(row[5])]
                # INSERT INTO TREE
                self.tree.insert('', 0, text=str(row[0]), values=test_lst)
                # [2019-11-11]\\self.tree.insert('', 0, text=row[1], values=row[2])
            #}
        #}
        except: #{
            print("FAILURE IN THE TREE-VIEW!")
        #}
        else: #{
            print("Operation done successfully")
        #}
    #}
    
    def delete_record(self): #{
        pass
    #}
    
    def open_modify_window(self): #{
        name = self.tree.item(self.tree.selection())['text']
        old_email_address = self.tree.item(self.tree.selection())['values'][0]
        self.transient = tk.Toplevel()
        
    #}
    
    def update_record(self, newphone, old_phone_number, name): #{
        pass
    #}
    
#}


# In[4]:


if __name__ == "__main__": #{
    window = tk.Tk()
    application = Quote(window)
    window.mainloop()
#}


# In[ ]:





# In[ ]:




