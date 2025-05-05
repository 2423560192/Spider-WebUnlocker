import math
import os
import pandas as pd
from concurrent.futures import ThreadPoolExecutor
from dbutils.pooled_db import PooledDB
import pymysql

# === 数据库配置 ===
mysql_config = {
    "host": "120.26.141.132",
    "user": "base_word",
    "password": "Y88yMfw8h84nhad7",
    "database": "base_word",
    "port": 3306,
    "charset": "utf8mb4"
}

# 创建数据库连接池
pool = PooledDB(
    creator=pymysql,
    maxconnections=100,
    mincached=20,
    maxcached=30,
    maxshared=30,
    blocking=True,
    ping=1,
    **mysql_config
)


def get_conn():
    return pool.connection()


def clean_value(val):
    if val is None or (isinstance(val, float) and math.isnan(val)):
        return None
    return str(val).strip() if isinstance(val, str) else val


def clean_number(val):
    try:
        if val is None or (isinstance(val, float) and math.isnan(val)):
            return None
        return int(float(val))
    except:
        return None


def process_version_and_book(cursor, version_name, book_name):
    # 确定年级
    grade = '小学'
    if '初中' in version_name and '鲁教初中' not in version_name:
        grade = '初中'
    elif '高中' in version_name:
        grade = '高中'

    # 处理版本
    cursor.execute(
        "INSERT IGNORE INTO versions (version_name, grade) VALUES (%s, %s)",
        (version_name, grade)
    )

    # 获取版本ID
    cursor.execute(
        "SELECT version_id FROM versions WHERE version_name = %s",
        (version_name,)
    )
    version_id = cursor.fetchone()[0]

    # 处理书籍
    cursor.execute(
        "INSERT IGNORE INTO books (book_name, version_id) VALUES (%s, %s)",
        (book_name, version_id)
    )

    # 获取书籍ID
    cursor.execute(
        "SELECT book_id FROM books WHERE book_name = %s AND version_id = %s",
        (book_name, version_id)
    )
    return cursor.fetchone()[0]


def process_ebook_images(cursor, filepath, book_id):
    try:
        df = pd.read_excel(filepath).where(pd.notnull(pd.read_excel(filepath)), None)
        for _, row in df.iterrows():
            data = {
                'page_number': clean_number(row.get('page_number')),
                'image_path': clean_value(row.get('image_path')).replace('ciyuankoudai', 'danci') if row.get(
                    'image_path') else None,
                'sound_path': clean_value(row.get('sound_path')),
                'english_text': clean_value(row.get('english_text')),
                'chinese_text': clean_value(row.get('chinese_text')),
                'axis_x': clean_number(row.get('axis_x')),
                'axis_y': clean_number(row.get('axis_y')),
                'axis_width': clean_number(row.get('axis_width')),
                'axis_height': clean_number(row.get('axis_height')),
                'img_book_id': book_id
            }

            if not all(v is None for v in data.values()):
                cursor.execute("""
                    INSERT INTO ebook_images
                    (page_number, image_path, sound_path, english_text, chinese_text, 
                     axis_x, axis_y, axis_width, axis_height, img_book_id)
                    VALUES (%(page_number)s, %(image_path)s, %(sound_path)s, %(english_text)s, 
                            %(chinese_text)s, %(axis_x)s, %(axis_y)s, %(axis_width)s, 
                            %(axis_height)s, %(img_book_id)s)
                """, data)
    except Exception as e:
        print(f"❌ 图文标注处理失败: {filepath} - {e}")


def process_lesson_data(cursor, filepath, book_id):
    try:
        df = pd.read_excel(filepath).where(pd.notnull(pd.read_excel(filepath)), None)

        # 创建所有单元
        unit_names = set()
        for _, row in df.iterrows():
            unit_name = clean_value(row.get('Name'))
            if unit_name:
                unit_names.add(unit_name)

        for unit_name in unit_names:
            cursor.execute("""
                INSERT IGNORE INTO units (unit_name, book_id)
                VALUES (%s, %s)
            """, (unit_name, book_id))

        # 插入页码信息
        for _, row in df.iterrows():
            unit_name = clean_value(row.get('Name'))
            page_number = clean_number(row.get('Page'))

            if unit_name and page_number is not None:
                cursor.execute("""
                    INSERT INTO unit_ebook_pages (book_id, unit_name, page_number)
                    VALUES (%s, %s, %s)
                """, (book_id, unit_name, page_number))
    except Exception as e:
        print(f"❌ 页码表处理失败: {filepath} - {e}")


def process_resources(cursor, dirpath, book_id):
    try:
        for root, _, files in os.walk(dirpath):
            for file in files:
                file_path = os.path.join(root, file).replace('\\', '/')
                relative_path = os.path.relpath(file_path, dirpath).replace('\\', '/')
                type_name = relative_path.split('/')[0] if '/' in relative_path else '其他'

                cursor.execute("""
                    INSERT INTO book_resources 
                    (book_id, resource_name, file_path, type)
                    VALUES (%s, %s, %s, %s)
                """, (book_id, file, file_path, type_name))
    except Exception as e:
        print(f"❌ 资源处理失败: {dirpath} - {e}")


def process_vocabulary_from_word_folder(cursor, word_folder_path, book_id):
    """处理单词文件夹中的Excel文件"""
    try:
        # 遍历单词文件夹中的所有Excel文件
        for filename in os.listdir(word_folder_path):
            if filename.endswith('.xlsx'):
                filepath = os.path.join(word_folder_path, filename)
                unit_name = os.path.splitext(filename)[0]

                # 创建单元
                cursor.execute("""
                    INSERT IGNORE INTO units (unit_name, book_id)
                    VALUES (%s, %s)
                """, (unit_name, book_id))

                # 获取单元ID
                cursor.execute("""
                    SELECT unit_id FROM units 
                    WHERE unit_name = %s AND book_id = %s
                """, (unit_name, book_id))
                unit_id = cursor.fetchone()[0]

                # 处理单词数据
                df = pd.read_excel(filepath).where(pd.notnull(pd.read_excel(filepath)), None)
                for _, row in df.iterrows():
                    if 'Word' in row and 'Chinese' in row:
                        cursor.execute("""
                            INSERT INTO vocabulary 
                            (word, chinese, phonetic, unit_id)
                            VALUES (%s, %s, %s, %s)
                        """, (
                            clean_value(row['Word']),
                            clean_value(row['Chinese']),
                            clean_value(row.get('Phonetic')),
                            unit_id
                        ))
    except Exception as e:
        print(f"❌ 单词文件夹处理失败: {word_folder_path} - {e}")


def process_book(version_name, book_name, book_path):
    conn = get_conn()
    try:
        conn.begin()
        cursor = conn.cursor()

        # 1. 处理版本和书籍信息
        book_id = process_version_and_book(cursor, version_name, book_name)

        # 2. 查找单词文件夹
        word_folder_path = os.path.join(book_path, "单词")
        if os.path.exists(word_folder_path):
            process_vocabulary_from_word_folder(cursor, word_folder_path, book_id)

        # 3. 处理其他文件
        for filename in os.listdir(book_path):
            filepath = os.path.join(book_path, filename)

            # 跳过单词文件夹(已经处理过)
            if filename == "单词":
                continue

            # 处理封面图片
            if filename.endswith('.jpg'):
                cursor.execute(
                    "UPDATE books SET book_img = %s WHERE book_id = %s",
                    (filepath, book_id)
                )

            # 处理图文标注
            elif filename == '图文标注.xlsx':
                process_ebook_images(cursor, filepath, book_id)

            # 处理页码表
            elif filename == 'lesson_data.xlsx':
                process_lesson_data(cursor, filepath, book_id)

            # 处理下载资源
            elif filename == '下载资源':
                process_resources(cursor, filepath, book_id)

        conn.commit()
        print(f"✅ 成功导入: {book_name}")
    except Exception as e:
        conn.rollback()
        print(f"❌ 导入失败: {book_name} - {e}")
    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    base_path = r'G:\数据\口袋开言-英语书'

    # 使用线程池并行处理
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = []
        for version_name in os.listdir(base_path):
            version_path = os.path.join(base_path, version_name)
            if not os.path.isdir(version_path):
                continue

            print(f"🔍 处理版本: {version_name}")
            for book_name in os.listdir(version_path):
                book_path = os.path.join(version_path, book_name)
                if os.path.isdir(book_path):
                    futures.append(
                        executor.submit(
                            process_book,
                            version_name,
                            book_name,
                            book_path
                        )
                    )

        # 等待所有任务完成
        for future in futures:
            try:
                future.result()
            except Exception as e:
                print(f"❌ 线程执行出错: {e}")

    print("🎉 所有书籍处理完成！")
