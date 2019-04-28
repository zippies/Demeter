# -*- encoding:utf-8 -*-
from commons.base.utils import load_page
from commons.base.driver import driver
from config import Config
import pytest


@pytest.fixture()
def login():
    if "xxxx" not in driver.current_url:
        return
    login_page = load_page("cas.login_page")
    login_page.login(Config.username, Config.password)

