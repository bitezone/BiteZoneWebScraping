import time
from typing import List
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from .models import Menu, MenuItem

from .utils import convert_to_date
from .db import *

from .web_driver import WebDriverManager

from .dataclasses import MenuItemData

def click_for_popup_acknowledgement():
    """click to close pop up acknowledgement button if existed"""
    driver: WebDriver = WebDriverManager.get_driver()
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    "//button[@onclick='NetNutrition.UI.setIgnoreMobileDisc();']",
                )
            )
        )
        pop_up_ack_btn = driver.find_element(
            By.XPATH, "//button[@onclick='NetNutrition.UI.setIgnoreMobileDisc();']"
        )
        pop_up_ack_btn.click()
    except TimeoutException:
        print("Pop_up_ack_btn was not detected")

    time.sleep(1)


def select_date_for_each_menu(idx: int):
    """navigating to respective dining hall through selecting drop down boxes

    Parameters
    ----------
    idx: int

        the index for the selection of dining hall

        Lakeside Dining Center - 1

        Cooper Dining Center - 2

        Pathfinder Dining Center - 3
    """
    driver: WebDriver = WebDriverManager.get_driver()
    navigation_contexts = [
        "nav-unit-selector",
        "nav-date-selector",
        "nav-meal-selector",
    ]
    for navigation_context in navigation_contexts:
        navigation_selector = driver.find_element(
            By.XPATH, f"//div[@id='{navigation_context}']"
        )
        inner_a_tag = navigation_selector.find_element(By.TAG_NAME, "a")

        WebDriverWait(driver, 20).until(EC.visibility_of(inner_a_tag))
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable(inner_a_tag)).click()

        navigation_list = navigation_selector.find_elements(
            By.XPATH,
            ".//a[@onclick='javascript:NetNutrition.UI.handleNavBarSelection(this);']",
        )
        if navigation_context == "nav-meal-selector":
            navigation_list[0].click()
        elif navigation_context == "nav-date-selector":
            navigation_list[0].click()
        elif navigation_context == "nav-unit-selector":
            navigation_list[idx].click()


def navigate_breadcrumb():
    """getting information relating to menu(date, time, location) and navigating"""
    back_buttons = get_navigation_breadcrumb()

    back_buttons[0].click()


def get_navigation_breadcrumb():
    driver: WebDriver = WebDriverManager.get_driver()
    breadcrumb_nav = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located(
            (By.XPATH, "//nav[@aria-label='Breadcrumb Navigation']")
        )
    )
    back_buttons: List[WebElement] = breadcrumb_nav.find_elements(By.XPATH, "./a")
    return back_buttons


def scrape_each_dining_hall(idx: int) -> None:
    """scraping data from each dining hall

    Parameters
    ----------
    idx: int

        the index for the selection of dining hall

        Lakeside Dining Center - 1

        Cooper Dining Center - 2

        Pathfinder Dining Center - 3
    """
    driver: WebDriver = WebDriverManager.get_driver()

    # navigating to the respective page of dining hall
    select_date_for_each_menu(idx)

    individual_menu_links = WebDriverWait(driver, 10).until(
        EC.visibility_of_all_elements_located(
            (By.XPATH, "//*[contains(@class, 'cbo_nn_menuLinkCell')]")
        )
    )

    # navigating to the specific menu on the selected dining hall
    for i in range(len(individual_menu_links)):
        individual_menu_links = WebDriverWait(driver, 10).until(
            EC.visibility_of_all_elements_located(
                (By.XPATH, "//*[contains(@class, 'cbo_nn_menuLinkCell')]")
            )
        )

        individual_menu_link = individual_menu_links[i]

        # Getting meal date ahead to store in the database
        meal_date_raw = (
            individual_menu_link.find_element(By.XPATH, "./parent::*/parent::*/header")
            .get_attribute("textContent")
            .split(", ")[1]
        )
        meal_date_format = convert_to_date(meal_date_raw)

        a_tag = WebDriverWait(individual_menu_link, 10).until(
            EC.visibility_of_element_located((By.XPATH, "./a"))
        )
        ActionChains(driver).click(a_tag).perform()
        time.sleep(3)

        individual_menu_selector = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located(
                (By.XPATH, "//div[contains(@class, 'table-responsive')]")
            )
        )

        back_buttons = get_navigation_breadcrumb()
        meal_date_time_bread_crumb = back_buttons[2].get_attribute("textContent")
        meal_location = back_buttons[1].get_attribute("textContent").split(" ")[0]
        meal_time_format = meal_date_time_bread_crumb.split(", ")[1]

        # db function to modify the menu if new or updated menu is detected
        menu = add_or_update_menu(
            meal_date_format=meal_date_format,
            meal_time_format=meal_time_format,
            meal_location=meal_location,
        )

        get_menu_data_from_selected_page(individual_menu_selector, menu)

        # reversing back to select dining menu
        navigate_breadcrumb()
        time.sleep(3)


def get_menu_data_from_selected_page(individual_menu_selector: WebElement, menu: Menu):
    """getting menu_items and menu_items category from the page

    Parameters
    ----------
    individual_menu_selector: WebElement
    """
    open_all_menu_category_toggle()

    menu_items_and_categories = individual_menu_selector.find_elements(
        By.XPATH, ".//tbody//tr"
    )

    menu_items_li: List[MenuItem] = []
    category_text: str | None = None

    for raw_item_selector in menu_items_and_categories:
        isCategory = True if raw_item_selector.get_attribute("role") else False

        if isCategory:
            category_selector = raw_item_selector.find_element(
                By.XPATH, ".//div[@role='button']"
            )
            category_text = category_selector.get_attribute("innerHTML").split("<")[0]
        else:
            menu_item_selector = raw_item_selector.find_element(
                By.XPATH, ".//a[@class='cbo_nn_itemHover']"
            )
            
            menu_item_object = MenuItemData()

            menu_item_object = get_nutritional_information(menu_item_selector, menu_item_object)

            menu_item_text = menu_item_selector.get_attribute("innerHTML").split("<")[0]
            
            menu_item_object.category = category_text
            menu_item_object.name = menu_item_text
            menu_item = create_menu_item_db(menu_item_object)

            
            menu_items_li.append(menu_item)
    connect_menu_and_menu_items(menu, menu_items_li)


def open_all_menu_category_toggle():
    driver: WebDriver = WebDriverManager.get_driver()
    category_selectors = driver.find_elements(By.XPATH, ".//div[@role='button']")

    for category_selector in category_selectors:
        ActionChains(driver).click(category_selector).perform()



def get_nutritional_information(menu_item_selector: WebElement, menu_item_obj: MenuItemData) -> MenuItemData:
    driver: WebDriver = WebDriverManager.get_driver()

    try:
        ActionChains(driver).click(menu_item_selector).perform()
    except Exception as e:
        print(menu_item_selector.get_attribute("outerHTML"))
        print("Failed to print :", e)
        return

    menu_item_obj.serving_size=get_serving_size()
    menu_item_obj.calories_per_serving=get_calorie()
    
    try:
        close_button_nutrition_info = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "btn_nn_nutrition_close"))
        )
        ActionChains(driver).click(close_button_nutrition_info).perform()
    except Exception as e:
        print("Failed to find or click close button:", e)
        
    return menu_item_obj


def get_serving_size() -> int:
    driver: WebDriver = WebDriverManager.get_driver()

    serving_size_element : WebElement = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.XPATH, ".//td[@class='cbo_nn_LabelBottomBorderLabel']")
        )
    )
    
    serving_size_text = serving_size_element.get_attribute("innerText")
    
    
    
    return serving_size_text[14:]

def get_calorie():
    driver: WebDriver = WebDriverManager.get_driver()

    calorie_element : WebElement = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.XPATH, ".//td[@class='cbo_nn_LabelDetail']//span[@class='cbo_nn_SecondaryNutrient']")
        )
    )
    
    calorie_text = calorie_element.get_attribute("innerText")
    
    return int(calorie_text)

    
