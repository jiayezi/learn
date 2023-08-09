import urllib.request
import urllib.parse


def create_request(page, city):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'}
    base_url = 'http://www.kfc.com.cn/kfccda/ashx/GetStoreList.ashx?op=cname'
    data = {'cname': city, 'pid': '', 'pageIndex': page, 'pageSize': '10'}
    data = urllib.parse.urlencode(data).encode('utf-8')
    request = urllib.request.Request(url=base_url, data=data, headers=headers)
    return request


def get_content(request):
    response = urllib.request.urlopen(request)
    content = response.read().decode('utf-8')
    return content


def download(content, i):
    with open(f'E:\\库\\桌面\\肯德基餐厅_{i}.json', 'wt', encoding='utf-8') as f:
        f.write(content)


if __name__ == '__main__':
    city = input('city:')
    start = int(input('start:'))
    end = int(input('end:'))
    for i in range(start, end + 1):
        request = create_request(i, city)
        content = get_content(request)
        download(content, i)
