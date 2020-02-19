# -*- coding: utf-8 -*-
"""
Created on Wed Feb 19 10:24:35 2020

METRICS

@author: derbates
"""

# IMPORT THE GOODS
import os, sys, time
from time import sleep
from pathlib import Path
from datetime import datetime
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog
from tkinter import messagebox
import pandas as pd
import numpy as np
from pandas import Series, DataFrame
import pyodbc
import matplotlib
from matplotlib import pyplot as plt
import seaborn as sns