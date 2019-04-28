# -*- encoding:utf-8 -*-
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from commons.base.decorators import retry, TraceAction
from commons.base.driver import driver
from config import Config
from commons.base.errors import ElementServerError
import selenium
import requests
import time
import sys
reload(sys)
sys.setdefaultencoding("utf-8")


class Element(object):
    def __init__(self, name, findby, value, page_url):
        self.name = name
        self.findby = findby
        self.value = value.replace('\\"', "") if findby == "xpath" else value
        self.page_url = page_url

    def __repr__(self):
        return "<Element name='%s' findby='%s' value='%s' page_url='%s'" % (
            self.name, self.findby, self.value, self.page_url
        )


# @TraceAction
class BasePage(object):
    def __init__(self):
        self.driver = driver
        self.actions = ActionChains(driver)
        self.elements = self._get_remote_elements()
        self.screenshot_count = 0
        # self.page_width = self.driver.get_window_size()['width']
        # self.page_height = self.driver.get_window_size()['height']

    @retry(3)
    def _get_remote_elements(self):
        url = Config.REMOTE_ELEMENT_URL
        data = {
            "page_url": self.driver.current_url.replace("%3A", ":").replace("%2F", "/")
        }
        elements = dict()

        resp = requests.post(url, json=data)
        if resp.status_code == 200:
            resp_eles = resp.json()
            for ele in resp_eles:
                elements[ele.get("name").encode()] = Element(
                    ele.get("name"),
                    ele.get("findby"),
                    ele.get("value"),
                    ele.get("page_url")
                )
        else:
            raise ElementServerError("获取页面元素异常: %s %s" % (resp.status_code, resp.request.url.replace("%2C", ",")))

        return elements

    def get_element(self, element_name, index=0):
        """
        根据元素中文命名，获取元素
        :param element_name: 元素名称
        :param index: 如果元素的xpath中存在"|"符号，使用index，指定具体使用的xpath值
        :return: Element对象
        """
        element = self.elements.get(element_name)
        if element:
            if "|" in element.value:
                if index:
                    xpath = element.value.split("|")[index]
                    return self.driver.find_element(by="xpath", value=xpath)
                else:
                    try:
                        for xpath in element.value.split("|"):
                            return self.driver.find_element(by="xpath", value=xpath)
                    except Exception as e:
                        pass
                    pass
            return self.driver.find_element(by=element.findby, value=element.value)
        else:
            raise Exception("当前页面未定义名称为'%s'的元素" % element_name)

    def get_text(self, element_name):
        ele = self.get_element(element_name)
        return ele.text

    def wait_element(self, element_name, timeout=10, noexist=False):
        start = time.time()
        while time.time() - start < timeout:
            try:
                if self.get_element(element_name):
                    if not noexist:
                        return True
                elif noexist:
                    return True
            except Exception as e:
                print "element not yet present"
            time.sleep(1)
        else:
            return False

    def click(self, element_name):
        # self.move_to_element(element_name)
        element = self.elements.get(element_name)
        if element:
            ele = self.driver.find_element(by=element.findby, value=element.value)
            if ele:
                ele.click()
            else:
                raise Exception("当前页面未找到元素：%s" % ele)
        else:
            raise Exception("当前页面未定义名称为'%s'的元素" % element_name)

    def input(self, element_name, value):
        # self.move_to_element(element_name)
        element = self.elements.get(element_name)
        if element:
            ele = self.driver.find_element(by=element.findby, value=element.value)
            if ele:
                ele.send_keys(value.decode("utf-8"))
            else:
                raise Exception("当前页面未找到元素：%s" % ele)
        else:
            raise Exception("当前页面未定义名称为'%s'的元素" % element_name)

    def press_key(self, key):
        k = eval("Keys." + key)
        self.actions.key_down(k).key_up(k).perform()

    def page_down(self):
        self.press_key("PAGE_DOWN")

    def move_to_element(self, element_name):
        element = None
        if isinstance(element_name, str):
            element = self.get_element(element_name)
        # elif isinstance(element_name, object):
        #     element = element_name.element
        elif isinstance(element_name, selenium.webdriver.remote.webelement.WebElement):
            element = element_name
        if element:
            self.actions.move_to_element(element).perform()
        else:
            raise Exception("当前页面未定义名称为'%s'的元素" % element_name)

    def execute_js(self, js):
        self.driver.execute_script(js)

    def quit(self):
        self.driver.quit()

    def close(self):
        self.driver.close()

    def refresh(self):
        self.driver.refresh()

    def back(self):
        self.driver.back()

    def sleep(self, seconds):
        time.sleep(seconds)
