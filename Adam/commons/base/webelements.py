# -*- encoding:utf-8 -*-


class Input(object):
    def __init__(self, page, name):
        self.page = page
        self.name = name
        self.element = self.page.get_element(name)

    @property
    def text(self):
        return self.element.text

    def clear(self):
        self.element.clear()

    def input(self, text):
        self.page.input(self.name, text)

    def __repr__(self):
        return "<Input name='%s'>" % self.name


class Button(object):
    def __init__(self, page, name):
        self.page = page
        self.name = name
        self.element = self.page.get_element(name)

    def click(self):
        self.element.click()

    @property
    def text(self):
        return self.element.text

    def __repr__(self):
        return "<Button name='%s'>" % self.name


class Table(object):
    def __init__(self, page, name):
        self.page = page
        self.name = name
        self.element = self.page.get_element(name)

    @property
    def table_rows(self):
        """返回当前table内的所有行"""
        return self.element.find_elements_by_xpath("//tbody/tr")

    def get_table_element(self, row, column):
        """
            row:行，column：列
            返回第row行，第column列的元素
        """
        return self.table_rows[row-1].find_elements_by_tag_name("td")[column-1]


class Select(object):
    def __init__(self, page, name):
        self.page = page
        self.name = name
        self.element = self.page.get_element(name.split("|")[0])

    def choice(self, num):
        self.element.click()
        select = self.page.get_element(self.name.split("|")[1])
        parent_tag_name = select.tag_name.lower()
        childs = None
        if parent_tag_name == "ul":
            childs = select.find_elements_by_tag_name("li")
        elif parent_tag_name == "select":
            childs = select.find_elements_by_tag_name("option")

        childs[num].click()
        return childs[num]