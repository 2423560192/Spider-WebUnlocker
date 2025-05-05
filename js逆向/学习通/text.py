import requests

cookies = {
    'orgfid': '43843',
    'lv': '0',
    'fid': '10948',
    '_uid': '254746500',
    'uf': 'b2d2c93beefa90dc1d23f9590714aa1c70bf2cc17eb00acb5902b9cd8aeec433c640c069eb4014d18427660ded8a8bd46072530a316e7a7e88b83130e7eb470482d49b6a3665adad8c436d94f20ea7098487ca4cea3b44019b689bb9b927bb55d6e665fbb0dabae5e7fafd565af53bf2',
    '_d': '1733808895932',
    'UID': '254746500',
    'vc': 'C6ADE5A20C30CD83C65FCAABB5624060',
    'vc2': '96902741DB87E7A66380132203C73C2A',
    'vc3': 'aRLyWlqNl%2BzBOqN3Oi%2BO2XGDYWJDvsiI4J6Gz4QtjeH1BUgF7Ev3xMf%2B9bxYe4GHUEUccMBKjLb7vHYj10%2BcMA41BAMrPao55hn12yOB1qyVNXvbwbzC8CEHT%2FjOBsuyEqKlSZwNDjczI%2BvwKmWD0zTXm8K02%2FXt0Abv0y07kBc%3Ddddf061e786acd3cd5dcd8a0f8eb4f51',
    'cx_p_token': '12d390d5c9334be888b835910f23e74a',
    'p_auth_token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1aWQiOiIyNTQ3NDY1MDAiLCJsb2dpblRpbWUiOjE3MzM4MDg4OTU5MzQsImV4cCI6MTczNDQxMzY5NX0.V4gItq8gwf51vmKNvK1VHyvS-F8Liq0iy89gj_ENw60',
    'xxtenc': '4dda3795246921ee7bd70463a84b14cc',
    'DSSTASH_LOG': 'C_38-UN_10404-US_254746500-T_1733808895934',
    'spaceFid': '10948',
    'spaceRoleId': '""',
    '_industry': '5',
    '247076912cpi': '285453141',
    '247076912ut': 's',
    '247076912t': '1733808909841',
    '247076912enc': 'c11ef02071da834f4b07820340a9450b',
    'k8s': '1733808927.015.5177.58909',
    'route': '7644025d506561102d55bac4c90cbeeb',
    'jrose': '7A8A1D4CCC859A24CCFE24AB967B2D95.mooc-2189577418-w7bnw',
    'createSiteSource': 'num3',
    'source': 'num3',
    'wfwEnc': 'D2750DA952924268D2EFAF2BF5C71F53',
}

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    # 'Cookie': 'orgfid=43843; lv=0; fid=10948; _uid=254746500; uf=b2d2c93beefa90dc1d23f9590714aa1c70bf2cc17eb00acb5902b9cd8aeec433c640c069eb4014d18427660ded8a8bd46072530a316e7a7e88b83130e7eb470482d49b6a3665adad8c436d94f20ea7098487ca4cea3b44019b689bb9b927bb55d6e665fbb0dabae5e7fafd565af53bf2; _d=1733808895932; UID=254746500; vc=C6ADE5A20C30CD83C65FCAABB5624060; vc2=96902741DB87E7A66380132203C73C2A; vc3=aRLyWlqNl%2BzBOqN3Oi%2BO2XGDYWJDvsiI4J6Gz4QtjeH1BUgF7Ev3xMf%2B9bxYe4GHUEUccMBKjLb7vHYj10%2BcMA41BAMrPao55hn12yOB1qyVNXvbwbzC8CEHT%2FjOBsuyEqKlSZwNDjczI%2BvwKmWD0zTXm8K02%2FXt0Abv0y07kBc%3Ddddf061e786acd3cd5dcd8a0f8eb4f51; cx_p_token=12d390d5c9334be888b835910f23e74a; p_auth_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1aWQiOiIyNTQ3NDY1MDAiLCJsb2dpblRpbWUiOjE3MzM4MDg4OTU5MzQsImV4cCI6MTczNDQxMzY5NX0.V4gItq8gwf51vmKNvK1VHyvS-F8Liq0iy89gj_ENw60; xxtenc=4dda3795246921ee7bd70463a84b14cc; DSSTASH_LOG=C_38-UN_10404-US_254746500-T_1733808895934; spaceFid=10948; spaceRoleId=""; _industry=5; 247076912cpi=285453141; 247076912ut=s; 247076912t=1733808909841; 247076912enc=c11ef02071da834f4b07820340a9450b; k8s=1733808927.015.5177.58909; route=7644025d506561102d55bac4c90cbeeb; jrose=7A8A1D4CCC859A24CCFE24AB967B2D95.mooc-2189577418-w7bnw; createSiteSource=num3; source=num3; wfwEnc=D2750DA952924268D2EFAF2BF5C71F53',
    'Referer': 'https://mooc1.chaoxing.com/mooc2/work/list?courseId=247076912&classId=111390241&cpi=285453141&ut=s&enc=07bf968eaf3b35705b4835bbcfd37c92',
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



response = requests.get('https://mooc1-1.chaoxing.com/mooc-ans/visit/stucoursemiddle?courseid=247076912&clazzid=111390241&vc=1&cpi=285453141&ismooc2=1&v=2',  cookies=cookies, headers=headers , verify=False)

print(response.text)