import json
from random import randint
from openai import OpenAI


with open('config.json') as f:
    cfg = json.load(f)

# 全局参数
CHUNK_SIZE = 800  # 每段最多 800 字

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

output_file = f"output/dataset_{model_name}_temp1.md"


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
    chunks_num = len(chunks)
    for i, chunk in enumerate(chunks):
        print(f'[处理片段] {i + 1}/{chunks_num}: {chunk[:50] + '...'}')  # 打印片段前50个字符
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

# 保存数据集到文件
def save_dataset(article_text, output_path):
    with open(output_path, "a", encoding="utf-8") as f:
        chunks = split_into_chunks(article_text)
        qa_outputs = process_article_chunks(chunks)
        for qa in qa_outputs:
            f.write(qa + "\n\n")
    print(f"\n🎉 处理完成，数据已保存到：{output_path}")



# 初始化 OpenAI 客户端
client = OpenAI(api_key=api_key, base_url=base_url)
# 读取系统提示词
with open('system_prompt.md', "rt", encoding="utf-8") as f:
    system_prompt = f.read().strip()


article_text = """
人类的意识由讯息构成，把一个人的精神意识讯息完整的转移到一个新的载体里复活，这样的人就会携带有完整的前世记忆来到这个世界，这就是转生。而这个过程中，有个最重要的科技道具，就是灵魂。

灵魂这个词在文学中的含义是某件事物的本质和精粹，比如某个酱料是某个食物的灵魂。对人而言，灵魂其实就是一些用来转生，保存人类完整意识讯息的道具。这是一种在旧载体和新载体之间传输精神意识信息的临时载体，就好像两台电脑之间传输数据时用的优盘。

在地球上，保存人类完整意识讯息的道具是一种纳米机器人。很久以前，人类转生的时候，会有无数纳米机器人搬运这个人的精神意识信息。一个纳米机器人的空间有限，只能保存一部分信息，无数纳米机器人的集合体才能构成一个人的完整精神意识讯息。一个完整的精神意识讯息，才是一个完整的灵魂。

现在绝大多数人都没有转生的机会。
转生是由一些上古的特别矩阵条件所设置的，在很久很久以前的神话世界，人人都有转生的资格。现在大多数人都无法转生，因为轮回转生系统被纳粹藏在了深深的地下和月球内部，被他们私用。现在只有极少数被纳粹安排的转生事件，比如藏传佛教的转世灵童。

这个世界绝大多数人都没有前世，也没有下辈子，因为这个世界绝大多数人都没有灵魂。灵魂是用来转移记忆的临时载体，如果你们有灵魂，就应该有前世记忆，但是转生设备被纳粹控制着，他们不会好心帮你们保存和转移记忆。从另一个角度来说，就算你们有灵魂，转生的时候记忆也会被纳粹洗掉，没有保存前世记忆的所谓灵魂，即使转生了，也和没有灵魂的人没什么区别，就像格式化过的旧硬盘和新生产的硬盘，在使用上没有任何区别。所以，你们有没有灵魂，结果都是一样的。历史上那些孟婆汤之类的传说，不过是为了掩盖这个真相。
"""
save_dataset(article_text, output_file)

# 处理完毕后，需要检查数据集中是否出现“作者”、“文章”、“文中”、“他认为”、“背景知识”等客观描述词，如果有的话，需要转换为更合适的描述。
# 还要检查问句中是否有“那个”、“这些”等模糊指代词，如果有的话，需要转换为更明确的描述。
# 还要检查问句中的“问”是否被写成了“筑/筴/闯/闏”这些笔画复杂、相似度高的字，否则在解析时会出现混乱。