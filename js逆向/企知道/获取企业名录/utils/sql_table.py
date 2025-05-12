import pymysql


def init_mysql(config):
    conn = pymysql.connect(
        host=config['DATABASE']['host'],  # 连接的服务器ip
        user=config['DATABASE']['user'],  # 用户名
        password=config['DATABASE']['password'],  # 密码
        charset='utf8mb4'  # 指定字符编码，不要加杠，如：utf-8
    )

    cursor = conn.cursor()  # 获取游标

    database = config['DATABASE']['database']

    # 创建数据库 company
    try:
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
        print("数据库 'company' 创建成功。")
    except:
        pass
    conn.select_db(database)

    return conn, cursor


def create_database_and_table(connection, cursor):
    try:
        # 创建表 company_info
        create_table_query = '''
    CREATE TABLE IF NOT EXISTS company_base_info (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '主键ID',
    company_name VARCHAR(255) NOT NULL COMMENT '企业名',
    company_id VARCHAR(255) UNIQUE COMMENT '信用代码',
    url VARCHAR(255) UNIQUE COMMENT '链接'
    ) COMMENT='公司名录表';
'''

        cursor.execute(create_table_query)
        print("表 'company_base_info' 创建成功。")
        # 提交更改
        connection.commit()
    except pymysql.MySQLError as e:
        print(f"数据库操作失败: {e}")