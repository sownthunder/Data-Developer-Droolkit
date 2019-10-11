# -*- coding: utf-8 -*-
"""
Created on Fri Oct 11 09:43:14 2019

pandas loop testing (FINALE)

@author: derbates
"""

# IMPORT THE GOODS
import os, sys, time
from time import sleep
from pathlib import Path

from urllib.request import urlopen
URL = 'https://www.twitter.com/'
PROXY_ADDRESS = '192.168.0.100'

if __name__ == "__main__": #{
    resp = urlopen(URL, proxies={"http":PROXY_ADDRESS})
#}

print("Proxy server returns response headers: %s " %resp.headers)