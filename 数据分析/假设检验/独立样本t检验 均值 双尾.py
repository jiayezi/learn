"""
独立样本t检验，总体方差未知，但要求两组数据方差相等

假设你是一位数据分析师，正在分析一个 A/B 测试的结果。你所在的公司尝试在两个用户群体中测试一个新的网页设计，分别记录了他们在网站上的停留时间（单位：秒）：
A组（旧设计）
B组（新设计）
你想知道：新设计是否显著地改变了用户的平均停留时间。

原假设 H₀：两组的平均停留时间没有差异（μ₁ = μ₂）
备择假设 H₁：两组的平均停留时间有差异（μ₁ ≠ μ₂）
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

# 设置字体（SimHei 支持中文）
plt.rcParams['font.family'] = 'SimHei'
# 解决负号'-'显示为方块的问题
plt.rcParams['axes.unicode_minus'] = False

# 样本数据
group_A = np.array([122, 138, 125, 140, 125, 129, 136, 134, 128, 126])
group_B = np.array([133, 130, 145, 151, 138, 142, 132, 143, 149, 140])
alpha = 0.05  # 显著性水平

# 样本均值
mean_A = np.mean(group_A)
mean_B = np.mean(group_B)

# 样本标准差（无偏）
std_A = np.std(group_A, ddof=1)
std_B = np.std(group_B, ddof=1)

# 样本大小
n_A = len(group_A)
n_B = len(group_B)

# 合并标准差
sp = np.sqrt(((n_A - 1) * std_A**2 + (n_B - 1) * std_B**2) / (n_A + n_B - 2))

# t统计量
t_stat = (mean_A - mean_B) / (sp * np.sqrt(1/n_A + 1/n_B))

# 自由度
df = n_A + n_B - 2

# p值（双尾检验）
p_value = 2 * stats.t.sf(np.abs(t_stat), df)

# 可选：使用scipy的ttest_ind函数进行t检验
# t_stat, p_value = stats.ttest_ind(group_A, group_B)

# 获取临界值（双尾）
t_critical = stats.t.ppf(1 - alpha / 2, df)

# 输出结果
print(f"均值 A: {mean_A:.2f}, 均值 B: {mean_B:.2f}")
print(f"合并标准差: {sp:.4f}")
print(f"t 统计量: {t_stat:.4f}")
print(f"p 值: {p_value:.4f}")
print(f"临界值: ±{t_critical:.4f}")

# 判断是否拒绝原假设
if p_value < alpha:
    print("✅ 拒绝原假设：两组的平均值有显著差异")
else:
    print("❌ 无法拒绝原假设：两组的平均值没有显著差异")

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
plt.title(f'独立样本t检验的t分布图（α = {alpha}）')
plt.xlabel('t值')
plt.ylabel('概率密度')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
