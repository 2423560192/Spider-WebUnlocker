def get_company_detail_data(url, ua):
    """
    抓取企业详情信息
    :param url:
    :return:
    """
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'cache-control': 'max-age=0',
        # 'cookie': 'smidV2=2024112415240248b94738dbcd573313cc844ab91e9f4a007e443c457176070; sensorsdata2015jssdkchannel=%7B%22prop%22%3A%7B%22_sa_channel_landing_url%22%3A%22%22%7D%7D; _bl_uid=dUm0j3eXvIn9LwwOmkj2c9Cw832O; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2230c4bf7f17cd4f3ab15d2fff3a32776f%22%2C%22first_id%22%3A%221935d0e61e312d7-0e3865b29a5f608-4c657b58-1638720-1935d0e61e490a%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMTkzNWQwZTYxZTMxMmQ3LTBlMzg2NWIyOWE1ZjYwOC00YzY1N2I1OC0xNjM4NzIwLTE5MzVkMGU2MWU0OTBhIiwiJGlkZW50aXR5X2xvZ2luX2lkIjoiMzBjNGJmN2YxN2NkNGYzYWIxNWQyZmZmM2EzMjc3NmYifQ%3D%3D%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%24identity_login_id%22%2C%22value%22%3A%2230c4bf7f17cd4f3ab15d2fff3a32776f%22%7D%2C%22%24device_id%22%3A%221935d0e61e312d7-0e3865b29a5f608-4c657b58-1638720-1935d0e61e490a%22%7D; wz_uuid=X%2F15e03afdfc0aee818303c475ee1ab410; Hm_lvt_8b5ea374777742fd73d0561bd1dfca6d=1732433045,1732499698,1732512686,1732515537; HMACCOUNT=41D5A6B7364EA1F9; Hm_lvt_9ea3e7293b7c088e0d2c88874b63e7dd=1732500300,1732512687,1732515538; Hm_lpvt_9ea3e7293b7c088e0d2c88874b63e7dd=1732515538; HMACCOUNT=41D5A6B7364EA1F9; accessToken=; token=; acw_tc=784e2c9017325157530527005e523e3640fd474047bfb5c08ca90e84b23f5d; x-web-ip=123.147.249.209, 47.121.110.199, 120.78.44.144, 100.121.99.250; .thumbcache_de0d870e3139ba2368b2e7ea8f11063c=s2WHnR7ofHPAD/oQTKVmbO3mhMh9zW/vxXyew/iVsJ1YotI8M/JnEpXcc7oVdoXZH2R9WZGRY6Ku4rn4M60OJA%3D%3D; Hm_lpvt_8b5ea374777742fd73d0561bd1dfca6d=1732515755',
        'priority': 'u=0, i',
        'referer': 'https://qiye.qizhidao.com/lib/scf8768b673967ee7e41db303bc2b3ea56/page-5/',
        'sec-ch-ua': '"Microsoft Edge";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0',
    }
    # 更换cookie
    headers['cookie'] = cookie
    # headers['accesstoken'] = re.search(r'token=([^;]+)', cookie).group(1)
    headers['user-agent'] = ua

    response = requests.get(
        url,
        headers=headers,
        proxies=proxies
    )
    data = response.text
    # print(data)

    lxml = etree.HTML(data)
    company_name = lxml.xpath('//*[@class="companyName"]/text()')
    company_id = lxml.xpath(
        '//*[@id="__layout"]/div/div[2]/div[2]/div/div[1]/div[1]/div[1]/div[3]/div[1]/div[1]/div[1]/div/div/div[2]/span/div/span[1]/span//text()')  # 统一社会信用代码
    re_name = lxml.xpath('//*[@id="businessInfo_num"]/div[2]/div[1]/div[2]/p[2]//text()')  # 曾用名
    company_people = lxml.xpath('//*[@id="businessInfo_num"]/div[2]/div[2]/div[1]/div[2]/span[2]/a//text()')  # 法人
    company_status = lxml.xpath('//*[@id="businessInfo_num"]/div[2]/div[2]/div[2]/div[2]/span/span//text()')  # 企业状态
    company_start_time = lxml.xpath('//*[@id="businessInfo_num"]/div[2]/div[2]/div[3]/div[2]//text()')  # 成立日期
    company_money = lxml.xpath('//*[@id="businessInfo_num"]/div[2]/div[3]/div[1]/div[2]//text()')  # 注册资本
    company_really_money = lxml.xpath('//*[@id="businessInfo_num"]/div[2]/div[3]/div[2]/div[2]//text()')  # 实缴资本
    company_type = lxml.xpath('//*[@id="businessInfo_num"]/div[2]/div[3]/div[3]/div[2]//text()')  # 组织机构类型
    company_code = company_id[0][8:-1]  # 组织机构代码
    company_nasui_id = company_id  # 纳税人识别号

    match = re.search(r'labelTitle:\s*"工商注册号",\s*labelValue:\s*"(\d+)"', data)
    if match:
        company_gongshang_id = match.group(1)
    else:
        company_gongshang_id = ''

    company_ctype = lxml.xpath('//*[@id="businessInfo_num"]/div[2]/div[5]/div[1]/div[2]//text()')  # 企业类型
    company_nasui_zizhi = lxml.xpath('//*[@id="businessInfo_num"]/div[2]/div[5]/div[2]/div[2]//text()')  # 增值税一般纳税人
    company_jinkou_code = lxml.xpath('//*[@id="businessInfo_num"]/div[2]/div[5]/div[3]/div[2]//text()')  # 进出口企业代码
    company_hangye = lxml.xpath('//*[@id="businessInfo_num"]/div[2]/div[6]/div[1]/div[2]//text()')  # 所属行业
    company_people_num = lxml.xpath('//*[@id="businessInfo_num"]/div[2]/div[6]/div[2]/div[2]//text()')  # 员工人数
    company_canbao_people_num = lxml.xpath('//*[@id="businessInfo_num"]/div[2]/div[6]/div[3]/div[2]//text()')  # 参保人数
    company_dengji = lxml.xpath('//*[@id="businessInfo_num"]/div[2]/div[7]/div[1]/div[2]//text()')  # 登记机关
    company_manage_date = lxml.xpath('//*[@id="businessInfo_num"]/div[2]/div[7]/div[2]/div[2]//text()')  # 经营期限
    company_hezhun_date = lxml.xpath('//*[@id="businessInfo_num"]/div[2]/div[7]/div[3]/div[2]//text()')  # 核准日期
    company_haiguan_code = lxml.xpath('//*[@id="businessInfo_num"]/div[2]/div[8]/div[1]/div[2]//text()')  # 海关注册编码
    company_english_name = lxml.xpath('//*[@id="businessInfo_num"]/div[2]/div[8]/div[2]/div[2]//text()')  # 英文名

    # 提取注册地址
    match = re.search(r'<div class="filter-source[^"]*"[^>]*>\s*(.*?)\s*</div>', data, re.DOTALL)
    if match:
        company_reg_addr = match.group(1).strip()  # 去掉两端空格
    else:
        company_reg_addr = None  # 或设置默认值

    company_manage_range = lxml.xpath('//*[@id="businessInfo_num"]/div[2]/div[10]/p[2]//text()')  # 经营范围
    # print(url)
    print('企业名:', "".join(company_name).strip() if company_name else "")
    print('信用代码:', "".join(company_id).strip() if company_id else "")
    # print('曾用名:', "".join(re_name).strip() if re_name else "")
    # print('法人:', "".join(company_people).strip() if company_people else "")
    # print('公司状态:', "".join(company_status).strip() if company_status else "")
    # print('成立日期:', "".join(company_start_time).strip() if company_start_time else "")
    # print('注册资本:', "".join(company_money).strip() if company_money else "")
    # print('实缴资本:', "".join(company_really_money).strip() if company_really_money else "")
    # print('组织机构类型:', "".join(company_type).strip() if company_type else "")
    # print('组织机构代码:', "".join(company_code).strip() if company_code else "")
    # print('纳税人识别号:', "".join(company_nasui_id).strip() if company_nasui_id else "")
    # print('工商注册号:', "".join(company_gongshang_id).strip() if company_gongshang_id else "")
    # print('企业类型:', "".join(company_ctype).strip() if company_ctype else "")
    # print('增值税一般纳税人:', "".join(company_nasui_zizhi).strip() if company_nasui_zizhi else "")
    # print('进出口企业代码:', "".join(company_jinkou_code).strip() if company_jinkou_code else "")
    # print('所属行业:', "".join(company_hangye).strip() if company_hangye else "")
    # print('员工人数:', "".join(company_people_num).strip() if company_people_num else "")
    # print('参保人数:', "".join(company_canbao_people_num).strip() if company_canbao_people_num else "")
    # print('登记机关:', "".join(company_dengji).strip() if company_dengji else "")
    # print('经营期限:', "".join(company_manage_date).strip() if company_manage_date else "")
    # print('核准日期:', "".join(company_hezhun_date).strip() if company_hezhun_date else "")
    # print('海关注册编码:', "".join(company_haiguan_code).strip() if company_haiguan_code else "")
    # print('英文名:', "".join(company_english_name).strip() if company_english_name else "")
    # print('注册地址:', "".join(company_reg_addr).strip() if company_reg_addr else "")
    # print('经营范围:', "".join(company_manage_range).strip() if company_manage_range else "")
    return {
        'company_name': "".join(company_name).strip() if company_name else "",
        'company_id': "".join(company_id).strip() if company_id else "",
        're_name': "".join(re_name).strip() if re_name else "",
        'company_people': "".join(company_people).strip() if company_people else "",
        'company_status': "".join(company_status).strip() if company_status else "",
        'company_start_time': "".join(company_start_time).strip() if company_start_time else "",
        'company_money': "".join(company_money).strip() if company_money else "",
        'company_really_money': "".join(company_really_money).strip() if company_really_money else "",
        'company_type': "".join(company_type).strip() if company_type else "",
        'company_code': "".join(company_code).strip() if company_code else "",
        'company_nasui_id': "".join(company_nasui_id).strip() if company_nasui_id else "",
        'company_gongshang_id': "".join(company_gongshang_id).strip() if company_gongshang_id else "",
        'company_ctype': "".join(company_ctype).strip() if company_ctype else "",
        'company_nasui_zizhi': "".join(company_nasui_zizhi).strip() if company_nasui_zizhi else "",
        'company_jinkou_code': "".join(company_jinkou_code).strip() if company_jinkou_code else "",
        'company_hangye': "".join(company_hangye).strip() if company_hangye else "",
        'company_people_num': "".join(company_people_num).strip() if company_people_num else "",
        'company_canbao_people_num': "".join(company_canbao_people_num).strip() if company_canbao_people_num else "",
        'company_dengji': "".join(company_dengji).strip() if company_dengji else "",
        'company_manage_date': "".join(company_manage_date).strip() if company_manage_date else "",
        'company_hezhun_date': "".join(company_hezhun_date).strip() if company_hezhun_date else "",
        'company_haiguan_code': "".join(company_haiguan_code).strip() if company_haiguan_code else "",
        'company_english_name': "".join(company_english_name).strip() if company_english_name else "",
        'company_reg_addr': "".join(company_reg_addr).strip() if company_reg_addr else "",
        'company_manage_range': "".join(company_manage_range).strip() if company_manage_range else "",
    }
