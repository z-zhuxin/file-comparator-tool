# 文件相似度对比工具主模块
from .comparator import FileComparator
from .word_parser import parse_word
from .pdf_parser import parse_pdf

__all__ = ['FileComparator', 'parse_word', 'parse_pdf']