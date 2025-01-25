import tkinter as tk
from tkinter import ttk
from .table_component import PortTable
from .control_panel import ControlPanel
import os

class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("端口管理器")
        
        # 设置窗口图标
        icon_path = os.path.join(os.path.dirname(__file__), "icon.ico")
        if os.path.exists(icon_path):
            self.root.iconbitmap(icon_path)
        
        # 应用主题
        self.style = ttk.Style()
        self.style.theme_use("clam")
        
        # 自定义样式
        self.style.configure("TFrame", background="#f0f0f0")
        self.style.configure("TLabel", background="#f0f0f0")
        self.style.configure("TButton", padding=5)
        self.style.configure("Treeview", 
                           background="#ffffff",
                           fieldbackground="#ffffff",
                           foreground="#333333")
        self.style.map("Treeview",
                      background=[("selected", "#0078d7")],
                      foreground=[("selected", "#ffffff")])
        
        # 设置窗口大小
        self.setup_window_size()
        
        # 配置网格布局
        self.root.grid_rowconfigure(0, weight=0)  # 工具栏
        self.root.grid_rowconfigure(1, weight=1)  # 表格区域
        self.root.grid_rowconfigure(2, weight=0)  # 状态栏
        self.root.grid_columnconfigure(0, weight=1)
        
        # 创建顶部工具栏
        self.toolbar = ttk.Frame(self.root)
        self.toolbar.grid(row=0, column=0, sticky="ew", padx=10, pady=(10, 5))
        
        # 创建主容器
        self.main_container = ttk.Frame(self.root)
        self.main_container.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)
        self.main_container.grid_rowconfigure(0, weight=1)
        self.main_container.grid_columnconfigure(0, weight=1)
        
        # 创建状态栏
        self.status_bar = ttk.Frame(self.root)
        self.status_bar.grid(row=2, column=0, sticky="ew", padx=10, pady=(5, 10))
        
        # 状态栏布局
        self.status_bar.grid_columnconfigure(0, weight=1)
        self.status_bar.grid_columnconfigure(1, weight=0)
        
        # 初始化组件
        self.table = PortTable(self.main_container)
        self.control_panel = ControlPanel(self.toolbar, self.table)
        
        # 初始化状态栏
        self.init_status_bar()
        
        # 绑定窗口大小变化事件
        self.root.bind("<Configure>", self.on_window_resize)
        
    def setup_window_size(self):
        # 获取屏幕尺寸
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        # 设置窗口大小为屏幕的80%
        width = int(screen_width * 0.8)
        height = int(screen_height * 0.8)
        self.root.geometry(f"{width}x{height}")
        
        # 设置窗口最小大小
        self.root.minsize(800, 600)
        
    def init_status_bar(self):
        # 连接数显示
        self.connection_count = tk.StringVar()
        self.connection_count.set("连接数：0")
        
        ttk.Label(self.status_bar, 
                 textvariable=self.connection_count,
                 font=("Arial", 9)).grid(row=0, column=0, sticky="w", padx=10)
        
        # 状态信息
        self.status_text = tk.StringVar()
        self.status_text.set("就绪")
        
        ttk.Label(self.status_bar,
                 textvariable=self.status_text,
                 font=("Arial", 9)).grid(row=0, column=1, sticky="e", padx=10)
        
    def on_window_resize(self, event):
        # 更新状态栏信息
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        self.status_text.set(f"窗口大小：{width}x{height}")
