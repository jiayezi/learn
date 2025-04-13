"""
单样本Z检验

我收集了 150 个美国家庭的样本，发现其中 57 个家庭可以上网。
以α=5%的水平检验是否有超过 30% 的美国家庭可以上网。

原假设 H₀: p ≤ 0.30（30%及以下的美国家庭可以上网）
备择假设 H₁: p > 0.30（超过30%的美国家庭可以上网）
"""
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

# 设置字体（SimHei 支持中文）
plt.rcParams['font.family'] = 'SimHei'
# 解决负号'-'显示为方块的问题
plt.rcParams['axes.unicode_minus'] = False

# 样本数据
n = 150  # 样本量
x = 57   # 成功次数
p0 = 0.30  # 原假设比例
alpha = 0.05  # 显著性水平

# 计算样本比例
p_hat = x / n
# 计算标准误差
se = np.sqrt(p0 * (1 - p0) / n)
# 计算Z统计量
z = (p_hat - p0) / se
# 计算右尾 P 值
p_value = 1 - stats.norm.cdf(z)
# 计算临界值（右尾）
z_critical = stats.norm.ppf(1 - alpha)
# 输出结果
print(f"样本比例 phat: {p_hat:.4f}")
print(f"标准误差 SE: {se:.4f}")
print(f"Z 统计量: {z:.4f}")
print(f"p值: {p_value:.4f}")

# 判断是否拒绝原假设
if p_value < alpha:
    print("拒绝原假设：超过30%的美国家庭可以上网。")
else:
    print("无法拒绝原假设：没有足够证据支持超过30%的美国家庭可以上网。")

# 可视化
z_range = np.linspace(-4, 4, 500)
y = stats.norm.pdf(z_range)
plt.figure(figsize=(10, 6))
plt.plot(z_range, y, label='标准正态分布', color='skyblue')
# 显著性区域填充（右尾）
plt.fill_between(z_range, y, where=(z_range > z_critical), color='red', alpha=0.3, label='拒绝域')
# 标记Z统计量
plt.axvline(z, color='orange', linestyle='--', label=f'Z统计量: {z:.2f}')
# 标记临界Z值
plt.axvline(z_critical, color='green', linestyle=':', label=f'临界值: {z_critical:.2f}')
# 图形设置
plt.title(f'单样本Z检验的Z分布图（α = {alpha}）')
plt.xlabel('Z值')
plt.ylabel('概率密度')
plt.legend()
plt.grid()
plt.tight_layout()
plt.show()
