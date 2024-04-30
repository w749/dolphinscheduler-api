import attr

from common.entity import Base
from adapt.adapt import VERSION

if __name__ == '__main__':
    a = Base(2, "today is good day", {"a": 1, "b": 2}, True, True)
    print(attr.asdict(a))
    print(VERSION)
