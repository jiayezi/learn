import requests
from lxml import etree

# 爬取网站：https://so.gushiwen.cn/user/login.aspx?from=http://so.gushiwen.cn/user/collect.aspx
# 观察到，__VIEWSTATE，__VIEWSTATEGENERATOR，code，这3个是变化的量
# 查看网页源码，搜索“__VIEWSTATE“和“__VIEWSTATEGENERATOR”，这两个变量在源码中

# 获取网页源码
url = 'https://so.gushiwen.cn/user/login.aspx?from=http://so.gushiwen.cn/user/collect.aspx'
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'}
response = requests.get(url=url, headers=headers)
content = response.text

# 解析源码，获取“__VIEWSTATE“和“__VIEWSTATEGENERATOR”的值
tree = etree.HTML(content)
viewstate = tree.xpath('//*[@id="__VIEWSTATE"]/@value')[0]
viewstate_generator = tree.xpath('//*[@id="__VIEWSTATEGENERATOR"]/@value')[0]

# 获取验证码图片
code_url = 'https://so.gushiwen.cn' + tree.xpath('//*[@id="imgCode"]/@src')[0]
# 使用session，使两次访问请求为同一个请求
session = requests.session()
response_code = session.get(code_url)
with open('code.jpg', 'wb') as f:
    f.write(response_code.content)

# 查看下载的图片，手动输入验证码
code_value = input('验证码：')

# 登陆
post_url = 'https://so.gushiwen.cn/user/login.aspx?from=http%3a%2f%2fso.gushiwen.cn%2fuser%2fcollect.aspx'
post_data = {'__VIEWSTATE': viewstate,
             '__VIEWSTATEGENERATOR': viewstate_generator,
             'from': 'http://so.gushiwen.cn/user/collect.aspx',
             'email': '1601235906@qq.com',
             'pwd': '435646463462462ertger45645',
             'code': code_value,
             'denglu': '登录'}
# 使用session，使两次访问请求为同一个请求
post_response = session.get(url=post_url, headers=headers, data=post_data)
with open('me.html', 'wt') as f:
    f.write(post_response.text)
