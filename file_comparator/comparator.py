from difflib import SequenceMatcher
from gensim.models import Word2Vec
from gensim.utils import simple_preprocess
from typing import List, Tuple, Optional
import numpy as np

class FileComparator:
    def __init__(self, algorithm: str = 'difflib'):
        """
        初始化文件比较器
        
        参数:
            algorithm: 相似度算法(difflib/word2vec)
        """
        self.algorithm = algorithm
        self.word2vec_model = None
        
    def preprocess_text(self, text: str) -> List[str]:
        """
        文本预处理
        
        参数:
            text: 输入文本
            
        返回:
            预处理后的词列表
        """
        return simple_preprocess(text)

    def train_word2vec(self, sentences: List[List[str]]):
        """
        训练Word2Vec模型
        
        参数:
            sentences: 训练句子列表
        """
        self.word2vec_model = Word2Vec(
            sentences=sentences,
            vector_size=100,
            window=5,
            min_count=1,
            workers=4
        )

    def calculate_similarity(self, text1: str, text2: str) -> float:
        """
        计算两个文本的相似度
        
        参数:
            text1: 第一个文本
            text2: 第二个文本
            
        返回:
            相似度分数(0-1)
        """
        if self.algorithm == 'difflib':
            # 增强版difflib比较
            tokens1 = simple_preprocess(text1)
            tokens2 = simple_preprocess(text2)
            
            # 计算三种粒度相似度
            char_level = SequenceMatcher(None, text1, text2).ratio()
            token_level = SequenceMatcher(None, tokens1, tokens2).ratio()
            line_level = SequenceMatcher(None, text1.splitlines(), text2.splitlines()).ratio()
            
            # 加权平均
            return 0.3*char_level + 0.5*token_level + 0.2*line_level
            
        elif self.algorithm == 'word2vec':
            if not self.word2vec_model:
                raise ValueError("Word2Vec模型未训练")
                
            words1 = self.preprocess_text(text1)
            words2 = self.preprocess_text(text2)
            
            # 使用TF-IDF加权词向量
            from sklearn.feature_extraction.text import TfidfVectorizer
            corpus = [' '.join(words1), ' '.join(words2)]
            vectorizer = TfidfVectorizer()
            tfidf = vectorizer.fit_transform(corpus)
            
            # 计算加权词向量
            vec1 = np.zeros(self.word2vec_model.vector_size)
            vec2 = np.zeros(self.word2vec_model.vector_size)
            
            for i, word in enumerate(words1):
                if word in self.word2vec_model.wv:
                    weight = tfidf[0, vectorizer.vocabulary_.get(word, 0)]
                    vec1 += weight * self.word2vec_model.wv[word]
            
            for i, word in enumerate(words2):
                if word in self.word2vec_model.wv:
                    weight = tfidf[1, vectorizer.vocabulary_.get(word, 0)]
                    vec2 += weight * self.word2vec_model.wv[word]
            
            # 归一化处理
            norm1, norm2 = np.linalg.norm(vec1), np.linalg.norm(vec2)
            if norm1 > 0 and norm2 > 0:
                return np.dot(vec1, vec2) / (norm1 * norm2)
            return 0.0
            
        else:
            raise ValueError(f"不支持的算法: {self.algorithm}")

    def compare_files(self, file1_path: str, file2_path: str, mode: str = 'line') -> Tuple[float, List[str], List[dict]]:
        """
        比较两个文件内容
        
        参数:
            file1_path: 第一个文件路径
            file2_path: 第二个文件路径
            mode: 比较模式 ('line'=行级对比, 'full'=全文对比)
            
        返回:
            Tuple[相似度分数(0-1), 差异行列表, 结构化差异信息]
            
        示例:
            # 行级对比模式
            similarity, diffs, details = comparator.compare_files("file1.txt", "file2.txt")
            
            # 全文对比模式
            similarity, diffs, details = comparator.compare_files("file1.txt", "file2.txt", mode='full')
        """
        # 根据文件类型选择解析器
        if file1_path.endswith('.docx'):
            from .word_parser import parse_word_to_lines
            lines1 = parse_word_to_lines(file1_path)
        elif file1_path.endswith('.pdf'):
            from .pdf_parser import parse_pdf_to_lines
            lines1 = parse_pdf_to_lines(file1_path)
        else:
            with open(file1_path, 'r', encoding='utf-8-sig', errors='replace') as f:
                lines1 = [line.strip() for line in f if line.strip()]

        if file2_path.endswith('.docx'):
            from .word_parser import parse_word_to_lines
            lines2 = parse_word_to_lines(file2_path)
        elif file2_path.endswith('.pdf'):
            from .pdf_parser import parse_pdf_to_lines
            lines2 = parse_pdf_to_lines(file2_path)
        else:
            with open(file2_path, 'r', encoding='utf-8-sig', errors='replace') as f:
                lines2 = [line.strip() for line in f if line.strip()]

        # 计算整体相似度
        text1 = '\n'.join(lines1)
        text2 = '\n'.join(lines2)
        similarity = self.calculate_similarity(text1, text2)

        # 根据模式选择对比方式
        if mode == 'full':
            # 全文对比模式
            matcher = SequenceMatcher(None, text1, text2)
            diffs = []
            diff_details = []
            
            for tag, i1, i2, j1, j2 in matcher.get_opcodes():
                if tag != 'equal':
                    # 全文差异标记
                    diffs.append(f"{tag.upper()} at {i1}-{i2} in file1, {j1}-{j2} in file2")
                    diff_details.append({
                        'type': tag,
                        'file1_pos': (i1, i2),
                        'file2_pos': (j1, j2),
                        'file1_content': text1[i1:i2],
                        'file2_content': text2[j1:j2]
                    })
        else:
            # 行级对比模式
            matcher = SequenceMatcher(None, lines1, lines2)
            diffs = []
            diff_details = []  # 存储结构化差异信息
        
        for tag, i1, i2, j1, j2 in matcher.get_opcodes():
            if tag != 'equal':
                # 保留原始差异行输出（兼容性）
                diffs.extend([f"- {line}" for line in lines1[i1:i2]])
                diffs.extend([f"+ {line}" for line in lines2[j1:j2]])
                
                # 新增结构化差异信息
                diff_details.append({
                    'type': tag,
                    'file1_lines': (i1+1, i2),  # 转换为1-based行号
                    'file2_lines': (j1+1, j2),
                    'file1_content': lines1[i1:i2],
                    'file2_content': lines2[j1:j2]
                })

        return similarity, diffs, diff_details

    def get_file_lines(self, file_path: str) -> List[str]:
        """
        获取文件的文本行列表
        
        参数:
            file_path: 文件路径
            
        返回:
            文件内容行列表
        """
        if file_path.endswith('.docx'):
            from .word_parser import parse_word_to_lines
            return parse_word_to_lines(file_path)
        elif file_path.endswith('.pdf'):
            from .pdf_parser import parse_pdf_to_lines
            return parse_pdf_to_lines(file_path)
        else:
            with open(file_path, 'r', encoding='utf-8-sig', errors='replace') as f:
                return [line.strip() for line in f if line.strip()]