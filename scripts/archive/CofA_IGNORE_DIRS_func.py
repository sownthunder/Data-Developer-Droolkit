# IMPORT THE GOODS
import os, sys, time
from time import sleep
from datetime import datetime
from pathlib import Path
import fnmatch, glob, shutil
import pandas as pd
import numpy as np
from pandas import Series, DataFrame

def scan_directory(the_directory, ignore_dir_list, file_type_list): #{
	# CREATE LIST VARIABLE TO HOLD CLEAN DATA
	path_list = []
	# COUNTER
	x = 0
	# TRY THE FOLLOWING
	try: #{
	    # SETUP VARIABLES
	    in_directory = Path(the_directory)
	    # BEGIN OS.WALK
	    for root, dirs, files in os.walk(scan_directory): #{
	        # FOR EACH ITEM IN IGNORE LIST...
	        for item in ignore_dir_list: #{
	            # IF THAT ITEM IS IN FACT IN DIRECTORY...
	            if str(item) in dirs: #{
	                # REMOVE FROM OS.WALK
	                dirs.remove(str(item))
	            #}
	        #}
	        # OTHERWISE IF THERE ARE FILES IN DIRECTORY
	        for f in files: #{
	            # FOR EACH ITEM IN 'file_type_list'
	            for item in file_type_list: #{
	                # CREATE FILE_MATCH VAR
	                file_match = str("*" + item)
	                # DO FNMATCH FOR THIS "item"
	                if fnmatch.fnmatch(f, file_match): #{
	                    # ASSEMBLE!
	                    file_path = os.path.join(root, f)
	                    # APPEND TO FILE LIST
	                    file_list.append(file_path)
	                   # INCREMENT COUNTER
	                   x += 1
	                #}
	                else: #{
	                    print("NOT A PDF : \t" + str(f))
	                #}
	            #}
	        #}
	    #}
	    # CREATE NEW DATAFRAME TO HOLD LIST
	    df_filelist = pd.DataFrame(data=None, columns=None, dtype=np.str)
	    # ASSIGN LIST TO COLUMN IN DATAFRAME
	    df_filelist['CofA'] = file_list
	    # EXPORT TO NECESSARY FOLDER
	    export_path = os.path.join()
	#}
	except: #{
	    test = 0
	#}
	else: #{
	    print("SUCCESS! VERY NICE!")
	#}
	finally: #{
	    print("FIN...")
	#} 
#}

if __name__ == "__main__": #{
	# INSTANTIATE GLOBAL VARIABLES
	out_file = "1"
	in_directory = "F:/APPS/CofA/"
#}