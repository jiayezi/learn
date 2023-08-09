import urllib.request
import urllib.parse
"""
# url = 'http://www.baidu.com/'
# response = urllib.request.urlopen(url)  # 访问网站，获取响应
# print(response.getcode())  # 获取状态码
# print(response.getheaders())  # 获取状态信息
# content = response.read().decode('utf-8')  # 读取响应内容
# print(content)
"""

"""
# 下载文件
img_url = 'https://picx.zhimg.com/v2-0b90d5d76806c4074b5297428423fbfa_1440w.jpg'
urllib.request.urlretrieve(img_url, 'img.jpg')
"""

"""
# 定制请求对象
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'}
url = 'http://www.baidu.com/'
request = urllib.request.Request(url=url, headers=headers)
response = urllib.request.urlopen(request)
content = response.read().decode('utf-8')
print(content)
"""

"""
# get请求，把中文参数转码之后上传
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'}
base_url = 'https://www.baidu.com/s?'
data = {'wd': '周杰伦', 'location': '中国'}
new_data = urllib.parse.urlencode(data)
url = base_url+new_data
request = urllib.request.Request(url=url, headers=headers)
response = urllib.request.urlopen(request)
content = response.read().decode('utf-8')
print(content)
"""

# post请求
headers = {'Cookie':' BAIDUID=613F9F714D9E6C7D36D37A0C70FFAC1B:FG=1; BIDUPSID=613F9F714D9E6C7D36D37A0C70FFAC1B; PSTM=1657503860; REALTIME_TRANS_SWITCH=1; FANYI_WORD_SWITCH=1; HISTORY_SWITCH=1; SOUND_SPD_SWITCH=1; SOUND_PREFER_SWITCH=1; BDUSS=zNGSjgxbk8wMTVONHRIVUJ3Z0UwSXNYLXppTDA4UEgzWWw4cE12cWVmYkVmVXRqRVFBQUFBJCQAAAAAAAAAAAEAAADgoBfyzsTS1dCh18rH5cTqAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAMTwI2PE8CNjS; BDUSS_BFESS=zNGSjgxbk8wMTVONHRIVUJ3Z0UwSXNYLXppTDA4UEgzWWw4cE12cWVmYkVmVXRqRVFBQUFBJCQAAAAAAAAAAAEAAADgoBfyzsTS1dCh18rH5cTqAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAMTwI2PE8CNjS; ZFY=7bk4lDlRHFXlIdw99e2UEB:ADtU3jmHNEfMSFaHenbHw:C; BAIDUID_BFESS=613F9F714D9E6C7D36D37A0C70FFAC1B:FG=1; MCITY=-75%3A; RT="z=1&dm=baidu.com&si=7bhl33jslkp&ss=ldi91evb&sl=3&tt=1re&bcn=https%3A%2F%2Ffclog.baidu.com%2Flog%2Fweirwood%3Ftype%3Dperf&ld=ing&ul=117l&hd=1196"; H_PS_PSSID=36551_38092_38130_37906_37990_36805_37924_38088_26350_22157_38008_37881; BA_HECTOR=a50k85000405a02lag8480001htp05k1l; BDRCVFR[feWj1Vr5u3D]=I67x6TjHwwYf0; PSINO=6; delPer=0; APPGUIDE_10_0_2=1; Hm_lvt_64ecd82404c51e03dc91cb9e8c025574=1675401630; Hm_lpvt_64ecd82404c51e03dc91cb9e8c025574=1675401697'}
url = 'https://fanyi.baidu.com/v2transapi?from=en&to=zh'
data = {'from': 'en', 'to': 'zh', 'query': 'python', 'transtype': 'realtime', 'simple_means_flag': '3',
        'sign': '477811.239938', 'token': '9dda717954a5114d9dad08d81a40b518', 'domain': 'common'}
data = urllib.parse.urlencode(data).encode('utf-8')
request = urllib.request.Request(url=url, data=data, headers=headers)
response = urllib.request.urlopen(request)
content = response.read().decode('utf-8')
print(content)








