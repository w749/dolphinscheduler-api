# coding=utf-8
import requests
from config import HEADERS
from adapt import adapt_cattrs


def request_post(url, params, data):
    return _request(url, params, data, "POST")


def request_get(url, params, data):
    return _request(url, params, data, "GET")


def request_delete(url, params, data):
    return _request(url, params, data, "DELETE")


def request_put(url, params, data, files):
    return requests.request("PUT", url, headers=HEADERS, data=data, params=params, files=files)


def _request(url, params, data, method):
    """
    request请求
    :param url: 请求基础url
    :param params: 请求query参数
    :param data: 表单字典
    :param method: 请求方法
    :return: Base
    """
    return requests.request(method, url, headers=HEADERS, data=data, params=params)


def object_from_json(js, clz):
    """
    从json转为类实体
    :param js: json字符串
    :param clz: 类
    :return: 类实体
    """
    return adapt_cattrs.structure(js, clz)
