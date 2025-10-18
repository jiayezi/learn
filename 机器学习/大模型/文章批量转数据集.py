import json
import os
import time
from random import randint
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading
from bs4 import BeautifulSoup
import pymysql
from openai import OpenAI


with open('config.json') as f:
    cfg = json.load(f)

# 全局参数
category_name = '文化'  # 分类名称
CHUNK_SIZE = 800  # 每段最多 800 字
SLEEP_TIME = 1    # 每篇文章之间休眠时间
processed_urls_file = f"output/processed_urls {category_name}.txt"  # 已处理的文章ID列表

# API和输出文件配置（gpt-4o速度快，答案丰富，价格贵。deepseek速度慢，答案较少，价格便宜）
# api_key = cfg['DEEPSEEK_API_KEY']
# base_url="https://api.deepseek.com"
# model_name="deepseek-chat" # deepseek提取的数据集质量很低，容易胡乱编造。

base_url="https://api.laozhang.ai/v1"
api_key = cfg['OpenAI_API_KEY']
model_name= "gpt-4.1"

# base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
# api_key = cfg['Gemini_API_KEY']
# model_name="gemini-2.5-flash"

output_file = f"output/dataset_{model_name} {category_name}.md"

def load_articles(category):
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

    # SQL 获取某个分类的所有文章内容
    sql = f"""SELECT p.ID, post_title, post_content
            FROM wp_posts p
            JOIN wp_term_relationships tr ON p.ID = tr.object_id
            JOIN wp_term_taxonomy tt ON tr.term_taxonomy_id = tt.term_taxonomy_id
            JOIN wp_terms t ON tt.term_id = t.term_id
            WHERE p.post_status = 'publish'
              AND p.post_type = 'post'
              AND tt.taxonomy = 'category'
              AND t.name = '{category}'
              order by p.ID
              """
    # 执行查询
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(sql)
            result = cursor.fetchall()
            # 返回文章ID、标题和内容的列表
            articles = [{'id': row['ID'], 'title': row['post_title'], 'content': row['post_content']} for row in result]

    return articles

# 读取已处理的文章ID
def load_processed_urls():
    if not os.path.exists(processed_urls_file):
        return set()
    with open(processed_urls_file, "r", encoding="utf-8") as f:
        return set(line.strip() for line in f if line.strip())

# 保存新处理的文章ID
def save_processed_url(article_id):
    with open(processed_urls_file, "a", encoding="utf-8") as f:
        f.write(article_id + "\n")


# 从数据库获取文章内容
def get_article_content(article):
    """从文章对象中提取并清理内容"""
    content = article['content']
    if not content:
        print(f"[跳过] 文章内容为空: {article['title']} (ID: {article['id']})")
        return ""
    
    # 清理HTML标签和多余空白
    soup = BeautifulSoup(content, "html.parser")
    text = soup.get_text().strip()
    
    # 清理多余的换行符
    while "\n\n" in text:
        text = text.replace("\n\n", "\n")
    
    return text


# 将文章文本尽量平均分成多个片段，每片最多 CHUNK_SIZE 字
def split_into_chunks(text, max_chars=CHUNK_SIZE):
    total_len = len(text)
    if total_len <= max_chars:
        return [text.strip()]

    # 估算需要多少段，确保每段不超过max_chars。(先对文章分成2组，检查每组是否超过max_chars个字，如果超过了，就分成3组，继续检查，以此类推，直到每组不超过max_chars字)
    num_chunks = 2
    while total_len / num_chunks > max_chars:
        num_chunks += 1
    approx_len = (total_len // num_chunks) + randint(-50, 50)  # 增加随机性，避免同一篇文章每次分割结果完全一样

    paragraphs = [p.strip() for p in text.split("\n") if p.strip()]
    chunks = []
    current = ""

    for i, para in enumerate(paragraphs):
        if len(current) + len(para) + randint(40, 60) <= approx_len:  # 添加一个随机安全边界，避免段落过长
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
    # chunks_num = len(chunks)
    for i, chunk in enumerate(chunks):
        # print(f'[处理片段] {i + 1}/{chunks_num}: {chunk[:50] + '...'}')  # 打印片段前50个字符
        messages.append({"role": "user", "content": f"【文章片段开始】\n{chunk}\n【文章片段结束】"})
        response = client.chat.completions.create(
            model=model_name,
            messages=messages,
            stream=False,           # 静态数据处理关闭流式输出，更方便直接获取完整结果。
            temperature = 0.9,      # 控制生成多样性。(使用gpt-4o时，temperature达到1.3会出现乱码)
            top_p=1,                # 控制词汇采样范围。 保持为1，控制随机性的主要用 temperature
            presence_penalty=0.0,   # 设置为正值会鼓励模型不要一味重复已有内容，稍微鼓励输出更多不同信息
            frequency_penalty=0.0,  # 不抑制重复（因为问答结构重复是正常的）
            max_tokens = 2048       # 设置为 2048 或更高，以免回答被截断
        )
        reply = response.choices[0].message.content.strip()
        messages.append({"role": "assistant", "content": reply})
        all_output.append(reply)
    return all_output

# 处理单篇文章
def process_single_article(article):
    article_id = str(article['id'])
    if article_id in processed_urls:
        return None
    print(f"[处理] 正在处理: {article['title']} (ID: {article_id})")
    article_text = get_article_content(article)
    if not article_text:
        return None
    chunks = split_into_chunks(article_text)
    qa_outputs = process_article_chunks(chunks)
    save_processed_url(article_id)
    time.sleep(SLEEP_TIME)  # 每篇文章之间休眠一段时间，避免请求过快
    return {"id": article_id, "title": article['title'], "qa_outputs": qa_outputs}

# 批量保存数据集到文件
def save_dataset(articles, output_path, max_workers):
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(process_single_article, article) for article in articles]

        with open(output_path, "a", encoding="utf-8") as f:
            for future in as_completed(futures):
                result = future.result()
                if not result:
                    continue
                with write_lock:
                    f.write(f"# 文章标题: {result['title']} (ID: {result['id']})\n")
                    for qa in result['qa_outputs']:
                        f.write(qa + "\n\n")
                    f.flush()
    print(f"\n🎉 所有文章处理完成，数据已保存到：{output_path}")


# 初始化 OpenAI 客户端
client = OpenAI(api_key=api_key, base_url=base_url)
# 读取系统提示词
with open('system_prompt.md', "rt", encoding="utf-8") as f:
    system_prompt = f.read().strip()

write_lock = threading.Lock()

processed_urls = load_processed_urls()
articles = load_articles(category_name)
print('已加载文章数量:', len(articles))
save_dataset(articles, output_file, max_workers=10)

# 处理完毕后，需要检查数据集中是否出现“作者”、“文章”、“文中”、“他认为”、“背景知识”等客观描述词，如果有的话，需要转换为更合适的描述。
# 还要检查问句中是否有“那个”、“这些”等模糊指代词，如果有的话，需要转换为更明确的描述。
# 还要检查问句中的“问”是否被写成了“筑/筴/闯/闏”这些笔画复杂、相似度高的字，否则在解析时会出现混乱。