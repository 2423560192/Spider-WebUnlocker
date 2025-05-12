import requests

url = 'http://dms-app.changan.com.cn:9001/dms/20230909/3b0d723645785acf655b53c6994a6bf8.js'

resp = requests.get(url)
print(resp.text)