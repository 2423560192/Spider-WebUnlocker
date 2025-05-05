import pymysql

# 数据库连接配置
mysql_config = {
    "host": "localhost",
    "user": "root",
    "password": "5201314",
    "database": "danci",
    "port": 3306,
    "charset": "utf8mb4"
}

# 清空顺序（先清子表，再清父表）
TABLES = [
    "book_resources",
    "unit_ebook_pages",
    "ebook_images",
    "vocabulary",
    "units",
    "books",
    "versions"
]

def clear_database():
    conn = pymysql.connect(**mysql_config)
    cursor = conn.cursor()

    try:
        cursor.execute("SET FOREIGN_KEY_CHECKS=0;")  # 关闭外键检查
        for table in TABLES:
            print(f"清空表：{table}")
            cursor.execute(f"DELETE FROM {table};")
        cursor.execute("SET FOREIGN_KEY_CHECKS=1;")  # 恢复外键检查
        conn.commit()
        print("✅ 所有数据已清空（表结构保留）")
    except Exception as e:
        print("❌ 出错：", e)
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    clear_database()
