# """
# 自动化word填写
# """
import os
import traceback

import pandas as pd
from docx import Document
from pandas import Timestamp

from doc_revert_docx import doc_to_docx
#
# 转文件格式
path=r'files'

docfiles=[]
filename=os.listdir(path)

for file in filename:
    docfile=os.path.join(path,file)
    docfiles.append(docfile)

for file in docfiles:
    try:
        if file.split('.')[-1] == 'doc':
            doc_to_docx(file)
            # 删除doc
            os.remove(file)
    except:
        continue


def find_index(lst , x):
    for i , st in enumerate(lst , 0):
        if x in st:
            return i + 1
    return None

# 输入excel名字
xl = input('请输入你的excel路径:')

xl = rf'{xl}'
# 遍历excel数据
if xl == None:
    excel_path = "工作簿1.xlsx"  # 替换为你的 Excel 文件路径
else:
    excel_path = xl
# data = pd.read_excel(excel_path, skiprows=1)  # 跳过第一行
data = pd.read_excel(excel_path)  # 跳过第一行
# data = data.iloc[:, 4:]  # 丢弃前4列
# 遍历数据并构建字典
data_dict_list = []

for index, row in data.iterrows():
    row_dict = row.to_dict()  # 将每行转换为字典
    data_dict_list.append(row_dict)  # 添加到列表中
print(data_dict_list)
# 打印每一行的字典形式
for i, row_dict in enumerate(data_dict_list):
    # print(f"第 {i} 行数据: {row_dict}")
    # 现在要处理哪张表
    text_id = str(row_dict['报告编号']).strip()
    file_path = path + '/' + text_id + '.docx'
    for k ,v in row_dict.items():
        # 打开报告
        try:
            doc = Document(file_path)
            table = doc.tables[0]
            for i, row in enumerate(table.rows):
                row_data = [cell.text.strip() for cell in row.cells]
                # 查找目标单元格并修改内容
                if k in " ".join(map(str , row_data)):
                    print(f"{k}----- {row_data}-----{v}")

                    # 获取索引并修改对应单元格的内容
                    index = find_index(row_data , k)

                    if index < len(row.cells):  # 确保索引不越界
                        if isinstance(v, Timestamp):
                            v = v.strftime('%Y-%m-%d')  # 转换为字符串，格式为 YYYY-MM-DD
                        try:
                            while row.cells[index].text != '':
                                index += 1
                            row.cells[index].text = v  # 修改内容
                        except:
                            pass
            doc.save(file_path)
        except Exception as e:
            # 获取详细的错误信息
            error_info = traceback.format_exc()

            # 输出错误信息
            # print(f"错误信息:\n{error_info}")
