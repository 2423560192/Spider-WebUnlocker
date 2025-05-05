import pandas as pd
from tqdm import tqdm
import time
from concurrent.futures import ThreadPoolExecutor, as_completed


# 处理单行数据的函数
def process_row(i, row, data1):
    word = row["word"]
    phonetic = row["phonetic"]
    meaning = row["meaning"]
    freq = row["frequency"]
    typ = row["type"]

    # 只处理 type == 1 的单词
    if typ != 1:
        return None

    # 收集后续的 type == 2 的短语
    phrases = []
    for j in range(i + 1, len(data1)):
        next_row = data1[j]
        if next_row["type"] != 2:
            break
        phrases.append({
            "短语": next_row["word"],
            "音标": f"/{next_row['phonetic']}/",
            "词义": next_row["meaning"],
            "频率": next_row["frequency"]
        })

    # 将短语列表格式化为字符串
    if phrases:
        phrase_str = "; \n".join(
            f"{p['短语']} ({p['词义']}, 频率: {p['频率']})"
            for p in phrases
        )
    else:
        phrase_str = ""

    # 返回结果
    return {word: phrase_str, f"/{phonetic}/": phrase_str, meaning: phrase_str}


# 处理第一张表格的函数
def process_first_table(first_table_file):
    # 读取第一张表格
    data1 = pd.read_excel(first_table_file).to_dict("records")
    word_phrases = {}

    # 使用多线程处理
    with ThreadPoolExecutor(max_workers=4) as executor:  # 可调整线程数
        # 提交所有任务
        future_to_row = {executor.submit(process_row, i, row, data1): i
                         for i, row in enumerate(data1)}

        # 使用 tqdm 显示进度
        for future in tqdm(as_completed(future_to_row), total=len(data1), desc="处理第一张表格"):
            result = future.result()
            if result:
                word_phrases.update(result)
                print(f"处理单词: {list(result.keys())[0]}")  # 打印第一个键（单词）

    return word_phrases


# 更新第二张表格的函数
def update_second_table(df, word_phrases):
    for index, row in tqdm(df.iterrows(), total=len(df), desc="更新第二张表格"):
        word = row["单词"]
        word_phonetic = row["音标"]
        word_meaning = row["词义"]

        # 查找对应的短语
        phrases = None
        if word in word_phrases:
            phrases = word_phrases[word]
        elif word_phonetic in word_phrases:
            phrases = word_phrases[word_phonetic]
        elif any(meaning in word_meaning for meaning in word_phrases.keys()):
            for meaning in word_phrases.keys():
                if meaning in word_meaning:
                    phrases = word_phrases[meaning]
                    break

        if phrases:
            df.at[index, "拓展短语"] = phrases

    return df


# 主程序
if __name__ == "__main__":
    # 文件路径
    first_table_file = "words.xlsx"
    second_table_file = "1600中考.xlsx"
    output_file = "1600中考-总.xlsx"

    # 处理第一张表格
    print("开始处理第一张表格...")
    word_phrases = process_first_table(first_table_file)

    # 读取并更新第二张表格
    print("开始处理第二张表格...")
    df = pd.read_excel(second_table_file)
    df = update_second_table(df, word_phrases)

    # 保存结果
    df.to_excel(output_file, index=False, engine="openpyxl")
    print(f"融合后的表格已保存到 {output_file}")