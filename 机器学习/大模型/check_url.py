import re

def extract_urls_from_dataset(dataset_path):
    with open(dataset_path, 'r', encoding='utf-8') as f:
        content = f.read()
    return set(re.findall(r'# 来源文章:\s*(https?://[^\s]+)', content))

def load_urls_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return set(line.strip() for line in f if line.strip())

# 路径配置
original_urls_file = 'original_urls.txt'
dataset_file = 'dataset_gpt-4o.md'
processed_urls_file = 'processed_urls.txt'

# 加载三类链接
original_urls = load_urls_from_file(original_urls_file)
dataset_urls = extract_urls_from_dataset(dataset_file)
processed_urls = load_urls_from_file(processed_urls_file)

# 计算差集
missing_in_processed = original_urls - processed_urls
missing_in_dataset = original_urls - dataset_urls
extra_in_dataset = dataset_urls - original_urls
in_processed_not_in_dataset = processed_urls - dataset_urls

# 输出报告
print(f"\n📊 链接比对结果:")
print(f"📌 原始链接数       : {len(original_urls)}")
print(f"📌 已处理链接数     : {len(processed_urls)}")
print(f"📌 数据集中链接数   : {len(dataset_urls)}")

# 1. 原始中有但未处理
if missing_in_processed:
    print(f"\n❗未处理的链接（{len(missing_in_processed)}）:")
    for url in sorted(missing_in_processed):
        print(url)

# 2. 原始中有但数据集缺失
if missing_in_dataset:
    print(f"\n⚠️ 数据集中缺失的链接（{len(missing_in_dataset)}）:")
    for url in sorted(missing_in_dataset):
        print(url)

# 3. 数据集中多出的链接
if extra_in_dataset:
    print(f"\n⚠️ 数据集中多余的链接（非原始文章）（{len(extra_in_dataset)}）:")
    for url in sorted(extra_in_dataset):
        print(url)

# 4. processed.txt 中有，但数据集中没有（可能处理失败）
if in_processed_not_in_dataset:
    print(f"\n⚠️ 标记为已处理但数据集中缺失的链接（{len(in_processed_not_in_dataset)}）:")
    for url in sorted(in_processed_not_in_dataset):
        print(url)

# 5. 完整一致
if not (missing_in_processed or missing_in_dataset or extra_in_dataset or in_processed_not_in_dataset):
    print("\n✅ 所有链接完全一致，无遗漏或冗余！")
