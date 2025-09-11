import os
import re
import shutil

def rename_files(input_path, output_path, keyword="R"):
    """
    批量重命名文件，将 keyword_数字 格式改为 数字_keyword 格式
    
    Args:
        input_path (str): 输入文件夹路径
        output_path (str): 输出文件夹路径
        keyword (str): 要处理的关键词，默认为 "R"
    
    Returns:
        dict: 重命名映射关系 {原文件名: 新文件名}
    """
    
    # 检查输入路径是否存在
    if not os.path.exists(input_path):
        print(f"错误：输入路径 {input_path} 不存在")
        return {}
    
    # 创建输出路径（如果不存在）
    if not os.path.exists(output_path):
        try:
            os.makedirs(output_path)
            print(f"创建输出目录: {output_path}")
        except Exception as e:
            print(f"错误：无法创建输出目录 {output_path}: {e}")
            return {}
    
    # 定义匹配模式：keyword_数字
    pattern = rf'^{keyword}_(\d+)(.*)$'
    
    renamed_count = 0
    skipped_count = 0
    rename_mapping = {}  # 存储重命名映射关系
    
    # 遍历输入文件夹中的所有文件
    for filename in os.listdir(input_path):
        file_path = os.path.join(input_path, filename)
        
        # 跳过文件夹，只处理文件
        if os.path.isdir(file_path):
            continue
        
        # 分离文件名和扩展名
        name, ext = os.path.splitext(filename)
        
        # 检查文件名是否匹配模式
        match = re.match(pattern, name)
        if match:
            number = match.group(1)
            remaining_part = match.group(2)
            
            # 构造新的文件名：数字_keyword + 剩余部分 + 扩展名
            new_name = f"{number}_{keyword}{remaining_part}{ext}"
            new_path = os.path.join(output_path, new_name)
            
            # 检查新文件名是否已存在
            if os.path.exists(new_path):
                print(f"警告：新文件名 {new_name} 已存在，跳过重命名 {filename}")
                continue
            
            try:
                # 复制文件到输出目录并重命名
                shutil.copy2(file_path, new_path)
                print(f"重命名并复制：{filename} -> {new_name}")
                rename_mapping[filename] = new_name
                renamed_count += 1
            except Exception as e:
                print(f"错误：处理 {filename} 时发生错误: {e}")
        else:
            # 不匹配模式的文件跳过
            print(f"跳过：{filename} （不匹配模式）")
            skipped_count += 1
    
    print(f"\n完成！共重命名了 {renamed_count} 个文件，跳过了 {skipped_count} 个文件")
    return rename_mapping

def find_matching_files(input_path, keyword):
    """
    在输入路径中查找匹配指定关键词的文件
    
    Args:
        input_path (str): 输入文件夹路径
        keyword (str): 要查找的关键词
    
    Returns:
        list: 匹配的文件列表
    """
    if not os.path.exists(input_path):
        return []
    
    pattern = rf'^{keyword}_(\d+)(.*)$'
    matching_files = []
    
    for filename in os.listdir(input_path):
        file_path = os.path.join(input_path, filename)
        
        # 跳过文件夹，只处理文件
        if os.path.isdir(file_path):
            continue
        
        # 分离文件名和扩展名
        name, ext = os.path.splitext(filename)
        
        # 检查文件名是否匹配模式
        match = re.match(pattern, name)
        if match:
            number = match.group(1)
            remaining_part = match.group(2)
            new_name = f"{number}_{keyword}{remaining_part}{ext}"
            matching_files.append({
                'original': filename,
                'renamed': new_name,
                'number': number
            })
    
    return matching_files

def interactive_search(input_path, rename_mapping):
    """
    交互式查找匹配关系
    
    Args:
        input_path (str): 输入文件夹路径
        rename_mapping (dict): 重命名映射关系
    """
    print("\n" + "="*50)
    print("查找匹配关系功能")
    print("="*50)
    
    while True:
        keyword = input("\n请输入要查找的关键词（输入 'q' 退出）: ").strip()
        
        if keyword.lower() == 'q':
            print("退出查找功能")
            break
        
        if not keyword:
            print("请输入有效的关键词")
            continue
        
        # 查找匹配的文件
        matching_files = find_matching_files(input_path, keyword)
        
        if not matching_files:
            print(f"未找到匹配关键词 '{keyword}' 的文件")
            continue
        
        print(f"\n找到 {len(matching_files)} 个匹配 '{keyword}' 的文件:")
        print("-" * 50)
        
        for i, file_info in enumerate(matching_files, 1):
            original = file_info['original']
            renamed = file_info['renamed']
            number = file_info['number']
            
            status = "✓ 已处理" if original in rename_mapping else "✗ 未处理"
            
            print(f"{i}. {original} -> {renamed} (数字: {number}) [{status}]")
        
        print("-" * 50)

def main():
    # 设置输入路径
    input_path = input("请输入源文件夹路径（直接回车使用当前目录）: ").strip()
    if not input_path:
        input_path = "."
    
    # 设置输出路径
    output_path = input("请输入输出文件夹路径: ").strip()
    if not output_path:
        print("错误：必须指定输出路径")
        return
    
    # 设置关键词（可以修改为其他单词）
    keyword = input("请输入要处理的关键词（直接回车使用默认值 'R'）: ").strip()
    if not keyword:
        keyword = "R"
    
    print(f"\n开始处理:")
    print(f"输入路径: {os.path.abspath(input_path)}")
    print(f"输出路径: {os.path.abspath(output_path)}")
    print(f"处理关键词: {keyword}")
    print(f"匹配模式: {keyword}_数字 -> 数字_{keyword}")
    print("-" * 50)
    
    # 执行重命名
    rename_mapping = rename_files(input_path, output_path, keyword)
    
    # 如果有文件被重命名，启动交互式查找功能
    if rename_mapping:
        interactive_search(input_path, rename_mapping)

if __name__ == "__main__":
    main() 