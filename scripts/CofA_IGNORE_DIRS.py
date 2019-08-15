#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os, sys, time
from time import sleep
from pathlib import Path
import fnmatch, glob, shutil


# In[2]:


import pandas as pd
import numpy as np
from pandas import Series, DataFrame


# In[3]:


from os.path import join, getsize


# In[4]:


in_directory = "F:/APPS/CofA/"


# In[5]:


ts = pd.Timestamp.now()


# In[6]:


time_now = str(ts)
time_now = time_now[:10]
print(time_now)


# In[7]:


# create list to hold clean data yo
path_list = []

# counter
x = 0

for root, dirs, files in os.walk(in_directory): #{
    # DIRECTORY SKIP CONDITIONS
    if 'Archive ERR' in dirs: #{
        dirs.remove('Archive ERR')  # don't visit Archive ERR directories
    #}
    if 'Archive - For all archive CofA, see G CofA folder' in dirs: #{
        dirs.remove('Archive - For all archive CofA, see G CofA folder') # skip
    #}
    if 'Instruction Sheets' in dirs: #{
        dirs.remove('Instruction Sheets') # skip
    #}
    # OTHERWISE IF THERE ARE FILES IN DIRECTORY
    for f in files: #{
        # IF FILE IS OF TYPE .pdf
        if fnmatch.fnmatch(f, "*.pdf"): #{
            # ASSEMBLE!
            file_path = os.path.join(root, f)
            """
            # GET CREATE TIME
            create_time = os.path.getctime(file_path)
            # GET MODIFIED TIME
            mod_time = os.path.getmtime(file_path)
            # MAKE 'ctime' INTO DATETIME / more readable
            readable_c = datetime.datetime.fromtimestamp(create_time).isoformat()
            # MAKE 'mtime' INTO DATETIME / more readable
            readable_m = datetime.datetime.fromtimestamp(mod_time).isoformat()
            # CONVERT TO pandas.Timestamp
            timeStamp_c = pd.Timestamp(readable_c)
            # AGAIN FOR MODIFIED TIME
            timeStamp_m = pd.Timestamp(readable_m)
            """
            path_list.append(file_path)
            x += 1
        #}
        else: #{
            print("NOT A PDF : \t" + str(f))
        #}
    #}
#}
# CREATE NEW DATAFRAME TO HOLD LIST
df_paths = pd.DataFrame()
# ASSIGN LIST TO COLUMN IN DATAFRAME
df_paths['CofA File'] = path_list
df_paths.to_csv("C:\CofA\log\CofA_Email_Node_List_" + time_now + "_pull.csv", index=False)
print("\n COUNT == " + str(x))