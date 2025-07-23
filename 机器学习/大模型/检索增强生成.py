import os
import pickle
import re
import faiss
from sentence_transformers import SentenceTransformer
from transformers import AutoTokenizer, AutoModelForCausalLM
from modelscope.hub.snapshot_download import snapshot_download


def clean_content(raw_text):
    """ 清理原始文本内容，去除不必要的标记和格式"""
    # 去除 "# 来源文章" 标记
    raw_text = re.sub(r'# 来源地址:.*', '', raw_text)
    # 去除 markdown 分割线
    raw_text = re.sub(r'^---$', '', raw_text, flags=re.MULTILINE)
    # 去除反引号代码块标记，包括 ``` 和 ```markdown
    raw_text = re.sub(r'```(?:markdown)?\n?', '', raw_text, flags=re.IGNORECASE)
    return raw_text.strip()


def parse_markdown_qa_single_turn(input_file_list):
    """ 解析 Markdown 文件，提取问答对 """
    content = ''
    for input_file in input_file_list:
        with open(input_file, 'rt', encoding='utf-8') as f:
            content += f.read() + '\n\n'

    content_cleaned = clean_content(content)

    # 提取所有问答对，(question, answer) 二元组列表
    qa_pairs = re.findall(r'### 问\s*(.*?)\n+### 答\s*(.*?)(?=\n### 问|\Z)', content_cleaned, re.DOTALL)

    return [f"问：{q.strip()}\n答：{a.strip()}" for q, a in qa_pairs]


# 指定数据集文件
model_name = "gpt-4.1"
input_file_list = [f'output/dataset_{model_name} 神话.md', f'output/dataset_{model_name} 本质.md', f'output/dataset_{model_name} 文化.md']

# 下载模型到本地
# 指定模型名称和下载路径
# model_id = 'Qwen/Qwen3-Embedding-0.6B'
# cache_dir = 'D:/models/Qwen3-Embedding-0.6B'
# snapshot_download(model_id, cache_dir=cache_dir)

# 指定模型路径
# embeddings_name = "Qwen3"
# EMBED_MODEL = "D:/models/Qwen3-Embedding-0.6B"
embeddings_name = "bge-large-zh"
EMBED_MODEL = "D:/models/bge-large-zh"
LLM_MODEL = "D:/models/Qwen3-0.6B"

# 定义索引和向量的存储路径
INDEX_PATH = f"output/faiss_index_bge_{embeddings_name}.idx"  # 向量索引结构
EMBED_PATH = f"output/doc_embeddings_{embeddings_name}.pkl"  # 文档向量
DOC_PATH = f"output/doc_texts_{embeddings_name}.pkl"  # 文档文本

# 加载 Embedding 模型
print('加载 Embedding 模型')
embedding_model = SentenceTransformer(EMBED_MODEL)
# print("embedding模型最大输入长度（token 数）:", embedding_model.tokenizer.model_max_length)

# 加载 LLM 模型
print('加载 LLM 模型')
tokenizer = AutoTokenizer.from_pretrained(LLM_MODEL)
llm = AutoModelForCausalLM.from_pretrained(LLM_MODEL, torch_dtype="auto", device_map="auto")

# 如果索引和向量文件都存在，则直接加载
if os.path.exists(INDEX_PATH) and os.path.exists(EMBED_PATH) and os.path.exists(DOC_PATH):
    print("📦 加载缓存的向量库和索引...")
    # 加载文档向量
    with open(EMBED_PATH, "rb") as f:
        doc_embeddings = pickle.load(f)
    # 加载文档文本
    with open(DOC_PATH, "rb") as f:
        documents = pickle.load(f)
    # 加载索引
    index = faiss.read_index(INDEX_PATH)
else:
    print('📄 加载原始文档数据...')
    documents = parse_markdown_qa_single_turn(input_file_list)
    # documents = [
    #     "“菩提”在佛教里有“不再提起”的意思，因此“菩提祖师”可以理解为“不要提起你的老师”或“不提祖师”。孙悟空的师父预见到他会闯下大祸，因此一直告诫他不要提及自己的师承，以免祸事牵连到师父头上。",
    #     "我认为龙的造型象征着“集大成之相，集百家之长”，代表龙族从地球动物中汇集众多优点后的集体共识。它是一种精神图腾，表达了包容万象、融合智慧的理念，而不是一种具体生物形象。",
    #     "翅膀是精灵族最重要的身份特征，不同的翅膀象征着他们不同的能力、身份和地位。翅膀不仅外形各异，还承载着希望、梦想与责任，是精灵们自我认同和追求的重要象征。",
    #     "我认为灵魂本质上是一种用于转生，保存和传输人类完整意识讯息的道具。它是连接旧载体和新载体之间的临时载体，可以帮助将精神意识信息从一个身体转移到另一个，就像两台电脑之间用优盘传递数据一样。",
    # ]
    print(f"✅ 成功加载段落数: {len(documents)}")

    print('🔍 开始计算向量...')
    doc_embeddings = embedding_model.encode(documents, convert_to_tensor=True, normalize_embeddings=True)
    print(f"✅ 成功计算段落向量: {doc_embeddings.shape}")

    print('📚 构建 FAISS 索引...')
    embedding_dim = doc_embeddings.shape[1]
    index = faiss.IndexFlatIP(embedding_dim)
    index.add(doc_embeddings.cpu().numpy())

    # 保存向量和索引
    faiss.write_index(index, INDEX_PATH)
    with open(EMBED_PATH, "wb") as f:
        pickle.dump(doc_embeddings, f)
    with open(DOC_PATH, "wb") as f:
        pickle.dump(documents, f)
    print("💾 向量和索引已保存")

# RAG 查询与生成
def rag_query(user_query, top_k=5):
    # 对用户问题生成向量
    query_embedding = embedding_model.encode([user_query], normalize_embeddings=True)

    # 从向量库中检索相似文档
    scores, indices = index.search(query_embedding, top_k)
    relevant_docs = [documents[i] for i in indices[0]]

    # 拼接提示词
    context = "\n\n".join([f"{i+1}. {doc}" for i, doc in enumerate(relevant_docs)])
    prompt = f"""请你扮演一个博学多才的史学家和文学家，假设你写过很多记载远古历史、社会现状和文化的文章。请根据以下信息回答读者问题。

以下是可能与读者问题相关的参考信息：
{context}

读者问题：{user_query}"""

    # 查看完整提示词
    with open('output/prompt.txt', 'wt', encoding='utf-8') as f:
        f.write(prompt)

    # 构造对话格式
    messages = [{"role": "user", "content": prompt}]
    text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True, enable_thinking=False)
    inputs = tokenizer([text], return_tensors="pt").to(llm.device)

    outputs = llm.generate(**inputs, max_new_tokens=1024, do_sample=True, temperature=0.7)
    answer = tokenizer.decode(outputs[0][inputs['input_ids'].shape[1]:], skip_special_tokens=True)
    return answer.strip()

# 使用
print('请输入你的问题（输入exit退出）：')
while True:
    query = input("👦用户：")
    if query.lower() in ["exit", "quit", "退出"]:
        break
    response = rag_query(query)
    print("💬 AI：", response)
    print("--------------------------------------------------")
