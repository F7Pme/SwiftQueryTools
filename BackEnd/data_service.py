#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import pandas as pd
from pathlib import Path

class SwiftDataService:
    """SWIFT数据服务类，负责数据加载和查询"""
    
    def __init__(self):
        """初始化数据服务"""
        # 项目根目录
        self.root_dir = Path(__file__).resolve().parent.parent
        # 数据文件路径
        self.data_file = self.root_dir / 'FakeData' / 'swift_data.xlsx'
        # 数据存储
        self.data = None
    
    def check_data_file(self):
        """检查数据文件是否存在"""
        return self.data_file.exists()
    
    def load_data(self):
        """加载Excel数据"""
        if not self.check_data_file():
            raise FileNotFoundError(f"数据文件不存在: {self.data_file}")
        
        try:
            # 使用pandas读取Excel文件
            self.data = pd.read_excel(self.data_file)
            print(f"已加载 {len(self.data)} 条SWIFT记录")
        except Exception as e:
            raise Exception(f"加载数据文件失败: {str(e)}")
    
    def query_swift(self, swift_code):
        """查询SWIFT代码"""
        if self.data is None:
            self.load_data()
        
        # 过滤匹配的SWIFT代码记录
        results = self.data[self.data['SWIFTCODE'].str.upper() == swift_code.upper()]
        
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