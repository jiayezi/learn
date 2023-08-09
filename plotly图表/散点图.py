import json
from plotly import express as px
import pandas as pd


# 提取数据
with open('data/eq_data_30_day_m1.json') as file:
    data = json.load(file)
all_eq_dicts = data['features']
mags, titles, lons, lats = [], [], [], []
for eq_dict in all_eq_dicts:
    mag = eq_dict['properties']['mag']
    title = eq_dict['properties']['title']
    lon = eq_dict['geometry']['coordinates'][0]
    lat = eq_dict['geometry']['coordinates'][1]
    mags.append(mag)
    titles.append(title)
    lons.append(lon)
    lats.append(lat)

data = pd.DataFrame(data=zip(lons, lats, titles, mags), columns=['经度', '纬度', '位置', '震级'])
data.head()

# 绘制散点图
fig = px.scatter(data, x='经度', y='纬度',  range_x=[-200, 200], range_y=[-90, 90],
                 width=1000, height=1000, title='全球地震散点图', size='震级', size_max=15, color='震级', hover_name='位置')

# fig.write_html('global_earthquakes.html')
fig.show()

