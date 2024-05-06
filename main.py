import json
import common
import utils
from settings import SETTINGS

from adapt import default_encoding, adapt_open
default_encoding()

if __name__ == '__main__':
    with adapt_open("data.json", "r") as f:
        js = json.load(f)
    print(js)
    print(utils.object_from_json(js, common.ProjectList).data[0].description)

    print(SETTINGS.BASE_URL)
    print(SETTINGS.USERNAME)
    print(SETTINGS.PASSWORD)

