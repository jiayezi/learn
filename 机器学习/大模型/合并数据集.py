import json

json_list = ['output/train_gpt-4.1_single_qa4079.json', 'output/train_gpt-4o_single_qa3609.json']

# 合并
merged_data = []
for file in json_list:
    with open(file, 'r', encoding='utf-8') as f:
        data = json.load(f)
        merged_data.extend(data)

save_path = f'output/train_gpt-4.1_and_4o_single_qa{len(merged_data)}.json'
with open(save_path, 'w', encoding='utf-8') as f:
    json.dump(merged_data, f, ensure_ascii=False, indent=2)
print(len(merged_data))

