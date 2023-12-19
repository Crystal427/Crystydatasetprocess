import os
import json
import re
import threading
import time
from collections import defaultdict
############################################################分割函数###

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

def split_text_marker(text, split_content):
    paragraphs = []
    punctuation = ['。', '，', '.', ',', '！', '？', '!', '?', '；', ';', '：', ':', '（', '）', '(', ')', '“', '”', '"', "'", '‘', '’', '—', '…']

    # 按特殊标记 "####" 分割文本
    sections = text.split("####")

    for section in sections:
        section_length = len(section)

        # 如果只有一段且段大小小于split_content，不进行操作
        if section_length < split_content and len(sections) == 1:
            paragraphs.append(section)
            continue

        # 如果有复数段且段大小小于split_content*1.35，合并到上一段
        if  section_length < split_content * 1.35 and paragraphs:
            paragraphs[-1] += section
            continue

        # 如果段大小大于split_content*1.35，使用原分割方法
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

############################################################文本处理###

def process_txt_file_EroCrysty(file_path, split_content, part_num, mark):
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read().replace('\n', '').replace(' ', '').replace('　', '')
    paragraphs = split_text(text, split_content)  # Use the split_text function provided earlier
    file_name = os.path.basename(file_path).replace('.txt', '')
    data = []
    for i in range(0, len(paragraphs), part_num):
        sample = {
            "id": f"{i//part_num}EroCrysty{mark}",
            "conversations": []
        }
        if i < len(paragraphs):
            # Add the first conversation entry with the title and the first paragraph
            sample["conversations"].append({
                "from": "user",
                "value": f'请你帮我写一篇小说，相关tag是"EroCrysty"，请参照下面这部分内容，续写"{paragraphs[i]}"'
            })
            if i + 1 < len(paragraphs):
                # Add the assistant's response with the second paragraph
                sample["conversations"].append({
                    "from": "assistant",
                    "value": paragraphs[i + 1]
                })

        # Add the rest of the conversations
        for j in range(2, part_num):
            if i + j < len(paragraphs):
                sample["conversations"].append({
                    "from": "user",
                    "value": "继续续写"
                })
                sample["conversations"].append({
                    "from": "assistant",
                    "value": paragraphs[i + j]
                })
        data.append(sample)
    return data



def process_txt_file_general(file_path, split_content, part_num, mark):
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read().replace('\n', '').replace(' ', '').replace('　', '')
    paragraphs = split_text(text, split_content)
    file_name = os.path.basename(file_path).replace('.txt', '')
    data = []
    for i in range(0, len(paragraphs), part_num):
        sample = {
            "id": f"{i//part_num}generalPixiv{mark}",
            "conversations": []
        }
        if i < len(paragraphs):
            # Add the first conversation entry with the title and the first paragraph
            sample["conversations"].append({
                "from": "user",
                "value": f'请你帮我写一篇小说，请参照下面这部分内容，续写"{paragraphs[i]}"'
            })
            if i + 1 < len(paragraphs):
                # Add the assistant's response with the second paragraph
                sample["conversations"].append({
                    "from": "assistant",
                    "value": paragraphs[i + 1]
                })

        # Add the rest of the conversations
        for j in range(2, part_num):
            if i + j < len(paragraphs):
                sample["conversations"].append({
                    "from": "user",
                    "value": "继续续写"
                })
                sample["conversations"].append({
                    "from": "assistant",
                    "value": paragraphs[i + j]
                })
        data.append(sample)
    return data

import os

def process_json_file(file_path, split_content, part_num, mark):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = json.load(f)

    novel_id = content["novelid"]
    conversations = content["conversations"][0]
    tags = conversations["tags"]
    description = conversations["description"]
    text = conversations["content"]
    paragraphs = split_text(text, split_content)

    # 获取文件名作为小说标题
    title = os.path.basename(file_path).split('.')[0]

    data = []
    for i in range(0, len(paragraphs), part_num):
        sample = {
            "id": f"{novel_id}jsons{mark}",
            "conversations": []
        }

        # 第一轮对话的用户请求
        if i < len(paragraphs):
            sample["conversations"].append({
                "from": "user",
                "value": f'请你帮我写一篇小说，相关tag是"{tags}"，简介是"{description}"，请参照这部分内容，续写下一部分"{paragraphs[i]}"'
            })

        # 第一轮对话的助手回答和后续对话
        for j in range(1, part_num):
            if i + j < len(paragraphs):
                if j == 1:
                    # 第一轮对话的助手回答
                    sample["conversations"].append({
                        "from": "assistant",
                        "value": paragraphs[i + j]
                    })
                else:
                    # 后续对话的用户请求和助手回答
                    sample["conversations"].append({
                        "from": "user",
                        "value": "继续续写"
                    })
                    sample["conversations"].append({
                        "from": "assistant",
                        "value": paragraphs[i + j]
                    })

        data.append(sample)
    return data

############################################################文件处理###

def generate_dataset(directory, split_content, part_num, mark):
    dataset = []
    for root, dirs, files in os.walk(directory):
        # Skip directories starting with '_'
        dirs[:] = [d for d in dirs if not d.startswith('_')]

        for file in files:
            file_path = os.path.join(root, file)
            if file.endswith('.txt'):
                # Check if the file is in a specific folder
                if 'Ero_MStock' in root.split(os.path.sep):
                    dataset.extend(process_txt_file_EroCrysty(file_path, split_content, part_num, mark))
                else:
                    dataset.extend(process_txt_file_general(file_path, split_content, part_num, mark))
            elif file.endswith('.json'):
                dataset.extend(process_json_file(file_path, split_content, part_num, mark))
    return dataset


############################################################数据集字数可视化###
def calculate_value_lengths(dataset):
    # 只计算长度至少为 100 的 'value' 字段
    return [len(conversation["value"]) for data in dataset for conversation in data["conversations"] if len(conversation["value"]) >= 100]


def generate_histogram(value_lengths, max_width=50):
    grouped_counts = defaultdict(int)
    for length in value_lengths:
        rounded_length = 100 * round(length / 100)
        grouped_counts[rounded_length] += 1

    max_count = max(grouped_counts.values(), default=0)

    histogram = ""
    for i in range(100, max(grouped_counts.keys(), default=100) + 100, 100):
        # Scale the bar length to max_width
        scaled_length = int((grouped_counts[i] / max_count) * max_width) if max_count else 0
        bar = '#' * scaled_length
        histogram += f"{i}: {bar}\n"
    
    return histogram




if __name__ == "__main__":
    directory = input("请输入文件目录的路径: ")
    split_content = int(input("请输入分段的最大字符数: "))
    part_num = int(input("请输入每个样本中最大的对话数量: "))
    part_num = part_num + 1
    mark = input("请输入标记字符串: ")
    dataset = generate_dataset(directory, split_content, part_num, mark)
    value_lengths = calculate_value_lengths(dataset)
    if value_lengths:
        print(generate_histogram(value_lengths))
    else:
        print("没有长度大于或等于 100 的数据。")

    with open(r'D:\dataset3.json', 'w', encoding='utf-8') as f:
        json.dump(dataset, f, ensure_ascii=False, indent=2)
    print("数据集已生成并保存到json文件中")
