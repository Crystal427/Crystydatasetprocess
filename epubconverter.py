import os
import ebooklib
from ebooklib import epub
from ebooklib.utils import debug

# 设置电子书所在的目录
epub_dir = r'C:\Users\zyr20\OneDrive\桌面\EroCrysty 3.0\working\节哀唷二之宫同学\请别忧伤了，二之宫君(未知汉化)'  

# 遍历目录下的EPUB文件
for filename in os.listdir(epub_dir):
    if filename.endswith('.epub'):
        full_path = os.path.join(epub_dir, filename)
        
        # 打开EPUB文件
        book = epub.read_epub(full_path)
        
        # 获取书名作为转换后的TXT文件名
        txt_filename = os.path.splitext(filename)[0] + '.txt'
        txt_full_path = os.path.join(epub_dir, txt_filename)

        # 打开TXT文件准备写入
        txt_file = open(txt_full_path, 'w', encoding='utf-8')
        
        # 遍历EPUB的章节内容
        for doc in book.get_items_of_type(ebooklib.ITEM_DOCUMENT):
            
            # 只提取文字内容
            content = ebooklib.epub.EpubItem.get_content(doc)
            
            # 写入TXT文件
            txt_file.write(content)
            
        # 关闭文件
        txt_file.close()
        
print('EPUB转TXT完成!')