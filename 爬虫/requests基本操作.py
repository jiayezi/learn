import requests

# 基本操作
# url = 'http://www.baidu.com'
# response = requests.get(url)
# # 设置编码格式
# response.encoding = 'utf-8'
# # 获取网页源码
# print(response.text)
# # 获取网址
# print(response.url)
# # 获取二进制数据
# print(response.content)
# # 获取相应的状态码
# print(response.status_code)
# # 获取相应头
# print(response.headers)

# get请求
# url = 'https://www.baidu.com/s?'
# headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'}
# params = {'wd': 'python'}
# response = requests.get(url, params=params, headers=headers)
# response.encoding = 'utf-8'
# content = response.text
# print(content)

# post请求
url = 'https://fanyi.baidu.com/v2transapi?from=en&to=zh'
headers = {'Accept-Language': 'zh-CN,zh;q=0.9',
'Acs-Token': '1675757127445_1675768377543_8wAHyB0PXIhrUzniB1WKB6OqBp7jYOEFShe/byEIrglSfLGY0mlVn6DogZP492w2tOEHRKmaxvRFMHoUhirw0QiU5aLAsb4zdSiqfULpdTJru2WqfgnHhqyHChus4CnAD3Poy0HGtYJfGRDLTgtgxdtysrgAHS+JLUaFYudxn75Vzs9605hk8iNAndIblJMbCU0MuAynoP7/qpBqxWxeL5j8l6p4GVGPdr/lXT52luctMPoEwV70XbjzRPC19Jy2oUnt4t/FnX1vL3O68StalqhoTOrQ2rt501GJEAXa7/NB/+zIQoCTMji7ZUXh4Ry1',
'Connection': 'keep-alive',
'Content-Length': '114',
'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
'Cookie': 'BAIDUID=26B4D84B8F91E48944503C338B28125E:FG=1; BDUSS=k4aGVhTH5ZMUFZflNkanVzWHpqeDJKRWZuNWd1MVU3NjRIMERabDBZclN-ck5qRVFBQUFBJCQAAAAAAAAAAAEAAADgoBfyzsTS1dCh18rH5cTqAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAANJxjGPScYxjVk; BDUSS_BFESS=k4aGVhTH5ZMUFZflNkanVzWHpqeDJKRWZuNWd1MVU3NjRIMERabDBZclN-ck5qRVFBQUFBJCQAAAAAAAAAAAEAAADgoBfyzsTS1dCh18rH5cTqAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAANJxjGPScYxjVk; APPGUIDE_10_0_2=1; REALTIME_TRANS_SWITCH=1; FANYI_WORD_SWITCH=1; HISTORY_SWITCH=1; SOUND_SPD_SWITCH=1; SOUND_PREFER_SWITCH=1; BIDUPSID=26B4D84B8F91E48944503C338B28125E; PSTM=1675488648; BAIDUID_BFESS=26B4D84B8F91E48944503C338B28125E:FG=1; Hm_lvt_64ecd82404c51e03dc91cb9e8c025574=1675426202,1675491686,1675685139,1675766959; Hm_lpvt_64ecd82404c51e03dc91cb9e8c025574=1675768377',
'Host': 'fanyi.baidu.com',
'Origin': 'https://fanyi.baidu.com',
'Referer': 'https://fanyi.baidu.com/',
'sec-ch-ua': '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
'sec-ch-ua-mobile': '?0',
'sec-ch-ua-platform': '"Windows"',
'Sec-Fetch-Dest': 'empty',
'Sec-Fetch-Mode': 'cors',
'Sec-Fetch-Site': 'same-origin',
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
'X-Requested-With': 'XMLHttpRequest'}
data = {'from': 'en',
'to': 'zh',
'query': 'eye',
'simple_means_flag': '3',
'sign': '67056.386753',
'token': '9712e0d255a2abfe01360d9665039966',
'domain': 'common'}
response = requests.post(url=url, data=data, headers=headers)
content = response.json()
print(content)


"""
如果电脑打开了代理工具，使用requests访问外网或https协议的网站会出现SSLError错误，有3种解决方式：
1.关闭翻墙工具，
2.在翻墙工具的设置中开启“指定协议”，
3.通过设置代理来访问，因为本地开启梯子后，梯子默认会把整个系统的流量指向电脑的某个端口，然后再由梯子进行接收往外转发，所以我们只需要在Python的requests请求中设置代理，即可将脚本请求转向梯子。但是这个代理并非梯子节点的代理，而是系统的代理。打开梯子后，在设置中找到对应的代理端口，然后加在代码中即可。
"""
# 在开启翻墙工具的情况下，通过设置代理来访问外网
# url = 'https://youtube.com'
# headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'}
# proxy = {'http': '127.0.0.1:7890', 'https': '127.0.0.1:7890'}
# response = requests.get(url, headers=headers, proxies=proxy)
# response.encoding = 'utf-8'
# content = response.text
# print(content)





