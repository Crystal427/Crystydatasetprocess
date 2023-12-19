import json
import os
import re
import concurrent.futures

# 设置包含JSON文件的目录路径
json_directory = r'D:\Jsons'
txt_directory = r'D:\novels_filiter'

def process_file(json_path):
    # 读取JSON文件
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"错误：无法解析{json_path}，错误信息：{str(e)}")
        return
    except Exception as e:
        print(f"错误：无法读取{json_path}，错误信息：{str(e)}")
        return

    # 获取"novelid"
    novel_id = data.get('novelid', '')

    if novel_id:
        # 构建txt文件的路径
        txt_filename = f'novel{novel_id}.txt'
        txt_path = os.path.join(txt_directory, txt_filename)

        # 读取txt文件的内容
        if os.path.exists(txt_path):
            try:
                with open(txt_path, 'r', encoding='utf-8') as f:
                    content = f.read()
            except Exception as e:
                print(f"错误：无法读取{txt_path}，错误信息：{str(e)}")
                return

            # 删除所有空格
            content = content.replace(' ', '')

            # 将多个连续换行符转换为一个换行符
            content = re.sub(r'\n+', '\n', content)

            # 添加到JSON结构
            if 'conversations' in data and data['conversations']:
                data['conversations'][0]['content'] = content
            else:
                print(f"警告：在{json_path}中没有找到'conversations'或者它是空的。")
                return

            # 保存回JSON文件
            try:
                with open(json_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=4)
                print(f"内容已成功更新到{json_path}。")
            except Exception as e:
                print(f"错误：无法写入{json_path}，错误信息：{str(e)}")
        else:
            print(f"错误：文件{txt_path}不存在。")
    else:
        print(f"错误：在{json_path}中'novelid'不存在或者值无效。")

# 获取所有JSON文件的路径
json_files = [os.path.join(json_directory, f) for f in os.listdir(json_directory) if f.endswith('.json')]

# 使用ThreadPoolExecutor并发执行
with concurrent.futures.ThreadPoolExecutor() as executor:
    executor.map(process_file, json_files)
