import json
import os

def find_long_descriptions(directory, dsp_len):
    """
    打印包含描述字段长度大于dsp_len的json文件名
    """
    for root, dirs, files in os.walk(directory):
        for filename in files:
            if filename.endswith('.json'):
                with open(os.path.join(root, filename), 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    conversations = data.get('conversations', [])
                    for convo in conversations:
                        description = convo.get('description', '')
                        if len(description) > dsp_len:
                            print(filename)
                            break  # 若当前文件已匹配，直接跳到下一个文件

directory = input("请输入你想搜索的目录: ")
dsp_len = int(input("请输入description的长度限制: "))
find_long_descriptions(directory, dsp_len)
