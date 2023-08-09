from bs4 import BeautifulSoup
import urllib.request

url = 'https://www.starbucks.com.cn/menu/'
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'Cookie': 'ZHh6ku4z=A7tZ8CCGAQAAEMAwoOTWGpFdCQ6hd-GjGettaSeqnHRDngQDBM1LB05FrV-fAXWw_wCucnyzwH8AAEB3AAAAAA|1|1|1303d3fb3bf61fc19932c00a115cc7ccc834597b',
    'Host': 'www.starbucks.com.cn',
    'Referer': 'https://www.starbucks.com.cn/',
    'sec-ch-ua': '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'}

request = urllib.request.Request(url=url, headers=headers)
response = urllib.request.urlopen(request)
content = response.read().decode('utf-8')

soup = BeautifulSoup(content, 'lxml')
# 提取class为"grid padded-3 product"的ul下面的strong标签
name_list = soup.select('ul[class="grid padded-3 product"] strong')
for name in name_list:
    print(name.get_text())
