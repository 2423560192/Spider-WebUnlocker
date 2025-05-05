import requests
import re
import json
import os


def extract_urls(text):
    """
    从文本中提取所有URL
    
    参数:
        text: 需要处理的文本内容
    返回:
        包含所有找到URL的列表
    """
    # URL正则表达式模式
    url_pattern = r'https?://[^\s()<>\"\']+|www\.[^\s()<>\"\']+\.[^\s()<>\"\']{2,}'

    # 查找所有URL
    found_urls = re.findall(url_pattern, text)
    return found_urls


def fetch_json_from_url(url, headers):
    """
    向URL发送请求并获取JSON数据
    
    参数:
        url: 需要请求的URL
        headers: 请求头
    返回:
        JSON数据(如果成功)或None(如果失败)
    """
    try:
        print(f"正在请求URL: {url}")
        # 发送GET请求到URL
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        # 尝试解析JSON
        json_data = response.json()
        return json_data
    except requests.exceptions.RequestException as e:
        print(f"请求URL失败: {e}")
        return None
    except json.JSONDecodeError:
        print(f"无法将响应解析为JSON: {url}")
        # 保存原始响应以供进一步分析
        filename = f"url_response_raw_{hash(url) & 0xffffffff}.txt"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(response.text)
            print(f"原始响应已保存到 {filename}")
        return None


def main(path, id):
    # 定义请求URL
    url = "https://admin-api.shansiweilai.com/api/note/getnote"

    # 设置请求头
    headers = {
        "Host": "admin-api.shansiweilai.com",
        "Scope": "com.dy.wordrecite.wx",
        "xweb_xhr": "1",
        "Authorization": "2245eb9ebe404d31f3c5d3c0323ceb83f4e1908e59f627e814c6166054d84b98",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090c33)XWEB/11581",
        "Content-type": "application/json;charset=UTF-8",
        "Accept": "*/*",
        "Sec-Fetch-Site": "cross-site",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://servicewechat.com/wx04555c1935d6e836/66/page-frame.html",
        "Accept-Language": "zh-CN,zh;q=0.9"
    }

    # 设置请求体数据
    data = {
        "op_path": "api.note.getnote",
        "version": -1,
        "note_id": id,
        "business_id": 104
    }
    """主函数：发送请求并提取URL"""
    try:
        # 发送POST请求
        print("正在发送请求...")
        response = requests.post(url, headers=headers, json=data)

        # 检查请求是否成功
        response.raise_for_status()

        # 解析JSON响应
        json_data = response.json()
        print(f"请求成功！状态码: {response.status_code}")

        # 将JSON数据转换为字符串以便提取URL
        json_str = json.dumps(json_data, ensure_ascii=False)

        # 提取URL
        urls = extract_urls(json_str)

        # 显示结果
        if urls:
            print(f"共找到 {len(urls)} 个URL:")

            # 创建保存URL请求结果的目录
            url_data_dir = "url_data"
            if not os.path.exists(url_data_dir):
                os.makedirs(url_data_dir)

            # 遍历并处理每个URL
            for i, url in enumerate(urls, 1):
                print(f"{i}. {url}")

                # 请求URL获取JSON数据
                # 创建一个简化版的请求头，移除一些可能导致问题的字段
                simple_headers = {
                    "User-Agent": headers["User-Agent"],
                    "Accept": headers["Accept"],
                    "Accept-Language": headers["Accept-Language"]
                }

                url_json = fetch_json_from_url(url, simple_headers)

                if url_json:
                    # 为每个URL生成唯一的文件名
                    filename = os.path.join(path, 'a.json')

                    # 保存JSON数据到文件
                    with open(filename, 'w', encoding='utf-8') as f:
                        json.dump(url_json, f, ensure_ascii=False, indent=4)
                        print(f"URL {i} 的JSON数据已保存到 {filename}")
                    return filename
        else:
            print("未找到任何URL")

    except requests.exceptions.RequestException as e:
        print(f"请求失败: {e}")
    except json.JSONDecodeError:
        print("无法解析JSON响应")
        # 如果JSON解析失败，尝试从原始文本中提取URL
        urls = extract_urls(response.text)
        if urls:
            print(f"从原始响应中找到 {len(urls)} 个URL:")
            for i, url in enumerate(urls, 1):
                print(f"{i}. {url}")
