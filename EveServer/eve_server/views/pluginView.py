# -*- coding: utf-8 -*-
from flask import Blueprint, send_file

url = Blueprint('plugin', __name__, url_prefix="/plugin")


@url.route("/download")
def download_plugin():
    return send_file("static/downloads/needle_plugin.tar.gz")
