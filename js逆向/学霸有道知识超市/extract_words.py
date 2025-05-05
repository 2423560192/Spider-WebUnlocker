import json
import os
import pandas as pd
import glob
import re
from jsonpath_ng import parse
from collections import defaultdict


def extract_words_from_json_file(file_path):
    """
    使用JSONPath从JSON文件中提取单词和意思
    
    参数:
        file_path: JSON文件路径
    返回:
        包含单词和意思的字典列表
    """
    try:
        # 读取JSON文件
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # 初始化结果列表
        word_list = []

        # 使用JSONPath提取matched_word_base_info
        jsonpath_expr = parse('$..matched_word_base_info')
        matches = [match.value for match in jsonpath_expr.find(data) if match.value]

        # 获取句子上下文
        sentences_expr = parse('$..cn_content')
        sentences = {sentence.context.value['sentence_id']: sentence.value
                     for sentence in sentences_expr.find(data) if hasattr(sentence.context, 'value')}

        # 处理每个词汇
        for match in matches:
            if not match:
                continue

            # 获取句子ID和中文上下文
            sentence_id = None
            context = ""

            # 尝试从路径获取句子ID
            context_expr = parse('$.sentence_id')
            context_matches = context_expr.find(
                match.context.context.context.value if hasattr(match, 'context') and hasattr(match.context,
                                                                                             'context') and hasattr(
                    match.context.context, 'context') else {})

            if context_matches:
                sentence_id = context_matches[0].value
                context = sentences.get(sentence_id, "")

            # 创建单词记录
            if isinstance(match, dict) and 'word' in match and 'meaning' in match:
                # 从意思中提取词性
                pos = ""
                meaning = match.get('meaning', '')

                # 尝试从意思中提取词性 (如 "n.[C]明星，星星")
                pos_match = re.match(r'^([a-z]+\.|\[[A-Z,]+\]|[a-z]+\.\[[A-Z,]+\])', meaning)
                if pos_match:
                    pos = pos_match.group(0)

                # 创建记录
                word_record = {
                    'word': match['word'],
                    'meaning': meaning,
                    'phonetic': match.get('phonetic', ''),
                    'part_of_speech': match.get('pos', pos),
                    'importance': match.get('importance', 0),
                    'source_file': os.path.basename(file_path),
                    'context': context,
                }

                # 添加音频URL
                if 'audio_url' in match:
                    word_record['audio_url'] = match['audio_url']

                # 添加频率分类
                importance = match.get('importance', 0)
                if importance == 1:
                    word_record['frequency'] = '高频'
                elif importance == 2:
                    word_record['frequency'] = '中频'
                elif importance == 3:
                    word_record['frequency'] = '低频'
                else:
                    word_record['frequency'] = '基础'

                word_list.append(word_record)

        return word_list
    except Exception as e:
        print(f"处理文件 {file_path} 时出错: {e}")
        import traceback
        traceback.print_exc()
        return []


def process_all_json_files(path):
    """
    处理url_data目录下的所有JSON文件，提取单词和意思
    """
    # 初始化结果列表
    all_words = []

    # 获取url_data目录下的所有JSON文件
    json_files = glob.glob(f"{path}/a.json")

    if not json_files:
        return

    print(f"找到 {len(json_files)} 个JSON文件")

    # 处理每个文件
    for file_path in json_files:
        print(f"正在处理文件: {file_path}")
        words = extract_words_from_json_file(file_path)
        if words:
            print(f"从 {file_path} 中提取了 {len(words)} 个单词")
            all_words.extend(words)
        else:
            print(f"从 {file_path} 中未提取到单词")

    print(f"总共提取了 {len(all_words)} 个单词")
    return all_words


def save_to_excel(words, output_file="单词列表.xlsx"):
    """
    将单词和意思保存到Excel文件中，按频率分组
    
    参数:
        words: 包含单词和意思的字典列表
        output_file: 输出的Excel文件名
    """
    if not words:
        print("没有数据可以保存")
        return

    # 创建DataFrame
    df = pd.DataFrame(words)

    # 重新排列列的顺序，确保重要的信息在前面
    columns_order = ['word', 'frequency', 'phonetic', 'meaning']

    # 重排列顺序
    df = df[columns_order]

    # 按频率和单词字母顺序排序
    frequency_order = {'高频': 0, '中频': 1, '低频': 2, '基础': 3}
    df['freq_order'] = df['frequency'].map(frequency_order)
    df = df.sort_values(by=['freq_order', 'word']).drop('freq_order', axis=1)

    # 保存到Excel
    df.to_excel(output_file, index=False)
    print(f"数据已保存到 {output_file}")


def main(path):
    """主函数：处理所有JSON文件并保存到Excel"""
    try:
        print("开始提取单词数据...")

        # 再处理所有URL响应文件
        url_words = process_all_json_files(path)

        # 合并所有单词
        all_words = url_words

        if not all_words:
            print("未提取到任何单词数据，请检查JSON文件格式")
            return

        # 去重（基于word字段）
        unique_words = []
        word_dict = {}  # 使用字典提高效率

        for word_info in all_words:
            word = word_info['word']
            if word not in word_dict:
                word_dict[word] = word_info
            elif word_info.get('importance', 0) > word_dict[word].get('importance', 0):
                # 如果遇到更重要的相同单词，则替换
                word_dict[word] = word_info

        unique_words = list(word_dict.values())

        print(f"去重后共有 {len(unique_words)} 个单词")

        # 保存到Excel
        save_to_excel(unique_words, os.path.join(path, "单词列表.xlsx"))


    except Exception as e:
        print(f"处理过程中出错: {e}")
        import traceback
        traceback.print_exc()
