# 文件相似度对比工具

提供命令行和GUI两种版本，用于计算文档内容相似度，支持Word、PDF等常见文档格式。

## GUI版本 (gui.exe)

### 功能特点
- 可视化操作界面
- 拖拽文件快速比较
- 实时显示相似度百分比
- 差异部分高亮标注
- 支持批量文件处理

### 使用方法
1. 下载或编译生成`gui.exe`
2. 双击运行程序
3. 通过界面选择要比较的文件
4. 查看相似度结果和差异对比

## 程序界面 
程序路径：`dist/gui.exe`
打开就可以直接使用
![image](https://github.com/user-attachments/assets/d3b694ef-853c-459b-9b4a-e67dc1f0d200)



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
