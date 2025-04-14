"""
双样本Z检验，要求总体标准差已知

假设你是一名教育研究员，想知道两所学校A和B的学生数学成绩是否有显著差异。
你从每个学校分别随机抽取了样本，并且知道总体方差（来自历史数据或官方统计）。
学校A的样本均值：mean_A = 75
学校B的样本均值：mean_B = 79
每组样本数量：n = 30
总体方差：σ1² = 38，σ2² = 36
显著性水平：α = 0.05（双尾）

零假设H₀：两组均值无显著差异，μ_A = μ_B
备择假设H₁：两组均值有显著差异，μ_A ≠ μ_B（双尾）
"""
import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt

# 设置字体（SimHei 支持中文）
plt.rcParams['font.family'] = 'SimHei'
# 解决负号'-'显示为方块的问题
plt.rcParams['axes.unicode_minus'] = False

# 给定参数
mean_A = 75
mean_B = 79
var_a = 38
var_b = 36
n_A = 30
n_B = 30
alpha = 0.05

# 计算Z值
z_score = (mean_A - mean_B) / np.sqrt((var_a / n_A) + (var_b / n_B))
# 计算 p 值（右尾）
p_value = 1 - norm.cdf(z_score)
# 双尾检验的临界值
z_critical = norm.ppf(1 - alpha/2)

# 输出结果
print(f"Z检验统计量：{z_score:.4f}")
print(f"双尾临界值：±{z_critical:.4f}")

# 判断是否拒绝零假设
if abs(z_score) > z_critical:
    print("结论：拒绝零假设，两个学校的学生均值有显著差异。")
else:
    print("结论：不拒绝零假设，两个学校的学生均值无显著差异。")

# 可视化
# 生成标准正态分布的x轴范围
x = np.linspace(-4, 4, 500)
y = norm.pdf(x, 0, 1)
# 绘图
plt.figure(figsize=(10, 6))
plt.plot(x, y, label='标准正态分布', color='skyblue')
# 显著性区域填充
plt.fill_between(x, y, where=(x < -z_critical) | (x > z_critical), color='red', alpha=0.3, label='拒绝域（双尾）')
# 绘制Z值
plt.axvline(z_score, color='orange', linestyle='--', label=f'Z值 = {z_score:.4f}')
# 绘制临界值
plt.axvline(z_critical, color='red', linestyle=':', label=f'临界值 = {z_critical:.4f}')

# 添加图例和标题
plt.title('单样本Z检验（双尾）')
plt.xlabel('Z值')
plt.ylabel('概率密度')
plt.legend()
plt.grid()
plt.show()