import requests
from lxml import etree

from 脚本开发.学习通.apis.makesi import save_info_makesi, save_info_hechuan_makesi
from 脚本开发.学习通.apis.maogai import save_info_maogai, save_info_hechuan_maogai
from 脚本开发.学习通.apis.sizheng import save_info_sizheng, save_info_hechuan_sizheng
from 脚本开发.学习通.apis.xiandaishi import save_info_xiandaishi, save_info_hechuan_xiandaishi
from 脚本开发.学习通.apis.xijp import save_info_xijinp, save_info_hechuan_xjp


def get_key_param(cookies, url):
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        # 'Cookie': 'orgfid=43843; lv=0; fid=10948; _uid=254746500; uf=b2d2c93beefa90dc1d23f9590714aa1c70bf2cc17eb00acb5902b9cd8aeec433c640c069eb4014d18427660ded8a8bd46072530a316e7a7e88b83130e7eb470482d49b6a3665adad8c436d94f20ea7098487ca4cea3b44019b689bb9b927bb55d6e665fbb0dabae5e7fafd565af53bf2; _d=1733808895932; UID=254746500; vc=C6ADE5A20C30CD83C65FCAABB5624060; vc2=96902741DB87E7A66380132203C73C2A; vc3=aRLyWlqNl%2BzBOqN3Oi%2BO2XGDYWJDvsiI4J6Gz4QtjeH1BUgF7Ev3xMf%2B9bxYe4GHUEUccMBKjLb7vHYj10%2BcMA41BAMrPao55hn12yOB1qyVNXvbwbzC8CEHT%2FjOBsuyEqKlSZwNDjczI%2BvwKmWD0zTXm8K02%2FXt0Abv0y07kBc%3Ddddf061e786acd3cd5dcd8a0f8eb4f51; cx_p_token=12d390d5c9334be888b835910f23e74a; p_auth_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1aWQiOiIyNTQ3NDY1MDAiLCJsb2dpblRpbWUiOjE3MzM4MDg4OTU5MzQsImV4cCI6MTczNDQxMzY5NX0.V4gItq8gwf51vmKNvK1VHyvS-F8Liq0iy89gj_ENw60; xxtenc=4dda3795246921ee7bd70463a84b14cc; DSSTASH_LOG=C_38-UN_10404-US_254746500-T_1733808895934; spaceFid=10948; spaceRoleId=""; _industry=5; 247076912cpi=285453141; 247076912ut=s; 247076912t=1733808909841; 247076912enc=c11ef02071da834f4b07820340a9450b; k8s=1733808927.015.5177.58909; route=7644025d506561102d55bac4c90cbeeb; jrose=7A8A1D4CCC859A24CCFE24AB967B2D95.mooc-2189577418-w7bnw; createSiteSource=num3; source=num3; wfwEnc=D2750DA952924268D2EFAF2BF5C71F53',
        'Referer': 'https://mooc2-ans.chaoxing.com/mooc2-ans/mycourse/stu?courseid=247076912&clazzid=111390241&cpi=285453141&enc=25e76b911b40b2141086e86df5518bd2&t=1733812604226&pageHeader=8&v=2',
        'Sec-Fetch-Dest': 'iframe',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-site',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    # 发起请求
    response = requests.get(url, cookies=cookies, headers=headers)
    lxml = etree.HTML(response.text)
    standardEnc = lxml.xpath('//input[@name="standardEnc"]/@value')[0]
    enc_work = lxml.xpath('//input[@name="enc_work"]/@value')[0]
    totalQuestionNum = lxml.xpath('//input[@name="totalQuestionNum"]/@value')[0]
    workAnswerId = lxml.xpath('//input[@name="workAnswerId"]/@value')[0]
    workRelationId = lxml.xpath('//input[@name="workRelationId"]/@value')[0]

    return standardEnc, enc_work, totalQuestionNum, workAnswerId, workRelationId


def get_link(cookies, courseId, classId, cpi, enc):
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        # 'Cookie': 'orgfid=43843; lv=0; fid=10948; _uid=254746500; uf=b2d2c93beefa90dc1d23f9590714aa1c70bf2cc17eb00acb5902b9cd8aeec433c640c069eb4014d18427660ded8a8bd46072530a316e7a7e88b83130e7eb470482d49b6a3665adad8c436d94f20ea7098487ca4cea3b44019b689bb9b927bb55d6e665fbb0dabae5e7fafd565af53bf2; _d=1733808895932; UID=254746500; vc=C6ADE5A20C30CD83C65FCAABB5624060; vc2=96902741DB87E7A66380132203C73C2A; vc3=aRLyWlqNl%2BzBOqN3Oi%2BO2XGDYWJDvsiI4J6Gz4QtjeH1BUgF7Ev3xMf%2B9bxYe4GHUEUccMBKjLb7vHYj10%2BcMA41BAMrPao55hn12yOB1qyVNXvbwbzC8CEHT%2FjOBsuyEqKlSZwNDjczI%2BvwKmWD0zTXm8K02%2FXt0Abv0y07kBc%3Ddddf061e786acd3cd5dcd8a0f8eb4f51; cx_p_token=12d390d5c9334be888b835910f23e74a; p_auth_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1aWQiOiIyNTQ3NDY1MDAiLCJsb2dpblRpbWUiOjE3MzM4MDg4OTU5MzQsImV4cCI6MTczNDQxMzY5NX0.V4gItq8gwf51vmKNvK1VHyvS-F8Liq0iy89gj_ENw60; xxtenc=4dda3795246921ee7bd70463a84b14cc; DSSTASH_LOG=C_38-UN_10404-US_254746500-T_1733808895934; spaceFid=10948; spaceRoleId=""; _industry=5; 247076912cpi=285453141; 247076912ut=s; 247076912t=1733808909841; 247076912enc=c11ef02071da834f4b07820340a9450b; k8s=1733808927.015.5177.58909; route=7644025d506561102d55bac4c90cbeeb; jrose=7A8A1D4CCC859A24CCFE24AB967B2D95.mooc-2189577418-w7bnw; createSiteSource=num3; source=num3; wfwEnc=D2750DA952924268D2EFAF2BF5C71F53',
        'Referer': 'https://mooc2-ans.chaoxing.com/mooc2-ans/mycourse/stu?courseid=247076912&clazzid=111390241&cpi=285453141&enc=c11ef02071da834f4b07820340a9450b&t=1733808909841&pageHeader=8&v=2',
        'Sec-Fetch-Dest': 'iframe',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-site',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    params = {
        'courseId': courseId,
        'classId': classId,
        'cpi': cpi,
        'ut': 's',
        # 'enc': '07bf968eaf3b35705b4835bbcfd37c92',
        'enc': enc,
    }

    response = requests.get('https://mooc1.chaoxing.com/mooc2/work/list', params=params, cookies=cookies,
                            headers=headers)
    lxml = etree.HTML(response.text)
    url = lxml.xpath('//div[@class="bottomList"]//li/@data')[0]
    return url


def get_enc(cookies, courseid, clazzid, cpi):
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        # 'Cookie': 'orgfid=43843; lv=0; fid=10948; _uid=254746500; uf=b2d2c93beefa90dc1d23f9590714aa1c70bf2cc17eb00acb5902b9cd8aeec433c640c069eb4014d18427660ded8a8bd46072530a316e7a7e88b83130e7eb470482d49b6a3665adad8c436d94f20ea7098487ca4cea3b44019b689bb9b927bb55d6e665fbb0dabae5e7fafd565af53bf2; _d=1733808895932; UID=254746500; vc=C6ADE5A20C30CD83C65FCAABB5624060; vc2=96902741DB87E7A66380132203C73C2A; vc3=aRLyWlqNl%2BzBOqN3Oi%2BO2XGDYWJDvsiI4J6Gz4QtjeH1BUgF7Ev3xMf%2B9bxYe4GHUEUccMBKjLb7vHYj10%2BcMA41BAMrPao55hn12yOB1qyVNXvbwbzC8CEHT%2FjOBsuyEqKlSZwNDjczI%2BvwKmWD0zTXm8K02%2FXt0Abv0y07kBc%3Ddddf061e786acd3cd5dcd8a0f8eb4f51; cx_p_token=12d390d5c9334be888b835910f23e74a; p_auth_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1aWQiOiIyNTQ3NDY1MDAiLCJsb2dpblRpbWUiOjE3MzM4MDg4OTU5MzQsImV4cCI6MTczNDQxMzY5NX0.V4gItq8gwf51vmKNvK1VHyvS-F8Liq0iy89gj_ENw60; xxtenc=4dda3795246921ee7bd70463a84b14cc; DSSTASH_LOG=C_38-UN_10404-US_254746500-T_1733808895934; spaceFid=10948; spaceRoleId=""; _industry=5; 247076912cpi=285453141; 247076912ut=s; 247076912t=1733808909841; 247076912enc=c11ef02071da834f4b07820340a9450b; k8s=1733808927.015.5177.58909; route=7644025d506561102d55bac4c90cbeeb; jrose=7A8A1D4CCC859A24CCFE24AB967B2D95.mooc-2189577418-w7bnw; createSiteSource=num3; source=num3; wfwEnc=D2750DA952924268D2EFAF2BF5C71F53',
        'Referer': 'https://mooc2-ans.chaoxing.com/mooc2-ans/mycourse/stu?courseid=247076912&clazzid=111390241&cpi=285453141&enc=25e76b911b40b2141086e86df5518bd2&t=1733812604226&pageHeader=8&v=2',
        'Sec-Fetch-Dest': 'iframe',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-site',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }
    # URL 和查询参数分开
    url = 'https://mooc1-1.chaoxing.com/mooc-ans/visit/stucoursemiddle'

    # 查询参数作为字典传入 params
    params = {
        'courseid': courseid,
        'clazzid': clazzid,
        'vc': '1',
        'cpi': cpi,
        'ismooc2': '1',
        'v': '2'
    }

    # 发起请求
    response = requests.get(url, params=params, cookies=cookies, headers=headers)

    lxml = etree.HTML(response.text)
    enc = lxml.xpath('//input[@name="workEnc"]/@value')[0]

    return enc


def get_base_param(cookies, course):
    headers = {
        'Accept': 'text/html, */*; q=0.01',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        # 'Cookie': 'orgfid=43843; lv=0; fid=10948; _uid=254746500; uf=b2d2c93beefa90dc1d23f9590714aa1c70bf2cc17eb00acb5902b9cd8aeec433c640c069eb4014d18427660ded8a8bd46072530a316e7a7e88b83130e7eb470482d49b6a3665adad8c436d94f20ea7098487ca4cea3b44019b689bb9b927bb55d6e665fbb0dabae5e7fafd565af53bf2; _d=1733808895932; UID=254746500; vc=C6ADE5A20C30CD83C65FCAABB5624060; vc2=96902741DB87E7A66380132203C73C2A; vc3=aRLyWlqNl%2BzBOqN3Oi%2BO2XGDYWJDvsiI4J6Gz4QtjeH1BUgF7Ev3xMf%2B9bxYe4GHUEUccMBKjLb7vHYj10%2BcMA41BAMrPao55hn12yOB1qyVNXvbwbzC8CEHT%2FjOBsuyEqKlSZwNDjczI%2BvwKmWD0zTXm8K02%2FXt0Abv0y07kBc%3Ddddf061e786acd3cd5dcd8a0f8eb4f51; cx_p_token=12d390d5c9334be888b835910f23e74a; p_auth_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1aWQiOiIyNTQ3NDY1MDAiLCJsb2dpblRpbWUiOjE3MzM4MDg4OTU5MzQsImV4cCI6MTczNDQxMzY5NX0.V4gItq8gwf51vmKNvK1VHyvS-F8Liq0iy89gj_ENw60; xxtenc=4dda3795246921ee7bd70463a84b14cc; DSSTASH_LOG=C_38-UN_10404-US_254746500-T_1733808895934; createSiteSource=num3; source=num3; wfwEnc=D2750DA952924268D2EFAF2BF5C71F53; spaceFid=10948; spaceRoleId=""; k8s=1733808902.314.11772.595545; jrose=85042667D7CE35BF20C4114C976C589B.mooc-p4-2191617661-qhqzr; route=f9c314690d8e5d436efa7770254d0199; _industry=5; 247076912cpi=285453141; 247076912ut=s; 247076912t=1733808909841; 247076912enc=c11ef02071da834f4b07820340a9450b',
        'Origin': 'https://mooc1-1.chaoxing.com',
        'Referer': 'https://mooc1-1.chaoxing.com/visit/interaction?s=4c533bd5bc337d351c1653ba4232fac4',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
        'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    data = {
        'courseType': '1',
        'courseFolderId': '0',
        'baseEducation': '0',
        'superstarClass': '',
        'courseFolderSize': '0',
    }

    response = requests.post('https://mooc1-1.chaoxing.com/mooc-ans/visit/courselistdata', cookies=cookies,
                             headers=headers, data=data)
    lxml = etree.HTML(response.text)
    li = lxml.xpath(f'//span[contains(@title, "{course}")]/ancestor::li[contains(@class, "course clearfix")][1]')[0]

    courseid = li.xpath('./@courseid')[0]
    clazzid = li.xpath('./@clazzid')[0]
    personid = li.xpath('./@personid')[0]

    return courseid, clazzid, personid


def get_extend_param(cookies, course):
    # 获取基础参数
    courseid, clazzid, cpi = get_base_param(cookies, course)

    # 获取enc
    enc = get_enc(cookies, courseid, clazzid, cpi)
    #
    # # 提取作业链接
    url = get_link(cookies, courseid, clazzid, cpi, enc)

    # 获取standardEnc等其余信息
    standardEnc, enc_work, totalQuestionNum, workAnswerId, workRelationId = get_key_param(cookies, url)
    #

    return courseid, clazzid, cpi, standardEnc, enc_work, totalQuestionNum, workAnswerId, workRelationId


def auto_save_answer(cookie, course):
    msg = ''
    if course == '习近平新时代':
        courseid, clazzid, cpi, standardEnc, enc_work, totalQuestionNum, workAnswerId, workRelationId = get_extend_param(
            cookie, course)

        # print(courseid, clazzid, cpi, standardEnc, enc_work, totalQuestionNum, workAnswerId, workRelationId)
        msg = save_info_xijinp(cookie, courseid, clazzid, cpi, standardEnc, enc_work, totalQuestionNum, workAnswerId,
                               workRelationId)

        if '失败' in msg:
            courseid, clazzid, cpi, standardEnc, enc_work, totalQuestionNum, workAnswerId, workRelationId = get_extend_param(
                cookie, course)
            # print(courseid, clazzid, cpi, standardEnc, enc_work)
            msg = save_info_hechuan_xjp(cookie, courseid, clazzid, cpi, standardEnc, enc_work, totalQuestionNum,
                                               workAnswerId, workRelationId)

    elif course == '马克思':
        courseid, clazzid, cpi, standardEnc, enc_work, totalQuestionNum, workAnswerId, workRelationId = get_extend_param(
            cookie, course)
        # print(courseid, clazzid, cpi, standardEnc, enc_work)
        msg = save_info_makesi(cookie, courseid, clazzid, cpi, standardEnc, enc_work, totalQuestionNum, workAnswerId,
                               workRelationId)

        if '失败' in msg:
            courseid, clazzid, cpi, standardEnc, enc_work, totalQuestionNum, workAnswerId, workRelationId = get_extend_param(
                cookie, course)
            msg = save_info_hechuan_makesi(cookie, courseid, clazzid, cpi, standardEnc, enc_work, totalQuestionNum,
                                               workAnswerId, workRelationId)


    elif course == '现代史':
        courseid, clazzid, cpi, standardEnc, enc_work, totalQuestionNum, workAnswerId, workRelationId = get_extend_param(
            cookie, course)
        # print(courseid, clazzid, cpi, standardEnc, enc_work)
        msg = save_info_xiandaishi(cookie, courseid, clazzid, cpi, standardEnc, enc_work, totalQuestionNum,
                                   workAnswerId,
                                   workRelationId)

        if '失败' in msg:
            courseid, clazzid, cpi, standardEnc, enc_work, totalQuestionNum, workAnswerId, workRelationId = get_extend_param(
                cookie, course)
            # print(courseid, clazzid, cpi, standardEnc, enc_work)
            msg = save_info_hechuan_xiandaishi(cookie, courseid, clazzid, cpi, standardEnc, enc_work, totalQuestionNum,
                                               workAnswerId, workRelationId)
    elif course == '毛泽东':
        courseid, clazzid, cpi, standardEnc, enc_work, totalQuestionNum, workAnswerId, workRelationId = get_extend_param(
            cookie, course)
        # print(courseid, clazzid, cpi, standardEnc, enc_work)
        msg = save_info_maogai(cookie, courseid, clazzid, cpi, standardEnc, enc_work, totalQuestionNum, workAnswerId,
                               workRelationId)

        if '失败' in msg:
            courseid, clazzid, cpi, standardEnc, enc_work, totalQuestionNum, workAnswerId, workRelationId = get_extend_param(
                cookie, course)
            msg = save_info_hechuan_maogai(cookie, courseid, clazzid, cpi, standardEnc, enc_work, totalQuestionNum,
                                               workAnswerId, workRelationId)

    elif course == '思想道德':
        courseid, clazzid, cpi, standardEnc, enc_work, totalQuestionNum, workAnswerId, workRelationId = get_extend_param(
            cookie, course)

        # print(courseid, clazzid, cpi, standardEnc, enc_work, totalQuestionNum, workAnswerId, workRelationId)
        msg = save_info_sizheng(cookie, courseid, clazzid, cpi, standardEnc, enc_work, totalQuestionNum, workAnswerId,
                               workRelationId)

        if '失败' in msg:
            courseid, clazzid, cpi, standardEnc, enc_work, totalQuestionNum, workAnswerId, workRelationId = get_extend_param(
                cookie, course)
            # print(courseid, clazzid, cpi, standardEnc, enc_work)
            msg = save_info_hechuan_sizheng(cookie, courseid, clazzid, cpi, standardEnc, enc_work, totalQuestionNum,
                                               workAnswerId, workRelationId)

    return msg
