import requests
from plotly import offline

# 获取数据
url = 'https://api.github.com/search/repositories?q=language:python&sort=stars'
# headers = {'Accept' 'application/vnd.github.v3+json'}
response = requests.get(url)
print(f'status code:{response.status_code}')
response_dict = response.json()
repo_dicts = response_dict['items']
print(f'repositories returned:{len(repo_dicts)}')

# 处理数据
stars, labels, links = [], [], []
for repo_dict in repo_dicts:
    repo_name = repo_dict['name']
    url = repo_dict['html_url']
    links.append(f'<a href="{url}">{repo_name}</a>')
    stars.append(repo_dict['stargazers_count'])

    owner = repo_dict['owner']['login']
    description = repo_dict['description']
    label = f'{owner}<br>{description}'
    labels.append(label)

# 可视化
data = [{'type': 'bar', 'x': links, 'y': stars, 'hovertext': labels,
         'marker': {'color': 'rgb(60,60,150)', 'line': {'width': 1.5, 'color': 'rgb(25,25,50)'}},
         'opacity': 0.6}]
my_layout = {'title': 'github上最受欢迎的python项目', 'titlefont': {'size': 28},
             'xaxis': {'title': '项目', 'titlefont': {'size': 24}, 'tickfont': {'size': 14}},
             'yaxis': {'title': '星星', 'titlefont': {'size': 24}, 'tickfont': {'size': 14}}}
fig = {'data': data, 'layout': my_layout}
offline.plot({'data': data, 'layout': my_layout}, filename='python_repos.html')
