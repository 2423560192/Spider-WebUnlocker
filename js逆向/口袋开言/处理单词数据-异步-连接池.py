import os
import math
import pandas as pd
import pymysql
import traceback
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime


# 日志记录
def log(msg):
    with open('import_log.txt', 'a', encoding='utf-8') as f:
        f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}\n")
    print(msg)


# 数据库配置
mysql_config = {
    "host": "localhost",
    "user": "root",
    "password": "5201314",
    "database": "danci",
    "port": 3306,
    "charset": "utf8mb4"
}


def clean_value(val):
    if val is None or (isinstance(val, float) and math.isnan(val)):
        return None
    return val


def clean_number(val):
    try:
        return int(val) if val is not None else None
    except:
        return None


def process_book(version_name, book_name, book_path):
    try:
        conn = pymysql.connect(**mysql_config)
        cursor = conn.cursor()

        grade = '无'
        if '初中' in version_name and '鲁教初中' not in version_name:
            grade = '初中'
        elif '高中' in version_name:
            grade = '高中'
        else:
            grade = '小学'

        try:
            cursor.execute("INSERT IGNORE INTO versions (version_name , grade) VALUES (%s , %s)", (version_name, grade))
            conn.commit()
        except Exception as e:
            log(f"❌ 插入版本失败: {version_name}, 错误: {e}")

        cursor.execute("SELECT version_id FROM versions WHERE version_name = %s", (version_name,))
        version_result = cursor.fetchone()
        if not version_result:
            log(f"❌ 无法找到版本ID: {version_name}")
            return
        version_id = version_result[0]

        cursor.execute("INSERT IGNORE INTO books (book_name, version_id) VALUES (%s, %s)", (book_name, version_id))
        conn.commit()

        cursor.execute("SELECT book_id FROM books WHERE book_name = %s", (book_name,))
        book_result = cursor.fetchone()
        if not book_result:
            log(f"❌ 无法找到书本ID: {book_name}")
            return
        book_id = book_result[0]

        for filename in os.listdir(book_path):

            filepath = os.path.join(book_path, filename)
            unit_name = os.path.splitext(filename)[0]

            if filename.endswith('.jpg'):
                cursor.execute("UPDATE books SET book_img = %s WHERE book_id = %s", (filepath, book_id))
                conn.commit()

            elif filename == '图文标注.xlsx':
                try:
                    df = pd.read_excel(filepath).where(pd.notnull(pd.read_excel(filepath)), None)
                    for _, row in df.iterrows():
                        try:
                            cursor.execute("""
                                INSERT INTO ebook_images
                                (page_number, image_path, sound_path, english_text, chinese_text, axis_x, axis_y, axis_width, axis_height, img_book_id)
                                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                            """, (
                                clean_number(row.get('page_number')),
                                clean_value(row.get('image_path', '')).replace('ciyuankoudai', 'danci'),
                                clean_value(row.get('sound_path')),
                                clean_value(row.get('english_text')),
                                clean_value(row.get('chinese_text')),
                                clean_number(row.get('axis_x')),
                                clean_number(row.get('axis_y')),
                                clean_number(row.get('axis_width')),
                                clean_number(row.get('axis_height')),
                                book_id
                            ))
                        except Exception as e:
                            log(f"❌ 图文标注插入失败: {e} 数据: {row.to_dict()}")
                    conn.commit()
                except Exception as e:
                    log(f"⚠️ 读取图文标注失败: {filename} - {e}")

            elif filename == 'lesson_data.xlsx':
                try:
                    df = pd.read_excel(filepath).where(pd.notnull(pd.read_excel(filepath)), None)
                    for _, row in df.iterrows():
                        unit_name = clean_value(row.get('Name'))
                        page_number = clean_number(row.get('Page'))
                        if unit_name and page_number:
                            try:
                                cursor.execute("""
                                    INSERT INTO unit_ebook_pages (book_id, unit_name, page_number)
                                    VALUES (%s, %s, %s)
                                """, (book_id, unit_name, page_number))
                            except Exception as e:
                                log(f"📘 页码插入失败：{e} - {row.to_dict()}")
                    conn.commit()
                except Exception as e:
                    log(f"⚠️ 页码表读取失败: {filename} - {e}")

            elif filename == '下载资源':
                for dirpath, _, filenames in os.walk(filepath):
                    for fname in filenames:
                        file_path = os.path.join(dirpath, fname).replace('\\', '/')
                        relative_path = os.path.relpath(file_path, filepath).replace('\\', '/')
                        type_name = relative_path.split('/')[0] if '/' in relative_path else '其他'
                        try:
                            cursor.execute("""
                                INSERT INTO book_resources (book_id, resource_name, file_path, type)
                                VALUES (%s, %s, %s, %s)
                            """, (book_id, fname, file_path, type_name))
                        except Exception as e:
                            log(f"❌ 资源插入失败: {fname} - {e}")
                conn.commit()

            elif filename not in ['lesson_data.xlsx', '图文标注.xlsx', '下载资源', '英语电子书图片']:
                try:
                    df = pd.read_excel(filepath).where(pd.notnull(pd.read_excel(filepath)), None)
                    cursor.execute("INSERT INTO units (unit_name, book_id) VALUES (%s, %s)", (unit_name, book_id))
                    conn.commit()
                    unit_id = cursor.lastrowid
                    for _, row in df.iterrows():
                        try:
                            cursor.execute("""
                                INSERT INTO vocabulary (word, chinese, phonetic, unit_id)
                                VALUES (%s, %s, %s, %s)
                            """, (
                                row['Word'],
                                row['Chinese'],
                                row.get('Phonetic'),
                                unit_id
                            ))
                        except Exception as e:
                            log(f"⚠️ 词汇插入失败: {e} - {row.to_dict()}")
                    conn.commit()
                except Exception as e:
                    log(f"⚠️ 单元词汇解析失败: {filename} - {e}")

        cursor.close()
        conn.close()
        log(f"🎉 完成导入: {book_name}")

    except Exception as e:
        log(f"💥 全局错误（{book_name}）: {traceback.format_exc()}")


if __name__ == "__main__":
    base_path = r'G:\数据\口袋开言'
    with ThreadPoolExecutor(max_workers=5) as executor:
        for version_name in os.listdir(base_path):
            version_path = os.path.join(base_path, version_name)
            for book_name in os.listdir(version_path):
                book_path = os.path.join(version_path, book_name)
                executor.submit(process_book, version_name, book_name, book_path)
