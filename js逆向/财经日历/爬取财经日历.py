import requests
from jsonpath import jsonpath
from openpyxl import workbook

ws = workbook.Workbook()
wb = ws.active

wb.append(['时间', '名称', '主办单位', '地区', '类型'])
ws.save('财经会议.xlsx')


def get_data(url):
    headers = {
        'Accept': '*/*',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Cookie': 'qgqp_b_id=64a7cce8d2eabd401bf2c5447420e3c3; st_si=63392611024962; st_pvi=73731030429905; st_sp=2023-04-11%2021%3A52%3A49; st_inirUrl=https%3A%2F%2Fwww.baidu.com%2Flink; st_sn=1; st_psi=20231021143914164-113300301035-6268646910; JSESSIONID=8227C94A9D04E85B960BCA79DFA8672B; st_asi=20231021143914164-113300301035-6268646910-dfcfwsy_dfcfwxsy_ycl_ewmxt-1; JSESSIONID=B7E10584604DAEAC1137A6A9788CC571',
        'Referer': 'https://data.eastmoney.com/cjrl/',
        'Sec-Fetch-Dest': 'script',
        'Sec-Fetch-Mode': 'no-cors',
        'Sec-Fetch-Site': 'same-site',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Chromium";v="118", "Google Chrome";v="118", "Not=A?Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"'
    }

    response = requests.request("GET", url, headers=headers).json()
    print(response)
    # 保存数据
    times = jsonpath(response, '$..result.data[0:].START_DATE')
    name = jsonpath(response, '$..result.data[0:].FE_NAME')
    sponsor_name = jsonpath(response, '$..result.data[0:].SPONSOR_NAME')
    city = jsonpath(response, '$..result.data[0:].CITY')
    category = jsonpath(response, '$..result.data[0:].FE_TYPE')
    for t, n, s, c, cat in zip(times, name, sponsor_name, city, category):
        print(t, n, s, c, cat)


if __name__ == '__main__':
    url = "https://datacenter-web.eastmoney.com/api/data/v1/get?reportName=RPT_CPH_FECALENDAR&pageNumber=1&pageSize=50&sortColumns=START_DATE&sortTypes=1&filter=(END_DATE%3E%3D%272013-01-01%27)(START_DATE%3C%272023-11-20%27)(STD_TYPE_CODE%3D%221%22)&source=WEB&client=WEB&columns=START_DATE%2CEND_DATE%2CFE_CODE%2CFE_NAME%2CFE_TYPE%2CCONTENT%2CSTD_TYPE_CODE%2CSPONSOR_NAME%2CCITY&p=1&pageNo=1&pageNum=1&_=1697870354002"

    get_data(url)
