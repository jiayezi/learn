import urllib.request
import json
import jsonpath
"""
# 下载json
url = 'https://dianying.taobao.com/cityAction.json?activityId&_ksTS=1675564031766_104&jsoncallback=jsonp105&action=cityAction&n_s=new&event_submit_doGetAllRegion=true'
headers = {
    'accept': 'text/javascript, application/javascript, application/ecmascript, application/x-ecmascript, */*; q=0.01',
    'accept-language': 'zh-CN,zh;q=0.9',
    'bx-v': '2.2.3',
    'cookie': 'cna=faA5HI9IrywCAXWw//4WIAIr; t=65c406c31c54888e618d42eeeb292783; thw=cn; cookie2=19d1bfef90acdf24db39e5e721c502d1; v=0; _tb_token_=ebe5a1e907343; tb_city=510100; tb_cityName="s8m2vA=="; l=fBQ_b7PHTGme5sOvBO5Bnurza7792IRb4sPzaNbMiIEGa6ZFtFi4pNCeKBU2SdtjgTCxketz_ANlDdLHR3AgCc0c07kqm0WS3xvtaQtJe; isg=BGNjVQtBBJUy48jMN6dAFcGw8qcNWPeaBr8PQZXADEI51IP2HSqc6g8KzqRa9E-S',
    'referer': 'https://dianying.taobao.com/',
    'sec-ch-ua': '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest'}
request = urllib.request.Request(url=url, headers=headers)
response = urllib.request.urlopen(request)
content = response.read().decode('utf-8')
content = content.split('(')[1].split(')')[0]
print(content)

with open(r'E:\库\桌面\淘票.json', 'wt', encoding='utf-8') as f:
    f.write(content)
"""

# 提取json里的部分数据
with open('E:/库/桌面/淘票.json', encoding='utf-8') as f:
    obj = json.load(f)
    city_list = jsonpath.jsonpath(obj, '$..regionName')
    print(city_list)
    print(len(city_list))
