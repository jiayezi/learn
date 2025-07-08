import json
import os
import requests
from bs4 import BeautifulSoup
import time
import pymysql
from openai import OpenAI


with open('config.json') as f:
    cfg = json.load(f)

# 全局参数
CHUNK_SIZE = 800  # 每段最多 800 字
SLEEP_TIME = 1    # 每篇文章之间休眠时间
processed_urls_file = "processed_urls.txt"  # 已处理的网址列表

# api_key = cfg['DEEPSEEK_API_KEY']
# base_url="https://api.deepseek.com"
# model="deepseek-chat"
# output_file = "dataset_deepseek.md"
base_url="https://api.laozhang.ai/v1"
api_key = cfg['OpenAI_API_KEY']
model="gpt-4o"
output_file = "dataset_gpt-4o.md"


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

    # 估算需要多少段，确保每段不超过max_chars。(先对文章分成2组，检查每组是否超过800个字，如果超过了，就分成3组，继续检查，以此类推，直到每组不超过800字)
    num_chunks = 2
    while total_len / num_chunks > max_chars:
        num_chunks += 1
    approx_len = total_len // num_chunks

    paragraphs = [p.strip() for p in text.split("\n") if p.strip()]
    chunks = []
    current = ""

    for i, para in enumerate(paragraphs):
        if len(current) + len(para) + 50 <= approx_len:  # 50 是一个安全边界，避免段落过长
            current += para + "\n"
        else:
            chunks.append(current.strip())
            current = para + "\n"

            # ✅ 智能提前终止判断（比如要拆分成3组，如果chunks列表中已经有两组数据了，就直接把剩下的文本当成最后一组，这种判断可避免在特殊情况下多拆分一次）
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
    chunks_num = len(chunks)
    for i, chunk in enumerate(chunks):
        print(f'[处理片段] {i + 1}/{chunks_num}: {chunk[:50] + '...'}')  # 打印片段前50个字符
        messages.append({"role": "user", "content": f"【文章片段开始】\n{chunk}\n【文章片段结束】"})
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            stream=False,           # 静态数据处理关闭流式输出，更方便直接获取完整结果。
            temperature = 1,        # 控制生成多样性。增加模型生成内容的多样性和创造性，有助于问答表达多样、答案更饱满自然。(使用gpt-4o时，temperature达到1.3会出现乱码)
            top_p=1,                # 控制词汇采样范围。 保持为1，控制随机性的主要用 temperature
            presence_penalty=0.0,   # 设置为正值会鼓励模型不要一味重复已有内容，稍微鼓励输出更多不同信息
            frequency_penalty=0.0,  # 不抑制重复（因为问答结构重复是正常的）
            max_tokens = 4096       # 设置为 2048 或更高，以免回答被截断
        )
        reply = response.choices[0].message.content.strip()
        messages.append({"role": "assistant", "content": reply})
        all_output.append(reply)
    return all_output

# 主处理逻辑
def save_dataset(urls, output_path):
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
            print(f"✅ 完成: {url}\n")
            time.sleep(SLEEP_TIME)
    print(f"\n🎉 所有文章处理完成，数据已保存到：{output_path}")



# 构建数据库连接信息
connection = pymysql.connect(
    host=cfg['db_host'],
    port=cfg['db_port'],
    user=cfg['db_user'],
    password=cfg['db_password'],
    database=cfg['db_name'],
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor  # 返回字典类型结果
)

# 初始化 OpenAI 客户端
client = OpenAI(api_key=api_key, base_url=base_url)

# 读取系统提示词
with open('system_prompt.md', "rt", encoding="utf-8") as f:
    system_prompt = f.read().strip()

# SQL 获取某个分类的所有文章链接
sql = """SELECT CONCAT('https://jiayezi.cn/archives/', p.ID) AS post_url
        FROM wp_posts p
        JOIN wp_term_relationships tr ON p.ID = tr.object_id
        JOIN wp_term_taxonomy tt ON tr.term_taxonomy_id = tt.term_taxonomy_id
        JOIN wp_terms t ON tt.term_id = t.term_id
        WHERE p.post_status = 'publish'
          AND p.post_type = 'post'
          AND tt.taxonomy = 'category'
          AND t.name = '神话'
          order by p.ID
          """

# 执行查询
with connection:
    with connection.cursor() as cursor:
        cursor.execute(sql)
        result = cursor.fetchall()
        article_urls = [row['post_url'] for row in result]

save_dataset(article_urls[:1], output_file)
