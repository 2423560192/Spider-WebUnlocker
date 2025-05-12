import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showerror
import pymysql
from dbutils.pooled_db import PooledDB
import threading

from link2_all import link2_main
from link3 import link3_main
from link1 import link1_main


class GoodsApp:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1400x800")
        self.root.title("试剂展示")
        self.root.configure(bg="#f5f5f5")
        self.db_pool = self._init_db_pool()

        # 创建进度条并隐藏
        self.progress = ttk.Progressbar(self.root, mode="indeterminate", length=200)
        self.progress.pack_forget()  # 初始时隐藏进度条

        self._apply_styles()
        self._create_widgets()

    def _init_db_pool(self):
        """初始化数据库连接池。"""
        try:
            pool = PooledDB(
                creator=pymysql,
                maxconnections=5,
                mincached=2,
                maxcached=5,
                blocking=True,
                host="localhost",
                user="root",
                password="5201314",
                db="shiji",
                charset="utf8mb4",
            )
            print("数据库连接池初始化成功！")
            return pool
        except Exception as e:
            print(f"数据库连接池初始化失败：{e}")
            self.root.destroy()

    def _apply_styles(self):
        """应用全局样式。"""
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background="#ffffff", foreground="#000000",
                        rowheight=25, fieldbackground="#f5f5f5")
        style.map("Treeview", background=[("selected", "#a3d2ca")],
                  foreground=[("selected", "#000000")])
        style.configure("Treeview.Heading", background="#0078d7",
                        foreground="#ffffff", font=("Arial", 10, "bold"))

    def _create_widgets(self):
        """创建UI组件。"""
        self._create_top_frame()
        self._create_result_table()

    def _create_top_frame(self):
        """创建顶部搜索框。"""
        frame = tk.Frame(self.root, bg="#ffffff")
        frame.pack(fill=tk.X, padx=10, pady=5)

        tk.Label(frame, text="搜索:", bg="#ffffff", font=("Arial", 10)).pack(side=tk.LEFT, padx=5)
        self.search_entry = tk.Entry(frame, font=("Arial", 10), relief="solid")
        self.search_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)

        tk.Button(frame, text="搜索", command=self._search_goods, bg="#0078d7",
                  fg="#ffffff", font=("Arial", 10), relief="flat").pack(side=tk.LEFT, padx=5)

    def _create_result_table(self):
        """创建结果表格。"""
        frame = tk.Frame(self.root, bg="#f5f5f5")
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        columns = ("id", "name", "cas", "erp_code", "spec", "price", "stock", "purity", "molecular_weight", "source")
        self.tree = ttk.Treeview(frame, columns=columns, show="headings", height=20)  # 设置高度为20行

        headings = {
            "id": "ID", "name": "名称", "cas": "CAS号", "erp_code": "国药编码",
             "spec": "规格", "price": "价格", "stock": "库存",
            "purity": "纯度", "molecular_weight": "分子量", "source": '来源'
        }
        for col, heading in headings.items():
            self.tree.heading(col, text=heading)
            self.tree.column(col, anchor="center", width=150 if col != "id" else 50)

        # 滚动条
        vsb = ttk.Scrollbar(frame, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscroll=vsb.set, xscroll=hsb.set)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        hsb.pack(side=tk.BOTTOM, fill=tk.X)
        self.tree.pack(fill=tk.BOTH, expand=True)

    def _search_goods(self):
        """根据用户输入搜索商品。"""
        query = self.search_entry.get().strip()
        if query:
            # 启动一个新线程来执行数据库查询，避免阻塞UI线程
            threading.Thread(target=self._perform_search, args=(query,), daemon=True).start()

    def _perform_search(self, query):
        """执行数据库查询并更新UI"""
        try:
            # 显示进度条
            self.root.after(0, self.progress.pack)
            self.progress.start()

            conn = self.db_pool.connection()
            cursor = conn.cursor()
            sql = """
                SELECT 
                    id, goodsName, casIndexNo, goodsErpCode, goodsSpec, goodsStorePrice, goodsShowStorage, purity, molecularWeight, source
                FROM goods
                WHERE goodsName LIKE %s
            """
            cursor.execute(sql, (f"%{query}%",))
            rows = cursor.fetchall()

            # 如果没有找到数据，重新去获取数据
            if not rows:
                print('没有数据，正在搜索......')
                print('网站1搜索中......')
                link1_main(query , conn)
                print('网站2搜索中......')
                link2_main(query , conn)
                print('网站3搜索中......')
                link3_main(query, conn)

                # 再次查询数据库
                cursor.execute(sql, (f"%{query}%",))
                rows = cursor.fetchall()

            cursor.close()
            conn.close()

            # 在主线程中更新表格内容
            self.root.after(0, self._update_table, rows)

        except Exception as e:
            self.root.after(0, showerror, "错误", f"搜索失败：{e}")

        finally:
            # 隐藏进度条
            self.root.after(0, self.progress.pack_forget)
            self.progress.stop()

    def _update_table(self, rows):
        """更新表格内容。"""
        self.tree.delete(*self.tree.get_children())
        lst = []
        i = 1
        for row in rows:
            row = list(row)
            row[0] = i
            i += 1
            st = "".join(map(str, row[1:]))
            if st in lst:
                continue
            lst.append(st)
            self.tree.insert("", "end", values=row)
        self._update_total_count(rows)

    def _update_total_count(self, rows):
        """更新窗口标题以显示数据总数。"""
        self.root.title(f"试剂展示 - 总数据条数: {len(rows)}")


if __name__ == "__main__":
    root = tk.Tk()
    app = GoodsApp(root)
    root.mainloop()