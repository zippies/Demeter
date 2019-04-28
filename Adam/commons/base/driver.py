# -*- encoding:utf-8 -*-
from selenium.webdriver import Chrome
from time import sleep
from config import Config


class Driver(Chrome):

    __driver = None

    def __new__(cls, **kwargs):
        if not cls.__driver:
            cls.__driver = super(Chrome, cls).__new__(cls, **kwargs)
        return cls.__driver

    @staticmethod
    def sleep(seconds):
        sleep(seconds)


driver = Driver(executable_path=Config.driver_path)
driver.set_page_load_timeout(30)
driver.implicitly_wait(10)
# driver.maximize_window()
