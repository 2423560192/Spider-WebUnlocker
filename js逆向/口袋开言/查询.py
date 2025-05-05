import tkinter as tk
from tkinter import ttk
import pymysql

# 数据库连接配置
mysql_config = {
    "host": "120.26.141.132",
    "user": "base_word",
    "password": "Y88yMfw8h84nhad7",
    "database": "base_word",
    "port": 3306,
    "charset": "utf8mb4"
}

# 查询书籍
def fetch_books_by_version(version_name):
    conn = pymysql.connect(**mysql_config)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT b.book_id, b.book_name
        FROM books b
        JOIN versions v ON b.version_id = v.version_id
        WHERE v.version_name LIKE %s
    """, ("%" + version_name + "%",))
    results = cursor.fetchall()
    conn.close()
    print("Fetched books for version_name", version_name, ":", results)  # Debugging
    return results

# 查询词汇
def fetch_words_by_book(book_id):
    conn = pymysql.connect(**mysql_config)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT u.unit_name, v.word, v.phonetic, v.chinese
        FROM vocabulary v
        JOIN units u ON v.unit_id = u.unit_id
        WHERE u.book_id = %s
        ORDER BY u.unit_id
    """, (book_id,))
    results = cursor.fetchall()
    conn.close()
    print("Fetched words for book_id", book_id, ":", results)  # Debugging
    return results

# 查询页码
def fetch_pages_by_book(book_id):
    conn = pymysql.connect(**mysql_config)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT unit_name, page_number
        FROM unit_ebook_pages
        WHERE book_id = %s
    """, (book_id,))
    results = cursor.fetchall()
    conn.close()
    return results

# 图文标注
def fetch_ebook_images(book_id):
    conn = pymysql.connect(**mysql_config)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT page_number, image_path, chinese_text, axis_x, axis_y, axis_width, axis_height
        FROM ebook_images
        WHERE img_book_id = %s
    """, (book_id,))
    results = cursor.fetchall()
    conn.close()
    return results

# 资源信息
def fetch_resources_by_book(book_id):
    conn = pymysql.connect(**mysql_config)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT type, resource_name, file_path
        FROM book_resources
        WHERE book_id = %s
    """, (book_id,))
    results = cursor.fetchall()
    conn.close()
    return results

# 主窗口类
class WordApp:
    def __init__(self, root):
        self.root = root
        self.root.title("📚 口袋英语数据可视化")
        self.root.geometry("1000x700")

        # 搜索栏
        search_frame = ttk.Frame(root)
        search_frame.pack(pady=10)

        ttk.Label(search_frame, text="🔍 输入版本名:").pack(side=tk.LEFT, padx=5)
        self.search_entry = ttk.Entry(search_frame, width=40)
        self.search_entry.pack(side=tk.LEFT)

        ttk.Button(search_frame, text="查询", command=self.search_books).pack(side=tk.LEFT, padx=5)

        # 书籍列表
        self.book_listbox = tk.Listbox(root, height=5, font=("微软雅黑", 11))
        self.book_listbox.pack(fill=tk.X, padx=20, pady=5)
        self.book_listbox.bind("<<ListboxSelect>>", self.on_book_select)

        # 标签页
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        self.word_tab = self.create_tab("📘 单词")
        self.page_tab = self.create_tab("📖 页码")
        self.image_tab = self.create_tab("🖼 图文标注")
        self.resource_tab = self.create_tab("📦 资源")

        self.book_id_map = {}

    def create_tab(self, title):
        frame = ttk.Frame(self.notebook)
        text = tk.Text(frame, wrap=tk.WORD, font=("微软雅黑", 11))
        text.pack(fill=tk.BOTH, expand=True)
        self.notebook.add(frame, text=title)
        return text

    def search_books(self):
        version_name = self.search_entry.get()
        books = fetch_books_by_version(version_name)
        self.book_listbox.delete(0, tk.END)
        self.book_id_map.clear()

        for book_id, book_name in books:
            self.book_listbox.insert(tk.END, book_name)
            self.book_id_map[book_name] = book_id

    def on_book_select(self, event):
        selection = self.book_listbox.curselection()
        if not selection:
            return

        book_name = self.book_listbox.get(selection[0])
        book_id = self.book_id_map[book_name]

        # Debugging Output
        print("Selected Book:", book_name, "with book_id:", book_id)

        self.display_words(book_id)
        self.display_pages(book_id)
        self.display_images(book_id)
        self.display_resources(book_id)

    def display_words(self, book_id):
        words = fetch_words_by_book(book_id)
        self.word_tab.delete(1.0, tk.END)

        if not words:  # If no words are found
            self.word_tab.insert(tk.END, "没有找到单词数据！")
            return

        current_unit = ""
        for unit, word, phonetic, chinese in words:
            if unit != current_unit:
                self.word_tab.insert(tk.END, f"\n📂【{unit}】\n", "bold")
                current_unit = unit
            line = f" - {word} [{phonetic or ''}]：{chinese}\n"
            self.word_tab.insert(tk.END, line)

    def display_pages(self, book_id):
        pages = fetch_pages_by_book(book_id)
        self.page_tab.delete(1.0, tk.END)
        for unit, page in pages:
            self.page_tab.insert(tk.END, f"{unit} ➤ 第 {page} 页\n")

    def display_images(self, book_id):
        imgs = fetch_ebook_images(book_id)
        self.image_tab.delete(1.0, tk.END)
        for page, en, zh, x, y, w, h in imgs:
            self.image_tab.insert(tk.END, f"📄 页码 {page}: {en} / {zh} ⤵️ 坐标({x},{y},{w},{h})\n")

    def display_resources(self, book_id):
        resources = fetch_resources_by_book(book_id)
        self.resource_tab.delete(1.0, tk.END)
        grouped = {}
        for type_, name, path in resources:
            grouped.setdefault(type_, []).append((name, path))

        for type_, files in grouped.items():
            self.resource_tab.insert(tk.END, f"\n📁【{type_}】\n", "bold")
            for name, path in files:
                self.resource_tab.insert(tk.END, f" - {name} ({path})\n")


# 启动程序
if __name__ == "__main__":
    root = tk.Tk()
    app = WordApp(root)
    root.mainloop()
