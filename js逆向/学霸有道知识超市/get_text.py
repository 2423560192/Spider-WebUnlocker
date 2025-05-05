import requests
import json
import os
from jsonpath import jsonpath


def fetch_speech_data(url):
    """
    从指定URL获取语音数据
    
    参数:
        url: API URL地址
    返回:
        JSON数据或None(如果请求失败)
    """
    try:
        print(f"正在请求URL: {url}")
        # 发送GET请求
        response = requests.get(url)
        response.raise_for_status()  # 如果请求失败，抛出异常

        # 解析JSON数据
        data = response.json()
        print(f"成功获取数据，共 {len(data)} 条记录")
        return data

    except Exception as e:
        print(f"获取数据失败: {e}")
        return None


def extract_text_structured(data):
    """
    从数据中提取文本，保留句子结构
    
    参数:
        data: JSON数据列表
    返回:
        格式化的文本字符串，保留句子结构
    """
    if not data:
        return ""

    # 提取所有句子
    sentences = []
    words = []
    current_sentence = ""

    # 对数据按照text_offset排序，确保文本顺序正确
    sorted_data = sorted(data, key=lambda x: x.get("text_offset", 0))

    for item in sorted_data:
        text = item.get("text", "")
        boundary_type = item.get("boundary_type", "")

        if boundary_type == "Sentence":
            # 找到一个完整句子，添加到结果中
            sentences.append(text)
        elif boundary_type == "Word":
            # 收集单词
            words.append(text)

    # 如果没有找到句子，则使用单词列表
    if not sentences and words:
        return " ".join(words)

    # 返回句子，每个句子一行
    return "\n".join(sentences)


def extract_text_simple(data):
    """
    简单提取所有文本并用空格连接
    
    参数:
        data: JSON数据列表
    返回:
        连接后的文本字符串
    """
    if not data:
        return ""

    # 从每个项目中提取text字段
    texts = []
    for item in data:
        if "text" in item and item["text"] and item.get("boundary_type") == "Word":
            texts.append(item["text"])

    # 用空格连接所有文本
    return " ".join(texts)


def save_to_file(text, filename="speech_text.txt"):
    """
    将文本保存到文件
    
    参数:
        text: 要保存的文本
        filename: 输出文件名
    """
    try:
        with open(filename, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"文本已保存到 {filename}")
    except Exception as e:
        print(f"保存文件失败: {e}")


def get_chinese_meaning(data):
    cn_contents = jsonpath(data, '$..data..cn_content')
    return "\n".join(cn_contents)


def main(path):
    # 提取a.json
    try:
        with open(os.path.join(path, 'a.josn'), "r", encoding="utf-8") as f:
            data = json.load(f)
    except:
        return
    print(data['en_result_url'])
    # 定义API URL
    url = data['en_result_url']

    # 获取中文意思
    ch_means = get_chinese_meaning(data)
    # 保存数据

    # 获取数据
    data = fetch_speech_data(url)
    save_to_file(ch_means, path + "/中文意思.txt")

    if data:
        # 提取结构化文本（包含句子分隔）
        structured_text = extract_text_structured(data)
        print(f"提取的结构化文本总长度: {len(structured_text)} 字符")

        # 保存结构化文本
        save_to_file(structured_text, path + "/英文意思.txt")

        # # 同时生成简单版本（单词之间用空格分隔）
        # simple_text = extract_text_simple(data)
        # print(f"提取的简单文本总长度: {len(simple_text)} 字符")
        #
        # # 保存简单文本
        # save_to_file(simple_text, path + "/speech_text_simple.txt")
    else:
        print("未能获取数据，程序终止")


if __name__ == "__main__":
    main()
