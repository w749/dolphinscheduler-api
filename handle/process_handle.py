# coding=utf-8
import argparse
import json
import os.path
import sys
import time

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../")
from handle import ProjectHandle
from common import BaseResponse, ProcessList, ProcessUpdate
from utils import url_join, request_post, request_get, get_logger, request_delete, object_to_json, request_text, \
    write_file, request_post_files, request_put


class ProcessHandle(object):
    """
    获取项目下所有工作流
    导入工作流
    下载工作流
    删除工作流
    上下线工作流
    更新工作流
    """
    def __init__(self):
        self._logging = get_logger(os.path.basename(__file__))
        self._project_code = str(ProjectHandle().get_project_id())
        self._process_list_url = url_join("/projects/" + self._project_code + "/process-definition/list")
        self._import_process_url = url_join("/projects/" + self._project_code + "/process-definition/import")
        self._export_process_url = url_join("/projects/" + self._project_code + "/process-definition/batch-export")
        self._release_process_url = url_join("/projects/" + self._project_code + "/process-definition/{}/release")
        self._operate_process_url = url_join("/projects/" + self._project_code + "/process-definition/{}")
        self._verify_name_url = url_join("/projects/" + self._project_code + "/process-definition/verify-name")

    def process_list(self, echo):
        """
        获取工作流列表
        """
        process_list_instance = request_get(self._process_list_url, {}, {}, {}, ProcessList)
        total_precesses = process_list_instance.data
        if echo:
            self._logging.info("Get {} processes. info is: ".format(len(total_precesses)))
            for precess in total_precesses:
                self._logging.info(object_to_json(precess.processDefinition))
        return total_precesses

    def export_process(self, process_code):
        """
        下载工作流内容并保存到文件
        Args:
            process_code: 工作流code，可以先调用process_list打印工作流列表获取code

        Returns:

        """
        data = {
            "codes": process_code
        }
        exists_process = {x.processDefinition.code: x.processDefinition.name for x in self.process_list(False)}
        if process_code in exists_process.keys():
            name = exists_process[process_code]
            filename = "{}_{}.json".format(name, str(int(time.time())))
            js = request_text(self._export_process_url, {}, data, "POST")
            write_file(filename, js, True)
        else:
            self._logging.error("Process code {} not found, exists codes {}".format(
                process_code, [json.dumps({"name": exists_process[x], "code": x}) for x in exists_process.keys()]))

    def import_process(self, filepath):
        """
        导入工作流
        Args:
            filepath: 本地工作流路径

        Returns:

        """
        if not os.path.exists(filepath):
            self._logging.error("Filepath {} not exists.".format(filepath))
            sys.exit(-1)
        files = {
            "file": open(filepath, "rb")
        }
        base_instance = request_post_files(self._import_process_url, {}, {}, files, BaseResponse)
        if base_instance.code == 0:
            self._logging.info("Process import success of {}".format(filepath))
            self.process_list(True)
        else:
            self._logging.error("Process import failed of {}, msg is '{}'".format(filepath, base_instance.msg))

    def release_process(self, process_code, is_online):
        """
        上下线工作流
        Args:
            process_code: 工作流code
            is_online: 是否上线

        Returns:

        """
        exists_process = {x.processDefinition.code: x.processDefinition.name for x in self.process_list(False)}
        if process_code in exists_process.keys():
            process_name = exists_process[process_code]
            state = "ONLINE" if is_online else "OFFLINE"
            data = {
                "name": process_name,
                "releaseState": state
            }
            base_instance = request_post(self._release_process_url.format(process_code), {}, {}, data, BaseResponse)
            if base_instance.code == 0:
                self._logging.info("Process {}({}) {} success.".format(process_code, process_name, state))
            else:
                self._logging.error("Process {}({}) {} failed, msg is '{}'".format(
                    process_code, process_name, state, base_instance.msg))
        else:
            self._logging.error("Process code {} not found, exists codes {}".format(
                process_code, [json.dumps({"name": exists_process[x], "code": x}) for x in exists_process.keys()]))

    def delete_process(self, process_code):
        """
        删除工作流
        Args:
            process_code: 工作流code

        Returns:

        """
        exists_process = {x.processDefinition.code: x.processDefinition.name for x in self.process_list(False)}
        if process_code in exists_process.keys():
            base_instance = request_delete(self._operate_process_url.format(process_code), {}, {}, {}, BaseResponse)
            if base_instance.code == 0:
                self._logging.info("Process {} delete success.".format(process_code))
            else:
                self._logging.error("Process {} delete failed, msg is '{}'".format(process_code, base_instance.msg))

    def update_process(self, filepath, is_help):
        """
        更新工作流
        Args:
            filepath: 修改后的工作流文件路径
            is_help: 打印帮助信息

        Returns:

        """
        if is_help:
            self._logging.info(""" The Usage for update process:
            1. Export process to a file first.
            2. Modify downloaded process file, The parameters that can be modified are: [processDefinition.name, 
                processDefinition.globalParamList, taskDefinitionList, processTaskRelationList].
            3. Provide the modified filepath to --update.
            """)
            sys.exit(-1)
        # 读取工作流内容
        if not os.path.exists(filepath):
            self._logging.error("Filepath {} not exists.".format(filepath))
            sys.exit(-1)
        with open(filepath, "rb") as f:
            content = json.load(f)[0]
        process_code = content["processDefinition"]["code"]
        process_name = content["processDefinition"]["name"]

        # 检查工作流code是否存在
        exists_process = {x.processDefinition.code: x.processDefinition.name for x in self.process_list(False)}
        if process_code not in exists_process.keys():
            self._logging.warning("Please export process first, then modify this file for update this process.")
            self._logging.error("Process code {} not found, exists codes {}".format(
                process_code, [json.dumps({"name": exists_process[x], "code": x}) for x in exists_process.keys()]))
            sys.exit(-1)

        # 验证工作流name是否可用
        params = {
            "name": process_name,
            "code": process_code
        }
        base_instance = request_get(self._verify_name_url, {}, params, {}, BaseResponse)
        if base_instance.code != 0:
            self._logging.error("Process name verify failed, please check it. msg is '{}'".format(base_instance.msg))
            sys.exit(-1)

        data = {"code": process_code,
                "name": process_name,
                "executionType": "PARALLEL",
                "timeout": 0,
                "description": "",
                "releaseState": "ONLINE",
                "locations": json.dumps(content["processDefinition"]["locations"]),
                "globalParams": json.dumps(content["processDefinition"]["globalParamList"]),
                "taskDefinitionJson": json.dumps(content["taskDefinitionList"]),
                "taskRelationJson": json.dumps(content["processTaskRelationList"])
                }
        instance = request_put(self._operate_process_url.format(process_code), {}, {}, data, ProcessUpdate)
        if instance.code == 0:
            self._logging.info("Process {}({}) update success, process info is '{}'".format(
                process_code, process_name, object_to_json(instance.data)))
        else:
            self._logging.error("Process {}({}) update failed, msg is '{}'".format(
                process_code, process_name, instance.msg))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Dolphin Scheduler process operation.")
    parser.add_argument("-l", "--list", action="store_true", help="get process list")
    parser.add_argument("-i", "--import", dest="im", help="import process, need a filepath")
    parser.add_argument("-e", "--export", help="export process, need process code, run -l get it")
    parser.add_argument("-u", "--inline", help="inline process, need process code, run -l get it")
    parser.add_argument("-o", "--offline", help="offline process, need process code, run -l get it")
    parser.add_argument("-d", "--delete", help="delete process, need process code, run -l get it")
    parser.add_argument("-p", "--update", help="update process, need a filepath")
    parser.add_argument("-r", "--reference", action="store_true", help="update process reference")
    args = parser.parse_args()

    handle = ProcessHandle()

    if args.list:
        handle.process_list(True)
    elif args.im:
        handle.import_process(args.im)
    elif args.export:
        handle.export_process(args.export)
    elif args.inline:
        handle.release_process(args.inline, True)
    elif args.offline:
        handle.release_process(args.offline, False)
    elif args.delete:
        handle.delete_process(args.delete)
    elif args.update:
        handle.update_process(args.update, False)
    elif args.reference:
        handle.update_process(args.update, True)
    else:
        parser.print_help()
