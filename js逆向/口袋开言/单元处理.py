import os
import shutil
from fnmatch import fnmatch


def should_exclude(filename, exclude_rules):
    """
    判断文件是否应该被排除

    :param filename: 文件名
    :param exclude_rules: 排除规则列表
    :return: bool 是否应该排除
    """
    # 空文件名不处理
    if not filename:
        return True

    # 检查所有排除规则
    for rule in exclude_rules:
        # 规则是文件夹名且当前文件在该文件夹中
        if rule.endswith('/') and filename.startswith(rule):
            return True
        # 通配符匹配 (如 *.jpg)
        elif '*' in rule and fnmatch(filename, rule):
            return True
        # 精确匹配
        elif filename == rule:
            return True
    return False


def process_directories(root_dir, trigger_file, exclude_rules):
    """
    递归处理目录，当发现触发文件时执行操作

    :param root_dir: 要搜索的根目录
    :param trigger_file: 触发处理的文件名
    :param exclude_rules: 排除规则列表
    """
    for dirpath, dirnames, filenames in os.walk(root_dir):
        # 检查当前目录是否包含触发文件
        if trigger_file in filenames:
            print(f"发现触发文件 {trigger_file} 在目录: {dirpath}")

            # 创建"单词"文件夹
            word_dir = os.path.join(dirpath, "单词")
            os.makedirs(word_dir, exist_ok=True)

            # 处理当前目录下的文件
            for filename in filenames:
                file_path = os.path.join(dirpath, filename)

                # 跳过触发文件和符合排除规则的文件
                if filename == trigger_file or should_exclude(filename, exclude_rules):
                    print(f"跳过文件: {filename} (符合排除规则)")
                    continue

                # 移动文件到"单词"文件夹
                try:
                    shutil.move(file_path, os.path.join(word_dir, filename))
                    print(f"移动文件: {filename} -> 单词/{filename}")
                except Exception as e:
                    print(f"无法移动文件 {filename}: {e}")

            # 处理子目录中的文件(避免重复处理)
            for dirname in dirnames[:]:  # 使用副本遍历
                full_dir_path = os.path.join(dirpath, dirname)
                # 如果子目录名匹配排除规则，则跳过
                if should_exclude(dirname + '/', exclude_rules):
                    print(f"跳过目录: {dirname}/ (符合排除规则)")
                    dirnames.remove(dirname)  # 从遍历列表中移除
                    continue

                # 移动整个目录到"单词"文件夹
                try:
                    dest_dir = os.path.join(word_dir, dirname)
                    if not os.path.exists(dest_dir):
                        shutil.move(full_dir_path, dest_dir)
                        print(f"移动目录: {dirname} -> 单词/{dirname}")
                except Exception as e:
                    print(f"无法移动目录 {dirname}: {e}")

            print(f"目录 {dirpath} 处理完成\n")


if __name__ == "__main__":
    # 配置参数
    ROOT_DIRECTORY = r"G:\数据\口袋开言-英语书"  # 要搜索的根目录
    TRIGGER_FILE = "图文标注.xlsx"  # 触发处理的文件名

    # 灵活的排除规则列表 (支持通配符和文件夹标记)
    EXCLUDE_RULES = [
        "lesson_data.xlsx",  # 精确匹配文件名
        "图文标注.xlsx",  # 精确匹配中文文件名
        "*.jpg",  # 所有jpg文件
        "cover.*",  # 所有以cover开头的文件
        "下载资源/",  # 整个"下载资源"文件夹
        "英语电子书图片/",  # 整个"英语电子书图片"文件夹
        "temp_*",  # 所有以temp_开头的文件或文件夹
    ]

    print("开始处理目录...")
    process_directories(ROOT_DIRECTORY, TRIGGER_FILE, EXCLUDE_RULES)
    print("所有目录处理完成")
