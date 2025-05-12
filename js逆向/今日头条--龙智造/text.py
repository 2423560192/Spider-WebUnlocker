import re
html = '123<p>的骄傲walke本头条号 的；普朗克</p>'
html = re.sub(r'<p>.*?本头条号.*?</p>', '', html)
print(html)
