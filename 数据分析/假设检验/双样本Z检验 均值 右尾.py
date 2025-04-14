"""
双样本Z检验，要求总体标准差已知

某公司想知道新的广告方案是否比旧方案更有效。于是随机抽取了两个独立的样本组，分别记录了广告投放后一周的日均销售额（单位：千元）：
旧广告方案样本（n1=30）：均值 = 50，已知方差 = 100
新广告方案样本（n2=35）：均值 = 54，已知方差 = 120
公司想知道新的广告是否显著提高了销售额。

原假设 H₀：新广告均值 ≤ 旧广告均值（μ₂ ≤ μ₁）
备择假设 H₁：新广告均值 > 旧广告均值（μ₂ > μ₁）
"""
from scipy.stats import norm
import numpy as np
import matplotlib.pyplot as plt

# 设置字体（SimHei 支持中文）
plt.rcParams['font.family'] = 'SimHei'
# 解决负号'-'显示为方块的问题
plt.rcParams['axes.unicode_minus'] = False

# 样本信息
x1 = 50  # 旧广告样本均值
x2 = 54  # 新广告样本均值

n1 = 30  # 旧广告样本容量
n2 = 35  # 新广告样本容量

sigma1_sq = 100  # 总体方差1
sigma2_sq = 120  # 总体方差2

# 显著性水平
alpha = 0.05

# 计算 Z 统计量
z_score = (x2 - x1) / np.sqrt(sigma1_sq / n1 + sigma2_sq / n2)
# 计算 p 值（右尾）
p_value = 1 - norm.cdf(z_score)
# 计算临界值
z_critical = norm.ppf(1 - alpha)

# 打印结果
print(f"Z值: {z_score:.4f}")
print(f"p值: {p_value:.4f}")

if p_value < alpha:
    print("拒绝原假设，说明新广告显著提高了销售额。")
else:
    print("无法拒绝原假设，说明新广告并未显著提高销售额。")

# 可视化
# 生成标准正态分布的x轴范围
x = np.linspace(-4, 4, 500)
y = norm.pdf(x, 0, 1)
# 绘图
plt.figure(figsize=(10, 6))
plt.plot(x, y, label='标准正态分布', color='skyblue')
# 显著性区域填充（右尾）
plt.fill_between(x, y, where=(x > z_critical), color='red', alpha=0.3, label='拒绝域（右）')
# 绘制Z值
plt.axvline(z_score, color='orange', linestyle='--', label=f'Z值 = {z_score:.4f}')
# 绘制临界值
plt.axvline(z_critical, color='red', linestyle=':', label=f'临界值 = {z_critical:.4f}')

# 添加图例和标题
plt.title('单样本Z检验（右尾）')
plt.xlabel('Z值')
plt.ylabel('概率密度')
plt.legend()
plt.grid()
plt.show()