"""
2019/08/6 - WAITING ON NITD from Mary-Anne, no need to finish script

"""

import os, sys, time
from time import sleep
from pathlib import Path
import fnmatch, glob, shutil
import wmi, psutil
import tempfile, logging
import ctypes
import codecs
import email, smtplib, ssl
import os.path as op
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
import pandas as pd
import numpy as np
from pandas import Series, DataFrame


if __name__ == "__main__": #{
	"""
	# SETUP LOGGER
	try: #{
	    logging.basicConfig(level=logging.INFO, stream=sys.stdout, )
	#}
	"""
	if sys.argv > 1: #{
		print("COMMAND LINE INTERFACE CALL")
	#}
	else: #{
		print("REGULAR GUI CALL")
		# SETUP LOG FILE VARIABLE
		in_file = "C:/CofA/log/CofA-backlog.csv"
		df_backlog = pd.read_csv(in_file, header=None, names=['CofA'], dtype=np.str, engine='python')
		len(df_backlog)
	#}



#}