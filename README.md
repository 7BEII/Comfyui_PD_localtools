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
