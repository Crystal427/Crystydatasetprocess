import os
import shutil

source_dir = r'H:\新建文件夹' 
target_dir = r'H:\c3'

for root, dirs, files in os.walk(source_dir):
    for filename in files:
        if filename.endswith('.txt'):
            shutil.move(os.path.join(root, filename), target_dir)