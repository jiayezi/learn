import urllib.request
import urllib.parse


def create_request(start):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'}
    base_url = 'https://movie.douban.com/j/chart/top_list?type=17&interval_id=100%3A90&action=&'
    data = {'start': (start - 1) * 20, 'limit': 20}
    data = urllib.parse.urlencode(data)
    url = base_url + data
    request = urllib.request.Request(url=url, headers=headers)
    return request


def get_content(request):
    response = urllib.request.urlopen(request)
    content = response.read().decode('utf-8')
    return content


def download(content, i):
    with open(f'E:\\库\\桌面\\豆瓣_{i}.json', 'wt', encoding='utf-8') as f:
        f.write(content)


if __name__ == '__main__':
    start = int(input('start:'))
    end = int(input('end:'))
    for i in range(start, end + 1):
        request = create_request(i)
        content = get_content(request)
        download(content, i)
