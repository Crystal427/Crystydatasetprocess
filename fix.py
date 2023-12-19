import json

def check_value_lengths(file_path, threshold):
    # 读取 JSON 文件
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    # 遍历 JSON 数据，检查每个 value 的长度
    for item in data:
        for convo in item['conversations']:
            if len(convo['value']) > threshold:
                print(item['id'])
                break  # 找到一个超过阈值的 value 后跳出循环

# 指定 JSON 文件的路径
file_path = r'D:\dataset2.json'  # 替换为您的 JSON 文件路径

# 设置长度阈值
threshold = 10000  # 您可以根据需要调整这个值

# 调用函数进行检查
check_value_lengths(file_path, threshold)
