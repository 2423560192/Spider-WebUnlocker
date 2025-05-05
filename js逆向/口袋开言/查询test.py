import pymysql

mysql_config = {
    "host": "localhost",
    "user": "root",
    "password": "5201314",
    "database": "danci",
    "port": 3306,
    "charset": "utf8mb4"
}


def fetch_books_by_version(version_name):
    conn = pymysql.connect(**mysql_config)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT b.book_id, b.book_name
        FROM books b
        JOIN versions v ON b.version_id = v.version_id
        WHERE v.version_name LIKE %s
    """, ("%" + version_name + "%",))

    books = cursor.fetchall()
    conn.close()
    return books


def fetch_words_by_book(book_id):
    conn = pymysql.connect(**mysql_config)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT v.word, v.chinese, v.phonetic
        FROM vocabulary v
        JOIN units u ON v.unit_id = u.unit_id
        WHERE u.book_id = %s
    """, (book_id,))

    words = cursor.fetchall()
    conn.close()
    return words


def main(version_name):
    # 1. 查询版本对应的书籍
    books = fetch_books_by_version(version_name)

    if books:
        print(f"查询到版本 '{version_name}' 对应的书籍：")
        for book_id, book_name in books:
            print(f"- {book_name} (ID: {book_id})")

            # 2. 根据书籍ID查询对应的单词
            words = fetch_words_by_book(book_id)
            if words:
                print(f"  对应的单词：")
                for word, chinese, phonetic in words:
                    print(f"    - {word} (中文: {chinese}, 音标: {phonetic})")
            else:
                print("  没有查询到单词数据")
    else:
        print(f"没有找到与版本 '{version_name}' 相关的书籍")


# 调用示例
version_name = '重庆大学版高中'
main(version_name)
