# 测试为什么数组前端渲染为转码

from urllib.parse import *

dic = {
    'word': [12, 22],
    "key":'python',
} #预期生成连接为?word=12&word=22

print(parse_qs('word=12&word=22'))
print(urlencode(dic,doseq=True))
print(urlencode(dic))

