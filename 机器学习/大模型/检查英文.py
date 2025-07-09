import re


def extract_english_words(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()

        # 匹配所有连续的英文字母（大小写）
        words = re.findall(r'[a-zA-Z]+', text)

        print("匹配到的英文字词如下：")
        for word in words:
            print(word)
    except FileNotFoundError:
        print(f"文件未找到：{file_path}")
    except Exception as e:
        print(f"发生错误：{e}")


# 使用示例
if __name__ == "__main__":
    file_path = 'dataset_gpt-4o.md'
    extract_english_words(file_path)