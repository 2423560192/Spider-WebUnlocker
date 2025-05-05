"""一个轻量级的 PyMySQL 封装，专为 Python3 编写"""

import time
import logging
import traceback
import pymysql.cursors

import asyncio
import aiomysql
import logging
import traceback

import logging
import traceback
from dbutils.pooled_db import PooledDB
import pymysql


class Connection:
    """单线程封装"""

    def __init__(self, host, database, user='root', password=None,
                 port=3306, max_idle_time=7 * 3600, connect_timeout=10,
                 time_zone="+0:00", charset="utf8mb4", sql_mode="TRADITIONAL"):
        """
        初始化数据库连接参数
        :param host: 数据库主机地址或Unix套接字路径
        :param database: 数据库名称
        :param user: 数据库用户名，可选
        :param password: 数据库密码，可选
        :param port: 数据库端口，默认0，如果host中没有指定端口时使用
        :param max_idle_time: 最大空闲时间，默认7小时（单位：秒）
        :param connect_timeout: 连接超时时间，默认10秒
        :param time_zone: 数据库连接的时区设置，默认+0:00
        :param charset: 连接使用的字符集，默认utf8mb4
        :param sql_mode: SQL模式，默认TRADITIONAL
        """
        self.host = host
        self.database = database
        self.max_idle_time = float(max_idle_time)  # 转换为浮点型，记录最大空闲时间
        self._last_use_time = time.time()  # 记录上次使用时间
        self._db = None  # 数据库连接对象，初始化为空

        # 配置数据库连接参数
        args = dict(
            use_unicode=True,  # 使用Unicode编码
            charset=charset,  # 字符集
            database=database,  # 数据库名称
            init_command=f'SET time_zone = "{time_zone}"',  # 初始化命令，设置时区
            cursorclass=pymysql.cursors.DictCursor,  # 查询结果以字典返回
            connect_timeout=connect_timeout,  # 连接超时设置
            sql_mode=sql_mode  # SQL模式
        )

        if user:
            args["user"] = user  # 添加用户名
        if password:
            args["passwd"] = password  # 添加密码

        if "/" in host:
            args["unix_socket"] = host  # 使用Unix套接字连接
        else:
            host_parts = host.split(":")  # 处理host:port格式
            args["host"] = host_parts[0]  # 主机地址
            args["port"] = int(host_parts[1]) if len(host_parts) == 2 else 3306  # 端口，默认为3306

        if port:
            args['port'] = port  # 如果明确指定了端口，覆盖前面的设置

        self._db_args = args  # 保存连接参数

        try:
            self.reconnect()  # 尝试连接数据库
        except Exception:
            logging.error("无法连接到 MySQL: %s", self.host, exc_info=True)  # 连接失败时记录错误日志

    def _ensure_connected(self):
        if self._db is None or (time.time() - self._last_use_time > self.max_idle_time):
            self.reconnect()
        self._last_use_time = time.time()

    def _cursor(self):
        self._ensure_connected()
        return self._db.cursor()

    def __del__(self):
        self.close()

    def close(self):
        if self._db:
            self._db.close()
            self._db = None

    def reconnect(self):
        self.close()
        self._db = pymysql.connect(**self._db_args)
        self._db.autocommit(True)

    def query(self, sql, *args, **kwargs):
        """执行查询，返回多行"""
        with self._cursor() as cursor:
            cursor.execute(sql, kwargs or args)
            return cursor.fetchall()

    def get(self, sql, *args, **kwargs):
        """执行查询，返回一行"""
        with self._cursor() as cursor:
            cursor.execute(sql, kwargs or args)
            return cursor.fetchone()

    def execute(self, sql, *args, **kwargs):
        """执行写操作，返回最后插入的ID"""
        with self._cursor() as cursor:
            try:
                cursor.execute(sql, kwargs or args)
                return cursor.lastrowid
            except pymysql.MySQLError as e:
                if e.args[0] == 1062:  # Duplicate entry
                    logging.warning("忽略重复插入: %s", e)
                else:
                    logging.error("执行SQL出错: %s\nSQL: %s", e, sql)
                    raise

    insert = execute  # 兼容旧接口

    ## =============== 高级封装 ===================

    def table_has(self, table_name, field, value):
        """检查表中是否有对应字段值"""
        sql = f"SELECT {field} FROM {table_name} WHERE {field}=%s LIMIT 1"
        return self.get(sql, value)

    def table_insert(self, table_name, item: dict):
        """插入一条数据，item是字典"""
        fields = list(item.keys())
        values = list(item.values())
        placeholders = ','.join(['%s'] * len(fields))
        field_list = ','.join(fields)
        sql = f"INSERT INTO {table_name} ({field_list}) VALUES ({placeholders})"
        try:
            return self.execute(sql, *values)
        except pymysql.MySQLError as e:
            if e.args[0] == 1062:
                logging.warning("重复插入被跳过")
            else:
                logging.error("插入数据出错: %s\n数据: %s", e, item)
                raise

    def table_update(self, table_name, updates: dict, field_where: str, value_where):
        """更新一条记录"""
        set_clause = ', '.join([f"{k}=%s" for k in updates.keys()])
        values = list(updates.values())
        values.append(value_where)
        sql = f"UPDATE {table_name} SET {set_clause} WHERE {field_where}=%s"
        self.execute(sql, *values)


class ConnectionPool:
    """
    多线程同步连接池
    """

    def __init__(self, host, database, user=None, password=None,
                 port=3306, charset="utf8mb4", max_connections=10,
                 min_cached=2, max_cached=5, blocking=True):
        """初始化连接池"""
        self._pool = PooledDB(
            creator=pymysql,
            maxconnections=max_connections,
            mincached=min_cached,
            maxcached=max_cached,
            blocking=blocking,
            host=host,
            port=port,
            user=user,
            password=password,
            database=database,
            charset=charset,
            use_unicode=True,
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=True
        )

    def _get_conn(self):
        """从连接池中获取一个连接"""
        return self._pool.connection()

    def query(self, sql, params=None):
        """执行查询，返回所有结果"""
        conn = self._get_conn()
        cursor = conn.cursor()
        try:
            cursor.execute(sql, params)
            result = cursor.fetchall()
            return result
        finally:
            cursor.close()
            conn.close()

    def get(self, sql, params=None):
        """执行查询，返回一条记录"""
        conn = self._get_conn()
        cursor = conn.cursor()
        try:
            cursor.execute(sql, params)
            return cursor.fetchone()
        finally:
            cursor.close()
            conn.close()

    def execute(self, sql, params=None):
        """执行插入/更新/删除，返回受影响的行数"""
        conn = self._get_conn()
        cursor = conn.cursor()
        try:
            rowcount = cursor.execute(sql, params)
            return rowcount
        except Exception as e:
            traceback.print_exc()
            logging.error(f"SQL执行错误: {e}\nSQL: {sql}\nParams: {params}")
            raise
        finally:
            cursor.close()
            conn.close()

    def insert(self, sql, params=None):
        """执行插入，返回最后插入的ID"""
        conn = self._get_conn()
        cursor = conn.cursor()
        try:
            cursor.execute(sql, params)
            return cursor.lastrowid
        except Exception as e:
            traceback.print_exc()
            logging.error(f"插入出错: {e}\nSQL: {sql}\nParams: {params}")
            raise
        finally:
            cursor.close()
            conn.close()

    def close(self):
        """连接池自己回收，不需要手动close"""
        pass

    ## =============== 高级封装 ===================

    def table_has(self, table_name, field, value):
        """检查表中是否有对应字段值"""
        sql = f"SELECT {field} FROM {table_name} WHERE {field}=%s LIMIT 1"
        return self.get(sql, value)

    def table_insert(self, table_name, item: dict):
        """插入一条数据，item是字典"""
        fields = list(item.keys())
        values = list(item.values())
        placeholders = ','.join(['%s'] * len(fields))
        field_list = ','.join(fields)
        sql = f"INSERT INTO {table_name} ({field_list}) VALUES ({placeholders})"
        try:
            return self.execute(sql, values)
        except pymysql.MySQLError as e:
            if e.args[0] == 1062:
                logging.warning("重复插入被跳过")
            else:
                logging.error("插入数据出错: %s\n数据: %s", e, item)
                raise

    def table_update(self, table_name, updates: dict, field_where: str, value_where):
        """更新一条记录"""
        set_clause = ', '.join([f"{k}=%s" for k in updates.keys()])
        values = list(updates.values())
        values.append(value_where)
        sql = f"UPDATE {table_name} SET {set_clause} WHERE {field_where}=%s"
        self.execute(sql, values)


# File: ezpymysql_async.py
# Author: veelion (异步版优化 by ChatGPT)

"""一个基于 aiomysql 的轻量级异步封装，适合 asyncio 程序使用"""




class AsyncConnection:
    """基于 aiomysql 的异步数据库连接封装"""

    def __init__(self, host, database, user=None, password=None,
                 port=3306, connect_timeout=10, charset="utf8mb4",
                 sql_mode="TRADITIONAL"):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.port = port
        self.connect_timeout = connect_timeout
        self.charset = charset
        self.sql_mode = sql_mode
        self._pool = None

    async def connect(self):
        """建立连接池"""
        self._pool = await aiomysql.create_pool(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            db=self.database,
            charset=self.charset,
            autocommit=True,
            connect_timeout=self.connect_timeout,
            sql_mode=self.sql_mode,
            cursorclass=aiomysql.DictCursor
        )

    async def close(self):
        """关闭连接池"""
        if self._pool:
            self._pool.close()
            await self._pool.wait_closed()

    async def query(self, sql, *args):
        """执行查询，返回多行"""
        async with self._pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(sql, args)
                result = await cur.fetchall()
                return result

    async def get(self, sql, *args):
        """执行查询，返回一行"""
        async with self._pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(sql, args)
                return await cur.fetchone()

    async def execute(self, sql, *args):
        """执行写操作，返回最后插入的ID"""
        async with self._pool.acquire() as conn:
            async with conn.cursor() as cur:
                try:
                    await cur.execute(sql, args)
                    return cur.lastrowid
                except aiomysql.MySQLError as e:
                    if e.args[0] == 1062:
                        logging.warning("忽略重复插入: %s", e)
                    else:
                        logging.error("SQL执行失败: %s\nSQL: %s", e, sql)
                        raise

    insert = execute

    ## =============== 高级封装 ===================

    async def table_has(self, table_name, field, value):
        """检查表中是否有对应字段值"""
        sql = f"SELECT {field} FROM {table_name} WHERE {field}=%s LIMIT 1"
        return await self.get(sql, value)

    async def table_insert(self, table_name, item: dict):
        """插入一条数据"""
        fields = list(item.keys())
        values = list(item.values())
        placeholders = ','.join(['%s'] * len(fields))
        field_list = ','.join(fields)
        sql = f"INSERT INTO {table_name} ({field_list}) VALUES ({placeholders})"
        try:
            return await self.execute(sql, *values)
        except aiomysql.MySQLError as e:
            if e.args[0] == 1062:
                logging.warning("重复插入被跳过")
            else:
                logging.error("插入数据出错: %s\n数据: %s", e, item)
                raise

    async def table_update(self, table_name, updates: dict, field_where: str, value_where):
        """更新一条记录"""
        set_clause = ', '.join([f"{k}=%s" for k in updates.keys()])
        values = list(updates.values())
        values.append(value_where)
        sql = f"UPDATE {table_name} SET {set_clause} WHERE {field_where}=%s"
        await self.execute(sql, *values)
