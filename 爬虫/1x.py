import os
import random
import requests
from lxml import etree
import re
import json
import time

"""
下载1x.com上的图片，有些图片不适合未成年人看，所以要登陆账号再获取请求标头
"""

user_id = '30892'
user_name = 'paradowski'

# 使用 requests.Session 来重用连接
session = requests.Session()

headers = {
    "Accept": "application/xml, text/xml, */*; q=0.01",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Cookie": "__stripe_mid=5374592c-6079-4c89-8ea1-6748c3199feb25f25c; 1xSession3=030360206ac19110b227238e5628e466; __stripe_sid=1f4e4934-d874-41df-b313-3135b6cacb0d966c07",
    "Priority": "u=1, i",
    "Referer": "https://1x.com/paradowski/overview",
    "Sec-Ch-Ua": "\"Not/A)Brand\";v=\"8\", \"Chromium\";v=\"126\", \"Google Chrome\";v=\"126\"",
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": "\"Windows\"",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest"
}


# 第一步，模拟翻页，获取所有图片的详情页网址
# url = f'https://1x.com/backend/lm2.php'
# url_list = []
# pattern = rf"location.href='(/photo/\d+/useroverview/{user_id})'"
# params = {'style': 'normal', 'mode': f'user:{user_id}:overview:'}
# has_more = True
# offset = 0
# while has_more:
#     params['from'] = offset
#     try:
#         response = session.get(url, params=params, headers=headers)
#         response.encoding = 'utf-8'
#         content = response.text
#         tmp_list = re.findall(pattern, content)
#         url_list.extend(tmp_list)
#
#         # 打印进度信息
#         print(f"Fetched {len(tmp_list)} URLs from page starting at {offset}.")
#
#         # 判断是否还有更多数据
#         if len(tmp_list) < 20:
#             has_more = False
#
#         offset += 20
#         # 使用随机延迟
#         time.sleep(random.uniform(1, 3))
#     except requests.RequestException as e:
#         print(f"Request failed at offset {offset}: {e}")
#         break
#
# print(len(url_list))
#
# url_detail_list = ['https://1x.com' + s for s in url_list]
# with open('img_detail_page_url.json', 'w') as f:
#     json.dump(url_detail_list, f, ensure_ascii=False, indent=4)


# 定义一个函数来清理文件名
def clean_filename(filename):
    return re.sub(r'[<>:"/\\|?*]', '_', filename)


# 第二步，访问每个图片详情页并提取信息
save_dir = 'E:/行星鉴定记录者/图片/Leszek Paradowski'
if not os.path.exists(save_dir):
    os.makedirs(save_dir)

with open('img_detail_page_url.json', encoding='utf-8') as f:
    urls = json.load(f)
    for counter, url in enumerate(urls):
        response = session.get(url, headers=headers)
        response.encoding = 'utf-8'
        content = response.text
        tree = etree.HTML(content)

        # 提取标题
        title = tree.xpath('/html/head/title/text()')[0]
        if title.startswith('Untitled'):
            title = title+f'_{counter:0>3d}'
        title = clean_filename(title)

        # 提取图片链接
        img_url = tree.xpath('//*[@oncontextmenu="return false;"]/@src')[0]

        img_path = os.path.join(save_dir, f"{title}.jpg")

        # 检查是否存在相同的文件名，若存在则在文件名后添加数字
        file_index = 1
        while os.path.exists(img_path):
            img_path = os.path.join(save_dir, f"{title} {file_index}.jpg")
            file_index += 1

        # 下载并保存图片
        img_response = session.get(img_url, headers=headers, stream=True)
        if img_response.status_code == 200:
            with open(img_path, 'wb') as img_file:
                for chunk in img_response.iter_content(1024):
                    img_file.write(chunk)
            print(counter, f"Downloaded: {title}")
        else:
            print(counter, f"Failed to download image from {img_url}")
        # 使用随机延迟
        time.sleep(random.uniform(1, 5))


