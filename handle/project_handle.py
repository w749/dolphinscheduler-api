# coding=utf-8
import argparse
import ast
import os.path
import sys


sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../")
from common import BaseResponse, ProjectList, ProjectInner
from settings import SETTINGS
from utils import url_join, request_post, request_get, get_logger, request_delete, object_from_json, object_to_json


class ProjectHandle(object):
    """
    创建项目，同时对外提供获取项目列表的功能
    """
    def __init__(self):
        self._logging = get_logger(os.path.basename(__file__))
        self._create_project_url = url_join("/projects")
        self._project_list_url = url_join("/projects/list")
        self._delete_project_url = url_join("/projects/{}")
        self._project = SETTINGS.PROJECT

    def create_project(self):
        """
        创建项目
        """
        data = {
            "projectName": self._project,
        }
        base_instance = request_post(self._create_project_url, {}, {}, data, BaseResponse)
        if base_instance.code == 0:
            # 将单引号形式的字典字符串转为字典
            project_dict = ast.literal_eval(base_instance.data)
            project_instance = object_from_json(project_dict, ProjectInner)
            self._logging.info("Create project {0} success. project {0} info: ".format(self._project))
            self._logging.info(object_to_json(project_instance))
            return project_instance.id
        else:
            self._logging.warning("Project {} already exists.".format(self._project))
            return -1

    def project_list(self, echo=True):
        """
        获取项目列表
        """
        project_list_instance = request_get(self._project_list_url, {}, {}, {}, ProjectList)
        total_projects = project_list_instance.data
        if echo:
            self._logging.info("Get {} projects. info is: ".format(len(total_projects)))
            for project in total_projects:
                self._logging.info(object_to_json(project))
        return total_projects

    def get_project_id(self):
        """
        获取项目对应的ID
        """
        project_list = self.project_list(False)
        project_filter = list(filter(lambda x: x.name == self._project, project_list))
        if len(project_filter) > 0:
            return project_filter[0].code
        else:
            self._logging.error("Project {} not exists, now create it.".format(self._project))
            return self.create_project()

    def delete_project(self, project_name):
        """
        删除项目
        """
        project_list = self.project_list(False)
        project_filter = list(filter(lambda x: x.name == project_name, project_list))
        if len(project_filter) > 0:
            base_instance = request_delete(self._delete_project_url.format(project_filter[0].code), {}, {}, {}, BaseResponse)
            if base_instance.code == 0:
                self._logging.info("Delete project {} success.".format(project_name))
            else:
                self._logging.warning("Delete project {} failed, msg is {}.".format(project_name, base_instance.msg))
        else:
            exists_projects = ", ".join([x.name for x in project_list])
            self._logging.warning("Exists project list [{}]".format(exists_projects))
            self._logging.error("Project {} not exists.".format(project_name))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Dolphin Scheduler project operation.")
    parser.add_argument("-l", "--list", action="store_true", help="get project list")
    parser.add_argument("-c", "--create", action="store_true", help="create project")
    parser.add_argument("-d", "--delete", help="delete the provided project")
    args = parser.parse_args()

    handle = ProjectHandle()

    if args.create:
        handle.create_project()
    elif args.list:
        handle.project_list()
    elif args.delete:
        handle.delete_project(args.delete)
    else:
        parser.print_help()
