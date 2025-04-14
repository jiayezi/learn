"""
单样本Z检验，要求总体标准差已知

某公司的网站过去的平均加载时间是 3 秒，总体标准差σ是已知的，为0.5s。
现在公司更换了服务器架构，开发团队对新系统进行了测试，随机抽取了 40 次加载时间的样本。我们想确认：加载时间有没有变慢？

原假设 H₀：μ ≤ 3（加载时间未变慢）
备择假设 H₁：μ > 3（加载时间变慢了）
"""
import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt

# 设置字体（SimHei 支持中文）
plt.rcParams['font.family'] = 'SimHei'
# 解决负号'-'显示为方块的问题
plt.rcParams['axes.unicode_minus'] = False

# 参数设定
mu_0 = 3.0  # 原假设下的均值
sigma = 0.5  # 已知的总体标准差
alpha = 0.05  # 显著性水平

# 样本数据（模拟40次加载时间）
sample = np.array([3.1, 3.2, 2.9, 3.3, 3.0, 2.8, 3.4, 3.1, 3.2, 3.0,
                   3.3, 3.5, 2.9, 3.2, 3.1, 3.0, 3.4, 3.3, 3.2, 3.1,
                   2.8, 3.0, 3.1, 3.3, 3.4, 3.2, 3.3, 3.1, 3.0, 2.9,
                   3.2, 3.3, 3.1, 3.0, 3.1, 3.2, 3.4, 3.3, 3.0, 2.9])

# 样本均值
sample_mean = np.mean(sample)
n = len(sample)
# Z检验统计量
z_score = (sample_mean - mu_0) / (sigma / np.sqrt(n))
# 右尾检验：计算p值
p_value = 1 - norm.cdf(z_score)
# 临界值（右尾）
z_critical = norm.ppf(1 - alpha)

# 输出结果
print(f"样本均值: {sample_mean:.3f}")
print(f"Z值: {z_score:.4f}")
print(f"临界值 (alpha=0.05): {z_critical:.4f}")
print(f"p值: {p_value:.4f}")

# 判断是否拒绝原假设
if p_value < alpha:
    print("结论：拒绝原假设，加载时间显著变慢了。")
else:
    print("结论：不拒绝原假设，没有证据表明加载时间变慢。")

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