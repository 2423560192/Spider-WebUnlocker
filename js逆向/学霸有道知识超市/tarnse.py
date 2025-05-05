import pandas as pd
from tqdm import tqdm
import time

# 读取第一张表格（只处理前10行）
first_table_file = "words2.xlsx"  # 替换为你的第一张表格文件路径
data1 = pd.read_excel(first_table_file).to_dict("records")

# 只处理前10行
data1 = data1

# 存储单词和短语的映射
word_phrases = {}

# 使用 tqdm 显示进度条，处理第一张表格
for i, row in enumerate(tqdm(data1, desc="处理第一张表格（前10行）", total=len(data1))):
    word = row["word"]
    phonetic = row["phonetic"]
    meaning = row["meaning"]
    freq = row["frequency"]
    typ = row["type"]

    # 只处理 type == 1 的单词
    if typ != 1:
        continue

    print(f"处理单词: {word}")

    # 收集后续的 type == 2 的短语
    phrases = []
    for j in range(i + 1, len(data1)):
        next_row = data1[j]
        if next_row["type"] != 2:
            break  # 如果遇到非 type == 2 的行，停止查找
        # 将 type == 2 的短语添加到列表
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

    # 存储单词和短语的映射（使用单词、音标和词义作为键）
    word_phrases[word] = phrase_str
    word_phrases[f"/{phonetic}/"] = phrase_str
    word_phrases[meaning] = phrase_str

    # 添加延迟（模拟处理）
    time.sleep(1)

# 读取第二张表格
second_table_file = "单词词典总2.xlsx"  # 替换为你的第二张表格文件路径
df = pd.read_excel(second_table_file)

# 更新第二张表格中的“拓展短语”列
for index, row in df.iterrows():
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
        # 更新“拓展短语”列（覆盖现有的值）
        df.at[index, "拓展短语"] = phrases

# 保存融合后的表格
output_file = "3500.xlsx"
df.to_excel(output_file, index=False, engine="openpyxl")

print(f"融合后的表格已保存到 {output_file}")