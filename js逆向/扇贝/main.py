import requests

cookies = {
    'csrftoken': '3a542f00ba861b6065685e957629c2bb',
    '_ga': 'GA1.2.309656701.1736329418',
    '_gat': '1',
    'sajssdk_2015_cross_new_user': '1',
    'tfstk': 'gLJS3Qs9tz4WZ6zDq4nV50ncvS6BFeMw9kspjHezvTB8JJTCu88EZH5Cd372Ua-PeyeBRZmkU4XzpBtGo97yUQRBlTv2aJ7rr9tp79gZ7Akwq3fhpVuwPegGKOI7wyUF2oQALM1o_Nhkq3X3mYlJCQ-uRn98IeBpJtCAjGXLp_LdDtQcxMURv8nXDZbA2wQdv-QAYgFL9eBKcnQcv9QKKwHf0D7WV0M_FgaigGtRlJepevf5527AmiJf6__OwZwpVKs5NNKWUmrZiip2h154YfXvjI8RcOM4wOKX9FO9-fPcFHdJ-sTooS_2MLxdJsrLCnt62CBvLDEGGEIC69CbvJKfEZLBUOHTliAv4BpkPkwdqLJNONfjvJfFHd596UZnjnBRvefMLV2lyHKMICWs37B9cBL6OgJ3QNiGiWZfsJsf7mibtWxV-A9FCntio_Ic0Pojcz6Awijf7mibtWfRmioZcma5H',
    'auth_token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MjMyOTQ1NzY3LCJleHAiOjE3MzcxOTM3NDcsImV4cF92MiI6MTczNzE5Mzc0NywiZGV2aWNlIjoiIiwidXNlcm5hbWUiOiJXZWNoYXRfOWU1ZWVjZWEwMzdjZjYwYSIsImlzX3N0YWZmIjowLCJzZXNzaW9uX2lkIjoiMWFiY2ViYTZjZGE1MTFlZjllZGQ2ZTRmZjI5OTllZDkifQ.JbTrQTlwx1oydcr7jetyydR2e_tPMUKT-Ijmeqwm79E',
    'sensorsdata2015jssdkcross': '%7B%22distinct_id%22%3A%22dxvtjy%22%2C%22first_id%22%3A%22194454c574a22-0a87ba47ca3cef-26011851-1638720-194454c574b1f41%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%A4%BE%E4%BA%A4%E7%BD%91%E7%AB%99%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC%22%2C%22%24latest_referrer%22%3A%22https%3A%2F%2Fopen.weixin.qq.com%2F%22%7D%2C%22%24device_id%22%3A%22194454c574a22-0a87ba47ca3cef-26011851-1638720-194454c574b1f41%22%7D',
}

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'zh-CN,zh;q=0.9',
    # 'cookie': 'csrftoken=3a542f00ba861b6065685e957629c2bb; _ga=GA1.2.309656701.1736329418; _gat=1; sajssdk_2015_cross_new_user=1; tfstk=gLJS3Qs9tz4WZ6zDq4nV50ncvS6BFeMw9kspjHezvTB8JJTCu88EZH5Cd372Ua-PeyeBRZmkU4XzpBtGo97yUQRBlTv2aJ7rr9tp79gZ7Akwq3fhpVuwPegGKOI7wyUF2oQALM1o_Nhkq3X3mYlJCQ-uRn98IeBpJtCAjGXLp_LdDtQcxMURv8nXDZbA2wQdv-QAYgFL9eBKcnQcv9QKKwHf0D7WV0M_FgaigGtRlJepevf5527AmiJf6__OwZwpVKs5NNKWUmrZiip2h154YfXvjI8RcOM4wOKX9FO9-fPcFHdJ-sTooS_2MLxdJsrLCnt62CBvLDEGGEIC69CbvJKfEZLBUOHTliAv4BpkPkwdqLJNONfjvJfFHd596UZnjnBRvefMLV2lyHKMICWs37B9cBL6OgJ3QNiGiWZfsJsf7mibtWxV-A9FCntio_Ic0Pojcz6Awijf7mibtWfRmioZcma5H; auth_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MjMyOTQ1NzY3LCJleHAiOjE3MzcxOTM3NDcsImV4cF92MiI6MTczNzE5Mzc0NywiZGV2aWNlIjoiIiwidXNlcm5hbWUiOiJXZWNoYXRfOWU1ZWVjZWEwMzdjZjYwYSIsImlzX3N0YWZmIjowLCJzZXNzaW9uX2lkIjoiMWFiY2ViYTZjZGE1MTFlZjllZGQ2ZTRmZjI5OTllZDkifQ.JbTrQTlwx1oydcr7jetyydR2e_tPMUKT-Ijmeqwm79E; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22dxvtjy%22%2C%22first_id%22%3A%22194454c574a22-0a87ba47ca3cef-26011851-1638720-194454c574b1f41%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%A4%BE%E4%BA%A4%E7%BD%91%E7%AB%99%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC%22%2C%22%24latest_referrer%22%3A%22https%3A%2F%2Fopen.weixin.qq.com%2F%22%7D%2C%22%24device_id%22%3A%22194454c574a22-0a87ba47ca3cef-26011851-1638720-194454c574b1f41%22%7D',
    'origin': 'https://web.shanbay.com',
    'priority': 'u=1, i',
    'referer': 'https://web.shanbay.com/',
    'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    'x-csrftoken': '3a542f00ba861b6065685e957629c2bb',
}

params = {
    'ipp': '10',
    'page': '2',
    'type_of': 'NEW',
}

response = requests.get(
    'https://apiv3.shanbay.com/wordsapp/user_material_books/uphcs/learning/words/today_learning_items',
    params=params,
    cookies=cookies,
    headers=headers,
)

data = response.json()['data']
import execjs
res = execjs.compile(open('loader.js').read()).call("get_data" , data)
print(res)