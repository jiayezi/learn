"""
单样本Z检验

一家饮料公司声称每瓶饮料的平均容量是 500 ml，总体标准差σ是已知的，为 5 ml。现在，质量检验员对这批饮料随机抽取了样本容量数据（n = 30），想要以α=5%的水平检验该批产品是否偏离了标称容量，即是否不等于 500 ml。

原假设 H₀：μ = 500（样本均值等于总体均值）
备择假设 H₁：μ ≠ 500（样本均值不等于总体均值）
显著性水平 α：0.05（双尾测试）
"""
import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt

# 设置字体（SimHei 支持中文）
plt.rcParams['font.family'] = 'SimHei'
# 解决负号'-'显示为方块的问题
plt.rcParams['axes.unicode_minus'] = False

# 参数设定
mu_0 = 500             # 原假设下的总体均值
sigma = 5              # 已知的总体标准差
alpha = 0.05           # 显著性水平

# 假设抽样得到的样本数据
sample = np.array([498, 502, 501, 500, 499, 497, 503, 504, 499, 501,
                   500, 498, 502, 500, 499, 498, 502, 503, 501, 500,
                   499, 500, 501, 502, 503, 500, 497, 498, 499, 501])

# 样本均值
sample_mean = np.mean(sample)
n = len(sample)
# Z检验统计量计算
z_score = (sample_mean - mu_0) / (sigma / np.sqrt(n))
# 双尾检验：计算p值
p_value = 2 * (1 - norm.cdf(abs(z_score)))
# 临界值（双尾）
z_critical = norm.ppf(1 - alpha / 2)

# 输出结果
print(f"样本均值: {sample_mean:.2f}")
print(f"Z值: {z_score:.4f}")
print(f"临界值 (alpha=0.05): ±{z_critical:.4f}")
print(f"p值: {p_value:.4f}")

# 判断是否拒绝原假设
if p_value < alpha:
    print("结论：拒绝原假设，认为样本均值显著地不同于500ml。")
else:
    print("结论：不拒绝原假设，认为样本均值与500ml没有显著差异。")

# 可视化
# 生成标准正态分布的x轴范围
x = np.linspace(-4, 4, 500)
y = norm.pdf(x, 0, 1)
# 绘图
plt.figure(figsize=(10, 6))
plt.plot(x, y, label='标准正态分布', color='skyblue')
# 显著性区域填充（双尾）
plt.fill_between(x, y, where=(x < -z_critical), color='red', alpha=0.3, label='拒绝域（左）')
plt.fill_between(x, y, where=(x > z_critical), color='red', alpha=0.3, label='拒绝域（右）')
# 绘制Z值
plt.axvline(z_score, color='orange', linestyle='--', label=f'Z值 = {z_score:.4f}')
# 绘制临界值
plt.axvline(z_critical, color='red', linestyle=':', label=f'临界值 = ±{z_critical:.4f}')
plt.axvline(-z_critical, color='red', linestyle=':')

# 添加图例和标题
plt.title('单样本Z检验（双尾）')
plt.xlabel('Z值')
plt.ylabel('概率密度')
plt.legend()
plt.grid()
plt.show()
