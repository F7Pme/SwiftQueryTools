#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import time
import webbrowser
from pathlib import Path
import subprocess

# 项目根目录
ROOT_DIR = Path(__file__).resolve().parent
# 数据文件路径
DATA_FILE = ROOT_DIR / 'FakeData' / 'swift_data.xlsx'

def check_data_file():
    """检查数据文件是否存在"""
    return DATA_FILE.exists()

def generate_data():
    """运行数据生成脚本"""
    generator_path = ROOT_DIR / 'Tools' / 'GenerateFakeData.py'
    
    print("正在生成测试数据...")
    try:
        # 使用Python执行GenerateFakeData.py脚本
        subprocess.run([sys.executable, str(generator_path)], check=True)
        print("数据生成成功！")
        return True
    except subprocess.CalledProcessError as e:
        print(f"数据生成失败: {e}")
        return False

def main():
    """主函数"""
    print("==== 跨境汇款查询工具 ====")
    
    # 检查数据文件是否存在
    if not check_data_file():
        print("未找到数据文件。")
        user_input = input("是否生成测试数据？(y/n): ").strip().lower()
        
        if user_input == 'y':
            if not generate_data():
                print("无法继续，请手动运行 Tools/GenerateFakeData.py 生成测试数据")
                return
        else:
            print("请先运行 Tools/GenerateFakeData.py 生成测试数据，然后再运行 main.py")
            return
    
    # 导入后端服务器模块（在确认数据存在后导入，避免导入错误）
    sys.path.append(str(ROOT_DIR))
    from BackEnd.server import start_server
    
    # 定义服务器参数
    host = '127.0.0.1'
    port = 5000
    
    # 启动浏览器
    url = f"http://{host}:{port}"
    print(f"正在启动浏览器访问：{url}")
    
    # 等待短暂时间后启动浏览器，确保服务器有时间启动
    def open_browser():
        time.sleep(1.5)
        webbrowser.open(url)
    
    # 启动浏览器线程
    import threading
    threading.Thread(target=open_browser, daemon=True).start()
    
    # 启动服务器
    start_server(host=host, port=port, debug=False)

if __name__ == "__main__":
    main() 