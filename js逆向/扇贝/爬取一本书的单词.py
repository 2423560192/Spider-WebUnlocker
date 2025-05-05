import json
import requests
import execjs
from jsonpath_ng import parse
import pandas as pd

# 请求配置
cookies = {
    'csrftoken': '3a542f00ba861b6065685e957629c2bb',
    '_ga': 'GA1.2.309656701.1736329418',
    'auth_token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MjMyOTQ1NzY3LCJleHAiOjE3NTA1NzI0NjIsImV4cF92MiI6MTc1MDU3MjQ2MiwiZGV2aWNlIjoiIiwidXNlcm5hbWUiOiJXZWNoYXRfOWU1ZWVjZWEwMzdjZjYwYSIsImlzX3N0YWZmIjowLCJzZXNzaW9uX2lkIjoiNGMyNWI4ZWMwODc2MTFmMGFmNDk2YWFkMzY0YzQwOTcifQ.jL63j_Hpg86-owiuA2e2PTSrcIL8O63Q2IXSHvF_Leg',
    'tfstk': 'gJBmXMOENsRbgU_KkaJb9v_j1ANJVm96yNH9WdLaaU8SksF1bFoGWaE_cjIwSNbJPqLv6PTZ7wQ9utJqHNANRGOqBSN_jAvfesH9kr9GbwpgJyeLpisX1dzLJpGqDmpXjn-ZQVpyzhpM0N0fFfsXCdz8HmW3Ii_EScv5gdrkUhxtudR2g3rkXHk2QERZzb-ezFJN7AkzUhxpbnRZQujyPhJw7NRqLPE2kZ_dUzlR5UIHpzb2mIYF0EjA0TyJpj1prAkNEMBw8RLoQAWkmgHU9Jk36e5BkBdlz8HDIg-GkUQULYvyt6s9jZ2m3KCPNt9AeymBiNYvTTAuU4xlEMCeVgV3qgXMoBW2ZcHB3KtN7Cf7-vKDH_AhnsZszi7po6JfXD4AqBfkO3RrjjJA9MB6TtymRUdBjZLR8JkkUCSPybleszD64lBr1fO2V3Ypvfjj3iTCOYquqXR6g3tbEuqo1fO2V3YLqucF5I-Wc8f..',
    'sensorsdata2015jssdkcross': '%7B%22distinct_id%22%3A%22dxvtjy%22%2C%22first_id%22%3A%22194454c574a22-0a87ba47ca3cef-26011851-1638720-194454c574b1f41%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E5%BC%95%E8%8D%90%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC%22%2C%22%24latest_referrer%22%3A%22https%3A%2F%2Fwww.52pojie.cn%2F%22%2C%22%24latest_referrer_host%22%3A%22www.52pojie.cn%22%7D%2C%22%24device_id%22%3A%22194454c574a22-0a87ba47ca3cef-26011851-1638720-194454c574b1f41%22%7D',
}

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cache-control': 'no-cache',
    'origin': 'https://web.shanbay.com',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://web.shanbay.com/',
    'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
    'x-csrftoken': '3a542f00ba861b6065685e957629c2bb',
}

base_url = "https://apiv3.shanbay.com/wordsapp/user_material_books/arryq/learning/words/unlearned_items"

# 加载 JavaScript 解密代码
js_code = execjs.compile(open('webpack_js.js', 'r', encoding='utf-8').read())


# 抓取数据函数
def fetch_data(start_page, end_page, items_per_page=10):
    """
    从 API 抓取多页数据并解密。

    参数:
    start_page (int): 开始页码
    end_page (int): 结束页码
    items_per_page (int): 每页条目数，默认为 10

    返回:
    list: 所有页的解密后的 JSON 数据列表
    """
    all_data = []

    for page in range(start_page, end_page + 1):
        print(f"正在抓取第 {page} 页...")
        params = {
            'ipp': str(items_per_page),
            'page': str(page),
        }

        try:
            response = requests.get(base_url, params=params, cookies=cookies, headers=headers)
            response.raise_for_status()
            encrypted_data = response.json()['data']
            decrypted_data = js_code.call('f', encrypted_data)
            all_data.append(json.loads(decrypted_data))
            print(f"第 {page} 页抓取成功")
        except requests.RequestException as e:
            print(f"请求第 {page} 页失败: {e}")
        except json.JSONDecodeError as e:
            print(f"解密第 {page} 页 JSON 失败: {e}")
        except Exception as e:
            print(f"抓取第 {page} 页时发生未知错误: {e}")

    return all_data


# 解析数据函数
def parse_data(data_list):
    """
    解析多页 JSON 数据，提取单词、意思和词性。

    参数:
    data_list (list): 包含多页 JSON 数据的列表

    返回:
    list: 解析后的结果列表，每个元素包含单词、意思和词性
    """
    all_results = []

    for page_data in data_list:
        # 定义 JSONPath 表达式
        word_expr = parse('$.objects[*].vocab_with_senses.word')
        definition_expr = parse('$.objects[*].vocab_with_senses.senses[*].definition_cn')
        pos_expr = parse('$.objects[*].vocab_with_senses.senses[*].pos')

        # 提取数据
        words = [match.value for match in word_expr.find(page_data)]
        definitions = [match.value for match in definition_expr.find(page_data)]
        pos_list = [match.value for match in pos_expr.find(page_data)]

        # 构建结果
        index = 0
        for i, word in enumerate(words):
            num_senses = len(page_data['objects'][i]['vocab_with_senses']['senses'])
            for j in range(num_senses):
                all_results.append({
                    "单词": word,
                    "意思": definitions[index],
                    "词性": pos_list[index]
                })
                index += 1

    return all_results


# 保存数据函数
def save_data(results, output_file="vocabulary_all_pages.xlsx"):
    """
    将解析结果保存到 Excel 文件。

    参数:
    results (list): 解析后的结果列表
    output_file (str): 输出 Excel 文件名，默认为 "vocabulary_all_pages.xlsx"
    """
    if results:
        df = pd.DataFrame(results)
        df.to_excel(output_file, index=False, engine='openpyxl')
        print(f"数据已保存到 {output_file}，共 {len(results)} 条记录")
    else:
        print("没有数据可保存")


# 主函数：整合抓取、解析和保存
def fetch_and_save_vocab(start_page, end_page, items_per_page=10, output_file="vocabulary_all_pages.xlsx"):
    """
    主函数：抓取、解析并保存多页词汇数据。

    参数:
    start_page (int): 开始页码
    end_page (int): 结束页码
    items_per_page (int): 每页条目数，默认为 10
    output_file (str): 输出 Excel 文件名，默认为 "vocabulary_all_pages.xlsx"
    """
    # 抓取数据
    data_list = fetch_data(start_page, end_page, items_per_page)

    # 解析数据
    results = parse_data(data_list)

    # 保存数据
    save_data(results, output_file)


# 示例用法
if __name__ == "__main__":
    start_page = 1
    end_page = 5  # 假设有 5 页数据
    fetch_and_save_vocab(start_page, end_page, items_per_page=10)
