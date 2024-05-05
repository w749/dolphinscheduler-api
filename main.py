import json

import common
import utils
from settings import SETTINGS

if __name__ == '__main__':
    with open("/Users/wangxun/workspace/my/project/dolphscheduler-api/data.json") as f:
        js = json.load(f)
    print(js)
    print(utils.object_from_json(js, common.ProjectList).data[0].description)

    print(SETTINGS.BASE_URL)
    print(SETTINGS.USERNAME)
    print(SETTINGS.PASSWORD)

