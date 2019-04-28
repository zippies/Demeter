# -*- encoding: utf-8 -*-
from flask import Blueprint, request, Response, render_template, url_for, redirect
from eve_server.db_models import db, Element, System
from lib.utils import get_element_by_page_url, element_exists_in_page, parse_relativeXpath
from jinja2 import Template
import HTMLParser
from config import Config
import traceback
import json
import requests
import time

url = Blueprint('elements', __name__)


@url.route("/")
def index():
    eles = Element.query.all()
    used_eles = [e for e in eles if e.is_used == 0]
    percent = float(len(used_eles)) / len(eles) * 100
    return render_template("elements.html", count=len(eles), percent=round(percent, 3))


@url.route("/save", methods=["POST"])
def save():
    info = {"code": 0, "errorMsg": None}
    eve = request.args.get("eve")
    try:
        elementname = request.form.get("elementname")
        ele = Element.query.filter_by(name=elementname).first()
        value = request.form.get("xpath_value")
        xpath = None
        if not eve:
            html = Template(Config.PAGE_TEMPLATE).render(page_body=request.form.get("page_body").replace("\\\"", "\""))
            value = parse_relativeXpath(value, html) or value
        page_url = request.form.get("url_value"). \
            replace(".", "\."). \
            replace("?", "\?"). \
            replace("{var}", "[^&/]+"). \
            replace("%3A", ":"). \
            replace("%2F", "/"). \
            replace("%2C", ",").\
            replace("{all}", ".*")

        if ele:
            if not request.args.get("force"):
                info["code"] = 1
                info["errorMsg"] = "该元素名称已存在"
            else:
                ele.name = request.form.get("elementname")
                ele.value = value
                ele.page_url = page_url
                db.session.add(ele)
                db.session.commit()
        else:
            ele = Element(
                request.form.get("findby") or "xpath",
                elementname,
                value,
                page_url
            )
            db.session.add(ele)
            db.session.commit()
    except Exception as e:
        print traceback.format_exc()
        info["code"] = -1
        info["errorMsg"] = str(e)

    return Response(json.dumps(info), headers={"Access-Control-Allow-Origin": "*"})


@url.route("/saveedit/<int:id>", methods=["POST"])
def saveedit(id):
    info = {"code": 0, "errorMsg": None}
    try:
        ele = Element.query.filter_by(id=id).first()
        if ele:
            ele.name = request.form.get("name")
            ele.findby = request.form.get("findby")
            ele.value = request.form.get("value")
            ele.page_url = request.form.get("page_url")
            db.session.add(ele)
            db.session.commit()
        else:
            info["code"] = -1
            info["errorMsg"] = "该元素不存在或已被删除"
    except Exception as e:
        info["code"] = -1
        info["errorMsg"] = str(e)
    return Response(json.dumps(info), headers={"Access-Control-Allow-Origin": "*"})


@url.route("/elements")
def elements():
    elements = Element.query.all()
    data = [
        {
            "name": """<input id='name_%s' type='text' class='form-control' value='%s' onKeyUp="value=value.replace(/-/g,'_')"/>""" % (
                ele.id, ele.name),
            "by": "<input id='findby_%s' type='text' class='form-control' value='%s'/>" % (
                ele.id, ele.findby),
            "value": """<input id='value_%s' type='text' class='form-control' value="%s" >""" % (
                ele.id, ele.value),
            "page_url": "<input id='page_url_%s' type='text' class='form-control' value='%s'/>" % (
                ele.id, ele.page_url),
            "operate": "<a href='#' class='btn btn-default save' id='save_%s'>save</a> <a href='#' class='btn btn-danger del' id='del_%s'>del</a>" % (
                ele.id, ele.id),
            "is_used": "<a href='#' class='form-control'><span class='glyphicon glyphicon-heart' style='color:%s'></span></a>" % ("red" if ele.is_used == 0 else "black")
        } for ele in elements
    ]
    return Response(json.dumps(data), headers={"Access-Control-Allow-Origin": "*"})


@url.route("/delelement/<int:id>")
def delelement(id):
    info = {"result": True, "errorMsg": None}
    try:
        ele = Element.query.filter_by(id=id).first()
        if ele:
            db.session.delete(ele)
            db.session.commit()
        else:
            info["result"] = False
            info["errorMsg"] = "element not exists"
    except Exception as e:
        info["result"] = False
        info["errorMsg"] = str(e)

    return Response(json.dumps(info), headers={"Access-Control-Allow-Origin": "*"})


@url.route("/get_page_elements", methods=["GET", "POST", "DELETE"])
def get_page_elements():
    if request.method == "GET":
        elements = [e.json() for e in Element.query.all()]
        elements_info = {
            "count": len(elements),
            "elements": elements
        }
        return Response(json.dumps(elements_info), headers={"Access-Control-Allow-Origin": "*"})
    elif request.method == "DELETE":
        elements = request.args.get("elements").split(".")
        for i in elements:
            e = Element.query.filter_by(id=i).first()
            e.is_used = -1
            db.session.add(e)
        db.session.commit()
        return Response("ok", headers={"Access-Control-Allow-Origin": "*"})

    start = time.time()
    page_url = request.json.get("page_url")
    domain = page_url.split("/")[2]
    system = System.query.filter(System.domains.like("%{domain}%".format(domain=domain))).first()
    eles = [ele for ele in Element.query.all() if not system or ele.page_url.split("/")[2].replace("\\", "") in str(system)]

    elements_info = get_element_by_page_url(eles, page_url)
    print "cost", time.time() - start
    return Response(json.dumps(elements_info), headers={"Access-Control-Allow-Origin": "*"})


@url.route("/get_element_by_xpath", methods=["POST"])
def get_element_by_xpath():
    html_parser = HTMLParser.HTMLParser()
    req_xpath = request.form.get("xpath")
    html_txt = html_parser.unescape(request.form.get("page_body"))
    page_url = request.form.get("page_url")
    html = Template(Config.PAGE_TEMPLATE).render(
        page_body=html_txt
    )
    print "req_xpath", req_xpath
    xpath = parse_relativeXpath(req_xpath, html) or req_xpath
    print "res_xpath", xpath
    eles = Element.query.filter_by(value=xpath.replace("\\\"", "")).all()
    element_info = get_element_by_page_url(eles, page_url)
    return Response(json.dumps(element_info), headers={"Access-Control-Allow-Origin": "*"})


@url.route("/health_check", methods=["POST"])
def health_check():
    from pprint import pprint
    start = time.time()
    info = {"code": 0, "content": None}
    page_url = request.form.get("page_url")
    page_body = request.form.get("page_body")
    html_parser = HTMLParser.HTMLParser()
    if not page_body:
        page_body = requests.get(page_url).text
    html_txt = html_parser.unescape(page_body)
    html = Template(Config.PAGE_TEMPLATE).render(
        page_body=html_txt
    )
    domain = page_url.split("/")[2]
    system = System.query.filter(System.domains.like("%{domain}%".format(domain=domain))).first()
    eles = [ele for ele in Element.query.all() if not system or ele.page_url.split("/")[2].replace("\\", "") in str(system)]
    elements_info = [e for e in get_element_by_page_url(eles, page_url) if not element_exists_in_page(e, html)]
    if elements_info:
        info["code"] = 1
        info["content"] = render_template("health_check.html", elements=elements_info)
    print "cost time2", time.time() - start
    return Response(json.dumps(info), headers={"Access-Control-Allow-Origin": "*"})
