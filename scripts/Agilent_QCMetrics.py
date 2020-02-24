# -*- coding: utf-8 -*-
"""
Created on Mon Feb 24 16:16:13 2020

@author: derbates

TABLES INPUTEED:
    - tblProdflow
    - PRODUCTS

==========================================
DETERMINES NUMBER OF "PfBatchID" over 
last 30 days, in 3 level bins 
(L1, L2, L3)
==========================================

"""

# IMPORT THE GOODS
import os, sys, time
from time import sleep
from pathlib import Path
from datetime import datetime, timedelta

class AgilentQCMetrics(): # {
    
    outbound_dir = "C:/data/outbound/"
    
    def __init__(self): # {
        pass
    # }
    
    def create_metrics_table(self): # {
        pass
    # }
    
# }

if __name__ == "__main__": # { 
    test_metrics = AgilentQCMetrics()
# }