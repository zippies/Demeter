# -*- encoding:utf-8 -*-
from config import Config
from commons.base.driver import driver
from commons.base.errors import ElementServerError
from multiprocessing import Manager
from commons.base.webelements import Input, Button, Table, Select
import traceback


def retry(count):
    def _deco(func):
        def _retry(self, *args, **kwargs):
            for i in range(count or Config.RETRY_COUNT):
                try:
                    return func(self, *args, **kwargs)
                except ElementServerError as e:
                    print "Error:", e
                    break
                except Exception as e:
                    print "Warning: get element from remote failure(%d) %s" % (i, str(e) + traceback.format_exc())
            else:
                raise Exception("Error: get element from remote failure(after 3th retry)")
        return _retry
    return _deco


def visit(url):
    def _deco(func):
        driver.get(url)
        return func

    return _deco


def TraceAction(TrackedClass):
    class Wrapper:
        action_chain = Manager().list()
        def __init__(self, *args, **kargs):
            self.wrapped = TrackedClass(*args, **kargs)
            self.funcs = [func for func in dir(self.wrapped) if
                          not func.startswith("_") and func not in self.wrapped.__dict__.keys()]

        def __getattr__(self, attrname):
            if attrname in self.funcs:
                self.action_chain.append(attrname)
                return eval("self.wrapped.%s" % attrname)
            return getattr(self.wrapped, attrname)

        def report(self):
            print ""

    return Wrapper


def input(name):
    def _deco(func):
        def _obj(page, *args, **kwargs):
            return Input(page, name=name)
        return _obj

    return _deco


def button(name):
    def _deco(func):
        def _obj(page, *args, **kwargs):
            return Button(page, name=name)
        return _obj

    return _deco


def table(name):
    def _deco(func):
        def _obj(page, *args, **kwargs):
            return Table(page, name=name)
        return _obj

    return _deco


def select(name):
    def _deco(func):
        def _obj(page, *args, **kwargs):
            return Select(page, name=name)
        return _obj

    return _deco