import argparse
from file_comparator import FileComparator
import sys

def main():
    # 设置命令行参数
    parser = argparse.ArgumentParser(
        description="文件相似度对比工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="示例:\n  python compare.py file1.docx file2.pdf\n  python compare.py -a word2vec doc1.pdf doc2.pdf"
    )
    
    parser.add_argument('file1', help='第一个文件路径')
    parser.add_argument('file2', help='第二个文件路径')
    parser.add_argument('-a', '--algorithm', choices=['difflib', 'word2vec'], 
                       default='difflib', help='相似度算法(difflib/word2vec)')
    parser.add_argument('-v', '--verbose', action='store_true', help='显示详细差异')
    
    args = parser.parse_args()
    
    try:
        print(f"正在比较文件: {args.file1} 和 {args.file2}")
        print(f"使用算法: {args.algorithm}")
        
        # 初始化比较器
        comparator = FileComparator(algorithm=args.algorithm)
        
        # 如果是word2vec算法，需要先训练模型
        if args.algorithm == 'word2vec':
            print("正在训练Word2Vec模型...")
            # 这里简化处理，实际应用中应该用更大的语料库训练
            sample_sentences = [
                ["this", "is", "a", "sample", "sentence"],
                ["another", "example", "sentence"]
            ]
            comparator.train_word2vec(sample_sentences)
        
        # 比较文件
        similarity, diffs = comparator.compare_files(args.file1, args.file2)
        
        # 输出结果
        print(f"\n相似度: {similarity*100:.2f}%")
        
        if args.verbose and diffs:
            print("\n差异部分:")
            for line in diffs[:50]:  # 限制输出前50行差异
                print(line)
            if len(diffs) > 50:
                print(f"...(共{len(diffs)}行差异，此处显示前50行)")
                
    except Exception as e:
        print(f"错误: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()