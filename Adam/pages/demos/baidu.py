# -*- encoding:utf-8 -*-
from commons.base.basepage import BasePage

class Page(BasePage):

    def login(self, username, password):
        """百度登录"""
        self.click("百度首页_登录_入口")
        self.click("百度首页_登录_用户名登录按钮")
        self.input("百度首页_登录_用户名输入框", username)
        self.input("百度首页_登录_密码输入框", password)
        self.click("百度首页_登录_登录按钮")
