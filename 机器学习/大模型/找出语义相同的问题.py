from sentence_transformers import SentenceTransformer

# 下载模型
# from huggingface_hub import snapshot_download
# snapshot_download(repo_id="BAAI/bge-large-zh", local_dir="D:/models/bge-large-zh")


import re
# 读取文本文件内容
with open("E:/语言模型训练/博客对话数据集606.txt", "rt", encoding="utf-8") as file:
    text = file.read()
# 使用正则表达式提取所有问题
questions = re.findall(r"问：(.*?)\s*答：", text, re.DOTALL)
# 去除每个问题开头和结尾的空白字符
questions = [q.strip() for q in questions]
print(f'提取到 {len(questions)} 个问题')

# 生成文本 Embedding
model = SentenceTransformer('D:/models/bge-large-zh')  # 中文效果更好
embeddings = model.encode(questions, convert_to_tensor=False, show_progress_bar=True)

# 使用 KMeans 聚类
from sklearn.cluster import KMeans
num_clusters = 900  # 你可以根据数据量调节
kmeans = KMeans(n_clusters=num_clusters, random_state=42)
labels = kmeans.fit_predict(embeddings)

# 查看每组聚类结果
import pandas as pd
df = pd.DataFrame({
    'question': questions,
    'cluster': labels
})

# 按类别分组统计数量
label_counts = df["cluster"].value_counts()
# 筛选大于2的聚类
label_counts = label_counts[label_counts > 2]
df2 = df[df["cluster"].isin(label_counts.index)]

# 保存聚类结果到 CSV 文件
df2.to_csv("E:/语言模型训练/问题的聚类结果.csv", index=False, encoding='utf-8-sig')
label_counts.to_csv("E:/语言模型训练/问题的聚类统计.csv", encoding='utf-8-sig')
