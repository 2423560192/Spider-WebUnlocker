# API爬虫工具

## 项目简介
这个Python项目用于从特定API获取数据并提取URL。该工具模拟了微信小程序的请求，从山思未来的API获取笔记内容，并提取单词数据。

## 功能特点
- 模拟微信小程序的HTTP请求
- 自动解析API响应的JSON数据
- 从响应中提取所有URL链接
- 自动请求提取到的URL并获取JSON数据
- 提取单词数据并保存到Excel文件
- 将所有响应数据保存到本地文件

## 文件说明
- `crawler.py`: 主爬虫脚本，用于获取API数据和URL内容
- `extract_words.py`: 数据提取脚本，用于从JSON中提取单词数据

## 使用方法
1. 确保已安装Python 3.6或更高版本
2. 安装所需依赖：
   ```
   pip install requests pandas openpyxl
   ```
3. 运行爬虫脚本：
   ```
   python crawler.py
   ```
4. 运行数据提取脚本：
   ```
   python extract_words.py
   ```

## 数据输出
- `response_data.json`: 原始API响应的JSON数据
- `url_data/url_X_YYYY.json`: 每个提取出的URL的响应数据
- `单词列表.xlsx`: 提取的单词和意思列表

## 参数说明
脚本中包含以下关键参数：
- `note_id`: 要获取的笔记ID
- `business_id`: 业务ID
- `Authorization`: 授权令牌（需要定期更新）

## 注意事项
- 授权令牌可能会过期，如果请求失败，请更新headers中的Authorization值
- 该工具仅用于学习和研究目的，请遵守相关网站的使用条款
- API返回的数据格式可能会变化，如果提取失败，请检查响应内容并更新正则表达式

## 待改进功能
- 添加命令行参数支持，便于指定不同的笔记ID
- 增加代理支持，提高请求的稳定性
- 实现自动化授权令牌获取
- 添加更多数据处理和分析功能
- 增加URL过滤功能，只请求特定类型的URL 