import os
import re

def remove_brackets(text):
    # 使用正则表达式去除方括号及其中文字
    pattern = r"\[[^\]]*\]"
    return re.sub(pattern, "", text)

def process_lrc_files(directory):
    # 获取目录下所有文件
    files = os.listdir(directory)

    # 存储处理后的内容
    merged_content = []

    # 遍历文件
    for file in files:
        if file.endswith(".lrc"):
            file_path = os.path.join(directory, file)
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.readlines()
                for line in content:
                    processed_line = remove_brackets(line.strip())
                    if processed_line:
                        # 将处理后的每行内容放在引号内
                        merged_content.append(f'"{processed_line}"')

    # 将合并后的内容写入输出文件
    output_file = "merged_output.txt"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("\n".join(merged_content))

    print(f"合并后的内容已保存到 {output_file} 文件中。")

# 用法示例
directory_path = r"D:\Crystal\Downloads\双子メスガキサキュバスの囁き敗北オナニーサポー"
process_lrc_files(directory_path)