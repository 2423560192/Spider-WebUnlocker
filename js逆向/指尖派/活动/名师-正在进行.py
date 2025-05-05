
import time

import pandas as pd
import requests
import json

def get_dai_activity():
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

    # 初始化结果列表和分页参数
    result = []
    current_page = 1
    page_size = 10  # 每页记录数，与json_data中的size一致

    while True:
        # 设置请求的JSON数据，更新current字段
        json_data = {
            'keyword': '',
            'actLevel': '',
            'size': page_size,
            'current': current_page,
            'plate': 3,
            'actSmallClassName': '',
            'actBigType': '',
            'status': 5,
            'orderBy': 1,
            'actSmallType': '',
        }

        try:
            # 发送POST请求
            response = requests.post('https://h5.wmzjp.com/act-activity/listActivities', headers=headers, json=json_data)
            response.raise_for_status()  # 检查响应状态码，错误时抛出异常
            data = response.json()

            # 检查数据是否有效
            if 'data' not in data or 'records' not in data['data']:
                print("数据中未找到记录。")
                break

            # 提取记录
            for record in data['data']['records']:
                activity = {
                    "name": record.get('name'),
                    "id": record.get('id'),
                    "beginTime": record.get('beginTime'),
                    "endTime": record.get('endTime')
                }
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
            time.sleep(3)  # 每页请求间隔1秒

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
            print(f"活动名称：{activity['name']}")
            print(f"ID：{activity['id']}")
            print(f"开始时间：{activity['beginTime']}")
            print(f"结束时间：{activity['endTime']}")
            print("-" * 50)
        print(f"总共获取活动数：{len(result)}")

        # 创建DataFrame并保存到Excel
        df = pd.DataFrame(result, columns=['name', 'id', 'beginTime', 'endTime'])
        df.columns = ['活动名称', 'ID', '开始时间', '结束时间']  # 设置中文列名
        output_file = '名师-正在进行.xlsx'
        df.to_excel(output_file, index=False, engine='openpyxl')
        print(f"结果已保存至 {output_file}")
    else:
        print("未获取到任何活动。")

    return result

if __name__ == "__main__":
    get_dai_activity()