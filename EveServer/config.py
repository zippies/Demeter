# -*- coding: utf-8 -*-
import os

class Config(object):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(os.path.abspath(os.path.dirname(__file__)),'data.sqlite')
    SECRET_KEY = 'code is fun'
    WTF_CSRF_SECRET_KEY = "whatdoyouwantfromme"
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    log_path = os.path.join(os.path.dirname(__file__),"logs")
    SQLALCHEMY_POOL_RECYCLE = 5

    REDIS_HOST = ""
    REDIS_PORT = "6379"
    REDIS_DB = "5"


    @staticmethod
    def init_app(app):
        pass

    PAGE_TEMPLATE = """<html><body>{{ page_body }}</body></html>"""

    SICK_ELEMENT_TEMPLATE = """
<!DOCTYPE html>
<html>
    <body>
        <div class="addon">
            {% for ele in elements %}
            <input type="text" value="{{ ele.name }}">
            {% endfor %}
        </div>
    </body>
</html>
    """