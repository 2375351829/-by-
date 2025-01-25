import tkinter as tk
from tkinter import ttk
import psutil
from port_manager import PortManager

class PortTable:
    def __init__(self, parent):
        self.parent = parent
        self.manager = PortManager()
        
        # 创建带滚动条的表格容器
        self.container = ttk.Frame(self.parent)
        self.container.grid(row=0, column=0, sticky="nsew")
        
        # 配置表格容器网格
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        
        # 创建表格
        self.tree = ttk.Treeview(self.container, columns=(
            "Port", "Protocol", "Local Address", "Status", "PID", "Process Name", "Process Path"), 
            show="headings",
            style="Custom.Treeview")
        
        # 添加分隔线
        ttk.Separator(self.container, orient="horizontal").grid(
            row=1, column=0, columnspan=2, sticky="ew", pady=(5, 0))
        
        # 设置表头
        self.setup_columns()
        
        # 添加滚动条
        self.add_scrollbar()
        
        # 初始化数据
        self.refresh()
        
    def setup_columns(self):
        from .utils import COLUMN_NAMES, COLUMN_WIDTHS
        
        for col in COLUMN_NAMES.keys():
            self.tree.heading(col, text=COLUMN_NAMES[col])
            self.tree.column(col, width=COLUMN_WIDTHS[col])
            
    def add_scrollbar(self):
        vsb = ttk.Scrollbar(self.container, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        
        # 布局
        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        
    def refresh(self):
        # 清空现有数据
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        # 获取新数据
        connections = self.manager.get_connections()
        listen_count = 0
        
        for conn in connections:
            if conn.status == 'LISTEN':
                listen_count += 1
                local_address = f"{conn.laddr.ip}:{conn.laddr.port}"
                try:
                    process = psutil.Process(conn.pid)
                    process_name = process.name()
                    process_path = process.exe()
                except psutil.NoSuchProcess:
                    process_name = "Unknown"
                    process_path = "Unknown"
                
                self.tree.insert("", "end", values=(
                    conn.laddr.port,
                    conn.type.name,
                    local_address,
                    conn.status,
                    conn.pid,
                    process_name,
                    process_path
                ))
        
        # 更新状态栏
        if hasattr(self.parent, 'connection_count'):
            self.parent.connection_count.set(f"连接数：{listen_count}")
