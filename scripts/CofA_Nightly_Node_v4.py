# -*- coding: utf-8 -*-
"""
Created on Fri Apr 17 11:09:00 2020

CofA_Nightly_Node_v4

USES:
    CofA_Nightly_Node_v3 (FINALE).py

@author: derbates
"""

# IMPORT THE GOODS
import os, sys, time
from time import sleep
from pathlib import Path
import logging, subprocess
from threading import Timer
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk
import pandas as pd
import numpy as np
from pandas import Series, DataFrame

class CofA_Nightly_Node(): # {
    
    def __init__(self): # {
        pass
    # }
# }