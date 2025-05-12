import pymysql
from dbutils.pooled_db import PooledDB

pool = PooledDB(
    creator=pymysql,
    maxconnections=5,
    mincached=2,
    maxcached=5,
    blocking=True,
    host="localhost",
    user="root",
    password="5201314",
    db="shiji",
    charset="utf8mb4",
)
