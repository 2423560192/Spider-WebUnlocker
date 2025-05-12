import pymysql
from dbutils.pooled_db import PooledDB


class DB:
    def __init__(self):
        self.host = 'localhost'
        self.user = 'root'
        self.password = '5201314'
        self.database = 'xiaofang'

        self.pooldb = PooledDB(
            creator=pymysql,  # 使用链接数据库的模块
            maxconnections=6,  # 连接池允许的最大连接数，0和None表示不限制连接数
            mincached=2,  # 初始化时，链接池中至少创建的空闲的链接，0表示不创建
            maxcached=5,  # 链接池中最多闲置的链接，0和None不限制
            maxshared=1,  # 链接池中最多共享的链接数量，0和None表示全部共享
            blocking=True,  # 连接池中如果没有可用连接后，是否阻塞等待。True，等待；False，不等待然后报错
            maxusage=None,  # 一个链接最多被重复使用的次数，None表示无限制
            setsession=[],  # 开始会话前执行的命令列表。如：["set datestyle to ...", "set time zone ..."]
            ping=0,
            host=self.host,
            port=3306,
            user=self.user,
            password=self.password,
            database=self.database,
            charset='utf8'
        )

    def connect(self):
        self.conn = self.pooldb.connection()
        self.cursor = self.conn.cursor()
        return self.conn, self.cursor

    def close(self):
        self.cursor.close()
        self.conn.close()

    def create_table(self):
        try:
            create_subsidy_table_query = '''
                CREATE TABLE IF NOT EXISTS subsidy_info2 (
                    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '主键ID',
                    creditCode VARCHAR(255) NOT NULL COMMENT '企业ID',
                    companyName VARCHAR(255) NOT NULL COMMENT '公司名',
                    businessLicenseImage VARCHAR(255) COMMENT '营业执照',
                    companyTypeName VARCHAR(255) COMMENT '场所类型',
                    dutyPerson VARCHAR(255) COMMENT '负责人',
                    phone VARCHAR(255) COMMENT '手机号',
                    addressInfo VARCHAR(255) COMMENT '地址',
                    businessScope TEXT COMMENT '简介'
                ) COMMENT='企业数';
                '''

            self.cursor.execute(create_subsidy_table_query)
            print("表创建成功。")

            # 提交更改
            self.conn.commit()

        except pymysql.MySQLError as e:
            print(f"数据库操作失败: {e}")

    def insert(self, data):
        # 插入数据的SQL语句
        insert_query = '''
                    INSERT INTO subsidy_info2 (
            creditCode, companyName, businessLicenseImage, companyTypeName, dutyPerson, phone, addressInfo, businessScope
        ) VALUES (
            %(creditCode)s, %(companyName)s, %(businessLicenseImage)s, %(companyTypeName)s, %(dutyPerson)s, %(phone)s, %(addressInfo)s, %(businessScope)s
        );
         '''

        self.cursor.execute(insert_query, data)

        self.conn.commit()

    def search(self):
        insert_query = '''
          SELECT creditCode FROM subsidy_info2;
        '''
        self.cursor.execute(insert_query)
        return self.cursor.fetchall()
