# coding=utf-8
import argparse
import os.path
import sys


sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../")
from common import BaseResponse, ResourceList
from settings import SETTINGS
from utils import (url_join, request_put_files, request_post_files, request_get, get_logger,
                   request_delete, object_to_json)


class ResourceHandle(object):
    """
    上传资源
    更新资源
    获取资源列表
    创建资源目录
    删除资源
    """
    def __init__(self):
        self._logging = get_logger(os.path.basename(__file__))
        self._resources_url = url_join("/resources")
        self._resource_list_url = url_join("/resources/list")

    def resource_list(self, echo=True):
        """
        获取资源列表
        """
        params = {
            "type": "FILE",
            "fullName": ""
        }
        resource_list_instance = request_get(self._resource_list_url, {}, params, {}, ResourceList)
        total_resources = resource_list_instance.data
        if echo:
            self._logging.info("Get {} resources. info is: ".format(len(total_resources)))
            for resource in total_resources:
                self._logging.info(object_to_json(resource))
        return total_resources

    def get_resource_info(self, filename):
        """
        获取资源名称对应的资源信息
        """
        resource_list = self.resource_list(False)
        resource_filter = list(filter(lambda x: x.name == filename, resource_list))
        if len(resource_filter) > 0:
            return resource_filter[0]
        else:
            self._logging.error("Resource {} not exists.".format(filename))
            return None

    def upload_resource(self, path):
        """
        上传资源，仅支持上传到根目录，只有资源名称不存在时才可以上传
        Args:
            path: 文件路径

        """
        if not os.path.exists(path):
            self._logging.error("File {} not exists.".format(path))
            raise RuntimeError()
        filename = os.path.basename(path)
        data = {
            "type": "FILE",
            "name": filename,
            "currentDir": "/"
        }
        files = {
            "file": open(path, "rb")
        }
        base_instance = request_post_files(self._resources_url, {}, data, files, BaseResponse)
        if base_instance.code == 0:
            resource_info = self.get_resource_info(filename)
            self._logging.info("Upload resource {0} success. resource {0} info: ".format(filename))
            self._logging.info(object_to_json(resource_info))
        else:
            self._logging.warning("Resource {} already exists, please delete it first or update it.".format(filename))

    def update_resource(self, path):
        """
        更新资源，只有资源名称存在时才可以上传
        Args:
            path: 文件路径

        """
        if not os.path.exists(path):
            self._logging.error("File {} not exists.".format(path))
            raise RuntimeError()
        filename = os.path.basename(path)
        resource_info = self.get_resource_info(filename)
        if not resource_info:
            self._logging.warning("Please upload resource {} first.".format(filename))
        else:
            data = {
                "type": "FILE",
                "name": filename,
                "user_name": SETTINGS.TENANT,
                "tenantCode": SETTINGS.TENANT,
                "fullName": resource_info.fullName
            }
            files = {
                "file": open(path, "rb")
            }
            request_put_files(self._resources_url, {}, data, files, BaseResponse)
            self._logging.info("Update resource {} success.".format(filename))

    def delete_resource(self, resource_name):
        """
        删除租户
        """
        resource_list = self.resource_list(False)
        resource_filter = list(filter(lambda x: x.name == resource_name, resource_list))
        if len(resource_filter) > 0:
            params = {
                "fullName": resource_filter[0].fullName
            }
            request_delete(self._resources_url, {}, params, {}, BaseResponse)
            self._logging.info("Delete resource {} success.".format(resource_name))
        else:
            exists_resources = ", ".join([x.name for x in resource_list])
            self._logging.warning("Exists resource list [{}]".format(exists_resources))
            self._logging.error("Resource {} not exists.".format(resource_name))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Dolphin Scheduler resource operation.")
    parser.add_argument("-l", "--list", action="store_true", help="get resource list")
    parser.add_argument("-p", "--upload", help="upload resource")
    parser.add_argument("-u", "--update", help="update resource")
    parser.add_argument("-d", "--delete", help="delete the provided resource")
    args = parser.parse_args()

    handle = ResourceHandle()

    if args.upload:
        handle.upload_resource(args.upload)
    elif args.update:
        handle.update_resource(args.update)
    elif args.delete:
        handle.delete_resource(args.delete)
    elif args.list:
        handle.resource_list()
    else:
        parser.print_help()
