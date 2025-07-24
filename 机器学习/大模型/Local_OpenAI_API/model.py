import threading
import torch
import transformers
from transformers import AutoTokenizer, AutoModelForCausalLM
from config import BASE_MODEL_PATH, LORA_MODEL_PATH

device = "cuda" if torch.cuda.is_available() else "cpu"

# 加载分词器
tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL_PATH)

# 加载基础模型
base_model = AutoModelForCausalLM.from_pretrained(
    BASE_MODEL_PATH,
    device_map="auto",
    torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32
)

# 可选加载 LoRA 权重
if LORA_MODEL_PATH:
    from peft import PeftModel
    model = PeftModel.from_pretrained(base_model, LORA_MODEL_PATH)
else:
    model = base_model

model.eval()

def generate_reply(messages, max_tokens, temperature):
    # 构造模型输入
    text = tokenizer.apply_chat_template(
        messages,
        tokenize=False, # 控制是否在应用模板后立即将文本转换为 token IDs
        add_generation_prompt=True, # 是否在对话模板末尾添加模型回复的引导符（告诉模型该生成回复了）
        enable_thinking=False # 思考模式
    )
    inputs = tokenizer(text, return_tensors="pt").to(model.device)

    # 模型生成回复
    outputs = model.generate(
        **inputs,
        max_new_tokens=max_tokens, # 生成的最大token数
        do_sample=True, # 是否启用随机采样（非确定性生成）
        temperature=temperature # 控制采样的随机性程度
    )

    reply = tokenizer.decode(outputs[0][inputs.input_ids.shape[-1]:], skip_special_tokens=True)
    return reply.strip()

def generate_stream(messages, max_tokens, temperature):
    # 构造模型输入
    text = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True,
        enable_thinking=False  # 思考模式
    )
    inputs = tokenizer(text, return_tensors="pt").to(model.device)

    # 使用 TextIteratorStreamer 进行流式生成
    streamer = transformers.TextIteratorStreamer(
        tokenizer, skip_prompt=True, skip_special_tokens=True
    )

    generation_kwargs = dict(
        **inputs,
        streamer=streamer,
        max_new_tokens=max_tokens,
        do_sample=True,
        temperature=temperature
    )

    thread = threading.Thread(target=model.generate, kwargs=generation_kwargs)
    thread.start()

    for new_text in streamer:
        yield new_text
