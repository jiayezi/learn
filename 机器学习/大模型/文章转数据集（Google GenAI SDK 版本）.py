import json
import os
import time
from random import randint
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading
import requests
from bs4 import BeautifulSoup
import pymysql
from google import genai
from google.genai import types

with open('config.json') as f:
    cfg = json.load(f)

# 全局参数
category_name = '文化'  # 分类名称
CHUNK_SIZE = 800  # 每段最多 800 字
SLEEP_TIME = 1    # 每篇文章之间休眠时间
original_urls_file = f'output/original_urls {category_name}.txt'
processed_urls_file = f"output/processed_urls {category_name}.txt"  # 已处理的网址列表

# API和输出文件配置
base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
api_key = cfg['Gemini_API_KEY']
model_name="gemini-2.5-flash"

output_file = f"output/dataset_{model_name} {category_name}.md"


def throttle_api_call():
    """
    限制API调用频率，确保每分钟最多CALL_LIMIT次调用。
    """
    with call_lock:
        current_time = time.time()
        # 只关心最近 60 秒内的调用次数，如果最早的一次调用发生在 60 秒前，就从列表里移除它。
        while call_timestamps and current_time - call_timestamps[0] >= CALL_INTERVAL:
            call_timestamps.pop(0)

        # 如果当前调用次数已经达到限制，就计算需要等待的时间，然后休眠。
        if len(call_timestamps) >= CALL_LIMIT:
            sleep_time = CALL_INTERVAL - (current_time - call_timestamps[0])
            print(f"[限速] 等待 {sleep_time:.1f} 秒以满足API调用限制")
            time.sleep(sleep_time+1)
            # 等待了一段时间，当前时间变了，所以再次清理一下列表中过期的调用记录。
            current_time = time.time()
            while call_timestamps and current_time - call_timestamps[0] >= CALL_INTERVAL:
                call_timestamps.pop(0)

        # 最后，记录这次调用的时间，加入调用记录列表中。
        call_timestamps.append(time.time())

def load_urls(category):
    if os.path.exists(original_urls_file):
        with open(original_urls_file, "rt", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip()]

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

    # SQL 获取某个分类的所有文章链接
    sql = f"""SELECT CONCAT('https://jiayezi.cn/archives/', p.ID) AS post_url
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
            article_urls = [row['post_url'] for row in result]

    # 保存原始链接到文件
    urls_text = "\n".join(article_urls)
    with open(original_urls_file, "wt", encoding="utf-8") as f:
        f.write(urls_text)

    return article_urls

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
    all_output = []
    chat = client.chats.create(model=model_name,
                               config=types.GenerateContentConfig(
        system_instruction=system_prompt,
        temperature=1,
        top_p=1,
        max_output_tokens=4096,
        thinking_config=types.ThinkingConfig(thinking_budget=0)))
    for i, chunk in enumerate(chunks):
        throttle_api_call()
        response = chat.send_message(f"【文章片段开始】\n{chunk}\n【文章片段结束】")
        reply = response.text.strip()
        all_output.append(reply)
    return all_output

# 处理单个文章链接
def process_single_article(url):
    if url in processed_urls:
        return None
    print(f"[处理] 正在处理: {url}")
    article_text = extract_article_text(url)
    if not article_text:
        return None
    chunks = split_into_chunks(article_text)
    qa_outputs = process_article_chunks(chunks)
    save_processed_url(url)
    time.sleep(SLEEP_TIME)  # 每篇文章之间休眠一段时间，避免请求过快
    return {"url": url, "qa_outputs": qa_outputs}

# 批量保存数据集到文件
def save_dataset(urls, output_path, max_workers):
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(process_single_article, url) for url in urls]

        with open(output_path, "a", encoding="utf-8") as f:
            for future in as_completed(futures):
                result = future.result()
                if not result:
                    continue
                with write_lock:
                    f.write(f"# 来源地址: {result['url']}\n")
                    for qa in result['qa_outputs']:
                        f.write(qa + "\n\n")
                    f.flush()
    print(f"\n🎉 所有文章处理完成，数据已保存到：{output_path}")


# 初始化 genai 客户端
client = genai.Client(api_key=api_key)

# 读取系统提示词
with open('system_prompt.md', "rt", encoding="utf-8") as f:
    system_prompt = f.read().strip()

# 请求节流控制（每分钟最多10次）
CALL_LIMIT = 10
CALL_INTERVAL = 60  # 秒
call_timestamps = []
call_lock = threading.Lock()

write_lock = threading.Lock()

processed_urls = load_processed_urls()
article_urls = load_urls(category_name)
print('已加载原始文章链接:', len(article_urls))
save_dataset(article_urls[50:], output_file, max_workers=2)

# 处理完毕后，需要检查数据集中是否出现“作者”、“文章”、“文中”、“提到”、“他认为”、“背景知识”等客观描述词，如果有的话，需要转换为更合适的描述。
# 还要检查问句中是否有“那个”、“这些”等模糊指代词，如果有的话，需要转换为更明确的描述。
# 还要检查问句中的“问”是否被写成了“筑/筴/闯/闏”这些笔画复杂、相似度高的字，否则在解析时会出现混乱。