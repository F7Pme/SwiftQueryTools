#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import pandas as pd
import io
import tempfile
from pathlib import Path
import uuid

class SwiftDataService:
    """SWIFT数据服务类，负责数据加载和查询"""
    
    def __init__(self):
        """初始化数据服务"""
        # 数据存储
        self.data = None
        # 临时文件目录
        self.temp_dir = tempfile.gettempdir()
        # 用户上传的文件
        self.uploaded_file = None
        # 是否已加载数据
        self.data_loaded = False
    
    def load_from_upload(self, file_storage):
        """从上传的文件中加载数据
        
        Args:
            file_storage: Flask's FileStorage对象
        
        Returns:
            bool: 是否成功加载
        """
        try:
            # 保存上传的文件到临时目录
            filename = str(uuid.uuid4()) + ".xlsx"
            temp_path = os.path.join(self.temp_dir, filename)
            file_storage.save(temp_path)
            self.uploaded_file = temp_path
            
            # 从临时文件加载数据
            self.data = pd.read_excel(temp_path)
            self.data_loaded = True
            
            print(f"已从上传文件加载 {len(self.data)} 条SWIFT记录")
            return True
        except Exception as e:
            print(f"加载上传文件失败: {str(e)}")
            return False
    
    def load_from_bytes(self, file_bytes):
        """从文件字节数据加载
        
        Args:
            file_bytes: 文件的二进制数据
            
        Returns:
            bool: 是否成功加载
        """
        try:
            # 使用BytesIO从内存中读取Excel
            file_stream = io.BytesIO(file_bytes)
            self.data = pd.read_excel(file_stream)
            self.data_loaded = True
            
            print(f"已从上传数据加载 {len(self.data)} 条SWIFT记录")
            return True
        except Exception as e:
            print(f"加载数据失败: {str(e)}")
            return False
    
    def is_data_loaded(self):
        """检查数据是否已加载"""
        return self.data_loaded
    
    def query_swift(self, swift_code, exact_match=False):
        """查询SWIFT代码
        
        Args:
            swift_code: 要查询的SWIFT代码
            exact_match: 是否精确匹配，False表示模糊匹配
        """
        if not self.data_loaded:
            return {"error": "未加载数据，请先上传Excel文件"}
        
        # 查询结果
        try:
            if exact_match:
                # 精确匹配
                results = self.data[self.data['SWIFTCODE'].str.upper() == swift_code.upper()]
            else:
                # 模糊匹配 - 包含输入字符串的所有记录
                results = self.data[self.data['SWIFTCODE'].str.upper().str.contains(swift_code.upper())]
            
            if len(results) == 0:
                return []
            
            # 转换为字典列表
            result_list = []
            for _, row in results.iterrows():
                result_dict = {
                    'swift_code': row['SWIFTCODE'],
                    'bank_role': row['银行角色'],
                    'message_type': row['报文类型'],
                    'direct_participant': row['直参行SWIFTCODE'] if pd.notna(row['直参行SWIFTCODE']) else None
                }
                result_list.append(result_dict)
            
            return result_list
        except Exception as e:
            return {"error": f"查询失败: {str(e)}"}
        
    def suggest_swift_codes(self, prefix, limit=10):
        """根据前缀建议SWIFT代码
        
        Args:
            prefix: SWIFT代码前缀
            limit: 返回结果限制
        """
        if not self.data_loaded:
            return []
            
        if not prefix:
            return []
        
        try:
            # 查找所有以前缀开头的SWIFT代码
            results = self.data[self.data['SWIFTCODE'].str.upper().str.contains(prefix.upper())]
            
            # 限制结果数量
            results = results.head(limit)
            
            # 只返回SWIFT代码列表
            return results['SWIFTCODE'].tolist()
        except Exception:
            return []
    
    def get_file_stats(self):
        """获取加载的文件统计信息"""
        if not self.data_loaded:
            return {"loaded": False}
        
        return {
            "loaded": True,
            "records": len(self.data),
            "columns": list(self.data.columns)
        }
    
    def cleanup(self):
        """清理临时文件"""
        if self.uploaded_file and os.path.exists(self.uploaded_file):
            try:
                os.remove(self.uploaded_file)
                print(f"已删除临时文件: {self.uploaded_file}")
            except:
                pass 