import attr


@attr.s
class Base(object):
    code = attr.ib(default=-1)
    msg = attr.ib(default="")
    data = attr.ib(default=None)
    failed = attr.ib(default=False)
    success = attr.ib(default=True)
