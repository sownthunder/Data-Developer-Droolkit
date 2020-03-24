# -*- coding: utf-8 -*-
"""
Created on Tue Mar 17 11:21:53 2020

@author: derbates
"""


# IMPORT THE GOODS
import os, sys, time
from time import sleep
import pyautogui

def main(): # {
    while 1: # {
        print("MOVING...")
        pyautogui.move(10, 10, 0.5)
        sleep(180)
    # }
# }

if __name__ == "__main__": # {
    main()
# }