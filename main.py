import argparse
from port_manager import PortManager
from gui.main_window import MainWindow
import tkinter as tk

def main():
    parser = argparse.ArgumentParser(description="本地端口管理器")
    parser.add_argument('-l', '--list', action='store_true', help='列出所有端口占用情况')
    parser.add_argument('-g', '--gui', action='store_true', help='启动图形界面')
    
    args = parser.parse_args()
    
    if args.gui:
        root = tk.Tk()
        app = MainWindow(root)
        root.mainloop()
    elif args.list:
        manager = PortManager()
        manager.show_connections()
    else:
        print("请使用 -h 查看帮助信息")

if __name__ == "__main__":
    main()
