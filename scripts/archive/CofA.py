# -*- coding: utf-8 -*-
"""
Created on Sat Feb 29 08:42:45 2020

EVERYTHING "CofA"

- F:/APPS/CofA/
- 

@author: derbates
"""

# IMPORT THE GOODS
import os, sys, time
from time import sleep
import pathlib, glob
from pathlib import Path
import fnmatch, shutil
import datetime
import pandas as pd
import numpy as np
from pandas import Series, DataFrame
import logging
import tempfile, threading
from PyPDF2 import PdfFileReader, PdfFileWriter
from zipfile import ZipFile
import email, smtplib, ssl
import os.path as op
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox, filedialog
from ttkthemes import ThemedStyle

class CofA(ttk.Frame): # {
    
    watermark_file = "C:/data/inbound/Agilent_CofA_Letterhead_03-21-19.pdf"
    
    def __init__(self): # {
        pass
    # }
    
# }