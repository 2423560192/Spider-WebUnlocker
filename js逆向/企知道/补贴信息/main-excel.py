"""
https://www.policypro.cn/match-company-info?companyId=3918120806940409856&companyName=中国建设银行股份有限公司
"""
import json
import requests
from jsonpath import jsonpath
import configparser
from openpyxl import Workbook


# 获取公司ID
def get_pid(name):
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Authorization': '197d547e2f46670089fb3c5880fcb389',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    }

    params = {
        'companyName': name,
        'platformId': '3479085520414310401',
    }

    response = requests.get(
        'https://policyapi.10nservice.com/api/v2/WebSmartMatch/GetCompanyBaseInfo',
        params=params,
        headers=headers,
    )

    data = response.json()['Data']
    pid = json.loads(data)['CompanyId']
    print(f"公司ID: {pid}")
    return pid


# 获取项目信息（资质、资金支持、荣誉品牌）
def get_projects(pid, class_name):
    headers = {
        'accept': 'application/json, text/plain, */*',
        'authorization': '197d547e2f46670089fb3c5880fcb389',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    }

    url = f'https://entapi.10nnet.com/api/v1/BusinessMain/GetValidProjectList?companyId={pid}&pageIndex=1&pageSize=1000&orderBy=GradeID+desc,MaxPublicityYear+desc&ClassName={class_name}&platformId=3479085520414310401'
    response = requests.get(url, headers=headers)
    data = response.json()['Data']

    ProjectTitle = jsonpath(data, '$..ProjectTitle')
    GradeName = jsonpath(data, '$..GradeName')
    ReleaseName = jsonpath(data, '$..ReleaseName')
    MaxPublicityYear = jsonpath(data, '$..MaxPublicityYear')
    EndYear = jsonpath(data, '$..EndYear')

    return ProjectTitle, GradeName, ReleaseName, MaxPublicityYear, EndYear


# 保存数据到Excel文件
def save_data_to_excel(ProjectTitle, GradeName, ReleaseName, MaxPublicityYear, EndYear, filename='ProjectInfo.xlsx'):
    # 创建工作簿
    wb = Workbook()
    ws = wb.active
    ws.title = "项目数据"

    # 写入表头
    headers = ['项目标题', '等级名称', '发布名称', '最大公示年份', '结束年份']
    ws.append(headers)

    # 写入数据
    for title, name, rename, maxyaer, endyear in zip(ProjectTitle, GradeName, ReleaseName, MaxPublicityYear, EndYear):
        year_range = f'{maxyaer}年-{endyear}年'
        ws.append([title, name, rename, year_range])

    # 保存Excel文件
    wb.save(filename)
    print(f"数据已保存到 {filename}")


# 加载配置文件
def loadConf():
    config = configparser.RawConfigParser()
    with open('utils/conf.ini', 'r', encoding='utf-8') as f:
        config.read_file(f)
    return config


# 主函数
def main():
    company_name = input('请输入公司名：').strip()
    config = loadConf()

    try:
        pid = get_pid(company_name)
    except Exception as e:
        print(f"获取公司ID失败: {e}")
        return

    ProjectTitles = []
    GradeNames = []
    ReleaseNames = []
    MaxPublicityYears = []
    EndYears = []

    # 获取不同类别的项目数据
    try:
        # 资质认定
        ProjectTitle, GradeName, ReleaseName, MaxPublicityYear, EndYear = get_projects(pid,
                                                                                       '%E8%B5%84%E8%B4%A8%E8%AE%A4%E5%AE%9A')
        ProjectTitles.extend(ProjectTitle)
        GradeNames.extend(GradeName)
        ReleaseNames.extend(ReleaseName)
        MaxPublicityYears.extend(MaxPublicityYear)
        EndYears.extend(EndYear)
    except Exception as e:
        print(f"获取资质认定数据失败: {e}")

    try:
        # 资金支持
        ProjectTitle, GradeName, ReleaseName, MaxPublicityYear, EndYear = get_projects(pid,
                                                                                       '%E8%B5%84%E9%87%91%E6%89%B6%E6%8C%81')
        ProjectTitles.extend(ProjectTitle)
        GradeNames.extend(GradeName)
        ReleaseNames.extend(ReleaseName)
        MaxPublicityYears.extend(MaxPublicityYear)
        EndYears.extend(EndYear)
    except Exception as e:
        print(f"无资质认定: {e}")

    try:
        # 荣誉品牌
        ProjectTitle, GradeName, ReleaseName, MaxPublicityYear, EndYear = get_projects(pid,
                                                                                       '%E8%8D%A3%E8%AA%89%E5%93%81%E7%89%8C')
        ProjectTitles.extend(ProjectTitle)
        GradeNames.extend(GradeName)
        ReleaseNames.extend(ReleaseName)
        MaxPublicityYears.extend(MaxPublicityYear)
        EndYears.extend(EndYear)
    except Exception as e:
        print(f"无资金支持: {e}")

    # 输出数据到Excel
    if ProjectTitles:
        save_data_to_excel(ProjectTitles, GradeNames, ReleaseNames, MaxPublicityYears, EndYears)
    else:
        print('无补贴信息')


if __name__ == '__main__':
    main()
