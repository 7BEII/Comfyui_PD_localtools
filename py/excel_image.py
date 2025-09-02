import os
import torch
from openpyxl import load_workbook
from PIL import Image
import io
from pathlib import Path
from datetime import datetime

class PD_excel_image:
    """
    Excel图片提取节点
    从Excel文件中提取所有图片并保存到指定目录
    """
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "input_directory": ("STRING", {
                    "default": "", 
                    "multiline": False,
                    "placeholder": "搜索目录路径 (例: C:\\Users\\Desktop\\excel_files)"
                }),  # 搜索Excel文件的目录路径
            },
            "optional": {
                "output_directory": ("STRING", {
                    "default": "", 
                    "multiline": False,
                    "placeholder": "输出目录路径 (留空则在输入目录下创建image-日期文件夹)"
                }),  # 输出目录路径，可选
                "filename_prefix": ("STRING", {
                    "default": "img_", 
                    "multiline": False
                }),  # 文件名前缀
                "image_format": (["auto", "png", "jpg", "jpeg", "bmp", "gif"], {
                    "default": "auto"
                }),  # 强制转换图片格式
                "include_filename": ("BOOLEAN", {"default": True}),  # 是否在文件名中包含源Excel文件名
            }
        }

    RETURN_TYPES = ("STRING",)  # 只返回状态信息文本
    RETURN_NAMES = ("status_text",)  # 返回值的名称
    FUNCTION = "extract_images"  # 指定执行的方法名称
    CATEGORY = "PD_File/Excel"  # 定义节点的类别

    def extract_images(self, input_directory, output_directory="", filename_prefix="img_", 
                      image_format="auto", include_filename=True):
        """
        从目录中的所有Excel文件中提取图片
        
        参数：
            input_directory (str): 搜索Excel文件的目录路径
            output_directory (str): 输出目录路径，留空则在输入目录下创建image-日期文件夹
            filename_prefix (str): 文件名前缀
            image_format (str): 强制转换的图片格式
            include_filename (bool): 是否在文件名中包含源Excel文件名
            
        返回：
            status_text (str): 包含处理结果和统计信息的状态文本
        """
        
        try:
            # 验证输入路径
            if not input_directory or not os.path.exists(input_directory):
                error_msg = f"❌ 输入目录不存在: {input_directory}"
                print(error_msg)
                return (error_msg,)
            
            # 设置输出目录：如果未指定，则在输入目录下创建image-日期文件夹
            if not output_directory or output_directory.strip() == "":
                current_date = datetime.now().strftime("%Y%m%d")
                output_directory = os.path.join(input_directory, f"image-{current_date}")
                print(f"📁 未指定输出目录，自动设置为: {output_directory}")
            
            # 创建输出目录
            output_path = Path(output_directory)
            output_path.mkdir(parents=True, exist_ok=True)
            
            # 搜索所有Excel文件
            input_path = Path(input_directory)
            excel_files = list(input_path.glob("*.xlsx")) + list(input_path.glob("*.xlsm"))
            
            if not excel_files:
                no_files_msg = f"ℹ️  在目录中没有找到Excel文件: {input_directory}\n📁 输出目录: {output_directory}"
                print(no_files_msg)
                return (no_files_msg,)
            
            print(f"🔍 找到 {len(excel_files)} 个Excel文件")
            print(f"📁 输出目录: {output_directory}")
            
            total_img_count = 0
            processed_files = 0
            
            # 遍历所有Excel文件
            for excel_file in excel_files:
                excel_filename = excel_file.stem  # 不包含扩展名的文件名
                print(f"📄 处理文件: {excel_file.name}")
                
                try:
                    # 加载Excel工作簿
                    wb = load_workbook(excel_file)
                    processed_files += 1
                    file_img_count = 0
                    
                    # 遍历所有工作表
                    for sheet in wb.worksheets:
                        sheet_name = sheet.title
                        
                        # 提取工作表中的图片
                        if hasattr(sheet, '_images'):
                            for image in sheet._images:
                                try:
                                    # 获取图片数据
                                    if hasattr(image, '_data'):
                                        img_bytes = image._data()
                                    elif hasattr(image, 'ref') and hasattr(image, 'image'):
                                        img_bytes = image.image
                                    else:
                                        print(f"  ⚠️  跳过无法读取的图片对象")
                                        continue
                                    
                                    # 打开图片
                                    img = Image.open(io.BytesIO(img_bytes))
                                    
                                    # 确定保存格式
                                    if image_format == "auto":
                                        save_format = img.format if img.format else "PNG"
                                        file_extension = save_format.lower()
                                    else:
                                        save_format = image_format.upper()
                                        file_extension = image_format.lower()
                                        
                                        # 格式转换处理
                                        if save_format == "JPG":
                                            save_format = "JPEG"
                                            file_extension = "jpg"
                                        
                                        # 如果转换为JPEG，需要处理透明度
                                        if save_format == "JPEG" and img.mode in ("RGBA", "P"):
                                            # 创建白色背景
                                            background = Image.new("RGB", img.size, (255, 255, 255))
                                            if img.mode == "P":
                                                img = img.convert("RGBA")
                                            background.paste(img, mask=img.split()[-1] if img.mode == "RGBA" else None)
                                            img = background
                                    
                                    # 生成文件名
                                    total_img_count += 1
                                    file_img_count += 1
                                    
                                    if include_filename:
                                        filename = f"{filename_prefix}{excel_filename}_{total_img_count}.{file_extension}"
                                    else:
                                        filename = f"{filename_prefix}{total_img_count}.{file_extension}"
                                    
                                    # 保存图片到统一目录
                                    save_path = output_path / filename
                                    
                                    # 保存时的参数
                                    save_kwargs = {}
                                    if save_format == "JPEG":
                                        save_kwargs["quality"] = 95
                                        save_kwargs["optimize"] = True
                                    elif save_format == "PNG":
                                        save_kwargs["optimize"] = True
                                    
                                    img.save(save_path, format=save_format, **save_kwargs)
                                    print(f"  💾 保存图片: {filename}")
                                    
                                except Exception as e:
                                    print(f"  ❌ 处理图片时出错: {str(e)}")
                                    continue
                    
                    if file_img_count > 0:
                        print(f"  ✅ 文件 '{excel_file.name}' 提取了 {file_img_count} 张图片")
                    else:
                        print(f"  ℹ️  文件 '{excel_file.name}' 没有找到图片")
                        
                except Exception as e:
                    print(f"  ❌ 无法打开Excel文件 '{excel_file.name}': {str(e)}")
                    continue
            
            # 生成结果报告
            if total_img_count > 0:
                success_msg = f"✅ 提取完成！\n📊 处理结果:\n  - 处理文件数: {processed_files} 个Excel文件\n  - 提取图片数: {total_img_count} 张\n📁 图片保存在: {output_directory}"
                print(success_msg)
                return (success_msg,)
            else:
                no_img_msg = f"ℹ️  没有找到图片\n📊 处理结果:\n  - 处理文件数: {processed_files} 个Excel文件\n  - 提取图片数: 0 张\n📁 输出目录: {output_directory}"
                print(no_img_msg)
                return (no_img_msg,)
                
        except Exception as e:
            error_msg = f"❌ 处理过程中发生错误: {str(e)}"
            print(error_msg)
            return (error_msg,)

# 节点注册
NODE_CLASS_MAPPINGS = {
    "PD_excel_image": PD_excel_image
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "PD_excel_image": "PD:Excel_image_reduce"
} 