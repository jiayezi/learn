"""
单样本t检验

假定灯泡寿命服从正态分布，我从一批灯泡中取50只检验寿命，计算的样本均值为1900小时，样本标准差为490小时。
以α=1%的水平检验这批灯泡的平均寿命是否是2000小时

原假设 H₀：μ = 2000
备择假设 H₁：μ ≠ 2000
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

# 设置字体（SimHei 支持中文）
plt.rcParams['font.family'] = 'SimHei'
# 解决负号'-'显示为方块的问题
plt.rcParams['axes.unicode_minus'] = False

# 给定参数
mu_0 = 2000 # 原假设均值
sample_mean = 1900  # 样本均值
sample_std = 490 # 样本标准差
n = 50 # 样本量
alpha = 0.01 # 显著性水平

# 自由度
df = n - 1
# 计算标准误差
standard_error = sample_std / np.sqrt(n)
# 计算t统计量
t_stat = (sample_mean - mu_0) / standard_error
# 双尾p值
p_value = 2 * stats.t.sf(abs(t_stat), df=df)
# 等价于
# p_value = 2 * (1 - stats.t.cdf(abs(t_stat), df=df))
# 获取临界值（双尾）
t_critical = stats.t.ppf(1 - alpha / 2, df)
# 输出结果
print(f"t统计量 = {t_stat:.4f}")
print(f"临界值 = ±{t_critical:.4f}")
print(f"p值 = {p_value:.4f}")

# 判断是否拒绝原假设
if p_value < alpha:
    print("结果：拒绝原假设，认为灯泡的平均寿命显著不等于2000小时。")
else:
    print("结果：不能拒绝原假设，灯泡的平均寿命可能为2000小时。")

# 可视化
# 生成t分布的x轴范围
x = np.linspace(-4, 4, 500)
y = stats.t.pdf(x, df)

# 绘图
plt.figure(figsize=(10, 6))
plt.plot(x, y, label=f't分布 (df={df})', color='skyblue')

# 显著性区域填充（双尾）
plt.fill_between(x, y, where=(x < -t_critical), color='red', alpha=0.3, label='拒绝域（左）')
plt.fill_between(x, y, where=(x > t_critical), color='red', alpha=0.3, label='拒绝域（右）')

# 标记t统计量
plt.axvline(t_stat, color='black', linestyle='--', label=f't统计量 = {t_stat:.2f}')

# 标记临界t值
plt.axvline(-t_critical, color='red', linestyle=':', label=f'临界值 = ±{t_critical:.2f}')
plt.axvline(t_critical, color='red', linestyle=':')

# 图形设置
plt.title(f'单样本t检验的t分布图（α = {alpha}）')
plt.xlabel('t值')
plt.ylabel('概率密度')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

