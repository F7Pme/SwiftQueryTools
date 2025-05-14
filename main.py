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

def main():
    """主函数"""
    print("==== 跨境汇款查询工具 ====")
    
    # 导入后端服务器模块
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