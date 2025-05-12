import re

ques = '<img width="700px" height="390px" src="https://fb.fbstatic.cn/api/tarzan/images/180f419a52ad01e.png?width=700" />'
img_url = re.findall('src="(.*?)"', ques)[0]
print(img_url)
ques = re.sub('<img(.*?)/>', ques, img_url)
print(ques)
