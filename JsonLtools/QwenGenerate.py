import json
import os

def process_txt_file(file_path, split_content, part_num, mark):
    conversations = []
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read().strip().replace(" ", "")
        paragraphs = []
        print("processingtxt")
        temp_paragraph = ""
        for line in text.split('\n'):
            if len(temp_paragraph + line) > split_content:
                last_punc = max(temp_paragraph.rfind('。'), temp_paragraph.rfind('，'))
                if last_punc != -1:
                    paragraphs.append(temp_paragraph[:last_punc + 1])
                    temp_paragraph = temp_paragraph[last_punc + 1:] + line
                else:
                    paragraphs.append(temp_paragraph)
                    temp_paragraph = line
            elif "####" in line:
                paragraphs.append(temp_paragraph)
                temp_paragraph = ""
            else:
                temp_paragraph += line

        if temp_paragraph:
            paragraphs.append(temp_paragraph)

        file_name = os.path.splitext(os.path.basename(file_path))[0]
        for i in range(0, len(paragraphs), part_num):
            conversation = [
                {"from": "user", "value": f"请你帮我写一篇小说，标题是“{file_name}”，请参照下面这部分内容，续写\"{paragraphs[i]}\""}
            ]
            for j in range(i + 1, min(i + part_num, len(paragraphs))):
                conversation.extend([
                    {"from": "user", "value": "继续续写"},
                    {"from": "assistant", "value": paragraphs[j]}
                ])
            conversations.append({"id": str(i) + "EroCrysty" + mark, "conversations": conversation})
    return conversations


def process_json_file(file_path, split_content, part_num, mark):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        novel_id = data["novelid"]
        content = data["conversations"][0]["content"]
        title = data["conversations"][0]["title"]
        tags = data["conversations"][0]["tags"]
        description = data["conversations"][0]["description"]
        print(tags)
        paragraphs = []
        temp_paragraph = ""
        for line in content.split('\n'):
            if len(temp_paragraph + line) > split_content:
                last_punc = max(temp_paragraph.rfind('。'), temp_paragraph.rfind('，'))
                if last_punc != -1:
                    paragraphs.append(temp_paragraph[:last_punc + 1])
                    temp_paragraph = temp_paragraph[last_punc + 1:] + line
                else:
                    paragraphs.append(temp_paragraph)
                    temp_paragraph = line
            else:
                temp_paragraph += line

        if temp_paragraph:
            paragraphs.append(temp_paragraph)

        conversations = []
        for i in range(0, len(paragraphs), part_num):
            conversation = [
                {"from": "user", "value": f"请你帮我写一篇小说，标题是“{title}”，相关tag是“{tags}”，简介是“{description}”，请参照下面这部分内容，续写\"{paragraphs[i]}\""}
            ]
            for j in range(i + 1, min(i + part_num, len(paragraphs))):
                conversation.extend([
                    {"from": "user", "value": "继续续写"},
                    {"from": "assistant", "value": paragraphs[j]}
                ])
            conversations.append({"id": novel_id + "EroCrysty" + mark, "conversations": conversation})
    return conversations


def process_directory(directory_path, split_content_txt, part_num_txt, split_content_json, part_num_json, mark):
    result = []
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            file_path = os.path.join(root, file)
            if file.endswith('.txt'):
                result.extend(process_txt_file(file_path, split_content_txt, part_num_txt, mark))
            elif file.endswith('.json'):
                result.extend(process_json_file(file_path, split_content_json, part_num_json, mark))
    return result


if __name__ == "__main__":
    directory_path = input("请输入文件夹路径: ")
    split_content_txt = int(input("请输入txt文件分段的文字数量: "))
    part_num_txt = int(input("请输入txt文件分段的最大段数: "))
    split_content_json = int(input("请输入json文件分段的文字数量: "))
    part_num_json = int(input("请输入json文件分段的最大段数: "))
    mark = input("请输入用户自定义字符串Mark: ")

    result = process_directory(directory_path, split_content_txt, part_num_txt, split_content_json, part_num_json, mark)
    with open(r"C:\Users\zyr20\Downloads\LLM\output.json", "w", encoding='utf-8') as f:
        print("Generating Json Files...")
        json.dump(result, f, ensure_ascii=False, indent=2)
