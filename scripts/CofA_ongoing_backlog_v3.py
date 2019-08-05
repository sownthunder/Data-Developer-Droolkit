#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os, sys, time
from time import sleep
from pathlib import Path
import fnmatch, glob, shutil
import wmi, psutil
import tempfile, logging
import ctypes
import codecs


# In[2]:


import pandas as pd
import numpy as np
from pandas import Series, DataFrame


# In[3]:


from datetime import datetime


# In[4]:


# SETUP LOGGER
try: #{
    logging.basicConfig(level=logging.INFO,
                        stream=sys.stdout,
                        format='%(asctime)s : \n\t\t\t\t [MESG] : %(message)s \n\t\t\t\t [LINE] : %(lineno)s',
                        datefmt='%Y-%m-%d-%H%M%S'
                        )
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
    print("[SETUP-LOGGER] FIN...")
#}


# ## *DEFINE FUNCTIONS*

# In[5]:


def convert(lst): #{
    return (lst[0].split())
#}


# In[6]:


def countdown(n):  # {
    while n > 0:  # {
        # print (n)
        sleep(1)  # sleep for 1 second
        n = n - 1
        if n == 0:  # {
            logging.info("Blast Off!")
        # }
    # }
# }


# ## *DEFINE DIRECTORIES*

# In[7]:


f_drive = Path("F:/APPS/CofA/")


# In[8]:


g_drive = Path("G:/C of A's/#Email Node/")


# In[9]:


c_drive = Path("C:/CofA/")


# ## import IDX as DataFrame

# In[10]:


idx_file = "C:/CofA/log/CofA-backlog.csv"  # WAS: .txt


# In[11]:


# DATAFRAME WITH 'INDEX' txt imported
df_idx = pd.read_csv(idx_file, header=None, names=['CofA'], dtype=np.str, engine='python', encoding="'cp1252'")


# In[12]:


logging.info(df_idx.describe)


# In[13]:


df_idx.head(5)


# In[14]:


# CREATE DATAFRAME OFF OF 'polling' DIR
scan_directory = "G:/C of A's/#Email Node/"
scan_path = Path(scan_directory)
g_list = os.listdir(scan_path)


# In[15]:


# CREATE SERIES FROM LIST
g1 = pd.Series(g_list)
g1.astype(dtype=np.str)


# In[16]:


# CREATE EMPTY DATAFRAME
df_g_list = pd.DataFrame()


# In[17]:


# ASSIGN SERIES TO DATAFRAME COLUMN
df_g_list['CofA'] = g1


# In[18]:


df_g_list.head(5)


# In[ ]:





# In[ ]:





# ---

# # `set_diff_df` CREATION << HERE >>

# In[19]:


set_diff_df = pd.concat([df_idx, df_g_list, df_idx]).drop_duplicates(keep=False)
logging.info(set_diff_df.describe)


# In[20]:


len(set_diff_df)


# ### *CREATE `TIMESTAMP`*

# In[21]:


ts = pd.Timestamp.now()


# In[22]:


time_now = str(ts)


# In[23]:

time_now = time_now[:10]
logging.info(time_now)


# # `to_csv`

# In[24]:


set_diff_df.to_csv("C:/CofA/log/CofA-email-diffs-"
                  + str(time_now)
                  + ".csv", index=False)


# # << ITER TUPLES >>

# In[25]:


try: #{
    for row in set_diff_df.itertuples(index=False, name='emails'): #{
        the_str = str(row[0])
        # GET LIST OF STRINGS
        listed_str = convert(row)
        #print(listed_str)
        # OLD NAME/F_DRIVE VARIABLE
        old_name = str(listed_str[1]) + "@" + str(listed_str[4])
        # F_DRIVE PATH
        f_drive_path = os.path.join(f_drive, old_name)
        # C_DRIVE_PATH
        c_drive_path = os.path.join(c_drive, old_name)
        # G_DRIVE_PATH
        g_drive_path = os.path.join(g_drive, str(row[0]))
        #print(f_drive_path)
        # IF F_DRIVE VERSION OF FILE **DOES NOT EXIST**
        if os.path.exists(f_drive_path) is False: #{
            logging.debug("[F-DRIVE] FALSE == " + str(f_drive_path))
            # CHECK IF IN C_DRIVE
            if os.path.exists(c_drive_path) is False: #{
                logging.debug("[C-DRIVE] FALSE == " + str(c_drive_path))
            #}
        #}
        # ELSE.... FILE DOES EXIST IN F_DRIVE
        else: #{
            # GET CREATION_DATE
            created = os.stat(f_drive_path).st_ctime_ns
            # CONVERT CREATION_DATE TO PANDAS.TIMESTAMP
            c_stamp = pd.Timestamp(created)
            # GET MODIFICATION_TIME
            modified = os.stat(f_drive_path).st_mtime_ns
            # CONVERT MODIFIED TIME TO PANDAS.TIMESTAMP
            m_stamp = pd.Timestamp(modified)
            #########################################3##
            # PANDAS.TIMEDELTA FOR SUBTRACTING DATES
            creation_delta = pd.Timedelta(created - modified)
            logging.debug("DELTA TIME (created - modified) >>> " + str(creation_delta))
            # CREATE CHECK DELTA TO USE 'AGAINST' CREATION_DELTA
            check_delta = pd.Timedelta(value=1, unit='min')
            # IF DELTA IS LESS THAN ONE-MINUTE (NEGATIVE)
            if (creation_delta <= check_delta): #{
                logging.debug("<< CREATION DATE IS OLDER >>")
                logging.debug("CREATED == " + str(c_stamp)) # WAS: logging.info
                logging.debug("MODIFIED == " + str(m_stamp))
                # SET STRING VAR FOR EMAIL OUTPUT
                date_str = str(c_stamp)
            #}
            # ELSE... DELTA IS GREATER THAN ONE-MINUTE
            else: #{
                logging.debug("<< MODIFIED DATE IS OLDER >>")
                logging.debug("MODIFIED == " + str(m_stamp)) # WAS: logging.info
                logging.debug("CREATED == " + str(c_stamp))
                # SET STRING VAR FOR EMAIL OUTPUT
                date_str = str(m_stamp)
            #}
            
            """
            # COMPARE CREATION DATE <> MODIFIED TIME
            if c_stamp > m_stamp: #{
                logging.info("CREATED == " + str(c_stamp))
            #}
            else: #{
                logging.info("MODIFIED == " + str(m_stamp) + "\n\r\t\t\t\t\tCREATED == " + str(c_stamp))
            #}
            """
        #}
        # NEW_NAME VARIABLE
        new_name = str(row[0])
        ########################
        #logging.info(the_str)
        #logging.info(convert(str(row[0])))
        #cmd_str = 'C:/EXE/CofA_AUTO_EMAIL_v2.exe "'
        cmd_str = 'C:/EXE/CofA_SMTP_Sender.exe "'
        # STRIP '#' AND '.PDF' FROM STRING
        logging.info("BEFORE STRIP == " + str(new_name))
        strip_name = new_name.replace("#", "")
        strip_name = strip_name.replace(".pdf", "")
        logging.info("AFTER STRIP == " + str(strip_name))
        cmd_str += str(new_name) + '" '
        cmd_str += '"Created on: '
        cmd_str += str(date_str) + '" '
        cmd_str += '"'
        cmd_str += str(g_drive_path) + '"'
        # SEND CMD-STR TO COMMAND_LINE
        os.popen(cmd_str)
        logging.info(cmd_str)
        logging.info("Sleeping...")
        sleep(8)  # WAS: 120
        """
        ###########################################################################################
        # CREATE 'APPENDAGE' DATAFRAME
        df_appendage = pd.DataFrame(data=[str(new_name)], columns=['CofA'], dtype=np.str)
        # [codecs.encode(obj=str(new_name), encoding='cp1252')]
        # APPEND THE DATAFRAME TO OUR INDEX_FILE
        """
        #df_appendage.to_csv(idx_file, mode='a', index=False)
        """
        # APPEND TO DATAFRAME OF 'df_idx' *AS* NEW DATAFRAME
        df_backlog = df_idx.append(df_appendage, ignore_index=True, sort=False)
        # OVERWRITE ".txt" FILE WITH NEW DATAFRAME
        df_backlog.to_csv(idx_file, columns=None,  # encoding="'cp1252'",
                          header=False, index=False, mode='w')
        #############################################
        """
        ## SAVE AND END
        #logging.info("SENT AT " + str(pd.Timestamp.now()))
        #path = "C:\CofA\log\CofA-backlog.txt"
        #fo = open(path, "a+")
        # USE 'new_name' BECAUSE ITS NOT 'STRIPPED'
        #fo.write("\n" + str(new_name))
        #fo.close()
        #logging.info("email <== ADDED TO BACK-LOG-COMPLETE ==> ")
        ## GET END TIME
        #time_end = pd.Timestamp.now()
        #logging.info("TOTAL RUNTIME == " + str(time_end - time_start))
        ################################################
        #countdown(2)
    #}
    time_end = pd.Timestamp.now()
    # calculate runtime
    run_time = pd.Timedelta(time_end - ts)
    logging.info("TOTAL RUNTIME == " + str(run_time))
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
    logging.info("\n" + typeE +
                     "\n" + fileE +
                     "\n" + lineE +
                     "\n" + messageE)
#}
else: #{
    logging.info("<< LOCKING WORKSTATION >>")
    # LOCK WORK STATION BECAUSE WE ARE NO LONGER AT WORK
    ctypes.windll.user32.LockWorkStation()
    if ctypes.windll.user32.LockWorkStation() == 1: #{
        logging.info("WORKSTATION LOCKED!")
    #}
    else: #{
        logging.info("WORKSTATION NOT LOCKED!")
    #}
    logging.info("[email-CofA] FIN...")
#}


# >>> `(do the following) ABOVE `

# In[ ]:





# ## 1) create *file_name* for `F:/APPS/CofA/`
# ## 2) create *path_var* for `F:/APPS/CofA/`
# ## 3) get *create_date/mod_date* from *path_var*

# In[ ]:





# In[ ]:





# ### `append` to `C:/CofA/log/CofA-backlog.txt`
# CREATE ROW ON FLY
"""
new_row = pd.DataFrame(('CofA':))
# In[ ]:





# In[ ]:





# ## `create_date`∆ & `mod_time`

# In[26]:


#date_path = os.path.join()


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# # EVERYTHING BELOW IS CRAP !
# ---

# ### READ IN `.TXT` FILE... *(for index)*
# OPEN A FILE
fo = open(idx_file, "r")

with open(idx_file) as f: #{
    content = f.readlines()
#}
# you may also want to remove whitespace characters like `\n` at the end of each line
content = [x.strip() for x in content]

# CLOSE THE FILE
fo.close()idx_str = "NUMBER WITHIN INDEX: \t" + str(len(content))
logging.info(idx_str)
# ### INTIALIZE `INDEX`
idx = pd.Index(content)logging.info(idx)print(str(idx[15]))idx.drop_duplicates()
# >>>  ## get prepared to **os.walk**()
# >>> `(SAVE ALREADY EMAILED PDFs TO LIST FOR "UPDATING")` 
# 
# `"C:/CofA/log/CofA-backlog.txt"`

# 
# ## os.walk thru
# `G:/C of A's/#Email Node/`
out_directory = "G:/C of A's/#Email Node/"outbound_path = Path(out_directory)count = 0

# iterate thru directory/directories
for root, d_names, f_names in os.walk(outbound_path): #{
    # IF THERE IS MORE THAN 1 FILE:
    if len(f_names): #{
        # FOR EACH FILE:
        for f in f_names: #{
            # IS IT IN INDEX??
            if idx.contains(str(f)): #{
                # DO NOTHING CHAD!
                email_str = "already emailed : " + str(f)
                logging.info(email_str)
                count += 1
            #}
            # ELSE.. << NOT IN INDEX >>
            else: #{
                #print("NOT IN INDEX !!!!")
                logging.info("ABOUT TO SEND == " + str(f))
                count += 1
            #}
        #}
    #}
#}
print("COUNT == " + str(count))print(len(os.listdir("G:/C of A's/#Email Node/")))
# # `ongoing_CofA_email_list.py`
# 
# ---

# ## CREATE `set_diff_df`

# In[27]:


df_emails = pd.DataFrame()
"""
