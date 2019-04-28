# -*- encoding:utf-8 -*-
from config import Config
import requests
import json
import os
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

none_used = {
    "count": 0,
    "ids": [],
    "names": []
}


def check_element_used(e):
    id = e.get("id")
    name = e.get("name")
    code = os.system("find cases commons pages -type f|xargs grep " + name)
    if code != 0:
        none_used["count"] += 1
        none_used["ids"].append(id)
        none_used["names"].append(name)


def get_all_elements():
    r = requests.get(Config.REMOTE_ELEMENT_URL)
    return r.json()


def unuse_all_elements(data):
    r = requests.delete("%s?elements=%s" % (Config.REMOTE_ELEMENT_URL, ".".join([str(i) for i in data])))
    return r.status_code, r.reason


if __name__ == "__main__":
    if sys.argv[1] == "check":
        elements = get_all_elements().get("elements")
        map(check_element_used, elements)
        print "=" * 100
        print json.dumps(none_used, ensure_ascii=False)
        if len(sys.argv) == 3 and sys.argv[2] == "clear" and none_used.get("ids"):
            code, reason = unuse_all_elements(none_used.get("ids"))
            if code == 200:
                print "[success]useless elements deleted"
            else:
                print "[error]", code, reason
        exit(0)

    from commons.base.driver import driver
    from config import Config, report_template
    from commons.base.utils import parse_report_file, savescreen
    from jinja2 import Template
    import time
    import pytest
    import os

    current_time = time.strftime("%Y_%m_%d_%H%M%S")
    with open("cur_time", "w") as f:
        f.write(current_time)

    sys.argv.extend(["--junitxml=%s.xml" % current_time])
    pytest.main(args=sys.argv[1:])
    savescreen("end")
    if Config.DEBUG:
        report_path = os.getcwd() + "/%s.xml" % current_time

        result_dict = parse_report_file(report_path, current_time)

        html_report = Template(report_template).render(
            test_result=result_dict
        )

        report_file = "file://" + os.getcwd() + "/reports/%s.html" % current_time

        with open("reports/%s.html" % current_time, "w") as f:
            f.write(html_report)

        os.system("rm -rf *.xml cur_time")

        driver.get(report_file)
        try:
            driver.switch_to_alert().accept()
        except:
            pass
    else:
        driver.close()
        print "View report at: ./reports/%s.html" % current_time

