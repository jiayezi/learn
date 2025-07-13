import json
import re


def clean_content(raw_text):
    # 去除 "# 来源文章" 标记
    raw_text = re.sub(r'# 来源地址:.*', '', raw_text)

    # 去除 markdown 分割线
    raw_text = re.sub(r'^---$', '', raw_text, flags=re.MULTILINE)

    # 去除反引号代码块标记，包括 ``` 和 ```markdown
    raw_text = re.sub(r'```(?:markdown)?\n?', '', raw_text, flags=re.IGNORECASE)

    return raw_text.strip()


def parse_markdown_qa_single_turn(input_file_list):
    content = ''
    for input_file in input_file_list:
        with open(input_file, 'rt', encoding='utf-8') as f:
            content += f.read() + '\n\n'

    content_cleaned = clean_content(content)

    # 匹配所有问答对（Markdown格式）
    qa_blocks = re.findall(r'### 问\s*(.*?)\n+### 答\s*(.*?)(?=\n### 问|\Z)', content_cleaned, re.DOTALL)

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


input_file_list = ['output/dataset_gpt-4o 神话.md','output/dataset_gpt-4o 本质.md','output/dataset_gpt-4o 文化.md']
parsed = parse_markdown_qa_single_turn(input_file_list)
output_file = f'output/train_single_{len(parsed)}.json'
save_to_json(parsed, output_file)
print(f"✅ 单轮问答格式转换完成：{output_file}")

# todo 多轮问答格式转换

# 解析后要检查生成的 JSON 文件中是否还有“###”，如果有的话，说明原始 Markdown 中还有错误的格式，导致部分问答对未处理。
