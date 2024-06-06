from typing import List

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
class TokenListInner(Inner):
    totalList = attrib(type=List[CreateTokenInner], default=[CreateTokenInner()])
    total = attrib(type=int, default=-1)
    totalPage = attrib(type=str, default="")
    pageSize = attrib(type=int, default=-1)
    currentPage = attrib(type=int, default=-1)
    pageNo = attrib(type=int, default=-1)


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


@attrs
class QueueInner(Inner):
    id = attrib(type=int, default=-1)
    queueName = attrib(type=str, default="")
    queue = attrib(type=str, default="")
    createTime = attrib(type=str, default="")
    updateTime = attrib(type=str, default="")


@attrs
class ProjectInner(Inner):
    id = attrib(type=int, default=-1)
    userId = attrib(type=int, default=-1)
    userName = attrib(type=str, default="")
    code = attrib(type=int, default=-1)
    name = attrib(type=str, default="")
    description = attrib(type=str, default="")
    createTime = attrib(type=str, default="")
    updateTime = attrib(type=str, default="")
    perm = attrib(type=int, default=-1)
    defCount = attrib(type=int, default=-1)
    instRunningCount = attrib(type=int, default=-1)


@attrs
class ResourceInner(Inner):
    id = attrib(type=int, default=-1)
    pid = attrib(type=str, default="")
    name = attrib(type=str, default="")
    fullName = attrib(type=str, default="")
    description = attrib(type=str, default="")
    children = attrib(type=list, default=[])
    type = attrib(type=str, default="")
    currentDir = attrib(type=str, default="")
    idValue = attrib(type=str, default="")
    dirctory = attrib(type=bool, default=False)


@attrs
class ProcessInnerSon(Inner):
    code = attrib(type=int, default=-1)
    name = attrib(type=str, default="")
    releaseState = attrib(type=str, default="")
    projectCode = attrib(type=int, default=-1)
    createTime = attrib(type=str, default="")
    updateTime = attrib(type=str, default="")


@attrs
class ProcessInner(Inner):
    processDefinition = attrib(type=ProcessInnerSon, default=ProcessInnerSon())


@attrs
class SchedulerInner(Inner):
    id = attrib(type=int, default=-1)
    processDefinitionCode = attrib(type=int, default=-1)
    processDefinitionName = attrib(type=str, default="")
    projectName = attrib(type=str, default="")
    definitionDescription = attrib(type=str, default="")
    startTime = attrib(type=str, default="")
    endTime = attrib(type=str, default="")
    timezoneId = attrib(type=str, default="")
    crontab = attrib(type=str, default="")
    failureStrategy = attrib(type=str, default="")
    warningType = attrib(type=str, default="")
    createTime = attrib(type=str, default="")
    updateTime = attrib(type=str, default="")
    userId = attrib(type=int, default=-1)
    userName = attrib(type=str, default="")
    releaseState = attrib(type=str, default="")
    warningGroupId = attrib(type=int, default=-1)
    processInstancePriority = attrib(type=str, default="")
    workerGroup = attrib(type=str, default="")
    tenantCode = attrib(type=str, default="")
    environmentCode = attrib(type=int, default=-1)
    environmentName = attrib(type=str, default="")


@attrs
class InstanceInner(Inner):
    id = attrib(type=int, default=-1)
    name = attrib(type=str, default="")
    processDefinitionCode = attrib(type=int, default=-1)
    state = attrib(type=str, default="")
    startTime = attrib(type=str, default="")
    endTime = attrib(type=str, default="")
    duration = attrib(type=str, default="")
    tenantCode = attrib(type=str, default="")


@attrs
class InstanceListInner(Inner):
    totalList = attrib(type=List[InstanceInner], default=[InstanceInner()])
    total = attrib(type=int, default=-1)
    totalPage = attrib(type=str, default="")
    pageSize = attrib(type=int, default=-1)
    currentPage = attrib(type=int, default=-1)
    pageNo = attrib(type=int, default=-1)


@attrs
class InstanceGlobalParamInner(Inner):
    prop = attrib(type=str, default="")
    direct = attrib(type=str, default="")
    type = attrib(type=str, default="")
    value = attrib(type=str, default="")


@attrs
class InstanceVariablesInner(Inner):
    globalParams = attrib(type=List[InstanceGlobalParamInner], default=[InstanceGlobalParamInner()])


@attrs
class InstanceTaskInner(Inner):
    taskCode = attrib(type=int, default=-1)
    taskDefinitionVersion = attrib(type=int, default=-1)
    logPath = attrib(type=str, default="")
    taskType = attrib(type=str, default="")
    state = attrib(type=str, default="")
    appLink = attrib(type=str, default="")
    name = attrib(type=str, default="")


@attrs
class InstanceTaskListInner(Inner):
    taskList = attrib(type=List[InstanceTaskInner], default=[InstanceTaskInner()])
