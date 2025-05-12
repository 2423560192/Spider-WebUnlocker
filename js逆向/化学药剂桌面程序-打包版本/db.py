import configparser

import pymysql
from dbutils.pooled_db import PooledDB


def loadConf():
    config = configparser.RawConfigParser()
    with open('utils/conf.ini', 'r', encoding='utf-8') as f:
        config.read_file(f)
    return config

config = loadConf()

pool = PooledDB(
    creator=pymysql,
    maxconnections=5,
    mincached=2,
    maxcached=5,
    blocking=True,
    host=config['DATABASE']['host'],
    user=config['DATABASE']['user'],
    password=config['DATABASE']['password'],
    db=config['DATABASE']['database'],
    charset="utf8mb4",
)
