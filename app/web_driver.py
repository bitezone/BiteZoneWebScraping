import os
from typing import Optional
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.webdriver import WebDriver


class WebDriverManager:
    _driver: Optional[WebDriver]  = None

    @classmethod
    def get_driver(cls):
        if cls._driver is None:
            cls._driver = cls._initialize_driver()
        return cls._driver

    @classmethod
    def _initialize_driver(cls):
        env = os.getenv("ENV", "local")

        chrome_options = Options()
        chrome_options.add_argument("--window-size=1920x1080")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        if env == "local":
            driver = webdriver.Chrome(
                service=Service(ChromeDriverManager().install()), options=chrome_options
            )
        elif env == "deployment":
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.binary_location = os.getenv("CHROME_PATH")
            service = Service(executable_path=os.getenv("CHROMEDRIVER_PATH"))
            driver = webdriver.Chrome(service=service, options=chrome_options)
            driver.implicitly_wait(60)
        else:
            raise ValueError(
                "Invalid ENVIRONMENT value. Set to either 'local' or 'deployment'."
            )
        return driver

    @classmethod
    def quit_driver(cls):
        if cls._driver:
            cls._driver.quit()
            cls._driver = None
