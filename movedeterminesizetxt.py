import os
import shutil

def find_and_copy_files(src_dir, dest_dir, size_threshold_kb):
    for root, dirs, files in os.walk(src_dir):
        for file in files:
            file_path = os.path.join(root, file)
            if os.path.getsize(file_path) > size_threshold_kb * 1024:
                meta_file = file.rsplit('.', 1)[0] + '-meta.txt'
                meta_file_path = os.path.join(root, meta_file)

                if os.path.exists(meta_file_path):
                    dest_file_path = os.path.join(dest_dir, os.path.relpath(file_path, src_dir))
                    dest_meta_file_path = os.path.join(dest_dir, os.path.relpath(meta_file_path, src_dir))

                    os.makedirs(os.path.dirname(dest_file_path), exist_ok=True)
                    shutil.copy2(file_path, dest_file_path)
                    shutil.copy2(meta_file_path, dest_meta_file_path)

# 示例用法
src_directory = r'E:\LLM\needfilter\Chinese-Pixiv-Novel\PixivNovel'  # 请替换成您的源目录路径
dest_directory = r'E:\LLM\needfilter\Chinese-Pixiv-Novel\Fi'  # 请替换成您的目标目录路径
size_threshold = 75  # 文件大小阈值，单位为KB

# 运行函数
find_and_copy_files(src_directory, dest_directory, size_threshold)

# 请取消注释最后一行，并在运行脚本之前用您希望使用的路径替换源目录和目标目录的路径。