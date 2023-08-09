from random import randint
import matplotlib.pyplot as plt


class Die:
    """骰子类"""

    def __init__(self, num_sides=6):
        """骰子默认6个面"""
        self.num_sides = num_sides

    def roll(self):
        """返回点数"""
        return randint(1, self.num_sides)


plt.style.use('_mpl-gallery')

# 生成数据
die1 = Die()
die2 = Die()
results = dict([(i, 0) for i in range(2, 13)])
for i in range(1000):
    results[die1.roll()+die2.roll()] += 1

fig, ax = plt.subplots()
ax.bar(list(results.keys()), list(results.values()), width=0.5)

# lim设置坐标轴范围，ticks设置刻度标记
ax.set(xlim=(1, 13), xticks=range(2, 13),
       ylim=(0, 200), yticks=range(10, 200, 10))


ax.tick_params(axis='both', labelsize=14)

plt.show()
