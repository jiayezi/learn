import json

def parse_dialogue(file_path):
    with open(file_path, 'rt', encoding='utf-8') as file:
        content = file.read()

    dialogues = content.strip().split('\n\n')
    parsed_data = []

    for dialogue in dialogues:
        lines = [line.strip() for line in dialogue.split('\n') if line.strip()]
        qa_pairs = []
        i = 0
        while i < len(lines) - 1:
            if lines[i].startswith('问：') and lines[i + 1].startswith('答：'):
                question = lines[i][2:].replace('\\n', '\n').strip()
                answer = lines[i + 1][2:].replace('\\n', '\n').strip()
                qa_pairs.append([question, answer])
                i += 2
            else:
                print(f"警告：格式异常，跳过：{lines[i:i+2]}")
                i += 1  # 尝试跳过异常，防止死循环

        # 构造每一轮样本
        for turn_idx in range(len(qa_pairs)):
            history = qa_pairs[:turn_idx]
            question, answer = qa_pairs[turn_idx]
            sample = {
                "instruction": question,
                "input": "",
                "output": answer,
                "system": "",
                "history": history
            }
            parsed_data.append(sample)

    return parsed_data

def save_to_json(data, output_path):
    with open(output_path, 'wt', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=2)

# 示例调用
input_file = 'data.txt'
output_file = 'train.json'
parsed_data = parse_dialogue(input_file)
save_to_json(parsed_data, output_file)
print(f"✅ 成功保存到：{output_file}，共生成 {len(parsed_data)} 条样本")
