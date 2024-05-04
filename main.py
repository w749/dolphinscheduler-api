import json

import attr

import common.response
import utils
from config import *
from common.response import Base
from adapt.adapt import VERSION

if __name__ == '__main__':
    with open("/Users/wangxun/workspace/my/project/dolphscheduler-api/data.json", "r") as f:
        js = json.load(f)
    print(js)
    print(utils.object_from_json(js, common.response.GetSessionId).data.securityConfigType)

