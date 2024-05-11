# coding=utf-8
import argparse
import os.path
import sys


sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../")
from handle import QueueHandle
from common import BaseResponse, TenantCreate, TenantList
from settings import SETTINGS
from utils import url_join, request_post, request_get, get_logger, request_delete, object_to_json


class TenantHandle(object):
    """
    新增租户时先判断租户是否存在，如果不存在再创建
    同时对外提供获取租户列表的功能
    """
    def __init__(self):
        self._logging = get_logger(os.path.basename(__file__))
        self._verify_code_url = url_join("/tenants/verify-code")
        self._create_tenant_url = url_join("/tenants")
        self._tenant_list_url = url_join("/tenants/list")
        self._delete_tenant_url = url_join("/tenants/{}")
        self._tenant = SETTINGS.TENANT

    def _verify_code(self):
        """
        验证租户是否存在
        """
        params = {
            "tenantCode": self._tenant
        }
        base_instance = request_get(self._verify_code_url, {}, params, {}, BaseResponse)
        result = base_instance.msg == "success"
        if not result:
            self._logging.warning(base_instance.msg)
        return result

    def create_tenant(self, queue_id):
        """
        创建租户
        Args:
            queue_id: 队列ID

        Returns:

        """
        data = {
            "tenantCode": self._tenant,
            "queueId": queue_id
        }
        if self._verify_code():
            tenant_create_instance = request_post(self._create_tenant_url, {}, {}, data, TenantCreate)
            self._logging.info("Create tenant {0} success. Tenant {0} info: ".format(self._tenant))
            self._logging.info(object_to_json(tenant_create_instance.data))
        else:
            self._logging.warning("Tenant {} already exists.".format(self._tenant))

    def tenant_list(self, echo=True):
        """
        获取租户列表
        """
        tenant_list_instance = request_get(self._tenant_list_url, {}, {}, {}, TenantList)
        total_tenants = tenant_list_instance.data
        if echo:
            self._logging.info("Get {} tenants. info is: ".format(len(total_tenants)))
            for tenant in total_tenants:
                self._logging.info(object_to_json(tenant))
        return total_tenants

    def delete_tenant(self, tenant_name):
        """
        删除租户
        """
        tenant_list = self.tenant_list(False)
        tenant_filter = list(filter(lambda x: x.tenantCode == tenant_name, tenant_list))
        if len(tenant_filter) > 0:
            request_delete(self._delete_tenant_url.format(tenant_filter[0].id), {}, {}, {}, BaseResponse)
            self._logging.info("Delete tenant {} success.".format(tenant_name))
        else:
            exists_tenants = ", ".join([x.tenantCode for x in tenant_list])
            self._logging.warning("Exists tenant list [{}]".format(exists_tenants))
            self._logging.error("Tenant {} not exists.".format(tenant_name))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Dolphin Scheduler tenant operation.")
    parser.add_argument("-l", "--list", action="store_true", help="get tenant list")
    parser.add_argument("-c", "--create", action="store_true", help="create tenant")
    parser.add_argument("-d", "--delete", metavar="tenant_name", help="delete the provided tenant")
    args = parser.parse_args()

    handle = TenantHandle()

    if args.create:
        queue_handle = QueueHandle()
        handle.create_tenant(queue_handle.get_queue_id())
    elif args.list:
        handle.tenant_list()
    elif args.delete:
        handle.delete_tenant(args.delete)
    else:
        parser.print_help()
