# coding=utf-8
import logging
import os.path


import requests
from settings import SETTINGS
from adapt import adapt_cattrs


def get_logger(name):
    """
    获取日志打印器
    """
    logger = logging.Logger(name, level=logging.INFO)
    handler = logging.StreamHandler()
    fmt = "%(asctime)s %(levelname)s [%(name)s] [%(filename)s(%(funcName)s:%(lineno)d)] - %(message)s"
    formatter = logging.Formatter(fmt)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


_logging = get_logger(os.path.basename(__file__))


def request_post(url, headers, params, data, clz):
    return _request(url, headers, params, data, "POST", clz)


def request_get(url, headers, params, data, clz):
    return _request(url, headers, params, data, "GET", clz)


def request_delete(url, headers, params, data, clz):
    return _request(url, headers, params, data, "DELETE", clz)


def request_put(url, params, data, files, clz):
    text = requests.request("PUT", url, headers=SETTINGS.HEADERS, data=data, params=params, files=files)
    return object_from_json(text, clz)


def _request(url, headers, params, data, method, clz):
    """
    所有的request请求封装
    Args:
        url: 请求基础url
        headers: 额外headers
        params: 请求query参数
        data: 表单数据
        method: 表单字典
        clz: Base的子类

    Returns:Base的子类的实体

    """
    if not headers:
        headers = SETTINGS.HEADERS
    response = requests.request(method, url, headers=headers, data=data, params=params)
    if response.status_code != 200 and response.status_code != 201:
        _logging.error("Request {} error".format(url))
        _logging.error(response.text)
        raise RuntimeError()
    return object_from_json(response.json(), clz)


def object_from_json(js, clz):
    """
    从json转为类实体，名称必须完全对应
    Args:
        js: json字符串
        clz: 类

    Returns:该类的实体

    """
    return adapt_cattrs.structure(js, clz)


def url_join(path):
    """
    拼接url
    Args:
        path: 路径

    Returns:与配置文件中BASE_URL拼接后的url

    """
    base_url = SETTINGS.BASE_URL if not str(SETTINGS.BASE_URL).endswith("/") else str(SETTINGS.BASE_URL).rstrip("/")
    return base_url + path
