# 文件相似度对比工具

一个用于计算两个文档内容相似度的Python程序，支持Word、PDF等常见文档格式。

## 功能特点

- 计算两个文件内容的相似度百分比(0-100%)
- 支持多种文档格式：
  - Microsoft Word (.docx)
  - PDF (.pdf)  
  - 纯文本 (.txt)
- 高亮显示差异部分
- 批量处理多个文件对比
- 生成详细对比报告

## 安装指南

1. 安装Python 3.8+
2. 安装依赖库：
```bash
pip install python-docx PyPDF2 difflib
```

3. 运行程序：
```bash 
python compare.py 文件1 文件2
```

## 使用示例

```python
# 基本用法
from comparator import compare_files
similarity = compare_files("doc1.docx", "doc2.pdf")
print(f"相似度: {similarity}%")

# 批量处理
from comparator import batch_compare
results = batch_compare("folder1", "folder2")
```

## 输出示例
```
文档A.docx 与 文档B.pdf 的相似度: 78.5%
差异部分:
- 文档A: "这是原始文本"
+ 文档B: "这是修改后的文本"
```

## 贡献指南
欢迎提交Pull Request或报告Issue

---

# File Similarity Comparison Tool

A Python program for calculating content similarity between documents, supporting Word, PDF etc.

## Features

- Calculate similarity percentage (0-100%)
- Support multiple formats:
  - Microsoft Word (.docx)
  - PDF (.pdf)
  - Plain text (.txt)  
- Highlight differences
- Batch processing
- Generate detailed reports

## License
MIT