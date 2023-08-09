from random import randint
from plotly.graph_objs import Bar, Layout
from plotly import offline


class Die:
    """骰子类"""

    def __init__(self, num_sides=6):
        """骰子默认6个面"""
        self.num_sides = num_sides

    def roll(self):
        """返回点数"""
        return randint(1, self.num_sides)


die1 = Die()
die2 = Die()
results = dict([(i, 0) for i in range(2, 13)])
for i in range(1000):
    results[die1.roll()+die2.roll()] += 1

# 绘制图表的数据
data = [Bar(x=list(results.keys()), y=list(results.values()))]
x_axis_config = {'title': '点数', 'dtick': 1}
y_axis_config = {'title': '频率'}
# 布局
my_layout = Layout(title='掷两个骰子1000次的结果', xaxis=x_axis_config, yaxis=y_axis_config)
# 生成图表，需要传入数据和布局对象，输出为网页文件
offline.plot({'data': data, 'layout': my_layout}, filename='d6.html')

