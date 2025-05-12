import traceback
import aiomysql

class AsyncMySQLClient:
    def __init__(self, host: str, user: str, password: str, db: str, port: int = 3306, loop=None):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.db = db
        self.loop = loop
        self.pool = None

    # 创建连接池
    async def connect(self):
        try:
            self.pool = await aiomysql.create_pool(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                db=self.db,
                loop=self.loop,
                autocommit=True
            )
            print("数据库连接成功")
        except Exception as e:
            print(f"数据库连接失败: {traceback.format_exc()}")

    # 关闭连接池
    async def close(self):
        if self.pool:
            self.pool.close()
            await self.pool.wait_closed()
            print("数据库连接池已关闭")

    # 执行多条语句
    async def executemany(self, query: str, args: list) -> int:
        if not self.pool:
            raise RuntimeError("连接池未初始化")
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.executemany(query, args)
                return cur.rowcount  # 返回受影响的行数

    # 封装批量插入
    async def insert_many(self, table: str, data_list: list) -> int:
        if not data_list:
            print("数据列表为空")
            return 0

        try:
            # 定义字段名和占位符
            keys = 'goodsName, casIndexNo, goodsErpCode, brandName, goodsSpec, goodsStorePrice, goodsShowStorage, purity, molecularWeight, source'
            values_placeholder = ','.join(['%s'] * 10)  # 每条记录有10个字段

            # 创建 SQL 插入查询语句
            query = f'INSERT INTO {table} ({keys}) VALUES ({values_placeholder})'

            # 执行批量插入
            affected_rows = await self.executemany(query, data_list)
            print(f"插入 {affected_rows} 条记录")
            return affected_rows

        except Exception as e:
            print(f"执行 SQL 插入失败: {traceback.format_exc()}")
            return 0