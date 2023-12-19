import os
import json
import re
import threading
import time

def split_text(text, split_content):
    paragraphs = []
    punctuation = ['。', '，', '.', ',', '！', '？', '!', '?', '；', ';', '：', ':', '（', '）', '(', ')', '“', '”', '"', "'", '‘', '’', '—', '…']

    # 按特殊标记 "####" 分割文本
    sections = text.split("####")

    for section in sections:
        while section:
            split_index = split_content

            # 如果当前部分长度大于或等于 split_content，寻找分割点
            if len(section) >= split_content:
                # 寻找最近的标点符号位置，但不超过128个字符
                punctuation_index = max([section[:split_index].rfind(p) for p in punctuation] + [-1])
                if punctuation_index >= 0 and split_index - punctuation_index <= 128:
                    # 如果找到标点符号，则在标点符号后分割
                    split_index = punctuation_index + 1
                # 否则直接在 split_content 位置分割

            # 添加分割后的段落
            paragraphs.append(section[:split_index])
            # 更新剩余部分
            section = section[split_index:]

    return paragraphs

def process_txt_file_EroCrysty(file_path, split_content, part_num, mark):
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read().replace('\n', '').replace(' ', '')
    paragraphs = split_text(text, split_content)
    file_name = os.path.basename(file_path).replace('.txt', '')
    data = []
    for i in range(0, len(paragraphs), part_num):
        sample = {
            "id": f"{i//part_num}EroCrysty{mark}",
            "conversations": []
        }
        for j, paragraph in enumerate(paragraphs[i:i+part_num], 1):
            if j == 1:
                sample["conversations"].append({
                    "from": "user",
                    "value": f'请你帮我写一篇小说，相关tag是"EroCrysty",请参照这部分内容，续写下一部分"{paragraph}"'
                })
            else:
                sample["conversations"].append({
                    "from": "user",
                    "value": "继续续写"
                })
                sample["conversations"].append({
                    "from": "assistant",
                    "value": paragraph
                })
        data.append(sample)
    return data

def process_txt_file_general(file_path, split_content, part_num, mark):
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read().replace('\n', '').replace(' ', '')
    paragraphs = split_text(text, split_content)
    file_name = os.path.basename(file_path).replace('.txt', '')
    data = []
    for i in range(0, len(paragraphs), part_num):
        sample = {
            "id": f"{i//part_num}Erogenral{mark}",
            "conversations": []
        }
        for j, paragraph in enumerate(paragraphs[i:i+part_num], 1):
            if j == 1:
                sample["conversations"].append({
                    "from": "user",
                    "value": f'请你帮我写一篇小说，请参照这部分内容，续写下一部分"{paragraph}"'
                })
            else:
                sample["conversations"].append({
                    "from": "user",
                    "value": "继续续写"
                })
                sample["conversations"].append({
                    "from": "assistant",
                    "value": paragraph
                })
        data.append(sample)
    return data

def process_json_file(file_path, split_content, part_num, mark):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = json.load(f)
    novel_id = content["novelid"]
    conversations = content["conversations"][0]
    tags = conversations["tags"]
    description = conversations["description"]
    text = conversations["content"]
    paragraphs = split_text(text, split_content)
    data = []
    for i in range(0, len(paragraphs), part_num):
        sample = {
            "id": f"{novel_id}jsons{mark}",
            "conversations": []
        }
        for j, paragraph in enumerate(paragraphs[i:i+part_num], 1):
            if j == 1:
                sample["conversations"].append({
                    "from": "user",
                    "value": f'请你帮我写一篇小说，相关tag是"{tags}"，简介是"{description}"，请参照这部分内容，续写下一部分"{paragraph}"'
                })
            else:
                sample["conversations"].append({
                    "from": "user",
                    "value": "继续续写"
                })
                sample["conversations"].append({
                    "from": "assistant",
                    "value": paragraph
                })
        data.append(sample)
    return data

def generate_dataset(directory, split_content, part_num, mark):
    dataset = []
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            if file.endswith('.txt'):
                # 检查文件是否在特定的文件夹内
                if 'Ero_MStock' in root.split(os.path.sep):
                    dataset.extend(process_txt_file_EroCrysty(file_path, split_content, part_num, mark))
                else:
                    dataset.extend(process_txt_file_general(file_path, split_content, part_num, mark))
            elif file.endswith('.json'):
                dataset.extend(process_json_file(file_path, split_content, part_num, mark))
    return dataset


if __name__ == "__main__":
    directory = input("请输入文件目录的路径: ")
    split_content = int(input("请输入分段的最大字符数: "))
    part_num = int(input("请输入每个样本中最大的对话数量: "))
    mark = input("请输入标记字符串: ")
    dataset = generate_dataset(directory, split_content, part_num, mark)
    with open(r'D:\dataset2.json', 'w', encoding='utf-8') as f:
        json.dump(dataset, f, ensure_ascii=False, indent=2)
    print("数据集已生成并保存到dataset.json文件中")
