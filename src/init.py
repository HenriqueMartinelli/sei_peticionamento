import time
import logging
import ctypes
import ctypes.wintypes
import selenium

from datetime import datetime
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException, ElementNotInteractableException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import TimeoutException, InvalidElementStateException, ElementClickInterceptedException
import traceback
from scheme.scheme import SITE_SCHEME
from webdriver_manager.chrome import ChromeDriverManager


logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


class BaseDriver:
    def __init__(self,
                 chrome_options: webdriver.ChromeOptions = None):
        self.tipo = 0
        self.path_docs = "/home/linux/projetos/sei_peticionamento/documentos"

        # self.chrome_options = Options()
        # self.chrome_options.add_argument('--headless')
        self.chrome_options = chrome_options
        self.driver_path: str = ChromeDriverManager().install()
        # self.driver_path = ""
        self.ID = "NOT DEFINED"
        self.current_frame = None
        self.outputEvent = list()


    def setDriver(self, executable_path, chrome_options):
        # self.DRIVER: webdriver = webdriver.Chrome(executable_path=executable_path, chrome_options=chrome_options)chrome_options.add_argument('--no-sandbox')
        self.DRIVER = selenium.webdriver.Chrome(options=chrome_options)
        return self.DRIVER
    
    def global_variables(self, content):
        self.ID = content['idTarefa']
        self.URL_PROCESS = content['url_processo']
        self.DRIVER.get(self.URL_PROCESS)


    def find_element(self, value, by=By.XPATH, retry_count=7, retry_sleep=1) -> WebElement:
        for attempt in range(retry_count):
            try:
                return self.DRIVER.find_element(by, value)
            except (NoSuchElementException, TimeoutException, ElementNotInteractableException):
                logging.warning(f"ID={self.ID}, {by}={value}: Element not found {attempt + 1}/{retry_count}")
                time.sleep(retry_sleep)
        raise NoSuchElementException(f"ID={self.ID}, {by}={value}: Element not found") 

    
    def find_element_by_clickable(self, value, by=By.XPATH, retry_count=5, retry_sleep=0.5) -> WebElement:
        for attempt in range(retry_count):
            try:
                return self.DRIVER.find_element(by, value).click()
            except (NoSuchElementException, TimeoutException, ElementNotInteractableException):
                print(f"{by}={value}: Element not found {attempt + 1}/{retry_count}")
                time.sleep(retry_sleep)
        raise NoSuchElementException(f"{by}={value}: Element not found")
        

    def send_keys_if_visible(self, element, text, by=By.CSS_SELECTOR, retry_count=7, retry_sleep=1) -> WebElement:
        screen = self.current_screen
        value = SITE_SCHEME[screen]["elements"][element]
        for attempt in range(retry_count):
            try:
                input_element = self.DRIVER.find_element(by, value)
                input_element.clear()
                return input_element.send_keys(text)
            except (NoSuchElementException, InvalidElementStateException, StaleElementReferenceException):
                logging.warning(f"ID={self.ID}, {by}={value}: Element not found {attempt + 1}/{retry_count}")
                time.sleep(retry_sleep)
        raise InvalidElementStateException(f"ID={self.ID}, {by}={value}: Element not Interactable") 
    

    def find_locator(self, element: str, screen: str = None, retry_count=7, retry_sleep=1, method=None, by=By.XPATH):
        screen = screen or self.current_screen
        locator = SITE_SCHEME[screen]["elements"][element]
        if method != None:
            return self.find_element_by_clickable(locator, by=by, retry_count=retry_count, retry_sleep=retry_sleep)
        return self.find_element(locator, by=by, retry_count=retry_count, retry_sleep=retry_sleep)


    def switch_to_frame(self, value, retry_count=3, retry_sleep=0.5):
        if self.current_frame == value:
            return
        self.switch_to_default_content()
        frame = self.find_element(value, By.XPATH, retry_count=retry_count, retry_sleep=retry_sleep)
        self.DRIVER.switch_to.frame(frame)
        self.current_frame = value

    def switch_to_default_content(self):
        if self.current_frame is None:
            return
        self.DRIVER.switch_to.default_content()
        self.current_frame = None
    
    def switch_to_screen(self, screen: str):
        if screen in SITE_SCHEME:
            self.current_screen = screen
        else:
            raise Exception(f"Screen {screen} not found")
        

    @staticmethod
    def screen_decorator(screen: str):
        def decorator(func):
            def wrapper(self, *args, **kwargs):
                if self.current_screen != screen:
                    raise Exception(f"Need to be on {screen} screen: {self.current_screen}")
                return func(self, *args, **kwargs)
            return wrapper
        return decorator
