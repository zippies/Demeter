# -*- encoding:utf-8 -*-
from commons.base.utils import load_page
from commons.base.decorators import visit


@visit("https://www.baidu.com/")
def test_01_login_baidu():
    """登录百度"""
    page = load_page("demos.baidu")
    page.login("xxx", "xxx")
