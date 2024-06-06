# coding=utf-8
import argparse
import ast
import json
import os.path
import sys


sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../")
from handle import ProjectHandle
from common import (BaseResponse, InstanceList, PageSizeEnum, InstanceStateEnum, InstanceVariablesList, InstanceInfo,
                    InstanceTaskListInner, InstanceExecuteTypeEnum)
from utils import url_join, request_get, get_logger, object_to_json, get_enum_member_json, \
    get_attribute_of_enum, object_from_json, request_post


class InstanceHandle(object):
    """
    获取实例列表
    获取实例对应的变量列表
    获取实例对应的任务状态信息
    操作实例：重跑/从失败开始/停止
    重跑实例中的任务
    """

    def __init__(self):
        self._logging = get_logger(os.path.basename(__file__))
        self._project_code = str(ProjectHandle().get_project_id())
        self._instance_list_url = url_join("/projects/" + self._project_code + "/process-instances")
        self._instance_variables_url = url_join(
            "/projects/" + self._project_code + "/process-instances/{}/view-variables")
        self._instance_info_url = url_join("/projects/" + self._project_code + "/process-instances/{}")
        self._instance_tasks_url = url_join("/projects/" + self._project_code + "/process-instances/{}/tasks")
        self._exec_instance_url = url_join("/projects/" + self._project_code + "/executors/execute")
        self._exec_task_url = url_join("/projects/" + self._project_code + "/executors/execute-task")

    def instance_list(self,
                      process_code=None,
                      page_no=1,
                      page_size=10,
                      state_type=None,
                      start_date=None,
                      end_date=None,
                      echo=True):
        """
        根据参数获取实例列表
        Args:
            process_code: 工作流code
            page_no: 返回页数
            page_size: 返回每页数据量
            state_type: 返回实例状态
            start_date: 实例开始时间
            end_date: 实例结束时间
            echo: 是否打印日志

        Returns:

        """
        params = {
            "processDefineCode": process_code,
            "pageNo": page_no,
            "pageSize": page_size,
            "stateType": state_type,
            "startDate": start_date,
            "endDate": end_date
        }
        instance_list_obj = request_get(self._instance_list_url, {}, params, {}, InstanceList)
        instance_list = instance_list_obj.data.totalList
        if len(instance_list) > 0:
            self._logging.info("Get instances {} of {}.".format(len(instance_list), instance_list_obj.data.total))
            if echo:
                self._logging.info("\n" + "\n".join([object_to_json(x) for x in instance_list]))
            return instance_list
        else:
            self._logging.warning("No instance was obtained")
            return []

    def instance_info_of_id(self, instance_id):
        """
        根据instance id获取instance info
        Args:
            instance_id: 实例ID

        Returns:InstanceInner

        """
        obj = request_get(self._instance_info_url.format(instance_id), {}, {}, {}, BaseResponse)
        if obj.code == 0:
            # 将单引号形式的字典字符串转为字典
            instance_dict = ast.literal_eval(obj.data)
            return object_from_json(instance_dict, InstanceInfo)
        else:
            self._logging.error("Get instance info of id {} failed, maybe instance id not exists, msg is '{}'".format(
                instance_id, obj.msg))
            sys.exit(-1)

    def instance_variables(self, instance_id):
        """
        获取实例参数列表
        Args:
            instance_id: 实例ID

        Returns:

        """
        instance = self.instance_info_of_id(instance_id)
        obj = request_get(self._instance_variables_url.format(instance_id), {}, {}, {}, InstanceVariablesList)
        if obj.code == 0:
            params_list = obj.data.globalParams
            params_dict = {x.prop: x.value for x in params_list}
            self._logging.info("Instance info is: {}".format(object_to_json(instance)))
            self._logging.info("Instance variables of id {} is: \n{}".format(
                instance_id, json.dumps(params_dict, indent=4)))
        else:
            self._logging.error("Get variables for id {} failed, maybe instance id not exists, msg is '{}'".format(
                instance_id, obj.msg))

    def instance_tasks(self, instance_id):
        """
        获取实例中的任务列表
        Args:
            instance_id: 实例ID

        Returns:

        """
        obj = request_get(self._instance_tasks_url.format(instance_id), {}, {}, {}, BaseResponse)
        if obj.code == 0:
            # 将单引号形式的字典字符串转为字典
            task_list_dict = ast.literal_eval(obj.data)
            task_list = object_from_json(task_list_dict, InstanceTaskListInner).taskList
            self._logging.info("Get the {} tasks of instance {}.".format(len(task_list), instance_id))
            self._logging.info("\n" + "\n".join([object_to_json(x) for x in task_list]))
        else:
            self._logging.error("Get instance tasks of id {} failed, maybe instance id not exists, msg is '{}'".format(
                instance_id, obj.msg))
            sys.exit(-1)

    def instances_execute(self, instance_id, execute_type):
        """
        执行实例操作
        Args:
            instance_id: 实例ID
            execute_type: 执行类型

        Returns:

        """
        data = {
            "processInstanceId": instance_id,
            "executeType": execute_type
        }
        obj = request_post(self._exec_instance_url, {}, {}, data, BaseResponse)
        if obj.code == 0:
            instance_list = self.instance_list(echo=False)
            instance = [x for x in instance_list if x.id == int(instance_id)][0]
            self._logging.info("Execute {} for id {} success, info is: \n {}".format(execute_type, instance_id,
                                                                                     object_to_json(instance)))
        else:
            self._logging.error("Execute {} for id {} failed, msg is '{}'".format(execute_type, instance_id, obj.msg))

    def task_execute(self, instance_id, task_code):
        """
        运行实例中的任务
        Args:
            instance_id: 实例ID
            task_code: 任务code

        Returns:

        """
        params = {
            "processInstanceId": instance_id,
            "startNodeList": task_code,
            "taskDependType": "TASK_ONLY"
        }
        obj = request_post(self._exec_task_url, {}, params, {}, BaseResponse)
        if obj.code == 0:
            instance_list = self.instance_list(echo=False)
            instance = [x for x in instance_list if x.id == int(instance_id)][0]
            self._logging.info("Execute {} for id {} success, info is: \n {}".format(task_code, instance_id,
                                                                                     object_to_json(instance)))
        else:
            self._logging.error("Execute {} for id {} failed, msg is '{}'".format(task_code, instance_id, obj.msg))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Dolphin Scheduler tenant operation.")
    subparsers = parser.add_subparsers(dest="subparsers_name")

    # instance list
    list_parser = subparsers.add_parser("list", help="Instance list operation, run -h get help.")
    list_group = list_parser.add_argument_group("list_group", "instance list group.")
    list_group.add_argument("-p", "--process", metavar="code", help="process code, default ALL")
    list_group.add_argument("-n", "--page-no", dest="page_no", metavar="number", default="1",
                            help="page number, default 1")
    list_group.add_argument("-s", "--page-size", dest="page_size", metavar="size", default="10",
                            help="page size, select a number: {}".format(get_enum_member_json(PageSizeEnum)))
    list_group.add_argument("-t", "--state", metavar="type", default="",
                            help="instance state, select a number: {}".format(get_enum_member_json(InstanceStateEnum)))
    list_group.add_argument("-a", "--start", dest="start_date", metavar="date",
                            help="start date, need use quotation marks, eg: '2024-05-01 00:00:00'")
    list_group.add_argument("-e", "--end", dest="end_date", metavar="date",
                            help="end date, need use quotation marks, eg: '2024-05-01 00:00:00'")

    # instance variables
    var_parser = subparsers.add_parser("vars", help="Instance variables.")
    var_parser.add_argument("-i", "--id", metavar="id", dest="instance_id", required=True,
                            help="instance id")

    # # instance info
    # info_parser = subparsers.add_parser("info", help="Instance variables.")
    # info_parser.add_argument("-i", "--id", metavar="id", dest="instance_id", required=True,
    #                          help="get instance info of id")

    # instance tasks
    task_parser = subparsers.add_parser("tasks", help="Instance tasks info.")
    task_parser.add_argument("-i", "--id", metavar="id", dest="instance_id", required=True,
                             help="instance id")

    # instance execute
    task_parser = subparsers.add_parser("instance", help="Instance operation.")
    task_parser.add_argument("-i", "--id", metavar="id", dest="instance_id", required=True,
                             help="instance id")
    task_parser.add_argument("-t", "--type", dest="execute_type", metavar="type", required=True,
                             help="execute type, select a number: {}".format(get_enum_member_json(InstanceExecuteTypeEnum)))

    # task execute
    task_parser = subparsers.add_parser("run", help="Instance task rerun.")
    task_parser.add_argument("-i", "--id", metavar="id", dest="instance_id", required=True,
                             help="instance id")
    task_parser.add_argument("-c", "--code", dest="task_code", metavar="task_code", required=True,
                             help="task code, run tasks command get taskCode field")

    args = parser.parse_args()

    handle = InstanceHandle()

    if args.subparsers_name == "list":
        arg_process_code = args.process
        arg_page_no = args.page_no
        arg_page_size = get_attribute_of_enum(args.page_size, PageSizeEnum, False, 10)
        arg_state_type = get_attribute_of_enum(args.state, InstanceStateEnum)
        arg_start_date = args.start_date
        arg_end_date = args.end_date
        handle.instance_list(arg_process_code, arg_page_no, arg_page_size, arg_state_type, arg_start_date, arg_end_date)
    elif args.subparsers_name == "vars":
        handle.instance_variables(args.instance_id)
    # elif args.subparsers_name == "info":
    #     handle.instance_info_of_id(args.instance_id)
    elif args.subparsers_name == "tasks":
        handle.instance_tasks(args.instance_id)
    elif args.subparsers_name == "instance":
        handle.instances_execute(args.instance_id, get_attribute_of_enum(args.execute_type, InstanceExecuteTypeEnum))
    elif args.subparsers_name == "run":
        handle.task_execute(args.instance_id, args.task_code)
    else:
        parser.print_help()
