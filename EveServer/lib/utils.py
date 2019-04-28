# -*- encoding:utf-8 -*-
from lxml import etree
import re
import sys

reload(sys)
sys.setdefaultencoding("utf-8")


def get_url_path(url):
    path = None
    if "https://cas" in url:  # cas登录页面元素通用
        path = "/".join(url.split("?")[1].split("/")[3:])
    else:
        path = "/".join(url.split("/")[3:])
    return path


def get_element_by_page_url(elements, page_url):
    matches = [e for e in elements if re.match(get_url_path(e.page_url), get_url_path(page_url))]
    elements_info = [e.json() for e in matches]
    return elements_info


def parse_relativeXpath(xpath, html):
    new_xpath = ""
    index = 0
    e = {
        "value": xpath,
        "findby": "xpath"
    }
    eles = element_exists_in_page(e, html)
    if not eles:
        print "find no elements"
        return None
    ele = eles[0]
    for i in range(len(xpath.split("/")) - 1):
        ele = ele.getparent()
        new_xpath = "//{tag}".format(tag=ele.tag)
        for key, value in ele.items():
            if key in ["name", "class", "id"]:
                new_xpath += "[@{key}='{value}']".format(key=key, value=value)
        new_ele = {
            "value": new_xpath,
            "findby": "xpath"
        }
        eles = element_exists_in_page(new_ele, html)
        if len(eles) == 1 and ele.tag != "li":
            index = i
            break

    suffix = xpath.split("/")[-(index + 1):]
    suffix.insert(0, new_xpath)
    return "/".join(suffix)


def element_exists_in_page(element, html):
    ele = None
    tree = etree.HTML(html)
    if element.get("findby") == "xpath":
        xpath = element["value"].replace("html[1]/", "")
        ele = tree.xpath(xpath)

    return ele


if __name__ == "__main__":
    html = None
    with open("../../tttt.html", "r") as f:
        html = f.read()
    xpath = "html[1]/body[1]/div[2]/div[1]/div[2]/div[1]/div[1]/div[3]/button[2]"
    # xpath = "//div[@class='ant-modal-content']/div[3]/button[2]"

    new_xpath = parse_relativeXpath(xpath, html)

    print new_xpath
