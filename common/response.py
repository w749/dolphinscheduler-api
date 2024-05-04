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
class GetSessionId(Base):
    """
    获取SessionId response
    """
    data = attrib(type=GetSessionIdInner, default=GetSessionIdInner())


@attrs
class CreateToken(Base):
    """
    创建token response
    """
    data = attrib(type=CreateTokenInner, default=CreateTokenInner())


@attrs
class CreateTenant(Base):
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