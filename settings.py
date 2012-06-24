# app-wide production settings can go in this file
MONGO_HOST = "localhost"
MONGO_PORT = 27017
MONGO_DATABASE = "fastco"
STATIC = "/static"
MIN = ""

try:
    # use localsettings.py to create development settings
    # e.g. local database connection, file paths, log settings
    from localsettings import *
except ImportError:
    pass
