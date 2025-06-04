import tkinter as tk
from tkinter import filedialog, ttk
from file_comparator import FileComparator

class FileCompareApp:
    def __init__(self, root):
        self.root = root
        self.root.title("文件相似度比较工具")
        self.root.geometry("1000x600")
        
        # 文件选择区域
        self.setup_file_select()
        
        # 文本对比区域
        self.setup_text_compare()
        
        # 结果显示区域
        self.setup_result_display()
        
        # 初始化比较器
        self.comparator = FileComparator()
    
    def setup_file_select(self):
        frame = ttk.LabelFrame(self.root, text="文件选择", padding=10)
        frame.pack(fill=tk.X, padx=10, pady=5)
        
        # 文件1选择
        ttk.Label(frame, text="原文:").grid(row=0, column=0, sticky=tk.W)
        self.file1_entry = ttk.Entry(frame, width=50)
        self.file1_entry.grid(row=0, column=1, padx=5)
        ttk.Button(frame, text="浏览...", command=lambda: self.select_file(self.file1_entry)).grid(row=0, column=2)
        
        # 文件2选择
        ttk.Label(frame, text="对比文:").grid(row=1, column=0, sticky=tk.W)
        self.file2_entry = ttk.Entry(frame, width=50)
        self.file2_entry.grid(row=1, column=1, padx=5)
        ttk.Button(frame, text="浏览...", command=lambda: self.select_file(self.file2_entry)).grid(row=1, column=2)
        
        # 比较按钮
        ttk.Button(frame, text="开始比较", command=self.compare_files).grid(row=2, column=1, pady=10)
    
    def setup_text_compare(self):
        frame = ttk.Frame(self.root)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # 原文显示
        ttk.Label(frame, text="原文内容").grid(row=0, column=0)
        self.text1 = tk.Text(frame, wrap=tk.WORD, height=20, width=50)
        self.text1.grid(row=1, column=0, sticky=tk.NSEW, padx=5)
        
        # 对比文显示
        ttk.Label(frame, text="对比文内容").grid(row=0, column=1)
        self.text2 = tk.Text(frame, wrap=tk.WORD, height=20, width=50)
        self.text2.grid(row=1, column=1, sticky=tk.NSEW, padx=5)
        
        # 配置滚动条
        scroll = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=self.sync_scroll)
        scroll.grid(row=1, column=2, sticky=tk.NS)
        self.text1.config(yscrollcommand=scroll.set)
        self.text2.config(yscrollcommand=scroll.set)
        
        # 配置网格权重
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(1, weight=1)
        frame.grid_rowconfigure(1, weight=1)
    
    def setup_result_display(self):
        frame = ttk.LabelFrame(self.root, text="比较结果", padding=10)
        frame.pack(fill=tk.X, padx=10, pady=5)
        
        # 相似度显示
        ttk.Label(frame, text="相似度:").grid(row=0, column=0)
        self.similarity_var = tk.StringVar()
        self.similarity_label = ttk.Label(frame, textvariable=self.similarity_var, 
                                         font=('Arial', 14, 'bold'), foreground='blue')
        self.similarity_label.grid(row=0, column=1, sticky=tk.W)
        
        # 差异统计
        ttk.Label(frame, text="差异行数:").grid(row=1, column=0)
        self.diff_var = tk.StringVar()
        ttk.Label(frame, textvariable=self.diff_var).grid(row=1, column=1, sticky=tk.W)
    
    def select_file(self, entry):
        filepath = filedialog.askopenfilename(
            filetypes=[("文本文件", "*.txt"), ("Word文档", "*.docx"), ("PDF文件", "*.pdf"), ("所有文件", "*.*")]
        )
        if filepath:
            entry.delete(0, tk.END)
            entry.insert(0, filepath)
    
    def sync_scroll(self, *args):
        self.text1.yview(*args)
        self.text2.yview(*args)
    
    def compare_files(self):
        file1 = self.file1_entry.get()
        file2 = self.file2_entry.get()
        
        if not file1 or not file2:
            tk.messagebox.showerror("错误", "请选择两个要比较的文件")
            return
        
        # 清空之前的显示
        self.text1.delete(1.0, tk.END)
        self.text2.delete(1.0, tk.END)
        
        # 执行比较
        similarity, diff_lines, diff_details = self.comparator.compare_files(file1, file2)
        
        # 显示结果
        self.similarity_var.set(f"{similarity*100:.2f}%")
        self.diff_var.set(str(len(diff_lines)))
        
        # 显示文件内容并高亮差异
        self.display_file_with_highlight(file1, file2, diff_lines)
    
    def display_file_with_highlight(self, file1, file2, diff_lines):
        # 通过比较器获取文件内容行
        lines1 = self.comparator.get_file_lines(file1)
        lines2 = self.comparator.get_file_lines(file2)
        
        # 配置高亮样式
        self.text1.tag_config('removed', background='#ffdddd')
        self.text2.tag_config('added', background='#ddffdd')
        
        # 清空文本区域
        self.text1.delete(1.0, tk.END)
        self.text2.delete(1.0, tk.END)
        
        # 解析差异行
        diff_map1 = set()
        diff_map2 = set()
        current_line = 0
        
        for diff in diff_lines:
            if diff.startswith('- '):
                diff_map1.add(current_line)
            elif diff.startswith('+ '):
                diff_map2.add(current_line)
            current_line += 1
        
        # 插入文本并标记差异
        for i, line in enumerate(lines1):
            self.text1.insert(tk.END, line + '\n')
            if i in diff_map1:
                self.text1.tag_add('removed', f"{i+1}.0", f"{i+1}.end")
        
        for i, line in enumerate(lines2):
            self.text2.insert(tk.END, line + '\n')
            if i in diff_map2:
                self.text2.tag_add('added', f"{i+1}.0", f"{i+1}.end")

if __name__ == "__main__":
    root = tk.Tk()
    app = FileCompareApp(root)
    root.mainloop()