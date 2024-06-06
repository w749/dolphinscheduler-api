# coding=utf-8
from enum import Enum


class InstanceStateEnum(Enum):
    """
    常用实例状态枚举
    """
    SUCCESS = 1
    RUNNING_EXECUTION = 2
    FAILURE = 3
    STOP = 4


class InstanceExecuteTypeEnum(Enum):
    """
    执行实例操作的类型
    """
    REPEAT_RUNNING = 1
    START_FAILURE_TASK_PROCESS = 2
    STOP = 3


class PageSizeEnum(Enum):
    """
    分页每页数据量枚举
    """
    TEN = 10
    THIRTY = 30
    FIFTY = 50
