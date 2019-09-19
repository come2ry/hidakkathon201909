import os
from datetime import timedelta


class DevelopmentConfig:

    DEBUG = True
    JSON_AS_ASCII = False
    API_SECRET_KEY = 'iU9GW39Ghs2Jh1Rq0n0Pn8AwIsiXnwB9'
    db_user = os.getenv('MYSQL_USER', 'hidakkathon')
    db_password = os.getenv('MYSQL_PASSWORD', 'hidakkathon')
    db_name = os.getenv('MYSQL_DATABASE', 'sugori_rendez_vous')

    host = '127.0.0.1'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{}:{}@{}/{}?charset=utf8'.format(
        db_user, db_password, host, db_name)

    SQLALCHEMY_POOL_RECYCLE = 90
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': 3,
    }

Config = DevelopmentConfig