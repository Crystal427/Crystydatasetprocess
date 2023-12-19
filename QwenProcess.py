import os
import json

def read_txt_files(directory):
    """读取目录及子目录下的所有txt文件，并返回文件名及其内容的列表。"""
    contents = []
    for subdir, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.txt'):
                with open(os.path.join(subdir, file), 'r', encoding='utf-8') as f:
                    contents.append((file[:-4], f.read()))  # 去除.txt后缀
    return contents

def split_content(text, split_content_length):
    """根据提供的长度和规则，将内容分段。"""
    parts = []
    start = 0
    length = len(text)

    while start < length:
        end = start + split_content_length
        if end < length:
            if text[end] == '####':
                parts.append(text[start:end])
                start = end + 4  # 跳过'####'
            elif '.' in text[start:end]:
                end = text.rfind('.', start, end) + 1
                parts.append(text[start:end])
                start = end
            elif '，' in text[start:end]:
                end = text.rfind('，', start, end) + 1
                parts.append(text[start:end])
                start = end
            else:
                parts.append(text[start:end])
                start = end
        else:
            parts.append(text[start:])
            break
    return parts

def construct_dataset(files, identity_prefix, split_content_length, part_num):
    """根据提供的文件内容和规则，构建数据集。"""
    dataset = []
    count = 0
    for file_name, content in files:
        parts = split_content(content, split_content_length)
        total_parts = len(parts)
        
        for i in range(0, total_parts, part_num):
            convos = []
            if i == 0:
                convos.append({
                    "from": "user",
                    "value": f"我想写一本小说，名字是：{file_name}，节选篇章：{parts[i]}"
                })
            else:
                convos.append({"from": "user", "value": "扩写"})
                convos.append({"from": "assistant", "value": parts[i]})
            
            for j in range(i+1, min(i+part_num, total_parts)):
                convos.append({"from": "user", "value": "扩写"})
                convos.append({"from": "assistant", "value": parts[j]})
            
            dataset.append({
                "id": f"identity_{count}EroCrysty{identity_prefix}",
                "conversations": convos
            })
            count += 1
    return dataset

def main():
    directory = input("请输入要读取的目录: ")
    identity_prefix = input("请输入id字段的后缀: ")
    split_content_length = int(input("请输入分段的文字数量: "))
    part_num = int(input("请输入最大段数: "))

    files = read_txt_files(directory)
    dataset = construct_dataset(files, identity_prefix, split_content_length, part_num)

    with open('dataset.json', 'w', encoding='utf-8') as f:
        json.dump(dataset, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    main()
