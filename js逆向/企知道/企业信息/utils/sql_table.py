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
    CREATE TABLE IF NOT EXISTS company_info (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '主键ID',
    company_name VARCHAR(255) NOT NULL COMMENT '企业名',
    company_id VARCHAR(255) UNIQUE COMMENT '信用代码',
    re_name VARCHAR(255) COMMENT '曾用名',
    company_people VARCHAR(255) COMMENT '法人',
    company_status VARCHAR(255) COMMENT '公司状态',
    company_start_time DATE COMMENT '成立日期',
    company_money VARCHAR(255) COMMENT '注册资本',
    company_really_money VARCHAR(255) COMMENT '实缴资本',
    company_type VARCHAR(255) COMMENT '组织机构类型',
    company_code VARCHAR(255) COMMENT '组织机构代码',
    company_nasui_id VARCHAR(255) COMMENT '纳税人识别号',
    company_gongshang_id VARCHAR(255) COMMENT '工商注册号',
    company_ctype VARCHAR(255) COMMENT '企业类型',
    company_nasui_zizhi VARCHAR(255) COMMENT '增值税一般纳税人',
    company_jinkou_code VARCHAR(255) COMMENT '进出口企业代码',
    company_hangye VARCHAR(255) COMMENT '所属行业',
    company_people_num VARCHAR(255) COMMENT '员工人数',
    company_canbao_people_num VARCHAR(255) COMMENT '参保人数',
    company_dengji VARCHAR(255) COMMENT '登记机关',
    company_manage_date VARCHAR(255) COMMENT '经营期限',
    company_hezhun_date VARCHAR(255) COMMENT '核准日期',
    company_haiguan_code VARCHAR(255) COMMENT '海关注册编码',
    company_english_name VARCHAR(255) COMMENT '英文名',
    company_reg_addr VARCHAR(255) COMMENT '注册地址',
    company_manage_range TEXT COMMENT '经营范围'
) COMMENT='企业信息表';
'''

        cursor.execute(create_table_query)
        print("表 'company_info' 创建成功。")

        create_subsidy_table_query = '''
        CREATE TABLE IF NOT EXISTS subsidy_info (
            id INT AUTO_INCREMENT PRIMARY KEY COMMENT '主键ID',
            company_id VARCHAR(255) NOT NULL COMMENT '企业ID',
            project_name VARCHAR(255) NOT NULL COMMENT '项目名称',
            project_grade VARCHAR(255) COMMENT '项目级别',
            project_type_eight VARCHAR(255) COMMENT '项目类型',
            categorys VARCHAR(255) COMMENT '受理部门',
            data_year VARCHAR(255) COMMENT '年度',
            subsidy_money VARCHAR(255) COMMENT '补贴金额',
            qita TEXT COMMENT '其他'
        ) COMMENT='补贴信息表';
        '''

        cursor.execute(create_subsidy_table_query)
        print("表 'subsidy_info' 创建成功。")

        # 提交更改
        connection.commit()
    except pymysql.MySQLError as e:
        print(f"数据库操作失败: {e}")