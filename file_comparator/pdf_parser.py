from PyPDF2 import PdfReader
from typing import List
import warnings

def parse_pdf(file_path: str) -> str:
    """
    解析PDF文档内容，返回纯文本
    
    参数:
        file_path: PDF文档路径
        
    返回:
        文档内容的纯文本字符串
    """
    try:
        with open(file_path, 'rb') as file:
            reader = PdfReader(file)
            
            # 检查是否加密
            if reader.is_encrypted:
                try:
                    reader.decrypt('')
                except:
                    raise ValueError("PDF文档已加密，无法解析")
            
            text_parts = []
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text_parts.append(page_text)
                    
            return '\n'.join(text_parts)
            
    except Exception as e:
        raise ValueError(f"解析PDF文档失败: {str(e)}")

def parse_pdf_to_lines(file_path: str) -> List[str]:
    """
    解析PDF文档内容，返回按行分割的文本列表
    
    参数:
        file_path: PDF文档路径
        
    返回:
        文档内容的文本行列表
    """
    full_text = parse_pdf(file_path)
    return [line.strip() for line in full_text.split('\n') if line.strip()]