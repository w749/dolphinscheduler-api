# coding=utf-8
from typing import List

from common.response_inner import *


@attrs
class Base(object):
    code = attrib(type=int, default=-1)
    msg = attrib(type=str, default="")
    data = attrib(type=Inner, default=Inner())
    failed = attrib(type=bool, default=False)
    success = attrib(type=bool, default=True)


@attrs
class BaseResponse(Base):
    """
    基础response
    """
    data = attrib(type=str, default="")


@attrs
class GetSessionId(Base):
    """
    获取SessionId response
    """
    data = attrib(type=GetSessionIdInner, default=GetSessionIdInner())


@attrs
class TokenCreate(Base):
    """
    创建token response
    """
    data = attrib(type=CreateTokenInner, default=CreateTokenInner())


@attrs
class TokenList(Base):
    """
    创建token response
    """
    data = attrib(type=TokenListInner, default=TokenListInner())


@attrs
class TenantCreate(Base):
    """
    创建租户 response
    """
    data = attrib(type=TenantInner, default=TenantInner())


@attrs
class TenantList(Base):
    """
    获取租户列表 response
    """
    data = attrib(type=List[TenantInner], default=[TenantInner()])


@attrs
class QueueCreate(Base):
    """
    创建队列 response
    """
    data = attrib(type=QueueInner, default=QueueInner())


@attrs
class QueueList(Base):
    """
    获取队列列表 response
    """
    data = attrib(type=List[QueueInner], default=[QueueInner()])


@attrs
class ProjectCreate(Base):
    """
    创建项目 response
    """
    data = attrib(type=ProjectInner, default=ProjectInner())


@attrs
class ProjectList(Base):
    """
    获取项目列表 response
    """
    data = attrib(type=List[ProjectInner], default=[ProjectInner()])


@attrs
class ResourceList(Base):
    """
    获取资源列表 response
    """
    data = attrib(type=List[ResourceInner], default=[ResourceInner()])


@attrs
class ProcessList(Base):
    """
    获取工作流列表 response
    """
    data = attrib(type=List[ProcessInner], default=[ProcessInner()])


@attrs
class ProcessUpdate(Base):
    """
    更新工作流 response
    """
    data = attrib(type=ProcessInnerSon, default=ProcessInnerSon())


@attrs
class SchedulerCreate(Base):
    """
    创建定时任务 response
    """
    data = attrib(type=SchedulerInner, default=SchedulerInner())


@attrs
class SchedulerList(Base):
    """
    获取资定时任务列表 response
    """
    data = attrib(type=List[SchedulerInner], default=[SchedulerInner()])
