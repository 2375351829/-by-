"""
此程序经供参考
By 凌风逐月工作室
"""


import tkinter as tk
from tkinter import ttk, filedialog
from gui.utils import show_error, show_info, show_warning, confirm_action

class ControlPanel:
    def __init__(self, root, table):
        self.root = root
        self.table = table
        
        # 创建控制面板容器
        self.container = ttk.Frame(self.root)
        self.container.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)
        
        # 配置网格布局
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        self.container.grid_columnconfigure(1, weight=1)
        self.container.grid_columnconfigure(2, weight=1)
        
        # 初始化组件
        self.create_actions_panel()
        self.create_sort_panel()
        self.create_search_panel()
        
    def create_actions_panel(self):
        # 操作按钮面板
        actions_frame = ttk.Frame(self.container)
        actions_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        
        # 刷新按钮
        refresh_btn = ttk.Button(actions_frame, text="刷新", command=self.table.refresh)
        refresh_btn.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        
        # 终止进程按钮
        kill_btn = ttk.Button(actions_frame, text="终止进程", command=self.kill_process)
        kill_btn.grid(row=1, column=0, padx=5, pady=5, sticky="ew")
        
        # 导出按钮
        export_btn = ttk.Button(actions_frame, text="导出", command=self.export_data)
        export_btn.grid(row=2, column=0, padx=5, pady=5, sticky="ew")
        
    def create_sort_panel(self):
        # 排序功能面板
        sort_frame = ttk.Frame(self.container)
        sort_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        
        # 排序标签
        ttk.Label(sort_frame, text="排序方式:").grid(row=0, column=0, sticky="w")
        
        # 排序选项
        self.sort_var = tk.StringVar(value="端口号")
        sort_options = ["端口号", "协议", "本地地址", "状态", "进程ID", "进程名称", "应用程序路径"]
        self.sort_menu = ttk.Combobox(sort_frame, textvariable=self.sort_var, 
                                    values=sort_options, state="readonly")
        self.sort_menu.grid(row=1, column=0, padx=5, pady=5, sticky="ew")
        
        # 排序按钮
        sort_btn = ttk.Button(sort_frame, text="排序", command=self.sort_data)
        sort_btn.grid(row=2, column=0, padx=5, pady=5, sticky="ew")
        
    def create_search_panel(self):
        # 搜索功能面板
        search_frame = ttk.Frame(self.container)
        search_frame.grid(row=0, column=2, sticky="nsew", padx=5, pady=5)
        
        # 搜索标签
        ttk.Label(search_frame, text="查询端口:").grid(row=0, column=0, sticky="w")
        
        # 端口输入框
        self.port_entry = ttk.Entry(search_frame)
        self.port_entry.grid(row=1, column=0, padx=5, pady=5, sticky="ew")
        
        # 搜索按钮
        search_btn = ttk.Button(search_frame, text="查询", command=self.search_port)
        search_btn.grid(row=2, column=0, padx=5, pady=5, sticky="ew")
        
    def kill_process(self):
        selected = self.table.tree.selection()
        if not selected:
            show_warning("请先选择一个进程")
            return
            
        # 获取选中的进程信息
        item = selected[0]
        values = self.table.tree.item(item, 'values')
        pid = int(values[4])  # PID在第5列
        process_name = values[5]  # 进程名称在第6列
        
        # 确认对话框
        if not confirm_action(f"确定要终止进程 {process_name} (PID: {pid}) 吗？"):
            return
            
        try:
            # 调用port_manager的kill_process方法
            self.table.manager.kill_process(pid)
            show_info(f"已成功终止进程 {process_name} (PID: {pid})")
            self.table.refresh()
        except Exception as e:
            show_error(f"终止进程时发生错误: {str(e)}")
        
    def export_data(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV文件", "*.csv")],
            title="保存端口数据"
        )
        
        if not file_path:
            return
            
        try:
            import csv
            with open(file_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                
                # 写入表头
                headers = [self.table.tree.heading(col)['text'] 
                          for col in self.table.tree['columns']]
                writer.writerow(headers)
                
                # 写入数据
                for item in self.table.tree.get_children():
                    row = self.table.tree.item(item)['values']
                    writer.writerow(row)
                    
            show_info(f"数据已成功导出到 {file_path}")
        except Exception as e:
            show_error(f"导出数据时发生错误: {str(e)}")
        
    def sort_data(self):
        sort_by = self.sort_var.get()
        column_map = {
            "端口号": "Port",
            "协议": "Protocol",
            "本地地址": "Local Address",
            "状态": "Status",
            "进程ID": "PID",
            "进程名称": "Process Name",
            "应用程序路径": "Process Path"
        }
        
        if sort_by not in column_map:
            show_error(f"不支持按 {sort_by} 排序")
            return
            
        column = column_map[sort_by]
        items = [(self.table.tree.set(child, column), child) 
                for child in self.table.tree.get_children('')]
        
        # 尝试将值转换为数字进行排序
        try:
            items.sort(key=lambda x: float(x[0]))
        except ValueError:
            items.sort(key=lambda x: x[0])
            
        # 重新排列表格项
        for index, (val, child) in enumerate(items):
            self.table.tree.move(child, '', index)
            
        show_info(f"已按 {sort_by} 排序")
        
    def search_port(self):
        port = self.port_entry.get().strip()
        if not port:
            show_warning("请输入要查询的端口号")
            return
            
        try:
            port = int(port)
            if port < 0 or port > 65535:
                show_error("端口号必须在0到65535之间")
                return
                
            # 清空当前选择
            for item in self.table.tree.selection():
                self.table.tree.selection_remove(item)
                
            # 查找匹配项
            found = False
            for item in self.table.tree.get_children():
                item_port = int(self.table.tree.set(item, "Port"))
                if item_port == port:
                    self.table.tree.selection_add(item)
                    self.table.tree.see(item)
                    found = True
                    
            if not found:
                show_info(f"未找到使用端口 {port} 的连接")
        except ValueError:
            show_error("请输入有效的端口号")
