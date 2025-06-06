import json

# 读取输入文件
input_path = '预训练数据集.txt'
output_path = 'pt.json'

# 创建结果列表
result = []

# 读取文件并处理
with open(input_path, 'rt', encoding='utf-8') as f:
    # 读取所有文本
    content = f.read()
    # 用空行分割文本
    documents = content.split('\n\n')
    # 转换为所需格式
    for doc in documents:
        doc_new = doc.strip().replace('答：', '').replace('\\n', '\n')
        result.append({"text": doc_new})

# 写入JSON文件
with open(output_path, 'wt', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print(f"处理完成！共处理了 {len(result)} 条数据")
