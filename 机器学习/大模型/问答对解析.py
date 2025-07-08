import json
import re


def clean_content(raw_text):
    # 去除 "# 来源文章" 标记
    raw_text = re.sub(r'# 来源文章:.*', '', raw_text)

    # 去除 markdown 分割线
    raw_text = re.sub(r'^---$', '', raw_text, flags=re.MULTILINE)

    # 去除反引号代码块标记，包括 ``` 和 ```markdown
    raw_text = re.sub(r'```(?:markdown)?\n?', '', raw_text, flags=re.IGNORECASE)

    return raw_text.strip()


def parse_markdown_qa_single_turn(file_path):
    with open(file_path, 'rt', encoding='utf-8') as f:
        content = clean_content(f.read())

    # 匹配所有问答对（Markdown格式）
    qa_blocks = re.findall(r'### 问\s*(.*?)\n+### 答\s*(.*?)(?=\n### 问|\Z)', content, re.DOTALL)

    parsed_data = []

    for question, answer in qa_blocks:
        question = question.strip()
        answer = answer.strip()
        if question and answer:
            sample = {
                "instruction": question,
                "input": "",
                "output": answer,
                "system": "",
                "history": []  # 空列表，LLaMA-Factory允许为空
            }
            parsed_data.append(sample)

    return parsed_data


def save_to_json(data, output_path):
    with open(output_path, 'wt', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


# 示例用法（按需修改路径）
input_file = 'dataset_gpt-4o.md'
output_file = 'train_llama_factory_single.json'

parsed = parse_markdown_qa_single_turn(input_file)
save_to_json(parsed, output_file)
print(f"✅ 单轮问答格式转换完成，共生成 {len(parsed)} 条样本：{output_file}")
