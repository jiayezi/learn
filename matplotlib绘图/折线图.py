import csv
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

dates = []
highs = []
lows = []
with open('data\\sitka_weather_2018_simple.csv') as file:
    data = csv.reader(file)
    next(data)
    for row in data:
        highs.append(int(row[5]))
        lows.append(int(row[6]))
        dates.append(row[2])

plt.style.use('fast')
fig, ax = plt.subplots()
ax.plot(dates, highs, c='red', alpha=0.5)  # 参数alpha指定透明度
ax.plot(dates, lows, c='blue', alpha=0.5)
ax.fill_between(dates, highs, lows, facecolor='blue', alpha=0.1)

# 设置标题和标签
ax.set_title('每日最高温度', fontsize=20)
ax.set_xlabel('日期', fontsize=16)
ax.set_ylabel('温度', fontsize=16)
ax.tick_params(axis='both', which='major', labelsize=14)
# ax.axis([0, 30, 0, 75])
fig.autofmt_xdate()  # 自适应标签，以免文字重叠
plt.show()

