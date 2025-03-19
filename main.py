#!/usr/bin/env python3
"""
main.py

This script scrapes the SUNY Oswego dining hall menu website
"""

import atexit
import app

from selenium.webdriver.chrome.webdriver import WebDriver

from app.web_driver import WebDriverManager

def main():

    driver: WebDriver = WebDriverManager.get_driver()

    url = "https://netnutrition.cbord.com/nn-prod/oswego"
    driver.get(url)
    driver.set_window_size(1920, 1080)
    print("Driver Started")
    app.click_for_popup_acknowledgement()
    for i in range(1, 4):
        print(i)
        app.scrape_each_dining_hall(i)
    atexit.register(WebDriverManager.quit_driver())


if __name__ == "__main__":
    main()
