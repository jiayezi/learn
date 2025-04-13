"""
单样本，Z检验（总体方差已知）

一家饮料公司声称每瓶饮料的平均容量是 500 ml，总体标准差σ是已知的，为 5 ml。现在，质量检验员对这批饮料随机抽取了样本容量数据（n = 30），想要以α=5%的水平检验该批产品是否偏离了标称容量，即是否不等于 500 ml。

原假设 H₀：μ = 500（样本均值等于总体均值）
备择假设 H₁：μ ≠ 500（样本均值不等于总体均值）
显著性水平 α：0.05（双尾测试）
"""
import numpy as np
from scipy.stats import norm

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

# 输出结果
print(f"样本均值: {sample_mean:.2f}")
print(f"Z值: {z_score:.4f}")
print(f"p值: {p_value:.4f}")

# 判断是否拒绝原假设
if p_value < alpha:
    print("结论：拒绝原假设，认为样本均值显著地不同于500ml。")
else:
    print("结论：不拒绝原假设，认为样本均值与500ml没有显著差异。")
