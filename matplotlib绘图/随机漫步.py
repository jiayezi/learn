from random import choice
from matplotlib import pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号


class RandomWalk:
    """存放随机漫步的数据"""

    def __init__(self, num=5000):
        self.num = num
        # 起点为(0, 0)
        self.x_values = [0]
        self.y_values = [0]

    def get_step(self):
        # 随机选择一个方向和距离
        direction = choice([-1, 1])
        distance = choice([0, 1, 2, 3, 4])
        # 确定移动到的目标位置
        step = direction * distance
        return step

    def fill_walk(self):
        """计算随机漫步包含的所有点"""
        # 不断漫步，直到列表达到指定的长度
        while len(self.x_values) < self.num:
            x_step = self.get_step()
            y_step = self.get_step()
            # 拒绝原地踏步
            if x_step == 0 and y_step == 0:
                continue

            # 计算一次漫步之后的坐标
            x = self.x_values[-1] + x_step
            y = self.y_values[-1] + y_step

            # 把坐标添加到列表里
            self.x_values.append(x)
            self.y_values.append(y)


rw = RandomWalk()
rw.fill_walk()

# 设置样式
plt.style.use('fast')

# 第一个返回值是图表对象，第二个返回值是自动化的坐标布局管理器。图表宽度27英寸，高度15英寸，每英寸72个点，所以图表的像素就是1944*1080。
fig, ax = plt.subplots(figsize=(27, 15), dpi=72)
# 绘制散点图
ax.scatter(rw.x_values, rw.y_values, s=15, c=range(rw.num), cmap=plt.cm.Blues)

# 再绘制起点和终点
# ax.scatter(0, 0, color=(0, 1, 0), s=100)
# ax.scatter(rw.x_values[-1], rw.y_values[-1], color=(1, 0, 0), s=100)

# 设置每个坐标轴的取值范围
# ax.axis([0, 1, 0, 1])

# 设置标题和坐标轴标签
ax.set_title('随机漫步', fontsize=24)
ax.set_xlabel('东西方向', fontsize=18)
ax.set_ylabel('南北方向', fontsize=18)
# 设置刻度标记的字号
ax.tick_params(axis='both', labelsize=14)

# 隐藏坐标轴
ax.get_xaxis().set_visible(False)
ax.get_yaxis().set_visible(False)

# 绘制折线图
# ax.plot(rw.x_values, rw.y_values, linewidth=3)  # 参数linewidth设置线条粗细

# 保存图片
# plt.savefig('img.png')

# 查看图表
plt.show()

# 查看内置样式
# print(plt.style.available)
