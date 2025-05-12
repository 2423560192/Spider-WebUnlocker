# -*- coding: utf-8 -*-
"""
加载配置文件
"""
import json


def loadConf():
    import configparser

    # 创建配置解析器
    config = configparser.ConfigParser()

    # 使用正确的编码打开文件
    with open('../conf.ini', 'r', encoding='utf-8') as f:
        config.read_file(f)

    return config
