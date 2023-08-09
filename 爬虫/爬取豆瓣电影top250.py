import requests
import parsel

headers = {'User-Agent': 'Mozilla/5.0  (windows-NT-10.0; win64; x64) ApplewebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Sefari/537.36'}

j = 0
actor1 = []
actor2 = []
year = []
country = []
movie_type = []

for i in range(0,255,25):
    url = 'https://movie.douban.com/top250?start='+str(i)
    response = requests.get(url,headers=headers)
    response.encoding = response.apparent_encoding
    selector = parsel.Selector(response.text)
    lis = selector.css('#content>div>div.article>ol>li>div>div.pic>a>img::attr(src)').getall()
    title = selector.css('#content>div>div.article>ol>li>div>div.info>div.hd>a>span:nth-child(1)::text').getall()
    director_info = selector.xpath('//*[@id="content"]/div/div[1]/ol/li/div/div[2]/div[2]/p[1]/text()[1]').getall()
    movie_info = selector.xpath('//*[@id="content"]/div/div[1]/ol/li/div/div[2]/div[2]/p[1]/text()[2]').getall()

    for director in director_info:
        director = director.strip().replace('\xa0\xa0\xa0','').replace('...','').replace('导演: ','').split('主演: ')
        if len(director)>1:
            actor1.append(director[0])
            actor2.append(director[1])
        else:
            actor1.append(director[0])
            actor2.append('无')

    for detail in movie_info:
        detail = detail.strip().split('\xa0/\xa0')
        year.append(detail[0])
        country.append(detail[1])
        movie_type.append(detail[2])

    for k in range(len(lis)):
        print(title[k]+'\t'+actor1[k+j*25]+'\t'+actor2[k+j*25]+'\t'+year[k+j*25]+'\t'+country[k+j*25]+'\t'+movie_type[k+j*25])
        # print(title[k], actor1[k + j * 25], actor2[k + j * 25], year[k + j * 25], country[k + j * 25],movie_type[k + j * 25])

    j+=1






