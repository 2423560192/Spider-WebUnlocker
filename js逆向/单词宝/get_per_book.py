import requests
from jsonpath_ng import parse


def get_parse_data(data):
    # 定义 JSONPath 表达式
    id_expr = parse('$.data[*][*]._id')  # 提取所有 _id
    name_expr = parse('$.data[*][*].name')  # 提取所有 name
    imgs = parse('$.data[*][*].thumb')  # 提取所有图片

    # 提取 _id 和 name
    ids = [match.value for match in id_expr.find(data)]
    names = [match.value for match in name_expr.find(data)]
    imgs = [match.value for match in imgs.find(data)]

    # 组合结果
    result = [{"_id": id_, "name": name, "img": img} for id_, name, img in zip(ids, names, imgs)]
    return result


def get_resp_data(grade):
    headers = {
        'Host': 'api.lelegs.net',
        'xweb_xhr': '1',
        'userid': '67e1f46e4ffa83fb6914fc2d',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090c33)XWEB/11581',
        'Content-type': 'application/json;charset=UTF-8',
        'accept': '*/*',
        'sec-fetch-site': 'cross-site',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://servicewechat.com/wx8390b4aaa8cbabff/45/page-frame.html',
        'accept-language': 'zh-CN,zh;q=0.9',
    }

    params = {
        'grade': grade,
    }

    response = requests.get('https://api.lelegs.net/yytx-v2/book/list', params=params, headers=headers)
    return response.json()


def get_data(grade):
    resp_data = get_resp_data(grade)
    data = get_parse_data(resp_data)
    return data
