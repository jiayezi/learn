import re


def clean_content(raw_text):
    # 去除 "# 来源地址" 标记
    raw_text = re.sub(r'# 来源地址:.*', '', raw_text)
    # 去除 markdown 分割线
    raw_text = re.sub(r'^---$', '', raw_text, flags=re.MULTILINE)

    # 去除反引号代码块标记，包括 ``` 和 ```markdown
    raw_text = re.sub(r'```(?:markdown)?\n?', '', raw_text, flags=re.IGNORECASE)

    return raw_text.strip()


if __name__ == "__main__":
    file_path = 'dataset_gpt-4o 本质 原始.md'
    with open(file_path, 'rt', encoding='utf-8') as f:
        content = clean_content(f.read())
    file_path_new = 'dataset_gpt-4o 本质 清理.md'
    with open(file_path_new, 'wt', encoding='utf-8') as f:
        f.write(content)
