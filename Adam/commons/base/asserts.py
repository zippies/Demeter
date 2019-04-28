# -*- encoding:utf-8 -*-
from commons.base.utils import savescreen


def assertEmpty(a, msg, funcname=None):
    if a:
        if funcname:
            savescreen(funcname)
        raise Exception(msg)


def assertNotEmpty(a, msg, funcname=None):
    if not a:
        if funcname:
            savescreen(funcname)
        raise Exception(msg)


def assertEquals(a, b, msg, funcname=None, func=str):
    if func(a) != func(b):
        if funcname:
            savescreen(funcname)
        raise Exception(msg + ":%s != %s" % (a, b))


def assertNotEquals(a, b, msg, funcname=None, func=str):
    if func(a) == func(b):
        if funcname:
            savescreen(funcname)
        raise Exception(msg + ":%s == %s" % (a, b))


def assertMultiNotEquals(list, msg, funcname=None, func=str):
    for i, (a, b) in enumerate(list):
        assertNotEquals(a, b, "第%s组数据" % (i + 1) + msg, funcname, func)


def assertMultiEquals(list, msg, funcname=None, func=str):
    for i, (a, b) in enumerate(list):
        assertEquals(a, b, "第%s组数据" % (i + 1) + msg, funcname, func)


def assertContains(a, b, msg, funcname=None, func=str):
    if type(b) not in [list, tuple]:
        if func(b) not in func(a):
            savescreen(funcname)
            raise Exception(msg + ":'%s' not in '%s'" % (b, a))
    else:
        errorList = []
        for i in b:
            if func(i) not in func(a):
                errorList.append("'%s' not in '%s'" % (i, a))
        if errorList:
            savescreen(funcname)
            raise Exception(msg + "|".join(errorList))
