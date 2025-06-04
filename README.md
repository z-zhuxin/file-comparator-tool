# 文件相似度对比工�?

一个用于计算两个文件内容相似度的Python程序，支持Word、PDF等常见文档格式�?

## 功能特点

- 计算两个文件内容的相似度百分�?0-100%)
- 支持多种文档格式�?
  - Microsoft Word (.docx)
  - PDF (.pdf) 
  - 纯文�?(.txt)
- 高亮显示差异部分
- 批量处理多个文件�?
- 生成详细对比报告

## 安装指南

### 依赖安装

```bash
pip install python-docx PyPDF2 pdfminer.six gensim
```

### 从源码安�?

```bash
git clone [项目仓库地址]
cd file-comparison-tool
pip install -r requirements.txt
```

## 使用示例

### 命令行使�?

```bash
python compare.py file1.docx file2.pdf
```

输出示例�?
```
相似�? 78.5%
差异部分:
- 文件1: "这是原始文本"
+ 文件2: "这是修改后的文本"
```

### Python API

```python
from file_comparator import compare_files

similarity = compare_files("file1.docx", "file2.pdf")
print(f"文件相似�? {similarity:.1f}%")
```

## 技术依�?

- **文件解析**:
  - Word: python-docx
  - PDF: PyPDF2/pdfminer.six
- **相似度计�?*:
  - difflib (基础)
  - gensim/spacy (高级NLP)

## 许可�?

MIT License
## GUI ����ʹ��ָ��

### ����·��
����λ����ĿĿ¼�µ� dist/gui.exe

### ���ܽ�ͼ
![GUI�����ͼ](docs/screenshot.png)