import configparser
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.messagebox import showerror
import pymysql
from PIL import Image, ImageDraw, ImageFont, ImageTk
from dbutils.pooled_db import PooledDB
import threading
import pandas as pd

# 导入链接模块
from link2_all import link2_main
from link2_thead import link2_main
from link3 import link3_main
from link1 import link1_main
from link1_deep import link1_deep_main
from link2_deep_thead import link2_deep_main
from link3_deep import link3_deep_main


class GoodsApp:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1400x800")
        self.root.title("High-throughput Reagent Management System V1.0.0")
        self.root.configure(bg="#FFFFFF")
        self.db_pool = self._init_db_pool()

        # 创建进度条并隐藏
        self.progress = ttk.Progressbar(self.root, mode="indeterminate", length=200)
        self.progress.pack_forget()  # 初始时隐藏进度条
        # 当前页面
        self.current_frame = None

        # 当前查询关键字
        self.query = None
        # 所有数据
        self.all_rows = None

        self._apply_styles()
        self._create_widgets()

        # 获取配置文件
        config = configparser.RawConfigParser()
        with open('utils/conf.ini', 'r', encoding='utf-8') as f:
            config.read_file(f)
        self.config = config

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
        self._show_page(self._create_index_page)  # 加载首页

    def _create_top_frame(self):
        """创建顶部搜索框。"""
        frame = tk.Frame(self.root, bg="#ffffff")
        frame.pack(fill=tk.X, padx=10, pady=5)

        # 加载并显示Logo图像
        try:
            logo_img = Image.open("logo.png")  # 替换为你的 logo 文件路径
            logo_img = logo_img.resize((110, 110))  # 调整为适当大小
            logo_tk = ImageTk.PhotoImage(logo_img)
            logo_label = tk.Label(frame, image=logo_tk, bg="#ffffff")
            logo_label.image = logo_tk  # 保持引用
            logo_label.pack(side=tk.LEFT, padx=5)

            title_label = tk.Label(frame, text="DNL2900", font=("Arial", 24, "bold"), bg="white", fg="#0078d7")
            title_label.pack(side="left")

        except Exception as e:
            print(f"Logo加载失败：{e}")

        tk.Label(frame, text="🔍", bg="#ffffff", font=("Arial", 15), fg='#0078d7').pack(side=tk.LEFT, padx=5)
        self.search_entry = ttk.Entry(frame, font=("Arial", 14), width=30)
        self.search_entry.pack(side=tk.LEFT, padx=5, pady=5)

        # 普通搜索按钮
        tk.Button(frame, text="Search", command=self._search_goods, bg="#0078d7",  # 背景颜色为蓝色
                  fg="#ffffff", font=("Arial", 10, 'bold'), relief="groove", width=12).pack(side=tk.LEFT, padx=10,
                                                                                            pady=5)

        # 深度搜索按钮
        tk.Button(frame, text="Deep Search", command=self._deep_search_goods, bg="#0078d7",  # 背景颜色为蓝色
                  fg="#ffffff", font=("Arial", 10, 'bold'), relief="groove", width=12).pack(side=tk.LEFT, padx=10,
                                                                                            pady=5)

        # Excel筛选按钮
        tk.Button(frame, text="Specific Search", command=self._search_excle_goods, bg="#0078d7",  # 背景颜色为蓝色
                  fg="#ffffff", font=("Arial", 10, 'bold'), relief="groove", width=12).pack(side=tk.LEFT, padx=10,
                                                                                            pady=5)

        # DFT按钮，设置背景颜色为蓝色，字体白色
        tk.Button(frame, text="DFT", command=self.show_dft, bg="#0078d7",
                  fg="#ffffff", font=("Arial", 10, 'bold'), relief="groove", width=12).pack(side=tk.LEFT, padx=10,
                                                                                            pady=5)

        # MD按钮，设置背景颜色为蓝色，字体白色
        tk.Button(frame, text="MD", command=self.show_md, bg="#0078d7",
                  fg="#ffffff", font=("Arial", 10, 'bold'), relief="groove", width=12).pack(side=tk.LEFT, padx=10,
                                                                                            pady=5)

        # 导出按钮
        tk.Button(frame, text="Export", command=self.export_to_excel, bg="#0078d7",
                  fg="#ffffff", font=("Arial", 10, 'bold'), relief="groove", width=12).pack(side=tk.LEFT, padx=10,
                                                                                            pady=5)

    def export_to_excel(self):
        """将完整数据导出到 Excel 文件。"""
        try:
            # 使用保存的完整数据（例如：self.all_rows）
            rows = self.all_rows
            if not rows:
                messagebox.showwarning("警告", "没有可导出的数据")
                return

            # 将数据转换为 DataFrame
            # columns = ["ID", "名称", "CAS号", "国药编码", "规格", "价格", "库存", "纯度/说明", "分子量", "来源"]
            columns = ["Product", "CAS", "CMN", "Specification", "Price", "inventory", "Purity", "Mol.wt.",
                       "Source"]
            lst = []
            for row in rows:
                lst.append(row[1:])
            df = pd.DataFrame(lst, columns=columns)

            # 将 DataFrame 写入 Excel 文件
            file_name = f"{self.query}.xlsx"
            df.to_excel(file_name, index=False)
            # 使用 messagebox 显示成功信息
            messagebox.showinfo("成功", f"数据已导出到 {file_name}")

        except Exception as e:
            messagebox.showerror("错误", f"导出失败：{e}")

    def _show_page(self, create_page_func):
        """切换到指定的页面"""
        if self.current_frame:
            self.current_frame.destroy()  # 销毁当前页面

        self.current_frame = create_page_func()  # 创建新的页面
        self.current_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def _create_index_page(self):
        """创建首页"""
        frame = tk.Frame(self.root, bg="#f5f5f5")

        # # 添加图片并使其填满整个frame
        # imgs = Image.open("bg.png")  # 替换为你的图片路径
        #
        # # 获取frame的大小
        # def resize_image(event):
        #     # 获取frame的新宽高
        #     width, height = event.width, event.height
        #     # 调整图片大小以适应frame
        #     img_resized = imgs.resize((width, height))
        #     img_tk = ImageTk.PhotoImage(img_resized)
        #     image_label.config(image=img_tk)
        #     image_label.image = img_tk  # 保持对图片的引用
        #
        # # 创建一个Label显示图片
        # image_label = tk.Label(frame, bg="#f5f5f5")
        # image_label.pack(fill=tk.BOTH, expand=True)
        #
        # # 绑定frame尺寸变化事件来动态调整图片大小
        # frame.bind("<Configure>", resize_image)

        return frame

    def show_md(self):
        """使用_show_page切换到文本展示页面"""
        self._show_page(self._create_md_page)

    def show_dft(self):
        """使用_show_page切换到文本展示页面"""
        self._show_page(self._create_dft_page)

    def _create_dft_page(self):
        frame = tk.Frame(self.root, bg="#f5f5f5")

        # 创建一个 Canvas 用于支持滚动
        canvas = tk.Canvas(frame)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # 创建一个滚动条并与 Canvas 绑定
        scrollbar = tk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill="y")
        canvas.configure(yscrollcommand=scrollbar.set)

        # 创建一个 Frame 用于将内容放置在 Canvas 上
        content_frame = tk.Frame(canvas)
        canvas.create_window((0, 0), window=content_frame, anchor="nw")

        # 读取 1.txt 文件内容
        try:
            with open('1.txt', 'r', encoding='utf-8') as file:
                md_text = file.read()
        except Exception as e:
            messagebox.showerror("错误", f"读取文件失败：{e}")
            return

        # 打开并调整图片大小
        try:
            img = Image.open('huaxue.png')  # 请确保 huaxue.png 文件存在

            # 设置图片的最大宽度和最大高度
            max_width, max_height = 400, 400  # 根据需要调整最大尺寸

            # 使用 thumbnail 方法调整图片大小，保持比例
            img.thumbnail((max_width, max_height))

            # 将调整后的图片转换为 Tkinter 可用格式
            img_tk = ImageTk.PhotoImage(img)

            # 显示图片
            img_label = tk.Label(content_frame, image=img_tk)
            img_label.image = img_tk  # 保存图片引用
            img_label.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=10)
        except Exception as e:
            messagebox.showerror("错误", f"图片加载失败：{e}")

        # 使用 Text 小部件显示文本，并去掉边框
        text_widget = tk.Text(content_frame, wrap=tk.WORD, font=("Arial", 12), bg="#f5f5f5", bd=0,
                              highlightthickness=0, height=100)
        text_widget.insert(tk.END, md_text)
        text_widget.config(state=tk.DISABLED)  # 设置为只读，用户可以复制但不能编辑
        text_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=10)

        # 更新 Canvas 的 scrollregion，以确保可以滚动
        content_frame.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))

        # 绑定鼠标滚轮事件
        def on_mouse_wheel(event):
            # Windows 系统中滚动事件是 MouseWheel
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        # 绑定滚轮事件
        canvas.bind_all("<MouseWheel>", on_mouse_wheel)

        frame.pack(fill=tk.BOTH, expand=True)
        return frame

    def _create_md_page(self):
        """创建一个页面来展示文本信息和图片，并且支持滚动"""
        frame = tk.Frame(self.root, bg="#f5f5f5")

        # 创建一个 Canvas 用于支持滚动
        canvas = tk.Canvas(frame)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # 创建一个 Frame 用于将内容放置在 Canvas 上
        content_frame = tk.Frame(canvas)
        canvas.create_window((0, 0), window=content_frame, anchor="nw")
        # 打开并调整图片大小
        img = Image.open('zhengfangti.png')  # 请确保 huaxue.png 文件存在

        # 设置图片的最大宽度和最大高度
        max_width, max_height = 400, 400  # 根据需要调整最大尺寸

        # 使用 thumbnail 方法调整图片大小，保持比例
        img.thumbnail((max_width, max_height))

        # 将调整后的图片转换为 Tkinter 可用格式
        img_tk = ImageTk.PhotoImage(img)

        # 显示图片
        img_label = tk.Label(content_frame, image=img_tk)
        img_label.image = img_tk  # 保存图片引用
        img_label.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=10)

        # 添加三个一模一样的输入框和加减按钮
        for _ in range(3):
            self._add_input_field(content_frame)

        # 添加 Add 和 Remove 按钮在所有输入框的下方，并且居中显示
        btn_frame = tk.Frame(content_frame)  # 创建一个新的 Frame 来包含按钮
        btn_frame.pack(side=tk.TOP, pady=10)

        btn_add = tk.Button(btn_frame, text="Add", font=("Arial", 12), width=6, height=1, )
        btn_add.pack(side=tk.LEFT, padx=5)

        btn_remove = tk.Button(btn_frame, text="Remove", font=("Arial", 12), width=6, height=1, )
        btn_remove.pack(side=tk.LEFT, padx=5)

        # 更新 Canvas 的 scrollregion，以确保可以滚动
        content_frame.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))

        return frame

    def _add_input_field(self, parent_frame):
        """添加输入框和加减按钮"""
        # 创建一个框架用于输入框和按钮的水平排列
        input_frame = tk.Frame(parent_frame)
        input_frame.pack(side=tk.TOP, pady=5)

        # 创建输入框
        entry = tk.Entry(input_frame, font=("Arial", 14), width=15)
        entry.pack(side=tk.LEFT, padx=10)  # 使用 pack 布局，放置在左边

        # 创建加减按钮
        btn_add = tk.Button(input_frame, text="+1", font=("Arial", 12), width=3, height=1,
                            command=lambda: self.change_value(entry, 1))
        btn_add.pack(side=tk.RIGHT, padx=5)  # 加号按钮放在输入框右侧

        btn_subtract = tk.Button(input_frame, text="-1", font=("Arial", 12), width=3, height=1,
                                 command=lambda: self.change_value(entry, -1))
        btn_subtract.pack(side=tk.LEFT, padx=5)  # 减号按钮放在输入框右侧

    def change_value(self, entry, delta):
        """改变输入框的值"""
        current_value = entry.get()
        if current_value.isdigit():
            entry.delete(0, tk.END)
            entry.insert(0, str(int(current_value) + delta))
        else:
            entry.delete(0, tk.END)
            entry.insert(0, str(delta))

    def _create_home_page(self):
        """创建首页"""
        frame = tk.Frame(self.root, bg="#f5f5f5")

        # 在这里重新创建 Treeview
        columns = ("id", "name", "cas", "erp_code", "spec", "price", "stock", "purity", "molecular_weight", "source")
        self.tree = ttk.Treeview(frame, columns=columns, show="headings", height=20)  # 设置高度为20行

        # headings = {
        #     "id": "ID", "name": "名称", "cas": "CAS号", "erp_code": "国药编码",
        #     "spec": "规格", "price": "价格", "stock": "库存",
        #     "purity": "纯度/说明", "molecular_weight": "分子量", "source": '来源'
        # }
        headings = {
            "id": "ID", "name": "Product", "cas": "CAS", "erp_code": "CMN",
            "spec": "Specification", "price": "Price", "stock": "Inventory",
            "purity": "Purity", "molecular_weight": "Mol.wt.", "source": "Source"
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

        return frame

    def _search_goods(self):
        """根据用户输入进行普通搜索。"""
        self._show_page(self._create_home_page)  # 加载首页
        query = self.search_entry.get().strip()
        self.query = query
        if query:
            threading.Thread(target=self._perform_search, args=(query,), daemon=True).start()

    def _search_excle_goods(self):
        self._show_page(self._create_home_page)  # 加载首页
        """根据excle进行筛选搜索。"""
        query = self.search_entry.get().strip()
        self.query = query
        if query:
            threading.Thread(target=self._perform_excel_search, args=(query,), daemon=True).start()

    def _deep_search_goods(self):
        self._show_page(self._create_home_page)  # 加载首页
        """进行深度搜索，调用更多的搜索源和方法。"""
        query = self.search_entry.get().strip()
        self.query = query
        if query:
            threading.Thread(target=self._perform_deep_search, args=(query,), daemon=True).start()

    def filter_excel(self, rows, names, cass):
        """根据excle筛选"""

        def judge_in(name, lst):
            for i in lst:
                if i in name:
                    return True
            return False

        lst = []
        for row in rows:
            if judge_in(row[1], names) or row[2] in cass:
                lst.append(row)

        return lst

    def _perform_search(self, query):
        """执行普通搜索的数据库查询并更新UI"""
        try:
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

            if not rows:
                print("深度搜索中......")
                print("网站1搜索中......")
                link1_main(query)
                print("网站2搜索中......")
                link2_main(query)
                print("网站3搜索中......")
                link3_main(query)

                # 再次查询数据库
                cursor.execute(sql, (f"%{query}%",))
                rows = cursor.fetchall()
            self.all_rows = rows

            cursor.close()
            conn.close()

            self.root.after(0, self._update_table, rows)

        except Exception as e:
            self.root.after(0, showerror, "错误", f"搜索失败：{e}")

        finally:
            self.root.after(0, self.progress.pack_forget)
            self.progress.stop()

    def _perform_deep_search(self, query):
        """执行深度搜索，除了数据库还可以调用其他资源"""
        try:
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
            print("深度搜索中......")
            print("网站1搜索中......")
            link1_deep_main(query)
            print("网站2搜索中......")
            link2_deep_main(query)
            print("网站3搜索中......")
            link3_deep_main(query)

            # 再次查询数据库
            cursor.execute(sql, (f"%{query}%",))
            rows = cursor.fetchall()

            self.all_rows = rows

            cursor.close()
            conn.close()

            self.root.after(0, self._update_table, rows)

        except Exception as e:
            self.root.after(0, showerror, "错误", f"深度搜索失败：{e}")

        finally:
            self.root.after(0, self.progress.pack_forget)
            self.progress.stop()

    def _perform_excel_search(self, query):
        """执行筛选搜索的数据库查询并更新UI"""
        try:
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

            df = pd.read_excel(self.config['INFO']['excel_name'])
            names = df[self.config['INFO']['name']]
            cass = df[self.config['INFO']['cas']]

            st = " ".join([i[1] for i in rows])

            for i in names:
                print('正在抓取：', i)
                if i not in st:
                    # 去搜索
                    print("深度搜索中......")
                    print("网站1搜索中......")
                    link1_main(i)
                    print("网站2搜索中......")
                    link2_main(i)
                    print("网站3搜索中......")
                    link3_main(i)

            # 再次查询数据库
            cursor.execute(sql, (f"%{query}%",))
            rows = cursor.fetchall()

            lst = self.filter_excel(rows, names, cass)

            self.all_rows = lst

            cursor.close()
            conn.close()
            self.root.after(0, self._update_table, lst)

        except Exception as e:
            self.root.after(0, showerror, "错误", f"搜索失败：{e}")

        finally:
            self.root.after(0, self.progress.pack_forget)
            self.progress.stop()

    def _perform_deep_excel_search(self, query):
        """执行深度搜索，除了数据库还可以调用其他资源"""
        try:
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

            df = pd.read_excel(self.config['INFO']['excel_name'])
            names = df[self.config['INFO']['name']]
            cass = df[self.config['INFO']['cas']]

            for i in names:
                print('正在抓取：', i)
                # 去搜索
                print("深度搜索中......")
                print("网站1搜索中......")
                link1_deep_main(i)
                print("网站2搜索中......")
                link2_deep_main(i)
                print("网站3搜索中......")
                link3_deep_main(i)

            # 再次查询数据库
            cursor.execute(sql, (f"%{query}%",))
            rows = cursor.fetchall()

            lst = self.filter_excel(rows, names, cass)
            self.all_rows = lst
            cursor.close()
            conn.close()

            self.root.after(0, self._update_table, lst)

        except Exception as e:
            self.root.after(0, showerror, "错误", f"搜索失败：{e}")

        finally:
            self.root.after(0, self.progress.pack_forget)
            self.progress.stop()

    def _update_table(self, rows):
        """更新表格内容。"""
        if not hasattr(self, 'tree') or self.tree is None:
            print("Treeview 控件不存在")
            return

        lst = []
        self.tree.delete(*self.tree.get_children())
        i = 1
        rows = list(sorted(rows, key=lambda x: x[1]))  # 排序
        new_rows = []
        for row in rows:
            row = list(row)
            row[0] = i
            i += 1
            st = "".join(map(str, row[1:]))
            if st in lst:
                continue
            lst.append(st)
            new_rows.append(row)

        for row in new_rows:
            self.tree.insert("", "end", values=row)

        self._update_total_count(rows)

    def _update_total_count(self, rows):
        """更新窗口标题以显示数据总数。"""
        self.root.title(f"High-throughput Reagent Management System V1.0.0 - Total Data Strip: {len(rows)}")


if __name__ == "__main__":
    root = tk.Tk()
    app = GoodsApp(root)
    root.mainloop()
