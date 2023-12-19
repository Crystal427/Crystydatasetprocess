import os
import re

def remove_pattern_from_files(directory):
    # 定义要匹配的正则表达式
    pattern = re.compile(r'\r')

    # 遍历指定目录下的所有文件
    for filename in os.listdir(directory):
        if filename.endswith('.json'):  # 检查是否是 txt 文件
            filepath = os.path.join(directory, filename)
            with open(filepath, 'r', encoding='utf-8') as file:
                content = file.read()

            # 使用 re.sub() 替换匹配的文字
            updated_content = pattern.sub('', content)

            # 将更新后的内容写回文件
            with open(filepath, 'w', encoding='utf-8') as file:
                file.write(updated_content)

            print(f'Updated {filename}')

if __name__ == "__main__":
    directory = input("Enter the path of the directory: ")
    remove_pattern_from_files(directory)
