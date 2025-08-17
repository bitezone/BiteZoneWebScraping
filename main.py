#!/usr/bin/env python3
"""
main.py

This main.py is the controller to scrapes the SUNY Oswego dining hall menu website and interaction between different py files within app folder.
"""

import atexit
import os
import time
import app

from selenium.webdriver.chrome.webdriver import WebDriver
from sqlalchemy.orm import Session

from app.web_driver import WebDriverManager
from dotenv import load_dotenv

def main():
    program_iteration_number = 1

    # Load environment variables from .env file
    load_dotenv() 
    
    
    driver: WebDriver = WebDriverManager.get_driver()
    try:
        url = os.getenv("SELECTED_WEBSCRAPE_URL") # Scrapes SUNY Oswego dining hall website

        driver.get(url)
        driver.set_window_size(1920, 1080)
        print("-----")
        print("Web scraping starting")
        print("Program Iteration Number ", program_iteration_number)
        print("-----")
        app.click_for_popup_acknowledgement()
        for i in range(1, 4):
            print("Scraping " + str(i) + "th dining hall")
            app.scrape_each_dining_hall(i)
        atexit.register(WebDriverManager.quit_driver)
    except Exception as e:
        print(f"Error occured: : {e}")
    finally:
        WebDriverManager.quit_driver()
        print("Scraping finished")
    
    # while True:

    #     try: 
    #         driver: WebDriver = WebDriverManager.get_driver()
    #         url = os.getenv("SELECTED_WEBSCRAPE_URL") # Scrapes SUNY Oswego dining hall website
    #         print(url, type(url)) 
    #         driver.get(url)
    #         driver.set_window_size(1920, 1080)
    #         print("-----")
    #         print("Web scraping starting")
    #         print("Program Iteration Number ", program_iteration_number)
    #         print("-----")
    #         app.click_for_popup_acknowledgement()
    #         for i in range(1, 4):
    #             print("Scraping " + str(i) + "th dining hall")
    #             app.scrape_each_dining_hall(i)
    #         atexit.register(WebDriverManager.quit_driver)
    #         print("Sleeping for 3 hours...")
    #         time.sleep(10800) 
    #     except Exception as e:
    #         print("!!!---")
    #         print(f"Error occurred: {e}")
    #         print("!!!---")
    #         print("Retrying in 1 hours...")
    #         time.sleep(3600)
            
    #     program_iteration_number += 1


if __name__ == "__main__":
    main()
