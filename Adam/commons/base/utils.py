# -*- encoding:utf-8 -*-
from commons.base.driver import driver
from lib.mysqlorm import DB
from config import Config
from datetime import datetime
import xmltodict
import time
import json
import os
import sys


def init(func):
    def _deco(self, *args, **kwargs):
        for k,v in kwargs.items():
            setattr(self, k, v)
        func(self, *args, **kwargs)
    return _deco


class Object(object):
    @init
    def __init__(self, *args, **kwargs):
        pass


def load_page(page_name):
    module_name = "pages.{page_name}".format(page_name=page_name)
    __import__(module_name)
    return sys.modules[module_name].Page()


def get_curtime():
    with open("cur_time", "r") as f:
        return f.read()


def savescreen(filename=None, immediate=False):
    cur_time = get_curtime()

    time_str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    screen = None
    if filename:
        sdr = os.path.join("reports", "screenshoots", cur_time, filename.split(".")[-1])
        if not os.path.isdir(sdr):
            os.system("mkdir -p " + sdr)
        screen = os.path.join(sdr, "%s.png" % time_str)
    else:
        screen = os.path.join("reports", "screenshoots", cur_time, "%s.png" % time_str)
    if not immediate: # 由于页面加载问题，立即截图可能会显示不出元素，因此等待加载2秒
        time.sleep(2)

    driver.get_screenshot_as_file(screen)


def get_type(case):
    ctype = None
    if case.has_key("error"):
        ctype = "error"
    elif case.has_key("failure"):
        ctype = "failed"
    elif case.has_key("skipped"):
        ctype = "skipped"
    else:
        ctype = "passed"

    return ctype


def find_png_file(report_png_list, dirname, files):
    for f in files:
        if f.endswith(".png"):
            report_png_list.append({"file": os.path.join(dirname, f), "dir": dirname})


def parse_report_file(report_path, cur_time):
    print "[测试报告路径]：", report_path

    test_result_dict = {
        "extras": [],
        "group": "挖财信贷测试",
        "project": "变量中心三期"
    }

    caseCount = passCount = skipCount = failCount = errorCount = totalTime = 0

    report_files = [report_path]

    for filename in report_files:
        with open(filename, "rb") as f:
            module = {
                "cases": []
            }

            test_data = xmltodict.parse(f.read()) #json.loads(content)
            testcases = []

            if isinstance(test_data.get("testsuite").get("testcase"), dict):
                testcases.append(test_data.get("testsuite").get("testcase"))
            else:
                testcases = test_data.get("testsuite").get("testcase")

            caseCount += len(testcases)

            for case in testcases:
                totalTime += float(case.get("@time"))
                ctype = get_type(case)
                log = None
                if ctype == "error":
                    errorCount += 1
                    log = case.get("error").get("#text").replace("\n\t", "<br>")
                elif ctype == "skipped":
                    skipCount += 1
                elif ctype == "failed":
                    failCount += 1
                    log = case.get("failure").get("#text").replace("\n\t", "<br>")
                else:
                    passCount += 1

                casename = case.get("@name")
                module["cases"].append({
                    "cost_time": float(case.get("@time")),
                    "module_name": case.get("@classname"),
                    "name": casename[casename.find("pisa"):] if "pisa" in casename else casename,
                    "type": get_type(case),
                    "log": log
                })

        test_result_dict["extras"].append(module)

    png_list = []
    png_path = os.path.join("reports", "screenshoots", cur_time)
    os.path.walk(png_path, find_png_file, png_list)

    test_result_dict["total_time"] = totalTime
    test_result_dict["case_count"] = caseCount
    test_result_dict["pass_count"] = passCount
    test_result_dict["skipped_count"] = skipCount
    test_result_dict["failed_count"] = failCount
    test_result_dict["error_count"] = errorCount
    test_result_dict["screenshoots"] = png_list
    return test_result_dict


db = DB(
    host=Config.mysql.get("host"),
    port=Config.mysql.get("port"),
    db = Config.mysql.get("db"),
    user = Config.mysql.get("user"),
    passwd = Config.mysql.get("password")
)