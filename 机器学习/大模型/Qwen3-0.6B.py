import sys
from transformers import AutoModelForCausalLM, AutoTokenizer

# https://qwenlm.github.io/blog/qwen3/
model_name = "D:/models/Qwen3-0.6B"

# 加载模型和分词器
tokenizer = AutoTokenizer.from_pretrained(model_name)
# 查看最大长度限制
print(tokenizer.model_max_length)

model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype="auto",
    device_map="auto"
)

# 对话历史记录
messages = []
# 添加系统消息
# system_messages = {"role": "system", "content": ''}
# messages.append(system_messages)
print("输入 'exit' 退出对话。输入 'new' 开启新对话。")

while True:
    # 多行输入
    # print("请输入多行内容，以单独一行 'end' 结束：")
    # lines = []
    # while True:
    #     line = input()
    #     if line.lower() == "end":
    #         break
    #     lines.append(line)
    # prompt = "\n".join(lines)

    prompt = input("用户：")

    if prompt.lower() in ['exit', 'quit', '退出']:
        print("已退出对话。")
        break
    if prompt == 'new':
        messages.clear()
        # messages.append(system_messages)
        print("已开启新对话。")
        continue

    # 添加用户输入到历史
    messages.append({"role": "user", "content": prompt})

    # 构造模型输入
    text = tokenizer.apply_chat_template(
        messages,
        tokenize=False, # 控制是否在应用模板后立即将文本转换为 token IDs
        add_generation_prompt=True, # 是否在对话模板末尾添加模型回复的引导符（告诉模型该生成回复了）
        enable_thinking=False # 思考模式
    )
    model_inputs = tokenizer([text], return_tensors="pt").to(model.device)

    # 模型生成回复
    generated_ids = model.generate(
        **model_inputs,
        max_new_tokens=2048, # 生成的最大token数。一个 token 可能对应多个字符，生成中文时，一个 token 可能对应一个汉字
        do_sample=True, # 是否启用随机采样（非确定性生成）
        temperature=0.7 # 控制采样的随机性程度
    )
    output_ids = generated_ids[0][len(model_inputs.input_ids[0]):].tolist()

    # 查找是否包含 thinking 内容
    try:
        index = len(output_ids) - output_ids[::-1].index(151668)
    except ValueError:
        index = 0

    thinking_content = tokenizer.decode(output_ids[:index], skip_special_tokens=True).strip("\n")
    content = tokenizer.decode(output_ids[index:], skip_special_tokens=True).strip("\n")

    # 输出回复
    print("\nAI：", content)
    print('---------------------------------------------------')
    print([content])

    messages = messages[-10:]  # 保留最近5轮问答（user+assistant）
    # 添加AI的回复到对话历史
    messages.append({"role": "assistant", "content": content})


