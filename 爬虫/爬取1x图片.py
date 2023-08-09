import urllib.request
import os
from lxml import etree
"""
# 第一步，获取每张图片的详情页面的网址
url_list = []
for i in range(0, 201, 20):
    url = f'https://1x.com/backend/lm2.php?style=normal&mode=user:148395:overview:&from={i}'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cache-control': 'max-age=0',
        'cookie': '1xSession3=89a5a097bcc8fbe9a032aea2dd248ef7',
        'referer': 'https://1x.com/arcadiaman'}
    request = urllib.request.Request(url=url, headers=headers)
    response = urllib.request.urlopen(request)
    content = response.read().decode('utf8')
    tmp_list = re.findall(r'/photo/\d+/useroverview/148395', content)
    url_list.extend(tmp_list)

print(len(url_list))

with open('img_detail_url.txt', 'wt') as f:
    for s in url_list:
        f.write('https://1x.com'+s+'\n')

"""

# 第二步，访问每个图片详情页并提取信息
name_list = os.listdir(r'E:\行星鉴定记录者\图片\Michael Bilotta\1x.com arcadiaman')
title_file = ''
with open('img_detail_url.txt', 'rt') as f:
    data = f.readlines()
    counter = 0
    for url in data:
        url = url.strip()
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cache-control': 'max-age=0',
            'cookie': '1xSession3=89a5a097bcc8fbe9a032aea2dd248ef7',
            'referer': 'https://1x.com/arcadiaman'}
        request = urllib.request.Request(url=url, headers=headers)
        response = urllib.request.urlopen(request)
        counter += 1
        content = response.read().decode('utf8')
        tree = etree.HTML(content)
        title = tree.xpath('/html/head/title/text()')[0].replace(' by Michael Bilotta', '')
        title_file += f'{title}\t{url}\n'
        print(f'{counter:>3d}\t{title}\t{url}')

with open('img_title_url.txt', 'wt', encoding='utf-8') as f:
    f.write(title_file)

