import requests
from lxml import etree
import re
import json
import time

user_id = '148395'
user_name = 'arcadiaman'

# 第一步，获取每张图片的详情页面的网址
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cache-control': 'max-age=0',
    'cookie': '1xSession3=89a5a097bcc8fbe9a032aea2dd248ef7',
    'referer': f'https://1x.com/{user_name}'}

url = f'https://1x.com/backend/lm2.php?'
params = {'style': 'normal', 'mode': f'user:{user_id}:overview:'}
url_list = []

for i in range(0, 201, 20):
    params['from'] = i
    response = requests.get(url, params=params, headers=headers)
    response.encoding = 'utf-8'
    content = response.text
    tmp_list = re.findall(rf'/photo/\d+/useroverview/{user_id}', content)
    url_list.extend(tmp_list)
    time.sleep(1)

print(len(url_list))

url_dict = {'url': 'https://1x.com' + s for s in url_list}

with open('img_detail_page_url.json', 'w') as f:
    json.dump(url_dict, f)


# 第二步，访问每个图片详情页并提取信息
img_title_url_dict = {}
with open('img_detail_page_url.json', encoding='utf-8') as f:
    url_dict = json.load(f)
    urls = url_dict['url']
    counter = 0
    for url in urls:
        response = requests.get(url, headers=headers)
        response.encoding = 'utf-8'
        counter += 1
        content = response.text
        tree = etree.HTML(content)
        title = tree.xpath('//*[@id="photodata-2843318"]/div[1]/div[1]/text()')[0]
        img_url = tree.xpath('//*[@id="img-2843320"]/@src')[0]
        if title is None:
            title = f'Untitled {counter:>3d}'
        img_title_url_dict[title] = img_url

with open('img_title_url_dict.json', 'w') as f:
    json.dump(img_title_url_dict, f)
