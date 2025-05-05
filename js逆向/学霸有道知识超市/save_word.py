import json

import pandas as pd
from jsonpath_ng import parse

# 读取文件内容为 JSON 字符串
with open('修复word.json', 'r', encoding='utf-8') as f:
    json_data = f.read()

# 将 JSON 字符串解析为 Python 对象
json_data = json.loads(json_data)
print(type(json_data))

# JSONPath 解析
word_path = parse("$..word")
phonetic_path = parse("$..phonetic_en")
meaning_path = parse("$..meaning")
types_path = parse("$..type")

words = [match.value for match in word_path.find(json_data)]
phonetics = [match.value for match in phonetic_path.find(json_data)]
meanings = [match.value for match in meaning_path.find(json_data)]
types = [match.value for match in types_path.find(json_data)]

# 给每个单词设定 "frequency"（这里假设 type=1 是高频，type=2 是中频）
frequencies = []
for item in json_data:
    if item["importance"] == "1":
        frequencies.append("高频")
    elif item["importance"] == "2":
        frequencies.append("中频")
    else:
        frequencies.append("低频")

# 创建 DataFrame
df = pd.DataFrame({
    "word": words,
    "frequency": frequencies,
    "phonetic": phonetics,
    "meaning": meanings,
    'type': types
})

# 保存为 Excel
df.to_excel("words.xlsx", index=False)

print("✅ 数据已保存为 words.xlsx")
