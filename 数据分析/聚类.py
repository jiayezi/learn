import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt


# 创建DataFrame
scores = pd.read_excel("E:/库/桌面/全科成绩.xlsx")

# 提取成绩列作为特征矩阵
features = scores.iloc[:, 3:]

# 数据标准化
scaler = StandardScaler()
scaled_features = scaler.fit_transform(features)

# # 使用肘部法则确定最佳聚类数
# inertia = []
# K = range(1, 10)
# for k in K:
#     kmeans = KMeans(n_clusters=k, random_state=42)
#     kmeans.fit(scaled_features)
#     inertia.append(kmeans.inertia_)
# # 绘制肘部法则图
# plt.figure(figsize=(8, 5))
# plt.plot(K, inertia, marker='o')
# plt.xlabel('Number of clusters')
# plt.ylabel('Inertia')
# plt.title('Elbow Method for Optimal K')
# plt.show()

# # 使用轮廓系数确定最佳聚类数
# from sklearn.metrics import silhouette_score
#
# silhouette_scores = []
# for k in range(2, 11):
#     kmeans = KMeans(n_clusters=k, random_state=42)
#     labels = kmeans.fit_predict(scaled_features)
#     score = silhouette_score(scaled_features, labels)
#     silhouette_scores.append(score)
#
# plt.figure(figsize=(8, 5))
# plt.plot(range(2, 11), silhouette_scores, marker='o')
# plt.xlabel('Number of clusters')
# plt.ylabel('Silhouette Score')
# plt.title('Silhouette Score for Optimal K')
# plt.show()


kmeans = KMeans(n_clusters=2, random_state=2)
scores['Cluster'] = kmeans.fit_predict(scaled_features)
scores.to_excel("E:/库/桌面/全科成绩聚类.xlsx")


# # 可视化聚类结果（以两科成绩为例）
# plt.figure(figsize=(8, 5))
# plt.scatter(scaled_features[:, 0], scaled_features[:, 1], c=scores['Cluster'], cmap='viridis', s=100)
# plt.xlabel('all (standardized)')
# plt.ylabel('yuwen (standardized)')
# plt.title('Student Clusters')
# plt.colorbar(label='Cluster')
# plt.show()


# 可视化结果（降维到2D后绘制）
from sklearn.decomposition import PCA

pca = PCA(n_components=2)
X_pca = pca.fit_transform(scaled_features)
plt.figure(figsize=(8, 6))
for cluster in set(scores['Cluster']):
    cluster_points = X_pca[scores['Cluster'] == cluster]
    plt.scatter(cluster_points[:, 0], cluster_points[:, 1], label=f'Cluster {cluster}')

plt.title('Student Clusters Based on Scores')
plt.xlabel('PCA Component 1')
plt.ylabel('PCA Component 2')
plt.legend()
plt.show()