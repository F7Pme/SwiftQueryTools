#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from pathlib import Path
import sys

# 添加项目根目录到Python路径
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR))

# 导入数据服务模块
from BackEnd.data_service import SwiftDataService

# 创建Flask应用
app = Flask(__name__)
CORS(app)  # 启用跨域资源共享

# 设置上传文件大小限制
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB

# 前端文件目录
FRONTEND_DIR = ROOT_DIR / 'FrontEnd'

# 初始化数据服务
data_service = SwiftDataService()

@app.route('/')
def index():
    """提供前端首页"""
    return send_from_directory(FRONTEND_DIR, 'index.html')

@app.route('/<path:path>')
def static_files(path):
    """提供前端静态文件"""
    return send_from_directory(FRONTEND_DIR, path)

@app.route('/api/upload', methods=['POST'])
def upload_file():
    """处理Excel文件上传"""
    # 检查是否有文件部分
    if 'file' not in request.files:
        return jsonify({'error': '没有找到上传的文件'}), 400
    
    file = request.files['file']
    
    # 检查文件名是否为空
    if file.filename == '':
        return jsonify({'error': '未选择文件'}), 400
    
    # 检查文件类型
    if not file.filename.endswith(('.xlsx', '.xls')):
        return jsonify({'error': '只支持Excel文件(.xlsx, .xls)'}), 400
    
    # 加载上传的文件
    if data_service.load_from_upload(file):
        # 获取文件信息
        stats = data_service.get_file_stats()
        return jsonify({'success': True, 'message': '文件上传成功', 'stats': stats}), 200
    else:
        return jsonify({'error': '文件处理失败，请确保格式正确'}), 400

@app.route('/api/query')
def query_swift():
    """查询SWIFT代码API"""
    swift_code = request.args.get('swift', '').strip().upper()
    exact_match = request.args.get('exact', 'false').lower() == 'true'
    
    if not swift_code:
        return jsonify({'error': '请提供SWIFT业务编号'}), 400
    
    # 检查是否已加载数据
    if not data_service.is_data_loaded():
        return jsonify({'error': '未加载数据，请先上传Excel文件'}), 400
    
    try:
        results = data_service.query_swift(swift_code, exact_match)
        return jsonify({'results': results})
    except Exception as e:
        app.logger.error(f"查询出错: {str(e)}")
        return jsonify({'error': f'查询出错: {str(e)}'}), 500

@app.route('/api/suggest')
def suggest_swift():
    """根据前缀建议SWIFT代码"""
    prefix = request.args.get('prefix', '').strip().upper()
    limit = int(request.args.get('limit', '10'))
    
    # 检查是否已加载数据
    if not data_service.is_data_loaded():
        return jsonify({'suggestions': []}), 200
    
    try:
        suggestions = data_service.suggest_swift_codes(prefix, limit)
        return jsonify({'suggestions': suggestions})
    except Exception as e:
        app.logger.error(f"获取建议出错: {str(e)}")
        return jsonify({'error': f'获取建议出错: {str(e)}'}), 500

@app.route('/api/status')
def get_status():
    """获取数据加载状态"""
    stats = data_service.get_file_stats()
    return jsonify(stats)

def start_server(host='127.0.0.1', port=5000, debug=False):
    """启动Flask服务器"""
    print(f"服务已启动，访问 http://{host}:{port} 使用查询工具")
    app.run(host=host, port=port, debug=debug)
    return True

if __name__ == '__main__':
    start_server(debug=True) 