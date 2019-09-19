import os
from datetime import timedelta


class DevelopmentConfig:

    DEBUG = True
    JSON_AS_ASCII = False
    API_SECRET_KEY = 'iU9GW39Ghs2Jh1Rq0n0Pn8AwIsiXnwB9'
    # DB_HOST: db
    #   DB_PORT: 3306
    #   DB_NAME: sugori_rendez_vous
    #   DB_USER: hidakkathon
    #   DB_PASS: hidakkathon

    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{user}:{password}@{host}/{database}?charset=utf8'.format(**{
        'user': os.getenv('DB_USER', 'hidakkathon'),
        'password': os.getenv('DB_PASS', 'hidakkathon'),
        'host': 'db',
        'database': os.getenv('DB_NAME', 'sugori_rendez_vous'),
    })

    SQLALCHEMY_POOL_RECYCLE = 90
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': 3,
    }

Config = DevelopmentConfig