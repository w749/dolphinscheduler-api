# coding=utf-8
import argparse
import os.path
import sys


sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../")
from common import BaseResponse, QueueCreate, QueueList
from settings import SETTINGS
from utils import url_join, request_post, request_get, get_logger, request_delete, object_to_json


class QueueHandle(object):
    """
    新增队列时先判断队列是否存在，如果不存在再创建
    同时对外提供获取队列列表的功能
    """
    def __init__(self):
        self._logging = get_logger(os.path.basename(__file__))
        self._verify_queue_url = url_join("/queues/verify")
        self._create_queue_url = url_join("/queues")
        self._queue_list_url = url_join("/queues/list")
        self._delete_queue_url = url_join("/queues/{}")
        self._queue = SETTINGS.QUEUE

    def _verify_queue(self):
        """
        验证队列是否存在
        """
        data = {
            "queue": self._queue,
            "queueName": self._queue
        }
        base_instance = request_post(self._verify_queue_url, {}, {}, data, BaseResponse)
        result = base_instance.msg == "success"
        if not result:
            self._logging.warning(base_instance.msg)
        return result

    def create_queue(self):
        """
        创建队列
        """
        data = {
            "queue": self._queue,
            "queueName": self._queue
        }
        if self._verify_queue():
            queue_create_instance = request_post(self._create_queue_url, {}, {}, data, QueueCreate)
            self._logging.info("Create queue {0} success. Queue {0} info: ".format(self._queue))
            self._logging.info(object_to_json(queue_create_instance.data))
            return queue_create_instance.data.id
        else:
            self._logging.warning("Queue {} already exists.".format(self._queue))
            return -1

    def queue_list(self, echo):
        """
        获取队列列表
        """
        queue_list_instance = request_get(self._queue_list_url, {}, {}, {}, QueueList)
        total_queues = queue_list_instance.data
        if echo:
            self._logging.info("Get {} queues. info is: ".format(len(total_queues)))
            for queue in total_queues:
                self._logging.info(object_to_json(queue))
        return total_queues

    def get_queue_id(self):
        """
        获取队列对应的ID
        """
        queue_list = self.queue_list(False)
        queue_filter = list(filter(lambda x: x.queueName == self._queue, queue_list))
        if len(queue_filter) > 0:
            return queue_filter[0].id
        else:
            self._logging.error("Queue {} not exists, now create it.".format(self._queue))
            return self.create_queue()

    def delete_queue(self, queue_name):
        """
        删除租户
        """
        queue_list = self.queue_list(False)
        queue_filter = list(filter(lambda x: x.queueName == queue_name, queue_list))
        if len(queue_filter) > 0:
            request_delete(self._delete_queue_url.format(queue_filter[0].id), {}, {}, {}, BaseResponse)
            self._logging.info("Delete queue {} success.".format(queue_name))
        else:
            exists_queues = ", ".join([x.queueName for x in queue_list])
            self._logging.warning("Exists queue list [{}]".format(exists_queues))
            self._logging.error("Queue {} not exists.".format(queue_name))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Dolphin Scheduler queue operation.")
    parser.add_argument("-c", "--create", action="store_true", help="create queue")
    parser.add_argument("-l", "--list", action="store_true", help="get queue list")
    parser.add_argument("-d", "--delete", help="delete the provided queue")
    args = parser.parse_args()

    handle = QueueHandle()

    if args.create:
        handle.create_queue()
    elif args.list:
        handle.queue_list(True)
    elif args.delete:
        handle.delete_queue(args.delete)
    else:
        parser.print_help()
