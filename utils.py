# coding=utf-8
import json
import logging
import os.path
import sys

import attr
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
    return _request(url, headers, params, data, {}, "POST", clz)


def request_get(url, headers, params, data, clz):
    return _request(url, headers, params, data, {}, "GET", clz)


def request_delete(url, headers, params, data, clz):
    return _request(url, headers, params, data, {}, "DELETE", clz)


def request_put(url, headers, params, data, clz):
    return _request(url, headers, params, data, {}, "PUT", clz)


def request_put_files(url, params, data, files, clz):
    return _request(url, {}, params, data, files, "PUT", clz)


def request_post_files(url, params, data, files, clz):
    return _request(url, {}, params, data, files, "POST", clz)


def request_text(url, params, data, method):
    """
    request请求并返回text
    Args:
        url: 请求基础url
        params: 请求query参数
        data: 表单数据
        method: 请求方法

    Returns:response.text

    """
    response = requests.request(method, url, headers=SETTINGS.HEADERS, data=data, params=params)
    if response.status_code != 200 and response.status_code != 201 and not response.json()["success"]:
        _logging.error("Request {} error".format(url))
        _logging.error(response.text)
        sys.exit(-1)
    _logging.info("Request {} success.".format(response.url))
    return response.text


def _request(url, headers, params, data, files, method, clz):
    """
    所有的request请求封装
    Args:
        url: 请求基础url
        headers: 额外headers
        params: 请求query参数
        data: 表单数据
        files: 文件
        method: 请求方法
        clz: Base的子类

    Returns:Base的子类的实体

    """
    if not headers:
        headers = SETTINGS.HEADERS
    response = requests.request(method, url, headers=headers, data=data, params=params, files=files)
    if response.status_code != 200 and response.status_code != 201 and not response.json()["success"]:
        _logging.error("Request {} error".format(url))
        _logging.error(response.text)
        sys.exit(-1)
    _logging.info("Request {} success.".format(response.url))
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


def object_to_json(obj):
    """
    将实体类格式化为json字符串
    Args:
        obj: 实体类

    Returns:json字符串

    """
    return json.dumps(attr.asdict(obj), ensure_ascii=False, separators=(",", ":"))


def write_file(filepath, content, is_del):
    """
    将content写入到file_path文件中
    Args:
        filepath: 文件路径
        content: 待写入内容
        is_del: 若文件存在是否删除

    Returns:

    """
    if os.path.exists(filepath):
        if is_del:
            os.remove(filepath)
        else:
            _logging.error("File {} already exists, please remove it first.".format(filepath))
            return
    with open(filepath, "w") as w:
        w.write(content)
    _logging.info("Write content to file {} success.".format(filepath))
