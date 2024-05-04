from attr import attrs, attrib


@attrs
class Inner(object):
    pass


@attrs
class GetSessionIdInner(Inner):
    securityConfigType = attrib(type=str, default="")
    sessionId = attrib(type=str, default="")


@attrs
class CreateTokenInner(Inner):
    id = attrib(type=int, default=-1)
    userId = attrib(type=int, default=-1)
    token = attrib(type=str, default="")
    expireTime = attrib(type=str, default="")
    createTime = attrib(type=str, default="")
    updateTime = attrib(type=str, default="")
    userName = attrib(type=str, default="")


@attrs
class TenantInner(Inner):
    id = attrib(type=int, default=-1)
    tenantCode = attrib(type=str, default="")
    description = attrib(type=str, default="")
    queueId = attrib(type=int, default=-1)
    queueName = attrib(type=str, default="")
    queue = attrib(type=str, default="")
    createTime = attrib(type=str, default="")
    updateTime = attrib(type=str, default="")

