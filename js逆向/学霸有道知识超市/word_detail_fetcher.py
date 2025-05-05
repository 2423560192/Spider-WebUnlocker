import requests
import json
import os
import pandas as pd
import time
from tqdm.auto import tqdm


def fetch_word_details(word):
    headers = {
        'Host': 'api.shansiweilai.com',
        'Scope': 'com.dy.wordrecite.wx',
        'xweb_xhr': '1',
        'Authorization': '7866f46214a7d8103df4b1715bbec2840c5eece513db53baedfa325cd33b0225',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090c33)XWEB/11581',
        'Content-type': 'application/json;charset=UTF-8',
        'Accept': '*/*',
        'Sec-Fetch-Site': 'cross-site',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://servicewechat.com/wx04555c1935d6e836/66/page-frame.html',
        'Accept-Language': 'zh-CN,zh;q=0.9',
    }

    json_data = {
        'op_path': 'wordrecite.chapter.wordsearch',
        'business_id': 104,
        'query': word,
        'word_bank_type': 2,
    }

    response = requests.post('https://api.shansiweilai.com/api/wordrecite/chapter/wordsearch', headers=headers,
                             json=json_data)

    return response.json()


def extract_word_data(api_data):
    """
    从API响应中提取所需的单词数据
    
    参数:
        api_data: API返回的数据
    返回:
        包含所需字段的字典
    """
    result = {}

    # 获取基本数据
    data = api_data.get("data", {})
    if not data:
        return result

    # 提取单词基本信息
    result["单词"] = data.get("word", "")
    result["音标"] = f"/{data.get('phonetic_en', '')}/"

    # 提取考试信息
    if "kao_pins" in data and isinstance(data["kao_pins"], list):
        for kao_pin_item in data["kao_pins"]:
            if isinstance(kao_pin_item, dict) and "kao_pin" in kao_pin_item:
                kao_pin = kao_pin_item["kao_pin"]
                tag = kao_pin.get("tag", "")

                if tag == "中考":
                    result["中考出现次数"] = kao_pin.get("appear_count", 0)
                    result["中考出现年数"] = kao_pin.get("recent_years", 0)
                    result["中考重要性"] = kao_pin.get("importance", 0)
                elif tag == "高考":
                    result["高考出现次数"] = kao_pin.get("appear_count", 0)
                    result["高考出现年数"] = kao_pin.get("recent_years", 0)
                    result["高考重要性"] = kao_pin.get("importance", 0)

    # 提取词义信息
    all_meanings = []
    if "meanings" in data and isinstance(data["meanings"], list):
        for meaning in data["meanings"]:
            if isinstance(meaning, dict):
                pos = meaning.get("pos", "")  # 词性
                meaning_text = meaning.get("meaning", "")  # 词义

                if pos and meaning_text:
                    all_meanings.append(f"{pos} {meaning_text}")

    result["词义"] = "\n".join(all_meanings) if all_meanings else ""
    result["常见释义"] = result["词义"]  # 复制词义作为常见释义

    # 提取拓展短语
    use_cases = []
    if "use_cases" in data and isinstance(data["use_cases"], list):
        for i, use_case in enumerate(data["use_cases"], 1):
            if isinstance(use_case, dict):
                en = use_case.get("en", "")
                zh = use_case.get("zh", "")

                if en and zh:
                    use_cases.append(f"{i}. {en} - {zh}")

    result["拓展短语"] = "\n".join(use_cases) if use_cases else ""

    # 计算频率
    zhongkao_importance = result.get("中考重要性", 0)
    gaokao_importance = result.get("高考重要性", 0)

    max_importance = max(zhongkao_importance, gaokao_importance)

    if max_importance >= 4:
        result["频率"] = "高频"
    elif max_importance >= 3:
        result["频率"] = "中频"
    elif max_importance >= 1:
        result["频率"] = "低频"
    else:
        result["频率"] = "基础"

    return result


def main2(path, file='单词列表.xlsx'):
    try:
        print("开始处理单词列表...")

        # 从Excel文件读取单词列表
        file_path = os.path.join(path, file)

        if not os.path.exists(file_path):
            print(f"错误：文件 {file_path} 不存在!")
            return

        # 读取Excel文件
        df = pd.read_excel(file_path)

        # 读取Excel文件
        df_all = pd.read_excel('总.xlsx')
        all_words = df_all['单词'].tolist()
        print(all_words)

        # 获取所有单词列
        words = df['word'].tolist()
        # 获取所有音标列
        phonetic_en = df['phonetic'].tolist()
        # 获取所有词义列
        meanings = df['meaning'].tolist()
        # 获取所有频率列
        frequency = df['frequency'].tolist()
        types = df['type'].tolist()

        # 初始化结果列表
        all_word_data = []

        # print(meanings)

        # 为每个单词获取详细信息
        print("开始获取单词详细信息...")
        print(len(words), len(phonetic_en), len(meanings), len(frequency))

        # 使用tqdm显示进度条和zip组合所有列数据
        for word, phonetic, meaning, freq, typ in tqdm(zip(words, phonetic_en, meanings, frequency, types),
                                                       desc="获取单词详情",
                                                       total=len(words)):
            if typ != 1 or word in all_words:
                continue
            print(word)
            # 获取单词详细信息
            word_details = fetch_word_details(word)
            # print("单词详细", word_details)

            # 提取单词数据
            word_data = extract_word_data(word_details)

            print(word, phonetic, meaning, freq)

            # 使用已有的音标、词义和频率数据补充

            word_data["音标"] = f"/{phonetic}/"

            word_data["词义"] = meaning

            word_data["频率"] = freq

            # 将单词数据添加到结果列表
            all_word_data.append(word_data)

            # 添加延迟，避免请求过于频繁
            time.sleep(1.5)
            # break

        print(f"成功获取 {len(all_word_data)} 个单词的详细信息")
        # 准备列名
        columns = [
            "单词", "音标",
            "中考出现次数", "中考出现年数", "中考重要性",
            "高考出现次数", "高考出现年数", "高考重要性",
            "词义", "拓展短语", "频率", "常见释义"
        ]

        # 创建DataFrame
        result_df = pd.DataFrame(all_word_data)

        # 确保所有列都存在
        for col in columns:
            if col not in result_df.columns:
                result_df[col] = ""

        # 只保留需要的列并按顺序排列
        result_df = result_df[columns]

        # 保存到Excel
        output_file = os.path.join(path, "40篇-3500.xlsx")
        result_df.to_excel(output_file, index=False)
        print(f"成功生成单词词典: {output_file} (包含 {len(result_df)} 个单词)")
    except Exception as e:
        print(f"处理过程中出错: {e}")
        import traceback
        traceback.print_exc()


def main(path, file='单词列表.xlsx'):
    try:
        print("开始处理单词列表...")

        # 从Excel文件读取单词列表
        file_path = os.path.join(path, file)

        if not os.path.exists(file_path):
            print(f"错误：文件 {file_path} 不存在!")
            return

        # 读取Excel文件
        df = pd.read_excel(file_path)

        # 读取Excel文件
        df_all = pd.read_excel('总.xlsx')
        all_words = df_all['单词'].tolist()
        print(all_words)

        # 获取所有单词列
        words = df['word'].tolist()
        # 获取所有音标列
        phonetic_en = df['phonetic'].tolist()
        # 获取所有词义列
        meanings = df['meaning'].tolist()
        # 获取所有频率列
        frequency = df['frequency'].tolist()

        # 初始化结果列表
        all_word_data = []

        # print(meanings)

        # 为每个单词获取详细信息
        print("开始获取单词详细信息...")
        print(len(words), len(phonetic_en), len(meanings), len(frequency))

        # 使用tqdm显示进度条和zip组合所有列数据
        for word, phonetic, meaning, freq in tqdm(zip(words, phonetic_en, meanings, frequency),
                                                  desc="获取单词详情",
                                                  total=len(words)):
            if word in all_words:
                continue
            print(word)
            # 获取单词详细信息
            word_details = fetch_word_details(word)
            # print("单词详细", word_details)

            # 提取单词数据
            word_data = extract_word_data(word_details)

            print(word, phonetic, meaning, freq)

            # 使用已有的音标、词义和频率数据补充

            word_data["音标"] = f"/{phonetic}/"

            word_data["词义"] = meaning

            word_data["频率"] = freq

            # 将单词数据添加到结果列表
            all_word_data.append(word_data)

            # 添加延迟，避免请求过于频繁
            time.sleep(1.5)
            # break

        print(f"成功获取 {len(all_word_data)} 个单词的详细信息")
        # 准备列名
        columns = [
            "单词", "音标",
            "中考出现次数", "中考出现年数", "中考重要性",
            "高考出现次数", "高考出现年数", "高考重要性",
            "词义", "拓展短语", "频率", "常见释义"
        ]

        # 创建DataFrame
        result_df = pd.DataFrame(all_word_data)

        # 确保所有列都存在
        for col in columns:
            if col not in result_df.columns:
                result_df[col] = ""

        # 只保留需要的列并按顺序排列
        result_df = result_df[columns]

        # 保存到Excel
        output_file = os.path.join(path, "40篇-3500.xlsx")
        result_df.to_excel(output_file, index=False)
        print(f"成功生成单词词典: {output_file} (包含 {len(result_df)} 个单词)")
    except Exception as e:
        print(f"处理过程中出错: {e}")
        import traceback
        traceback.print_exc()
