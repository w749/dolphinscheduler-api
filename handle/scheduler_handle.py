# coding=utf-8
import argparse
import ast
import json
import os.path
import sys

import attr


sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../")
from settings import SETTINGS
from handle import ProjectHandle, ProcessHandle
from common import BaseResponse, SchedulerList, SchedulerInner
from utils import url_join, request_post, get_logger, read_file, request_put, object_from_json, object_to_json


class SchedulerHandle(object):
    """
    获取定时任务列表
    创建定时任务
    更新定时任务
    上下线定时任务
    """
    def __init__(self):
        self._logging = get_logger(os.path.basename(__file__))
        self._project_code = str(ProjectHandle().get_project_id())
        self._process_list = {x.processDefinition.code: x.processDefinition.name
                              for x in ProcessHandle().process_list(False)}
        self._scheduler_list_url = url_join("/projects/" + self._project_code + "/schedules/list")
        self._create_scheduler_url = url_join("/projects/" + self._project_code + "/schedules")
        self._update_scheduler_url = url_join("/projects/" + self._project_code + "/schedules/{}")
        self._online_scheduler_url = url_join("/projects/" + self._project_code + "/schedules/{}/online")
        self._offline_scheduler_url = url_join("/projects/" + self._project_code + "/schedules/{}/offline")
        self._scheduler_json_str = read_file(SETTINGS.SCHEDULER_FILE)

    def _get_scheduler_info_inner(self, scheduler):
        """
        内部方法，提取SchedulerInner中必要的信息
        Args:
            scheduler: SchedulerInner

        Returns:必要信息字典

        """
        keys = ["id", "processDefinitionCode", "processDefinitionName", "startTime", "endTime", "crontab",
                     "createTime", "updateTime", "releaseState"]
        s_dict = attr.asdict(scheduler)
        return {key: s_dict[key] for key in s_dict.keys() if key in keys}

    def _verify_process_code(self, process_code):
        """
        验证工作流code是否存在
        Args:
            process_code: 工作流code

        Returns:

        """
        if process_code not in self._process_list:
            self._logging.error("Process code {} not found, exists codes {}".format(
                process_code,
                [json.dumps({"name": self._process_list[x], "code": x}) for x in self._process_list.keys()]))
            sys.exit(-1)

    def _get_id_for_process(self, process_code):
        """
        根据工作流code获取scheduler id
        Args:
            process_code: 工作流code

        Returns:scheduler id

        """
        self._verify_process_code(process_code)
        total_schedulers = self.scheduler_list(False)
        schedulers = [x for x in total_schedulers if x.processDefinitionCode == process_code]
        if len(schedulers) > 0:
            scheduler = self._get_scheduler_info_inner(schedulers[0])
            return str(scheduler["id"])
        else:
            self._logging.error("Get scheduler id for process {} failed, "
                                "maybe you should create scheduler for process first.".format(process_code))
            sys.exit(-1)

    def scheduler_list(self, echo=True):
        """
        获取定时任务列表
        """
        scheduler_list_instance = request_post(self._scheduler_list_url, {}, {}, {}, SchedulerList)
        total_schedulers = scheduler_list_instance.data
        if echo:
            self._logging.info("Get {} schedulers. info is: ".format(len(total_schedulers)))
            self._logging.info("\n" + "\n".join([json.dumps(self._get_scheduler_info_inner(x)) for x in total_schedulers]))
        return total_schedulers

    def create_schedule(self, process_code):
        """
        创建定时任务
        Args:
            process_code: 工作流code

        Returns:

        """
        self._verify_process_code(process_code)
        data = {
            "schedule": self._scheduler_json_str,
            "failureStrategy": "CONTINUE",
            "warningType": "NONE",
            "processInstancePriority": "MEDIUM",
            "warningGroupId": "0",
            "workerGroup": "default",
            "tenantCode": SETTINGS.TENANT,
            "processDefinitionCode": process_code,
        }
        base_instance = request_post(self._create_scheduler_url, {}, {}, data, BaseResponse)
        if base_instance.code == 0:
            # 将单引号形式的字典字符串转为字典
            scheduler_dict = ast.literal_eval(base_instance.data)
            scheduler_instance = object_from_json(scheduler_dict, SchedulerInner)
            self._logging.info("Create Scheduler for process {} success, info is: ")
            self._logging.info(json.dumps(self._get_scheduler_info_inner(scheduler_instance)))
        else:
            self._logging.error("Scheduler {} create failed, maybe process not online, msg is '{}'".format(
                process_code, base_instance.msg))

    def update_scheduler(self, process_code):
        """
        更新已存在的工作流定时任务
        Args:
            process_code: 工作流code

        Returns:

        """
        self._verify_process_code(process_code)
        scheduler_id = self._get_id_for_process(process_code)
        data = {
            "schedule": self._scheduler_json_str,
            "failureStrategy": "CONTINUE",
            "warningType": "NONE",
            "processInstancePriority": "MEDIUM",
            "warningGroupId": "0",
            "workerGroup": "default",
            "tenantCode": SETTINGS.TENANT
        }
        base_instance = request_put(self._update_scheduler_url.format(scheduler_id), {}, {}, data, BaseResponse)
        if base_instance.code == 0:
            scheduler = [x for x in self.scheduler_list(False) if x.processDefinitionCode == process_code][0]
            self._logging.info("Update scheduler for process {} success, info is: ".format(process_code))
            self._logging.info(json.dumps(self._get_scheduler_info_inner(scheduler)))
        else:
            self._logging.error("Update scheduler for process {} failed, maybe you should offline scheduler first, "
                                "msg is '{}'".format(process_code, base_instance.msg))

    def online_scheduler(self, process_code, is_online=True):
        """
        上下线 scheduler
        Args:
            process_code: 工作流code
            is_online: 是否上线

        Returns:

        """
        self._verify_process_code(process_code)
        scheduler_id = self._get_id_for_process(process_code)
        url = self._online_scheduler_url if is_online else self._offline_scheduler_url
        state = "Online" if is_online else "Offline"
        base_instance = request_post(url.format(scheduler_id), {}, {}, {}, BaseResponse)
        if base_instance.code == 0:
            self._logging.info("{} scheduler for process {} success.".format(state, process_code))
        else:
            self._logging.error("{} scheduler for process {} failed, msg is '{}'".format(
                state, process_code, base_instance.msg))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Dolphin Scheduler queue operation.")
    parser.add_argument("-l", "--list", action="store_true", help="get scheduler list")
    parser.add_argument("-c", "--create", metavar="code", help="create scheduler for process, run --process -l get it")
    parser.add_argument("-u", "--update", metavar="code", help="update scheduler for process")
    parser.add_argument("-o", "--online", metavar="code", help="online scheduler for process")
    parser.add_argument("-f", "--offline", metavar="code", help="offline scheduler for process")
    args = parser.parse_args()

    handle = SchedulerHandle()

    if args.list:
        handle.scheduler_list()
    elif args.create:
        handle.create_schedule(int(args.create))
    elif args.update:
        handle.update_scheduler(int(args.update))
    elif args.online:
        handle.online_scheduler(int(args.online))
    elif args.offline:
        handle.online_scheduler(int(args.offline), False)
    else:
        parser.print_help()
