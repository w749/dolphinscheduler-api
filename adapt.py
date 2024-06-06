# coding=utf-8
import platform
import subprocess

"""
解决python2和python3的兼容性问题
"""
VERSION = int(platform.python_version()[0])

if VERSION == 2:
    import sys
    import cattr
    adapt_cattrs = cattr

    def default_encoding():
        reload(sys)
        sys.setdefaultencoding('utf-8')

    def adapt_open(filename, method):
        return open(filename, method)

    def adapt_subprocess_run(args):
        return subprocess.call(args)
else:
    import cattrs
    adapt_cattrs = cattrs

    def default_encoding():
        pass

    def adapt_open(filename, method):
        return open(filename, method, encoding="utf-8")

    def adapt_subprocess_run(args):
        return subprocess.run(args)
