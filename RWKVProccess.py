import os

def process_folder(input_folder, output_folder):
    # 检查输出文件夹是否存在，如果不存在则创建
    os.makedirs(output_folder, exist_ok=True)
    
    # 遍历输入文件夹中的文件    
    for file_name in os.listdir(input_folder):
        # 构建输入文件的完整路径
        input_file = os.path.join(input_folder, file_name)
        
        # 读取文件内容，指定正确的编码
        with open(input_file, 'r', encoding='UTF-8') as file:
            content = file.read()
        
        content = content.replace(' ', '').replace('\n', 'ENTERMARK')
        content = content.replace('　　', '').replace('\n', 'ENTERMARK')
        # 删除空格并替换回车
        content = content.replace('ENTERMARKENTERMARKENTERMARK', '\\n')
        content = content.replace('　　', '').replace('ENTERMARKENTERMARK', '\\n')
        content = content.replace('ENTERMARK', '\\n')
        
        # 构建输出文件的完整路径
        output_file = os.path.join(output_folder, file_name)
        
        # 写入处理后的内容到输出文件
        with open(output_file, 'w', encoding='UTF-8') as file:
            file.write(content)

# 指定要处理的输入文件夹路径
input_folder = r''
# 指定输出文件夹路径
output_folder = r''
# 处理文件夹中的文件
process_folder(input_folder, output_folder)