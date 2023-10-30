import os
import json
import re

def split_text(text, split_content):
    paragraphs = []
    current_paragraph = ""
    for sentence in re.split(r'([。,])', text):
        current_paragraph += sentence
        if "####" in current_paragraph:
            paragraphs.append(current_paragraph.replace("####", "").strip())
            current_paragraph = ""
        elif len(current_paragraph) > split_content:
            paragraphs.append(current_paragraph.strip())
            current_paragraph = ""
    if current_paragraph:
        paragraphs.append(current_paragraph.strip())
    return paragraphs

def process_txt_file(file_path, split_content, part_num, mark):
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
                    "value": f'请你帮我写一篇小说，标题是“{file_name}”，请参照下面这部分内容，续写"{paragraph}"'
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
    title = conversations["title"]
    tags = conversations["tags"]
    description = conversations["description"]
    text = conversations["content"]
    paragraphs = split_text(text, split_content)
    data = []
    for i in range(0, len(paragraphs), part_num):
        sample = {
            "id": f"{novel_id}EroCrysty{mark}",
            "conversations": []
        }
        for j, paragraph in enumerate(paragraphs[i:i+part_num], 1):
            if j == 1:
                sample["conversations"].append({
                    "from": "user",
                    "value": f'请你帮我写一篇小说，标题是“{title}”，相关tag是“{tags}”，简介是“{description}”，请参照下面这部分内容，续写“{paragraph}”'
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
                dataset.extend(process_txt_file(file_path, split_content, part_num, mark))
            elif file.endswith('.json'):
                dataset.extend(process_json_file(file_path, split_content, part_num, mark))
    return dataset

if __name__ == "__main__":
    directory = input("请输入文件目录的路径: ")
    split_content = int(input("请输入分段的最大字符数: "))
    part_num = int(input("请输入每个样本中最大的对话数量: "))
    mark = input("请输入标记字符串: ")
    dataset = generate_dataset(directory, split_content, part_num, mark)
    with open(r'C:\Users\zyr20\Downloads\LLM\datasettunmini.json', 'w', encoding='utf-8') as f:
        json.dump(dataset, f, ensure_ascii=False, indent=2)
    print("数据集已生成并保存到dataset.json文件中")
