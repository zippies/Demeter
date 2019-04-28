# -*- coding: utf-8 -*-
from datetime import datetime
from . import db


class System(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    domains = db.Column(db.Text)
    createdtime = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        return "<System %s>:%s" % (self.name, self.domains)


class Element(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    findby = db.Column(db.String(64))
    name = db.Column(db.String(64))
    value = db.Column(db.String(512))
    page_url = db.Column(db.String(512))
    is_used = db.Column(db.Integer, default=-1)  # 健康值 0： 被使用  -1：未被使用
    createdtime = db.Column(db.DateTime, default=datetime.now)

    def __init__(self, findby, name, value, page_url):
        self.findby = findby
        self.name = name
        self.value = value
        self.page_url = page_url

    def json(self):
        return {
            "id": self.id,
            "name": self.name,
            "findby": self.findby,
            "value": self.value,
            "is_used": self.is_used,
            "page_url": self.page_url
        }

    def __repr__(self):
        return "<Element: name='%s' findby='%s' value='%s' is_used='%s' page_url='%s'>" % (
        self.name, self.findby, self.value, self.is_used, self.page_url)


class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.Integer)    # 0: json  1: string  3: template
    content = db.Column(db.Text)
    createdtime = db.Column(db.DateTime, default=datetime.now)

    def __init__(self, type, content):
        self.type = type
        self.content = content