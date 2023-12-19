import json
import os

# 设置要扫描的目录
directory_path = r"D:\Jsons_pre"

# 遍历指定目录下的所有文件
for filename in os.listdir(directory_path):
    if filename.endswith(".json"):
        filepath = os.path.join(directory_path, filename)
        
        # 读取JSON数据
        with open(filepath, 'r', encoding='utf-8') as file:
            data = json.load(file)
        
        # 检查并修改JSON数据
        for conversation in data.get("conversations", []):
            # 修改tags字段的值
            if "tags" in conversation:
                conversation["tags"] = conversation["tags"].replace(" ", "，")
            
            # 确保description字段的值没有空格和换行符
            if "description" in conversation:
                conversation["description"] = conversation["description"].replace(" ", "").replace("\n", "").replace("\r", "").replace("\\", "")
            
            # 确保content字段的值没有空格和换行符
            if "content" in conversation:
                conversation["content"] = conversation["content"].replace(" ", "").replace("\n", "").replace("\r", "").replace("\\", "")
            
        
        # 将修改后的数据保存回文件
        with open(filepath, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

print("JSON文件已更新完毕！")
