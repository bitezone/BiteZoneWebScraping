#!/usr/bin/env python3
"""
main.py

This script scrapes the SUNY Oswego dining hall menu website
"""

import time
import os
from selenium import webdriver
from selenium.common import NoSuchElementException, TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

env = os.getenv("ENV", "local")

chrome_options = Options()
chrome_options.add_argument("--window-size=1920x1080")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

if env == "local":
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
elif env == "deployment":
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.binary_location = os.getenv("CHROME_PATH")
    service = Service(executable_path=os.getenv("CHROMEDRIVER_PATH"))
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.implicitly_wait(60)
else:
    raise ValueError("Invalid ENVIRONMENT value. Set to either 'local' or 'deployment'.")

##### Getting SUNY Oswego Dining hall menu
url = "https://netnutrition.cbord.com/nn-prod/oswego"
driver.get(url)
driver.set_window_size(1920, 1080)
print("Driver Started")
##### Clicking OK for the web page
try:
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//button[@onclick='NetNutrition.UI.setIgnoreMobileDisc();']"))
    )
    pop_up_ack_btn = driver.find_element(By.XPATH, "//button[@onclick='NetNutrition.UI.setIgnoreMobileDisc();']")
    pop_up_ack_btn.click()
except TimeoutException:
    print("Pop_up_ack_btn was not detected")

### Selecting the right dining hall
# navigation_contexts = driver.find_elements(By.XPATH, "//li[@class='nav-item navigation__list-item navigation__context-selector']")

# for navigation_context in navigation_contexts:
#     navigation_list = navigation_context.find_elements(By.XPATH, ".//a[@onclick='javascript:NetNutrition.UI.handleNavBarSelection(this);']")
#     print(navigation_list[0].get_attribute("outerHTML"))
#     time.sleep(2)

# navigation_list[0].click()

time.sleep(1)
navigation_contexts = ["nav-unit-selector", "nav-date-selector", "nav-meal-selector"]
for navigation_context in navigation_contexts:
    navigation_selector = driver.find_element(By.XPATH, f"//div[@id='{navigation_context}']")
    inner_a_tag = navigation_selector.find_element(By.TAG_NAME, "a")

    WebDriverWait(driver, 20).until(EC.visibility_of(inner_a_tag))
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable(inner_a_tag)).click()

    navigation_list = navigation_selector.find_elements(By.XPATH,
                                     ".//a[@onclick='javascript:NetNutrition.UI.handleNavBarSelection(this);']")
    if navigation_context == "nav-meal-selector":
        navigation_list[0].click()
    elif navigation_context == "nav-date-selector":
        navigation_list[0].click()
    elif navigation_context == "nav-unit-selector":
        navigation_list[1].click()


individual_menu_links = WebDriverWait(driver, 10).until(
    EC.visibility_of_all_elements_located((By.XPATH, "//*[contains(@class, 'cbo_nn_menuLinkCell')]"))
)

for i in range(len(individual_menu_links)):
    print(i)
    individual_menu_links = WebDriverWait(driver, 10).until(
        EC.visibility_of_all_elements_located((By.XPATH, "//*[contains(@class, 'cbo_nn_menuLinkCell')]"))
    )

    individual_menu_link = individual_menu_links[i]
    print(individual_menu_link.text)

    a_tag = WebDriverWait(individual_menu_link, 10).until(
        EC.visibility_of_element_located((By.XPATH, "./a"))
    )
    a_tag.click()
    time.sleep(3) # Issue - selector needed instead of random time


    breadcrumb_nav = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//nav[@aria-label='Breadcrumb Navigation']"))
    )
    back_button = breadcrumb_nav.find_element(By.XPATH, "./a")
    back_button.click()
    time.sleep(3) # Issue - selector needed instead of random time


time.sleep(2)
driver.quit()
