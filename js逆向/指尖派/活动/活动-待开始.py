
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import pandas as pd
import requests
import json
from datetime import datetime

def get_proxy():
    """从代理API获取代理地址"""
    proxy_api = 'http://api2.xkdaili.com/tools/XApi.ashx?apikey=XK69862370B1CA650629&qty=1&format=txt&split=0&sign=87a269171ead05ba5185eba8eb5a162a&time=3'
    try:
        response = requests.get(proxy_api, timeout=10)
        response.raise_for_status()
        proxy_address = response.text.strip()
        if not proxy_address:
            print("代理API返回空地址")
            return None
        print(f"成功获取代理地址：{proxy_address}")
        return {'http': f'http://{proxy_address}', 'https': f'http://{proxy_address}'}
    except Exception as e:
        print(f"获取代理失败：{e}")
        return None

def get_selected_activities():
    # 定义请求头
    headers = {
        'Host': 'h5.wmzjp.com',
        'accept': 'application/json, text/plain, */*',
        'xweb_xhr': '1',
        'authorization': 'Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdXRoIjp7InBhc3N3b3JkIjpudWxsLCJ1c2VybmFtZSI6InpqcDEwMDEwMDAwNTMxMjciLCJhdXRob3JpdGllcyI6W10sImFjY291bnROb25FeHBpcmVkIjp0cnVlLCJhY2NvdW50Tm9uTG9ja2VkIjp0cnVlLCJjcmVkZW50aWFsc05vbkV4cGlyZWQiOnRydWUsImVuYWJsZWQiOnRydWUsInVzZXJJZCI6MTAwMTAwMDA1MzEyNywib3BlbklkIjoib0ZPODI2U2lSRjlCbE5KVXo3bWxoMWptaE8wYyIsInNjaG9vbElkIjo2LCJiaW5kZWQiOjB9LCJqdGkiOiIzNWMzMDM5Ni1jMjZiLTRjMjgtYjVlMS1hZTBhZmRhNWM2NTQiLCJpYXQiOjE3NDUzODg3MjMsImV4cCI6MTc0NTk5MzUyM30.iHFy4wJv_IqBV-TDBIFbfQwNcKXqbnvx6nusXetTqZ8',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090c33)XWEB/11581',
        'Content-type': 'application/json;charset=UTF-8',
        'sec-fetch-site': 'cross-site',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://servicewechat.com/wxbd5a45d082ccacaa/34/page-frame.html',
        'accept-language': 'zh-CN,zh;q=0.9',
    }

    # 获取代理
    # proxies = get_proxy()
    # if not proxies:
    #     print("无法获取代理，将尝试直接请求")
    proxies = None

    # 初始化结果列表和分页参数
    result = []
    current_page = 1
    page_size = 10  # 每页记录数，与json_data中的size一致
    filtered_count = 0  # 记录被过滤的活动数

    # 定义要提取的字段和中文列名
    fields = {
        'name': '活动名称',
        'id': 'ID',
        'beginTime': '开始时间',
        'endTime': '结束时间',
        'actBigTypeName': '活动大类名称',
        'orgName': '组织名称',
        'totalNumber': '总人数',
        'applicantsNumber': '报名人数',
        'enrollBeginTime': '报名开始时间',
        'enrollEndTime': '报名结束时间',
        'blurb': '活动简介',
        'signNumber': '签到次数',
        'siteName': '场地名称',
    }

    # 获取当前时间
    current_time = datetime.now()

    while True:
        # 设置请求的JSON数据，更新current字段
        json_data = {
            'keyword': '',
            'actLevel': '',
            'size': page_size,
            'current': current_page,
            'plate': 1,
            'actSmallClassName': '',
            'actBigType': '',
            'status': 4,
            'orderBy': 1,
            'actSmallType': '',
        }

        try:
            # 发送POST请求
            response = requests.post(
                'https://h5.wmzjp.com/act-activity/listActivities',
                headers=headers,
                json=json_data,
                proxies=proxies,
                timeout=10
            )
            response.raise_for_status()  # 检查响应状态码，错误时抛出异常
            data = response.json()

            # 检查数据是否有效
            if 'data' not in data or 'records' not in data['data']:
                print("数据中未找到记录。")
                break

            # 提取指定字段并过滤结束时间
            for record in data['data']['records']:
                activity = {fields[key]: record.get(key, '') for key in fields}
                # 检查结束时间
                end_time_str = activity['报名结束时间']
                if end_time_str:
                    try:
                        end_time = pd.to_datetime(end_time_str, errors='coerce')
                        if pd.isna(end_time) or end_time < current_time:
                            filtered_count += 1
                            continue  # 跳过已结束的活动
                    except Exception as e:
                        print(f"解析活动 {activity['活动名称']} 的结束时间失败：{e}")
                        filtered_count += 1
                        continue
                result.append(activity)

            # 获取分页元数据
            total = data['data'].get('total', 0)
            size = data['data'].get('size', page_size)
            pages = data['data'].get('pages', 1)

            # 打印进度
            print(f"已获取第 {current_page}/{pages} 页，当前记录数：{len(result)}")

            # 如果已获取所有页面或无更多记录，退出循环
            if current_page >= pages or not data['data']['records']:
                break

            # 进入下一页
            current_page += 1

            # 添加请求间隔，避免触发API限速
            time.sleep(3)  # 每页请求间隔3秒

        except requests.RequestException as e:
            print(f"获取第 {current_page} 页时发生错误：{e}")
            break
        except ValueError as e:
            print(f"解析第 {current_page} 页JSON时发生错误：{e}")
            break
        except Exception as e:
            print(f"第 {current_page} 页发生未知错误：{e}")
            break

    # 打印结果
    if result:
        for activity in result:
            print(f"活动名称：{activity['活动名称']}")
            print(f"ID：{activity['ID']}")
            print(f"开始时间：{activity['开始时间']}")
            print(f"结束时间：{activity['结束时间']}")
            print(f"场地名称：{activity['场地名称']}")
            print("-" * 50)
        print(f"总共获取活动数：{len(result)}")
        if filtered_count > 0:
            print(f"因结束时间早于当前时间过滤掉的活动数：{filtered_count}")

        # 创建DataFrame并保存到Excel
        df = pd.DataFrame(result)
        output_file = '待开始的活动.xlsx'
        df.to_excel(output_file, index=False, engine='openpyxl')
        print(f"结果已保存至 {output_file}")
    else:
        print("未获取到任何活动。")
        if filtered_count > 0:
            print(f"因结束时间早于当前时间过滤掉的活动数：{filtered_count}")

    return result

if __name__ == "__main__":
    get_selected_activities()