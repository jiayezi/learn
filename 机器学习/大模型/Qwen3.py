import sys
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel
# from modelscope.hub.snapshot_download import snapshot_download

# https://qwenlm.github.io/blog/qwen3/

# 下载模型到本地
# 指定模型名称和下载路径
# model_id = 'Qwen/Qwen3-1.7B'
# cache_dir = 'D:/models/Qwen3-1.7B'
# snapshot_download(model_id, cache_dir=cache_dir)

model_name = "D:/models/Qwen3-1.7B"

# 加载模型和分词器
tokenizer = AutoTokenizer.from_pretrained(model_name)
# 查看最大长度限制
print(tokenizer.model_max_length)

base_model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype="auto",
    device_map="auto"
)
model = PeftModel.from_pretrained(base_model, "D:/models/lora_model")

# 对话历史记录
messages = []
# 添加系统消息
system_messages = {"role": "system", "content": '你是用户的女朋友，你需要温柔地回答用户的问题，给出建议和鼓励。你可以使用表情符号来表达情感。请注意，你的回答应该是积极的、支持性的，并且能够让用户感到被关心和理解。'}
messages.append(system_messages)
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
        max_new_tokens=2048, # 生成的最大token数
        do_sample=True, # 是否启用随机采样（非确定性生成）
        temperature=1 # 控制采样的随机性程度
    )
    output_ids = generated_ids[0][len(model_inputs.input_ids[0]):].tolist()

    # 查找是否包含 thinking 内容
    try:
        index = len(output_ids) - output_ids[::-1].index(151668)
    except ValueError:
        index = 0

    content = tokenizer.decode(output_ids[index:], skip_special_tokens=True).strip("\n")

    # 输出回复
    print("\nAI：", content)
    print('---------------------------------------------------')

    messages = messages[-10:]  # 保留最近5轮问答（user+assistant）
    # 添加AI的回复到对话历史
    messages.append({"role": "assistant", "content": content})


