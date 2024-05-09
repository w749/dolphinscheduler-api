# coding=utf-8
import json
import os

from adapt import adapt_open

"""
配置文件操作解析
"""

_CURRENT_FOLDER = os.path.dirname(os.path.abspath(__file__))
_SETTING_FILE = "{}/settings.json".format(_CURRENT_FOLDER)


def singleton(cls):
    """
    单例模式装饰器
    """
    def inner():
        if hasattr(cls, "__instance"):
            return getattr(cls, "__instance")
        obj = cls()
        setattr(cls, "__instance", obj)
        return obj
    return inner


@singleton
class Config(object):
    """
    配置类
    """
    def __init__(self):
        if not os.path.exists(_SETTING_FILE):
            raise IOError("{} not exists".format(_SETTING_FILE))

        with adapt_open(_SETTING_FILE, "r") as f:
            self._config = json.load(f)

        self._ds = self._config["ds"]
        self.BASE_URL = self._ds["baseUrl"]
        self.USERNAME = self._ds["username"]
        self.PASSWORD = self._ds["password"]
        self.TOKEN_EXPIRE_TIME = self._ds["tokenExpireTime"]
        self.TOKEN = self._ds["token"]
        self.PROJECT = self._ds["project"]
        self.TENANT = self._ds["tenant"]
        self.QUEUE = self._ds["queue"]
        self.HEADERS = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/123.0.0.0 Safari/537.36 Edg/123.0.0.0",
            "token": self.TOKEN
        }

    def rewrite_token(self, token):
        """
        将token重写回配置文件
        """
        self._config["ds"]["token"] = token
        with open(_SETTING_FILE, "w") as w:
            json.dump(self._config, w, indent=2, separators=(",", ":"))


SETTINGS = Config()
