"""
此程序经供参考
By 凌风逐月工作室
"""

from tkinter import messagebox

def show_error(message):
    """显示错误消息对话框"""
    messagebox.showerror("错误", message)

def show_info(message):
    """显示信息对话框"""
    messagebox.showinfo("信息", message)

def show_warning(message):
    """显示警告对话框"""
    messagebox.showwarning("警告", message)

def confirm_action(message):
    """显示确认对话框"""
    return messagebox.askyesno("确认", message)

# 常量定义
COLUMN_NAMES = {
    "Port": "端口号",
    "Protocol": "协议", 
    "Local Address": "本地地址",
    "Status": "状态",
    "PID": "进程ID",
    "Process Name": "进程名称",
    "Process Path": "应用程序路径"
}

COLUMN_WIDTHS = {
    "Port": 80,
    "Protocol": 80,
    "Local Address": 150,
    "Status": 80,
    "PID": 80,
    "Process Name": 150,
    "Process Path": 300
}
