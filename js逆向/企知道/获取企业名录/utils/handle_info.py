import pymysql


def save_base_info(connection, base_info):
    try:
        insert_query = '''
                INSERT INTO company_base_info (
                    company_name, company_id, url
                ) VALUES (
                    %(company_name)s, %(company_id)s, %(url)s
                );
                '''

        for base in base_info:
            with connection.cursor() as cursor:
                cursor.execute(insert_query, base)
                connection.commit()  # 提交插入操作
        print('插入成功')
    except pymysql.MySQLError as e:
        print(f"Error: {e.args}, {e.args}")

