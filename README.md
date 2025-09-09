# ComfyUI PD Local Tools

## PD_Name_ReplaceWordOrder

调整文件名中关键词位置顺序的节点，可以批量重命名文件，将指定关键词移动到文件名的最前面或最后面。

### 功能特点

现在的效果示例：
原文件：abc_keyword_123.txt
    选择 front：结果为 keywordabc__123.txt（保留原有的下划线）
    选择 end：结果为 abc__123keyword.txt（保留原有的下划线）
    原文件：test-keyword-file.txt
    选择 front：结果为 keywordtest--file.txt（保留原有的连字符）
    选择 end：结果为 test--filekeyword.txt（保留原有的连字符）

## PDimage_dual_batch_v1

双文件夹图片批量处理节点，自动匹配两个文件夹中命名相同的图片，
精确命名匹配：基于文件名（不含扩展名）进行匹配，不受图片尺寸影响。
尺寸不开放调整，只匹配名称，返回确保输出张量符合ComfyUI的要求(B,H,W,C) 正确通道图片。返回确保是list 或者说bach 就是目标路径下所有匹配成功批次的image1   另一个就是image2 其他逻辑去掉
返回批次列表：将所有匹配成功的图片组织成两个批次（image1_batch 和 image2_batch）
output_mode 就是 torch.Size 第二和第三通道（高度和宽度）可以不完全一致，只匹配名称输出，确保顺利输出图片

### 功能特点

- **自动匹配**：根据文件名自动匹配两个文件夹中的对应图片
- **多种处理模式**：支持4种不同的图片处理模式
- **批量处理**：一次性处理所有匹配的图片对
- **智能尺寸处理**：确保输出图片具有一致的尺寸
- **详细反馈**：提供处理结果和匹配信息的详细反馈

### 输入参数

- **image1_path** (STRING): 第一个图片文件夹路径
- **image2_path** (STRING): 第二个图片文件夹路径  
- **max_size** (INT): 最大尺寸，范围64-4096，默认512
- **resize_mode** (SELECT): 图片处理模式
  - `none`: 不处理尺寸，保持原样
  - `letterbox_white`: 等比例缩放并用白色填充（默认）
  - `letterbox_black`: 等比例缩放并用黑色填充
  - `crop_center`: 等比例缩放后居中裁切

### 输出

- **image1_list** (IMAGE): 处理后的第一个文件夹图片批次
- **image2_list** (IMAGE): 处理后的第二个文件夹图片批次
- **combined_info** (STRING): 处理信息，包含批次数量和匹配的图片名称

### 处理模式说明

#### letterbox_white/letterbox_black
- 保持图片原始宽高比
- 等比例缩放到适合目标尺寸
- 用指定颜色填充空白区域
- 图片居中显示

#### crop_center
- 等比例缩放图片使其能覆盖目标尺寸
- 居中裁切到目标尺寸
- 可能裁切部分图片内容
- 确保填满整个目标区域

### 使用场景

- **图像对比**：处理需要对比的两组图片
- **数据集准备**：为机器学习准备配对的训练数据
- **批量处理**：需要同时处理多个图片对的场景
- **尺寸标准化**：将不同尺寸的图片统一到相同尺寸

### 支持的图片格式

- JPG/JPEG
- PNG
- BMP
- TIFF/TIF
- WebP

### 注意事项


