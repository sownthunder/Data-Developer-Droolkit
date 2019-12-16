"""
"""

# IMPORT THE GOODS
import os, sys, time
from time import sleep
import logging
from urllib.parse import urljoin, urlparse
import pandas as pd
import numpy as np
from pandas import Series, DataFrame
from random import choice, randint
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.proxy import Proxy, ProxyType
from http_request_randomizer.requests.proxy.requestProxy import RequestProxy
import pyautogui

class LinkLooper:  # {

    def __init__(self, the_link_list, logout_dir):  # {
        self.the_link_list = the_link_list
        self.logout_dir = logout_dir
        # TRY THE FOLLOWING
        try:  # {
            # CREATE PROXY LIST
            self.proxies = self.collect_proxy_list()
            logging.info(str(self.proxies[0].get_address()))
            logging.info(str(self.proxies[1].country))
            # INSTANTIATE DRIVER
            # [2019-12-14]\\self.driver = self.setup_driver()
            # self.timeout = 3  # TIME TO WAIT FOR EACH PAGE TO LOAD
            # VISIT SITE
            # [2019-12-14]\\self.driver.get('https://www.expressvpn.com/what-is-my-ip')
            """ [2019-12-14]
            # WAIT FOR PAGE TO LOAD
            try:  # {
                element_present = EC.presence_of_element_located((By.ID, 'main'))
                WebDriverWait(self.driver, self.timeout).until(element_present)
            # }
            except TimeoutException:  # {
                logging.info("Timed out waiting for page to load")
            # }
            else:  # {
                logging.info("Page Loaded Successfully...")
            # }
            """
            # [2019-12-14]\\self.driver.get("https://pornhub.com/model/heather-kane")
        # }
        except:  # {
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
        # }
        else: # {
            logging.info("Operation Completed Successfully...")
        # }
    #}

    def setup_driver(self, use_proxy):  # {
        # CHECK IF WE WANT TO USE PROXY / FIREFOX
        if use_proxy is True:  # {
            PROXY = self.proxies[0].get_address()
            webdriver.DesiredCapabilities.FIREFOX['proxy'] = {
                "httpProxy": PROXY,
                "ftpProxy": PROXY,
                "sslProxy": PROXY,

                "proxyType": "MANUAL",

            }
            # RETURN FIREFOX
            return webdriver.Firefox(executable_path=r"C:\FireFox\geckodriver.exe")
        # }
        else: #{
            # USE CHROME
            return webdriver.Chrome()
        # }
    # }

    def tear_down(self, the_driver): # {
        the_driver.quit()
    # }

    def collect_proxy_list(self):  # {
        reg_proxy = RequestProxy()
        # create proxy list
        proxies = reg_proxy.get_proxy_list()
        # COLLECT CAMBODIA
        cam = []
        # COLLECT INDIA
        ind = []
        for proxy in proxies:  # {
            if proxy.country == "Cambodia":  # {
                cam.append(proxy)
            # }
            elif proxy.country == "India":  # {
                ind.append(proxy)
            #}
        #}
        return list(cam + ind)
        # [2019-12-14]\\return proxies
    # }

    def create_new_record(self, the_link, watch_duration, the_timestamp, current_count):  # {
        # CREATE EMPTY DATAFRAME
        new_entry_df = pd.DataFrame(data=None, dtype=np.str)
        # CREATE COLUMNS AND RESPECTIVE DATA
        new_entry_df["Link"] = [the_link]
        new_entry_df["w_Duration"] = [watch_duration]
        new_entry_df["w_Timestamp"] = [the_timestamp]
        new_entry_df["Current_Count"] = [current_count]
        # RETURN THE DATAFRAME
        return new_entry_df
    #}

    def run_videos(self, the_driver, the_link_list):  #{
        # SETUP TIMEOUT
        timeout = 3
        # TRY THE FOLLOWING
        try:  # {
            logging.info(str(the_driver.title))
            # GET PARENT WINDOW
            parent_window = the_driver.current_window_handle
            # LOOP THRU LIST
            for link in the_link_list:  # {
                # OPEN LINK IN NEW WINDOW
                the_driver.execute_script("window.open('" + str(link) + "')")
                # WAIT FOR PAGE TO LOAD
                try:  # {
                    element_present = EC.presence_of_element_located((By.ID, 'main'))
                    WebDriverWait(the_driver, timeout).until(element_present)
                # }
                except TimeoutException:  # {
                    logging.error("Timed out waiting for page to load")
                #}
                else:  # {
                    logging.info("Page Loaded Successfully...")
                # }
                # GETLIST OF ALL WINDOWS CURRENT OPENED (Parent + CHild)
                all_windows = the_driver.window_handles
                logging.info("WINDOW_HANDLES:\n" + str(all_windows))
                # GET CHILD WINDOW
                child_window = [window for window in all_windows if window != parent_window][0]
                # SWITCH TO CHILD WINDOW
                the_driver.switch_to.window(child_window)
                # WAIT FOR PAGE TO LOAD
                try:  # {
                    element_present = EC.presence_of_all_elements_located((By.ID, 'main'))
                    WebDriverWait(the_driver, timeout).until(element_present)
                # }
                except TimeoutException:  # {
                    logging.error("Timed out waiting for page to load")
                # }
                else:  # {
                    logging.info("Page Loaded Successfully...")
                # }
                # GET SCREEN SIZE
                screen_size = pyautogui.size()
                print(" SCREEN SIZE == " + str(screen_size))

                logging.info(str(the_driver.title))
                # GET COUNT VIA LINK
                video_count = the_driver.find_element(By.CLASS_NAME, "count")
                logging.info("CURRENT COUNT:\n" + str(video_count))
                # WATCH FOR RANDOM DURATION
                rand_duration = randint(75, 150)  # WAS: 75, 120
                logging.info("WATCHING VIDEO FOR RANDOM DURATION OF == " + str(rand_duration))
                # COUNTDOWN
                countdown(rand_duration)
                # CLOSE CHILD WINDOW
                the_driver.close()
                # SWITCH BACK TO PARENT WINDOW
                the_driver.switch_to.window(parent_window)
            # }
        # }
        except:  # {
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
        # }
        finally:  # {
            logging.info("<END>>")
            # QUIT DRIVER
            the_driver.quit()
        # }
    # }

# }

class Logger():  # {

    def __init__(self):  # {
        # Initiating the Logger object
        self.logger = logging.getLogger(__name__)

        # Set the level of the logger This is SUPER USEFUL since it enables
        # Explanation regarding the logger levels can be founder here:
        # https://docs.python.org/3/howto/logging.html
        self.logger.setLevel(logging.DEBUG)

        """
        # Create file handler which logs even debug messages
        fh = logging.FileHandler('spam.log')
        fh.setLevel(logging.DEBUG)
        """

        # Create the logs.log file
        # [2019-12-13]\\file_handler = logging.FileHandler("C:/data/Logs/VideoLogger/vlogs.log")
        file_handler = logging.FileHandler("C:/data/Logs/LINKLOOPER.log")

        # Create the console handler with a higher log level
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.ERROR)

        # Format the logs structure so that every line would include:
        # the time, name level name and log message
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        # Adding the format handlers
        self.logger.addHandler(console_handler)
        self.logger.addHandler(file_handler)

        # and printing the logs to the console as well
        self.logger.addHandler(logging.StreamHandler(sys.stdout))
    # }

# }

def countdown(n): #{
    while n >= 0: #{
        sleep(1)
        logging.debug(n)
        # decrement count
        n -= 1
    #}
    else: #{
        logging.debug("Blast Off!")
    #}
#}

def main():  # {
    # RE-INSTANTIATE GLOBAL VARIABLES
    global link_list, logger
    # TRY THE FOLLOWING
    try:  # {
        # CREATE CLASS OBJECT
        linky = LinkLooper(the_link_list=link_list, logout_dir="C:/data/Logs/LINKLOOPER.log")
        # CREATE DRIVER OBJECT
        driver = linky.setup_driver(use_proxy=False)
        driver.maximize_window()
        sleep(1)
        # GO TO FIRST SITE
        driver.get("https://www.reddit.com/u/hkdoesplay/")
        #driver.get('https://www.expressvpn.com/what-is-my-ip')
        """
        timeout = 13
        # WAIT FOR PAGE TO LOAD
        try:  # {
            element_present = EC.presence_of_element_located((By.ID, 'main'))
            WebDriverWait(driver, timeout).until(element_present)
        # }
        except TimeoutException:  # {
            logging.info("Timed out waiting for page to load")
        # }
        else:  # {
            logging.info("Page Loaded Successfully...")
        # }
        """
        # CALL CLASS FUNCTION
        linky.run_videos(the_driver=driver, the_link_list=link_list)
        # [2019-12-14]\\sleep(30)
        # [2019-14-14]\\linky.run_videos(linky.driver)
    # }
    except WebDriverException:  # {
        logging.critical("<<< PROXY REFUSED CONNECTIONS >>>")
        # QUIT DRIVER BEFORE RESTART
        driver.quit()
        # RE-START!
        main()
    # }
    except:  # {
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
    # }
    else:  # {
        logging.info("Operation Completed Successfully...")
    # }
# }

if __name__ == "__main__": #{
    # INSTANTIATE GLOBAL VARIABLES
    logger = Logger().logger
    link_list = ["https://www.pornhub.com/view_video.php?viewkey=ph5c6194121f3d7",
                 "https://www.pornhub.com/view_video.php?viewkey=ph5c8896dda73b3",
                 "https://www.pornhub.com/view_video.php?viewkey=ph5d6c469674cc3",
                 "https://www.pornhub.com/view_video.php?viewkey=ph5d22824e4bd08",
                 "https://www.pornhub.com/view_video.php?viewkey=ph5d47460626ec3",
                 "https://www.pornhub.com/view_video.php?viewkey=ph5c7a4145d18eb",
                 "https://www.pornhub.com/view_video.php?viewkey=ph5c7a3dc09c578",
                 "https://www.pornhub.com/view_video.php?viewkey=ph5b33ca06e0067",
                 "https://www.pornhub.com/view_video.php?viewkey=ph5d8308fb9eca8",
                 "https://www.pornhub.com/view_video.php?viewkey=ph5c7a4145d18eb",
                 "https://www.pornhub.com/view_video.php?viewkey=ph5d2272209124e"]
    pyautogui.PAUSE = 0.5
    #  MAIN FUNCTION <<<< INFINITE >>>>
    while 1:  # {
        main()
    # }
# }