import platform


VERSION = int(platform.python_version()[0])

if VERSION == 2:
    import cattr
    adapt_cattrs = cattr
else:
    import cattrs
    adapt_cattrs = cattrs
