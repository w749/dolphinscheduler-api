# coding=utf-8
import json
import os


"""
配置文件操作解析
"""

_CURRENT_FOLDER = os.path.dirname(os.path.abspath(__file__))
_SETTING_FILE = "{}/../settings.json".format(_CURRENT_FOLDER)

if not os.path.exists(_SETTING_FILE):
    raise IOError("{} not exists".format(_SETTING_FILE))

with open(_SETTING_FILE, "r") as f:
    _config = json.load(f)

_ds = _config["ds"]
BASE_URL = _ds["baseUrl"]
USERNAME = _ds["username"]
PASSWORD = _ds["password"]
TOKEN = _ds["token"]
HEADERS = {
    "token": TOKEN
}


def rewrite_token(token):
    """
    将token重写回配置文件
    """
    _config["ds"]["token"] = token
    with open(_SETTING_FILE, "w") as w:
        json.dump(_config, w, indent=2, separators=(",", ":"))
