# 测试文件说明

此目录用于存放文件相似度对比工具的测试文件。

## 测试文件建议

1. **Word文档**:
   - test1.docx (示例文档1)
   - test2.docx (与test1.docx有部分相同内容)

2. **PDF文档**:
   - test1.pdf (示例PDF1)
   - test2.pdf (与test1.pdf有部分相同内容)

3. **文本文件**:
   - test1.txt
   - test2.txt

## 测试方法

1. 安装依赖:
```bash
pip install -r requirements.txt
```

2. 运行测试:
```bash
# 测试Word文档
python compare.py test_files/test1.docx test_files/test2.docx -v

# 测试PDF文档 
python compare.py test_files/test1.pdf test_files/test2.pdf -v

# 测试不同格式文件
python compare.py test_files/test1.docx test_files/test1.pdf
```

3. 检查输出:
- 相似度百分比
- 差异内容(使用-v参数时显示)