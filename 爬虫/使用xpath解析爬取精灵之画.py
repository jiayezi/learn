from lxml import etree
import urllib.request
import os

url = 'https://www.michaelbilotta.com/'
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'}
request = urllib.request.Request(url=url, headers=headers)
response = urllib.request.urlopen(request)
content = response.read().decode('utf-8')

# 解析服务器响应的文件
tree = etree.HTML(content)

# 获取想要的数据，xpath路径可以直接用浏览器的开发者工具复制
for i in range(1, 181):
    img_url = tree.xpath(f'//*[@id="sections"]/section/div[2]/div/div/div/div/div/figure[{i}]/div/a/img/@data-src')[0]
    img_name_list = tree.xpath(
        f'//*[@id="sections"]/section/div[2]/div/div/div/div/div/figure[{i}]/figcaption/div/p/text()')
    if img_name_list:
        img_name = img_name_list[0]
    else:
        img_name = img_url[img_url.rfind('/') + 1:]
        print(img_url)

    if os.path.exists(f'E:/行星鉴定记录者/图片/Michael Bilotta/michaelbilotta.com/{img_name}.jpg'):
        continue
    img_name = img_name.replace('\\', '').replace('/', '').replace(':', '：').replace('*', '').replace('?', '？').replace(
        '<', '').replace('>', '').replace('|', '')
    urllib.request.urlretrieve(img_url, f'E:/行星鉴定记录者/图片/Michael Bilotta/michaelbilotta.com/{img_name}.jpg')
