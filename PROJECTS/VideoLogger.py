"""
2019/12/05 - 08:15 PM

"/static/components/react/react-dom.production.min.js"

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
        file_handler = logging.FileHandler("C:/data/Logs/VideoLogger/vlogs.log")

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

class VideoLogger():  # {

    def __init__(self, log_file):  # {
        self.log_file = log_file
        # TRY THE FOLLOWING
        try: #{
            # CREATE PROXY LIST
            self.proxies = self.collect_proxy_list()
            print(self.proxies[0].get_address())
            print(self.proxies[1].country)
            # INSTANTIATE DRIVER
            self.driver = self.setup_driver(use_proxy=False)
            # VISIT SITE
            self.driver.get("https://pornhub.com/model/heather-kane")
            ###########################################
            # RUN
            self.run_videos(the_driver=self.driver)
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
            logging.info("Operation Completed Succesfully...")
        # }

    # }

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
        else:  # {
            the_capabilities = webdriver.DesiredCapabilities.CHROME['proxy'] = {
                "httpProxy": PROXY,
                "ftpProxy": PROXY,
                "sslProxy": PROXY,

                "proxyType": "MANUAL",

            }
            return webdriver.Chrome(desired_capabilities=the_capabilities)
        # }
    # }

    def tear_down(self, the_driver):  # {
        the_driver.quit()
    # }

    def collect_proxy_list(self):  # {
        reg_proxy = RequestProxy()
        # create proxy list
        proxies = reg_proxy.get_proxy_list()
        return proxies
    # }

    """
    create an EMPTY DataFrame and add in one ROW of the columns required...
    RETURNS: dataframe with filled data inside colummmns
    """
    def populate_data_entry(self, the_link, watch_duration, the_timestamp, current_count): #{
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

    def run_videos(self, the_driver):  # {
        # TRY THE FOLLOWING:
        try:   #{
            logging.info(str(the_driver.title))
            # GET PARENT WINDOW
            parent_window = the_driver.current_window_handle
            # CREATE LIST TO HOLD TITLES
            title_list = []
            # PULL LINKS
            video_titles = the_driver.find_elements(By.CLASS_NAME, "title")
            # SLICE LIST TO EXCLUDE CRAP STRINGS
            # [2019-12-11]\\video_titles = list(video_titles[:-4])
            for title in video_titles:  # {
                print("TITLE == " + title.text)
                logging.info("TITLE == " + str(title.text))
                # CHECK LENGTH REQUIREMENTS
                if len(title.text) >= 16:  # {
                    # APPEND TO LIST
                    title_list.append(str(title.text))
                # }
                else:  # {
                    logging.info("NOPE! THE FOLLOWING MOST LIKELY NOT A LINK:\n" + title.text)
                # }
            # }
            print("(length) LIST OF TITLES:\n" + str(len(title_list)))
            # PRINT OUT LIST
            print(title_list)
            # USE 'choice' to GET one from list
            title_choice = str(choice(video_titles))
            print("TITLE CHOOSEN:\n" + title_choice)
            # GET LINK VIA TITLE
            video_link = the_driver.find_element(By.LINK_TEXT, str(title_choice))
            # EXECUTE CODE TO OPEN **NEW** WINDOW
            the_driver.execute_script("window.open('" + video_link.text + "')")
            # GET LIST OF ALL WINDOWS CURRENTLY OPENED (Parent + CHild)
            all_windows = the_driver.window_handles
            print("WINDOW_HANDLES:\n" + str(all_windows))
            # GET CHILD WINDOW
            child_window = [window for window in all_windows if window != parent_window][0]
            # SWITCH TO CHILD WINDOW
            the_driver.switch_to.window(child_window)
            logging.info(str(the_driver.title))
            # [2019-12-10]\\SWITCH TO NEW WINDOW
            # [2019-12-10]\\the_driver.switch_to_window(the_driver.window_handles[1])
            # [2019-12-10]\\OPEN UP NEW LINK IN NEW WINDOW
            # [2019-12-10]\\the_driver.get(video_link)
            ################################################################
            # ON VIDEO PAGE
            #########################################################
            # GET COUNT VIA LINK
            video_count = the_driver.find_element(By.CLASS_NAME, "count")
            print("CURRENT COUNT:\n" + str(video_count))
            # WATCH FOR RANDOM DURATION
            countdown(randint(75, 120))
            # LIKE or DISLIKE?
            # >>>>>> 50/50 chance of there being another "watch_instance" created?
            coin_toss = fifty_fifty()
            print(coin_toss)
            #########################################
            # close child window
            the_driver.close()
            # SWITCH BACK TO PARENT WINDOW
            the_driver.switch_to.window(parent_window)
            logging.info(str(the_driver.title))
        # }
        except NoSuchElementException:  # {
            print("NO ELEMENT FOUND NUBB")
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
            print("[run_videos] SUCCESS! VERY NICE!")
        # }
    # }

# }

def countdown(n):  # {
    while n >= 0:  # {
        sleep(1)
        print(n)
        # decrement count
        n -= 1
    # }
    else:  # {
        print("Blast Off!")
    # }
# }

def fifty_fifty():  # {
    # flip a coin!
    coin_flip = randint(0, 1)
    if coin_flip == 0:  # {
        return "heads!"
    # }
    else:  # {
        return "tails!"
    # }
# }

def main():  # {
    # RE-INSTANTIATE GLOBAL VARIABLES
    global logger
    vlog = VideoLogger(log_file="C:/data/Logs/VLOGGER.log")
    # [2019-12-14]\\sleep(30)
    # [2019-12-14]\\vlog.run_videos(vlog.driver)
# }

if __name__ == "__main__":  # {
    # INSTANTIATE GLOBAL VARIABLES / SETUP LOGGER
    logger = Logger().logger
    # MAIN FUNCTION CALL
    main()
    # [2019-12-14]\\fifty_fifty()
# }
