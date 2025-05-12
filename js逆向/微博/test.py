import json
cookies_lst = open('cookies.json' , 'r').read()
print(json.loads(cookies_lst))