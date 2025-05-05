import requests
from lxml import etree

from openpyxl import workbook

cookies = {
    'k8s': '1735103804.598.11257.175606',
    'jrose': '7C539F57754C776908C5E1E8DEDB64C1.mooc-p4-1335914108-d83z2',
    'route': '384a56f0aa1d1c34a64006dc82a9a2b0',
    'lv': '0',
    '_uid': '319010921',
    'UID': '319010921',
    'vc': 'F8ABF7EB07E3BCBEF9AEE23130371840',
    'vc2': 'B62DA6BD9688D0519B699EEFC04ECD01',
    'xxtenc': '9362397f95393c25bfb4a7647751494e',
    'source': '""',
    'fid': '10948',
    'uf': 'b2d2c93beefa90dc1d23f9590714aa1cad9f32c0ff6f38983eab4da746e6135cd74fb4ed584f19d5d83da49ba85f50572a80cd29a298e70788b83130e7eb470482d49b6a3665adad8c436d94f20ea7098487ca4cea3b44011b998cca02f125834e258750070f0706e7fafd565af53bf2',
    '_d': '1735104401098',
    'vc3': 'fWbBxx3H77DR3RGrH5q1BI4I3dJsqIPIXpxxeZFOKGCDUCtpnwviUJsox4MaHr0aRBqUoPVPS7rs4r11RaxDEVXEoBXbqu6lttb6Ff7TohWbWc3I8%2B5oC40qje%2Fq7dN14miuEuH2mFmJMHkvfA4MOOZkc%2B6THr72GZWsx4%2BPG58%3D25ebd78a700d8c49e0e0c825d58c150d',
    'cx_p_token': '543df6bd7ee850688996f86f45dca20a',
    'p_auth_token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1aWQiOiIzMTkwMTA5MjEiLCJsb2dpblRpbWUiOjE3MzUxMDQ0MDEwOTksImV4cCI6MTczNTcwOTIwMX0.ITXpYIP3bM_Tr-kDKIsK732H6cA8kzkRczfuZjPdwgw',
    'DSSTASH_LOG': 'C_38-UN_10404-US_319010921-T_1735104401099',
    'thirdRegist': '0',
}

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    # 'Cookie': 'k8s=1735103804.598.11257.175606; jrose=7C539F57754C776908C5E1E8DEDB64C1.mooc-p4-1335914108-d83z2; route=384a56f0aa1d1c34a64006dc82a9a2b0; lv=0; _uid=319010921; UID=319010921; vc=F8ABF7EB07E3BCBEF9AEE23130371840; vc2=B62DA6BD9688D0519B699EEFC04ECD01; xxtenc=9362397f95393c25bfb4a7647751494e; source=""; fid=10948; uf=b2d2c93beefa90dc1d23f9590714aa1cad9f32c0ff6f38983eab4da746e6135cd74fb4ed584f19d5d83da49ba85f50572a80cd29a298e70788b83130e7eb470482d49b6a3665adad8c436d94f20ea7098487ca4cea3b44011b998cca02f125834e258750070f0706e7fafd565af53bf2; _d=1735104401098; vc3=fWbBxx3H77DR3RGrH5q1BI4I3dJsqIPIXpxxeZFOKGCDUCtpnwviUJsox4MaHr0aRBqUoPVPS7rs4r11RaxDEVXEoBXbqu6lttb6Ff7TohWbWc3I8%2B5oC40qje%2Fq7dN14miuEuH2mFmJMHkvfA4MOOZkc%2B6THr72GZWsx4%2BPG58%3D25ebd78a700d8c49e0e0c825d58c150d; cx_p_token=543df6bd7ee850688996f86f45dca20a; p_auth_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1aWQiOiIzMTkwMTA5MjEiLCJsb2dpblRpbWUiOjE3MzUxMDQ0MDEwOTksImV4cCI6MTczNTcwOTIwMX0.ITXpYIP3bM_Tr-kDKIsK732H6cA8kzkRczfuZjPdwgw; DSSTASH_LOG=C_38-UN_10404-US_319010921-T_1735104401099; thirdRegist=0',
    'Referer': 'https://mooc1.chaoxing.com/mooc2/work/list?courseId=247141827&classId=111406002&cpi=375798610&ut=s&enc=832e2153d45dca77ee1dfb5c29b93d5c',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

params = {
    'courseId': '247141827',
    'classId': '111406002',
    'cpi': '375798610',
    'workId': '39695669',
    'answerId': '55070184',
    'standardEnc': '0ec2dd2de503ac31f46feae86b9cf3df',
    'enc': '20df459da9041a242176d240b5a1d6b3',
}

response = requests.get('https://mooc1.chaoxing.com/mooc-ans/mooc2/work/dowork', params=params, cookies=cookies, headers=headers)
text = response.text

# 题目
lxml = etree.HTML(text)

ques = lxml.xpath('//div[@class="padBom50 questionLi fontLabel singleQuesId"]')
ans = lxml.xpath('//div[contains(@class, "stem_answer")]')


def save(ques, ans):
    end = []
    try:
        for k, v in ans.items():
            if 'checked' in v:
                end.append(k)
                ans[k] = v.replace('checked', '')
        op = ''
        for k, v in ans.items():
            op += k + ':' + v + '\n'
        wb.append([ques, op, " ".join(end)])
        ws.save(f'{name}.xlsx')
    except:
        ans = ans.replace('<p>', '').replace('</p>', '')
        wb.append([ques, ans])
        ws.save(f'{name}.xlsx')


name = '毛概'

ws = workbook.Workbook()
wb = ws.active
wb.append(['题目', '选项', '答案'])
ws.save(f'{name}.xlsx')

for que, an in zip(ques, ans):
    q = " ".join([i.strip() for i in que.xpath('./h3//text()')])
    ass = an.xpath('./div[@class="clearfix answerBg"]')
    dic = {}
    if '简答题' in q or '论述题' in q:
        ass = an.xpath('./div[@class="eidtDiv"]')[0]
        dic = ass.xpath('./textarea/text()')[0]
    else:
        for i in ass:
            choose = i.xpath('./span/text()')[0]
            text = i.xpath('./div/p/text()')[0]
            check = i.xpath('./span[contains(@class , "check_answer")]')
            if check:
                dic[choose] = text + '    checked'
            else:
                dic[choose] = text
    print(q)
    print(dic)
    print('-----------------')
    save(q, dic)
