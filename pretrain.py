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

def process_txt_file_EroCrysty(file_path, split_content):
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read().replace('\n', '').replace(' ', '').replace('　', '').replace('@@Copys@@', '').replace(' ', '')
    paragraphs = split_text(text, split_content)  # Use the split_text function provided earlier

    data = []
    for i in range(0, len(paragraphs)):
                sample = {
                    "instruction": paragraphs[i]
                }
                data.append(sample)

    return data


def process_json_file(file_path, split_content):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = json.load(f)

    conversations = content["conversations"][0]
    text = conversations["content"]
    paragraphs = split_text(text, split_content)

    # 获取文件名作为小说标题
    title = os.path.basename(file_path).split('.')[0]

    data = []
    for i in range(0, len(paragraphs)):
                sample = {
                    "instruction": paragraphs[i]
                }
                data.append(sample)

    return data

############################################################文件处理###
def generate_dataset(directory, split_content):
    dataset = []
    copy_files = []  # List to store paths of files with @@Copys@@

    for root, dirs, files in os.walk(directory):
        dirs[:] = [d for d in dirs if not d.startswith('_')]

        for file in files:
            file_path = os.path.join(root, file)

            if file.endswith('.txt'):
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    dataset.extend(process_txt_file_EroCrysty(file_path, split_content))
            elif file.endswith('.json'):
                dataset.extend(process_json_file(file_path, split_content))

    return dataset




if __name__ == "__main__":
    directory = input("请输入文件目录的路径: ")
    split_content = int(input("请输入分段的最大字符数: "))
    dataset = generate_dataset(directory, split_content)
    with open(r'D:\datasetnvl5.json', 'w', encoding='utf-8') as f:
        json.dump(dataset, f, ensure_ascii=False, indent=2)
    print("数据集已生成并保存到json文件中")
