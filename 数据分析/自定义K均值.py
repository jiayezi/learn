import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_blobs


class KMeans:
    def __init__(self, n_clusters=3, max_iter=100, tol=1e-4, random_state=None):
        """
        初始化K均值聚类器
        参数：
        n_clusters: 聚类数量（K值）
        max_iter: 最大迭代次数
        tol: 容忍度，当中心点变化小于该值时提前停止
        random_state: 随机种子，用于复现结果
        """
        self.n_clusters = n_clusters
        self.max_iter = max_iter
        self.tol = tol
        self.random_state = random_state
        self.centroids = None  # 存储聚类中心
        self.labels = None  # 存储每个样本的簇标签

    def _init_centroids(self, X):
        """随机初始化聚类中心"""
        np.random.seed(self.random_state)
        # 从数据中随机选择K个样本作为初始中心
        indices = np.random.choice(X.shape[0], self.n_clusters, replace=False)
        return X[indices]

    def _compute_distances(self, X):
        """计算每个样本到所有聚类中心的距离"""
        # 使用向量化计算所有样本到所有中心的平方距离
        # 利用广播机制：X形状(n_samples, n_features)，centroids形状(n_clusters, n_features)
        # 扩展维度后相减得到形状(n_samples, n_clusters, n_features)
        # 平方后沿特征轴求和得到形状(n_samples, n_clusters)
        distances = np.sum((X[:, np.newaxis] - self.centroids) ** 2, axis=2)
        return distances

    def fit(self, X):
        """
        训练K均值模型
        参数：
        X: 训练数据，形状为(n_samples, n_features)
        """
        # 初始化聚类中心
        self.centroids = self._init_centroids(X)

        for iteration in range(self.max_iter):
            # 计算所有样本到聚类中心的距离
            distances = self._compute_distances(X)

            # 分配样本到最近的簇（取距离最小的索引）
            new_labels = np.argmin(distances, axis=1)

            # 如果簇分配没有变化则提前终止
            if self.labels is not None and np.all(new_labels == self.labels):
                break

            self.labels = new_labels

            # 计算新的聚类中心
            new_centroids = np.zeros_like(self.centroids)
            for i in range(self.n_clusters):
                # 获取属于当前簇的所有样本
                cluster_samples = X[self.labels == i]
                if len(cluster_samples) > 0:
                    # 计算簇内样本的均值作为新的中心
                    new_centroids[i] = cluster_samples.mean(axis=0)
                else:
                    # 处理空簇：保持原中心不变（或可以重新初始化）
                    new_centroids[i] = self.centroids[i]

            # 检查中心点变化是否小于容忍度
            centroid_shift = np.sqrt(np.sum((new_centroids - self.centroids) ** 2))
            if centroid_shift < self.tol:
                break

            self.centroids = new_centroids

    def predict(self, X):
        """预测新样本的簇标签"""
        distances = self._compute_distances(X)
        return np.argmin(distances, axis=1)

    def fit_predict(self, X):
        """训练模型并预测簇标签"""
        self.fit(X)
        return self.labels


# 示例使用和可视化
if __name__ == "__main__":
    # 生成测试数据
    X, y = make_blobs(n_samples=300, centers=3, n_features=4)
    # 创建并训练模型
    kmeans = KMeans(n_clusters=3)
    kmeans.fit(X)

    # 可视化结果
    plt.figure(figsize=(10, 6))

    # # 二维数据可视化
    # plt.scatter(X[:, 0], X[:, 1], c=kmeans.labels, cmap='viridis', edgecolor='k', s=50)
    # # 绘制聚类中心
    # plt.scatter(kmeans.centroids[:, 0], kmeans.centroids[:, 1],
    #             c='red', marker='X', s=200, edgecolor='k', linewidth=1)
    #
    # plt.title("K-means Clustering Results")
    # plt.xlabel("Feature 1")
    # plt.ylabel("Feature 2")
    # plt.show()


    # t-SNE是一种专门用于高维数据可视化的降维技术
    from sklearn.manifold import TSNE

    tsne = TSNE(n_components=2, random_state=42)
    X_tsne = tsne.fit_transform(X)

    plt.scatter(X_tsne[:, 0], X_tsne[:, 1], c=kmeans.labels, cmap='viridis')

    plt.title("t-SNE Visualization of High-D Data")
    plt.show()

