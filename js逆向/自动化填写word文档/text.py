import os

fr = r'C:\Users\lenovo\PycharmProjects\爬虫开发\脚本开发\自动化填写word文档\SHJCTGHC2023（7）001.docx'

if os.path.exists(fr):
    print("文件存在")
else:
    print(f"文件不存在: {fr}")
