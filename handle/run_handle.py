# coding=utf-8
import argparse
import json
import os.path
import sys


sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../")
from handle import ProjectHandle
from common import BaseResponse
from utils import url_join, get_logger, request_post
from datetime import datetime


class RunHandle(object):
    """
    补数
    """

    def __init__(self):
        self._logging = get_logger(os.path.basename(__file__))
        self._project_code = str(ProjectHandle().get_project_id())
        self._run_process_url = url_join("/projects/" + self._project_code + "/executors/start-process-instance")

    def run(self, process_code, start_time, end_time, tenant_code):
        """
        执行补数操作
        Args:
            process_code: process ID
            start_time: 补数开始时间
            end_time: 补数结束时间
            tenant_code: 租户

        Returns:

        """
        params = {
            "processDefinitionCode": process_code,
            "scheduleTime": json.dumps({
                "complementStartDate": start_time,
                "complementEndDate": end_time
            }),
            "tenantCode": tenant_code,
            "execType": "COMPLEMENT_DATA",
            "failureStrategy": "CONTINUE",
            "warningType": "NONE",
            "processInstancePriority": "MEDIUM",
            "taskDependType": "TASK_POST",
            "complementDependentMode": "OFF_MODE",
            "runMode": "RUN_MODE_SERIAL",
            "executionOrder": "DESC_ORDER"
        }
        obj = request_post(self._run_process_url, {}, {}, params, BaseResponse)
        if obj.code == 0:
            self._logging.info("Complement data success for process id {} at {} to {} success."
                               .format(process_code, start_time, end_time))
        else:
            self._logging.error("Complement data failed for process id {} at {} to {}, msg is '{}'"
                                .format(process_code, start_time, end_time, obj.msg))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Dolphin Scheduler complement data operation.")
    parser.add_argument("-c", "--code", required=True, metavar="code", help="process code, run process -l get it")
    parser.add_argument("-s", "--start", metavar="start_time", help="start time, default now, need "
                                                                    "use quotation marks, eg: '2024-05-01 00:00:00'")
    parser.add_argument("-e", "--end", metavar="end_time", help="end time, default now, need "
                                                                "use quotation marks, eg: '2024-05-01 00:00:00'")
    parser.add_argument("-t", "--tenant-code", dest="tenant", metavar="tenant", default="hdfs", help="tenant code, default hdfs")
    args = parser.parse_args()

    _datetime_format = "%Y-%m-%d %H:%M:%S"
    handle = RunHandle()

    start = datetime.now().strftime(_datetime_format)
    end = datetime.now().strftime(_datetime_format)
    tenant = args.tenant
    if args.start:
        start = args.start
    if args.end:
        end = args.end

    handle.run(args.code, start, end, tenant)
