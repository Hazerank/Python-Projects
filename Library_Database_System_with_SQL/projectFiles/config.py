import os
class Config(object):
    SECRET_KEY = os.environ.get("SECRET_KEY") or "you-will-never-guess"
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'hazar'
    MYSQL_PASSWORD = '1789'
    MYSQL_DB = 'project3'