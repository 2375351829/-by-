import psutil
import prettytable
import os

class PortManager:
    def __init__(self):
        self.connections = []
        self.table = prettytable.PrettyTable()
        self.table.field_names = ["Port", "Protocol", "Local Address", "Status", "PID", "Process Name", "Process Path"]

    def kill_process(self, pid):
        """终止指定进程"""
        try:
            process = psutil.Process(pid)
            process.terminate()
            process.wait(timeout=3)
        except psutil.NoSuchProcess:
            raise Exception(f"进程 {pid} 不存在")
        except psutil.AccessDenied:
            raise Exception(f"没有权限终止进程 {pid}")
        except Exception as e:
            raise Exception(f"终止进程失败: {str(e)}")

    def get_connections(self):
        """获取所有网络连接"""
        self.connections = psutil.net_connections(kind='inet')
        # 每次获取新连接时初始化表格
        self.table = prettytable.PrettyTable()
        self.table.field_names = ["Port", "Protocol", "Local Address", "Status", "PID", "Process Name", "Process Path"]
        return self.connections
        
    def parse_connections(self):
        """解析连接信息"""
        for conn in self.connections:
            if conn.status == 'LISTEN':
                local_address = f"{conn.laddr.ip}:{conn.laddr.port}"
                pid = conn.pid
                try:
                    process = psutil.Process(pid)
                    process_name = process.name()
                    process_path = process.exe()
                except psutil.NoSuchProcess:
                    process_name = "Unknown"
                    process_path = "Unknown"
                
                # 提取端口号
                port = str(conn.laddr.port)
                self.table.add_row([
                    port,
                    conn.type.name,
                    local_address,
                    conn.status,
                    pid,
                    process_name,
                    process_path
                ])
    
    def show_connections(self):
        """显示端口占用情况"""
        self.get_connections()
        self.parse_connections()
        print(self.table)

    def export_to_txt(self, filepath):
        """导出端口信息到txt文件"""
        self.get_connections()
        self.parse_connections()
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(str(self.table))

    def check_port(self, port):
        """检查端口是否被占用"""
        self.get_connections()
        for conn in self.connections:
            if conn.status == 'LISTEN' and conn.laddr.port == port:
                try:
                    process = psutil.Process(conn.pid)
                    return {
                        'status': 'occupied',
                        'process': {
                            'pid': conn.pid,
                            'name': process.name(),
                            'path': process.exe(),
                            'is_system': process.username() == 'SYSTEM'
                        }
                    }
                except psutil.NoSuchProcess:
                    return {'status': 'occupied', 'process': None}
        return {'status': 'available'}

if __name__ == "__main__":
    manager = PortManager()
    manager.show_connections()
