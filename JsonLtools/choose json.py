import os
import random
import shutil
"""
随机选择num_files个文件
"""


def copy_random_json_files(src_dir, dest_dir, num_files=1000):
    if not os.path.exists(src_dir):
        print("源目录不存在")
        return
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    json_files = [f for f in os.listdir(src_dir) if f.endswith('.json')]
    
    if len(json_files) < num_files:
        print("源目录中的 JSON 文件数量不足")
        return
    
    selected_files = random.sample(json_files, num_files)
    
    for file in selected_files:
        src_file = os.path.join(src_dir, file)
        dest_file = os.path.join(dest_dir, file)
        shutil.copy2(src_file, dest_file)
        print(f"{file} 已复制")

src_dir = r"C:\Users\zyr20\Downloads\LLM\EroCrysty 5.0"
dest_dir = r"C:\Users\zyr20\Downloads\LLM\EroCrysty 5.0mini"
copy_random_json_files(src_dir, dest_dir)
