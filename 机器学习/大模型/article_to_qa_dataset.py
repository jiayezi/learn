import json
import os
from urllib.parse import quote_plus
import requests
from bs4 import BeautifulSoup
import time
from sqlalchemy import create_engine, text
from openai import OpenAI


# 全局参数
CHUNK_SIZE = 800  # 每段最多 800 字
SLEEP_TIME = 1    # 每篇文章之间休眠时间
output_file = "dataset.md"
processed_urls_file = "processed_urls.txt"  # 已处理的网址列表


# 读取已处理的网址
def load_processed_urls():
    if not os.path.exists(processed_urls_file):
        return set()
    with open(processed_urls_file, "r", encoding="utf-8") as f:
        return set(line.strip() for line in f if line.strip())

# 保存新处理的网址
def save_processed_url(url):
    with open(processed_urls_file, "a", encoding="utf-8") as f:
        f.write(url + "\n")


# 从网页提取正文内容
def extract_article_text(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        content_div = soup.find("div", class_="entry-content clear")
        if not content_div:
            print(f"[跳过] 找不到正文内容: {url}")
            return ""

        text = content_div.get_text().strip()
        while "\n\n" in text:
            text = text.replace("\n\n", "\n")
        return text
    except Exception as e:
        print(f"[错误] 提取失败: {url}\n原因: {e}")
        return ""


# 将文章文本尽量平均分成多个片段，每片最多 CHUNK_SIZE 字
def split_into_chunks(text, max_chars=CHUNK_SIZE):
    total_len = len(text)
    if total_len <= max_chars:
        return [text.strip()]

    # 估算需要多少段，确保每段不超过max_chars。(先对文章分成2组，检查每组是否超过800字，如果超过了，就分成3组，继续检查，直到每组不超过800字)
    num_chunks = 2
    while total_len / num_chunks > max_chars:
        num_chunks += 1
    approx_len = total_len // num_chunks

    paragraphs = [p.strip() for p in text.split("\n") if p.strip()]
    chunks = []
    current = ""

    for i, para in enumerate(paragraphs):
        if len(current) + len(para) + 1 <= approx_len:
            current += para + "\n"
        else:
            chunks.append(current.strip())
            current = para + "\n"

            # ✅ 智能提前终止判断（比如要拆分成3组，如果chunks列表中已经有两组数据了，就直接把剩下的文本当成最后一组，这种判断可避免多拆分一次）
            if len(chunks) == num_chunks - 1:
                # 剩下的所有段落合并为最后一组
                remaining_text = "\n".join(paragraphs[i+1:]).strip()
                if remaining_text:
                    current += remaining_text
                break

    if current:
        chunks.append(current.strip())

    return chunks


# 向模型发送请求，保持上下文对话
def process_article_chunks(chunks):
    messages = [
        {"role": "system", "content": system_prompt}
    ]
    all_output = []
    for i, chunk in enumerate(chunks):
        messages.append({"role": "user", "content": f"【文章片段开始】\n{chunk}\n【文章片段结束】"})
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=messages,
            stream=False,
            temperature = 1.3
        )
        reply = response.choices[0].message.content.strip()
        messages.append({"role": "assistant", "content": reply})
        all_output.append(reply)
    return all_output

# 主处理逻辑
def save_articles(urls, output_path):
    processed = load_processed_urls()
    with open(output_path, "a", encoding="utf-8") as f:
        for idx, url in enumerate(urls, 1):
            if url in processed:
                print(f"[跳过] 已处理: {url}")
                continue
            print(f"[{idx}/{len(urls)}] 正在处理: {url}")
            article_text = extract_article_text(url)
            if not article_text:
                continue
            chunks = split_into_chunks(article_text)
            qa_outputs = process_article_chunks(chunks)
            f.write(f"# 来源文章: {url}\n")
            for qa in qa_outputs:
                f.write(qa + "\n\n")
            f.flush()  # 每篇处理完立即将缓冲区中的数据写入磁盘
            save_processed_url(url)
            print(f"✅ 完成: {url}")
            time.sleep(SLEEP_TIME)
    print(f"\n🎉 所有文章处理完成，数据已保存到：{output_path}")



with open('config.json') as f:
    cfg = json.load(f)

# 对密码进行 URL 编码（密码中包含 @ 会导致连接字符串解析错误，因为 @ 在 URL 中是保留字符，用于分隔“用户名”和“主机地址”。）
encoded_password = quote_plus(cfg['db_password'])
# 构造数据库连接 URL
db_url = f"mysql+pymysql://{cfg['db_user']}:{encoded_password}@{cfg['db_host']}:{cfg['db_port']}/{cfg['db_name']}"
# 创建引擎并执行 SQL
engine = create_engine(db_url)

# 初始化 OpenAI 客户端（DeepSeek）
api_key = cfg['DEEPSEEK_API_KEY']
client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")

# 提示词模板
system_prompt = """
你是一个语言模型助手，负责将用户提供的文章内容转化为多个高质量的问答对数据集，用于训练一个能理解用户思想体系的大语言模型。转换时请严格遵循以下要求：

1. 输出为 Markdown 格式：每组问答用 ### 问 和 ### 答 标记段落开头。所有内容保持 Markdown 风格（例如用 *斜体* 或 **加粗** 表示重点，或者用 - 分项列出信息）。每组问答结构如下：
### 问
（提问内容）

### 答
（回答内容）

2. 每组问答需涵盖文章中的一个独立概念、信息点或设定，内容密度高的段落可拆分为多组问答，确保覆盖全部关键信息。

3. 最好使用第二人称“你”提问，回答使用第一人称“我”作答，适当保留原文的说话风格。

4. 问句要自然、具体、聚焦，指向清晰；答案要尽可能充实、通顺、自然、完整、准确、符合人类常规表达习惯，适当展开表达，丰富语义信息，避免简略的回应。在不改变原意的前提下，可以适当补充上下文、扩展逻辑链条或加深解释，让答案内容更加完整饱满。

5. 问句与答案需高度匹配，确保语义衔接紧密，有利于语言模型学习正确的提问-回答对齐模式。

6. 不要更改原意、削弱原文观点或引入外部评价；所有问答均基于原文内容提取生成。

请你现在处理以下这篇文章的一部分内容（如下），并按照上述要求提取高质量问答数据。
请专注于当前提供的内容片段，完整提取其中的独立概念、信息点或设定，尽可能覆盖全部关键信息。
无需等待全文提供，每次用户将继续发送下一部分内容，请保持处理风格一致。
"""

# SQL 获取某个分类的所有文章链接
sql = """SELECT CONCAT('https://jiayezi.cn/archives/', p.ID) AS post_url
        FROM wp_posts p
        JOIN wp_term_relationships tr ON p.ID = tr.object_id
        JOIN wp_term_taxonomy tt ON tr.term_taxonomy_id = tt.term_taxonomy_id
        JOIN wp_terms t ON tt.term_id = t.term_id
        WHERE p.post_status = 'publish'
          AND p.post_type = 'post'
          AND tt.taxonomy = 'category'
          AND t.name = '神话'"""

# 执行查询
with engine.connect() as conn:
    result = conn.execute(text(sql))
    article_urls = [row['post_url'] for row in result.mappings()]

save_articles(article_urls, output_file)
