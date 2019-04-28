# -*- coding: utf-8 -*-
from flask import Flask
from lib.redis_cache import Cache
from config import Config
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
db = SQLAlchemy()
cache = Cache(Config.REDIS_HOST, Config.REDIS_PORT, Config.REDIS_DB)

def createApp():
    config = Config()
    app.config.from_object(config)
    db.init_app(app)
    from views import elementsView, pluginView
    app.register_blueprint(elementsView.url)
    app.register_blueprint(pluginView.url)

    return (app)
