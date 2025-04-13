"""
单样本t检验

某种元件的寿命 (以小时为单位)服从正态分布，我抽取16只元件测出的寿命如下:
280，159，101，212，379，224，179，264，222，362，168，149， 250，260，170，485。
以α=5%的水平检验这种元件的平均寿命是否大于225小时。

原假设 H₀：μ ≤ 225（元件平均寿命小于等于225小时）
备择假设 H₁：μ > 225（元件平均寿命大于225小时）
"""
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

# 设置字体（SimHei 支持中文）
plt.rcParams['font.family'] = 'SimHei'
# 解决负号'-'显示为方块的问题
plt.rcParams['axes.unicode_minus'] = False

# 样本数据
data = [280, 159, 101, 212, 379, 224, 179, 264, 222, 362, 168, 149, 250, 260, 170, 485]
# 参数
alpha = 0.05 # 显著性水平
n = len(data) # 样本量
popmean = 225 # 原假设均值

# # 在有样本数据的情况下可以使用单样本t检验函数计算t统计量和右尾p值
# t_stat, p_two_tailed = stats.ttest_1samp(data, popmean)
# p_one_tailed = p_two_tailed / 2 if t_stat > 0 else 1 - p_two_tailed / 2

# 自由度
df = n - 1
# 计算样本均值
sample_mean = np.mean(data)
# 样本标准差（使用 n-1 作为自由度）
sample_std = np.std(data, ddof=1)
standard_error = sample_std / np.sqrt(n)
# 计算t统计量
t_stat = (sample_mean - popmean) / standard_error
# 计算右尾 p 值
p_one_tailed = 1 - stats.t.cdf(t_stat, df)
# 临界t值（右尾）
t_critical = stats.t.ppf(1 - alpha, df)
# 输出结果
print(f"样本均值: {sample_mean:.2f}")
print(f"样本标准差: {sample_std:.2f}")
print(f"t统计量: {t_stat:.4f}")
print(f"临界t值 (alpha=0.05): {t_critical:.4f}")
print(f"右尾p值: {p_one_tailed:.4f}")

if p_one_tailed < alpha:
    print("拒绝原假设：数据支持元件平均寿命大于225小时")
else:
    print("不能拒绝原假设：没有足够证据表明元件平均寿命大于225小时")

# 可视化
x = np.linspace(-4, 4, 500)
y = stats.t.pdf(x, df)

plt.figure(figsize=(10, 6))
plt.plot(x, y, label=f't分布 (df={df})', color='skyblue')

# 显著性区域填充（右尾）
plt.fill_between(x, y, where=(x > t_critical), color='red', alpha=0.3, label='拒绝域')
# 标记t统计量
plt.axvline(t_stat, color='black', linestyle='--', label=f't统计量 = {t_stat:.2f}')
# 标记临界t值
plt.axvline(t_critical, color='red', linestyle=':', label=f'临界值 = {t_critical:.2f}')

# 图形设置
plt.title(f'单样本t检验的t分布图（α = {alpha}）')
plt.xlabel('t 值')
plt.ylabel('概率密度')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
