import time
from typing import List
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from sqlalchemy.orm import Session

from .web_driver import WebDriverManager


def click_for_popup_acknowledgement():
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
    driver: WebDriver = WebDriverManager.get_driver()
    breadcrumb_nav = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located(
            (By.XPATH, "//nav[@aria-label='Breadcrumb Navigation']")
        )
    )
    back_buttons: List[WebElement] = breadcrumb_nav.find_elements(By.XPATH, "./a")
    print(back_buttons[2].get_attribute("textContent"))  # Selected date
    print(back_buttons[1].get_attribute("textContent"))
    back_buttons[0].click()


def scrape_each_dining_hall(idx: int, session: Session):
    driver: WebDriver = WebDriverManager.get_driver()

    select_date_for_each_menu(idx)

    individual_menu_links = WebDriverWait(driver, 10).until(
        EC.visibility_of_all_elements_located(
            (By.XPATH, "//*[contains(@class, 'cbo_nn_menuLinkCell')]")
        )
    )

    for i in range(len(individual_menu_links)):
        individual_menu_links = WebDriverWait(driver, 10).until(
            EC.visibility_of_all_elements_located(
                (By.XPATH, "//*[contains(@class, 'cbo_nn_menuLinkCell')]")
            )
        )

        individual_menu_link = individual_menu_links[i]

        a_tag = WebDriverWait(individual_menu_link, 10).until(
            EC.visibility_of_element_located((By.XPATH, "./a"))
        )
        a_tag.click()
        time.sleep(3)

        individual_menu_selector = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located(
                (By.XPATH, "//div[contains(@class, 'table-responsive')]")
            )
        )

        get_menu_data_from_selected_page(individual_menu_selector, session)

        navigate_breadcrumb()
        time.sleep(3)


def get_menu_data_from_selected_page(individual_menu_selector: WebElement, session: Session):

    menu_items_and_categories = individual_menu_selector.find_elements(
        By.XPATH, "//tbody//tr"
    )

    for raw_item_selector in menu_items_and_categories:
        isCategory = True if raw_item_selector.get_attribute("role") else False
        if isCategory:
            category_selector = raw_item_selector.find_element(
                By.XPATH, ".//div[@role='button']"
            )
            # print(category_selector.get_attribute("innerHTML"))
            category_text = category_selector.get_attribute("innerHTML").split("<")[0]
            # print("--Category--")
            # print(category_text)
            # print("-----")
        else:
            # menu raw_item_selector
            menu_item_selector = raw_item_selector.find_element(
                By.XPATH, ".//a[@class='cbo_nn_itemHover']"
            )
            menu_item_text = menu_item_selector.get_attribute("innerHTML").split("<")[0]
            # print(menu_item_text)

