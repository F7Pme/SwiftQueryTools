#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import random
import pandas as pd
import string
from pathlib import Path

def generate_swift_code():
    """生成随机的11位SWIFT代码"""
    # 前4位是银行代码（字母）
    bank_code = ''.join(random.choices(string.ascii_uppercase, k=4))
    # 中间2位是国家代码（字母）
    country_code = random.choice(['CN', 'US', 'GB', 'JP', 'HK', 'SG', 'DE', 'FR', 'AU', 'CA'])
    # 后2位是地点代码（字母）
    location_code = ''.join(random.choices(string.ascii_uppercase, k=2))
    # 最后3位是分行代码（可选，通常是XXX）
    branch_code = 'XXX'
    
    return f"{bank_code}{country_code}{location_code}{branch_code}"

def generate_fake_data(num_rows=3000):
    """生成假数据并保存为Excel"""
    # 创建存储目录
    fake_data_dir = Path('../FakeData')
    fake_data_dir.mkdir(exist_ok=True)
    
    # 定义报文类型
    message_types = ['CIPS报文', 'MT103', 'MT202', 'MT202COV', 'MT210']
    
    # 生成直接参与者SWIFT列表（约20%的记录）
    direct_participants = [generate_swift_code() for _ in range(int(num_rows * 0.2))]
    
    # 生成数据
    data = []
    for i in range(1, num_rows + 1):
        # 序号
        index = i
        # SWIFT代码
        swift_code = generate_swift_code()
        
        # 决定银行角色 - 80%是间接参与者，20%是直接参与者
        is_direct = swift_code in direct_participants
        bank_role = '直接参与者' if is_direct else '间接参与者'
        
        # 直参行代码 - 只有间接参与者才有
        direct_participant = None if is_direct else random.choice(direct_participants)
        
        # 报文类型
        message_type = random.choice(message_types)
        
        # 添加到数据列表
        data.append({
            '序号': index,
            'SWIFTCODE': swift_code,
            '银行角色': bank_role,
            '直参行SWIFTCODE': direct_participant,
            '报文类型': message_type
        })
    
    # 创建pandas DataFrame
    df = pd.DataFrame(data)
    
    # 保存到Excel
    output_file = fake_data_dir / 'swift_data.xlsx'
    df.to_excel(output_file, index=False, engine='openpyxl')
    
    print(f"已生成假数据并保存至: {output_file}")
    return str(output_file)

if __name__ == "__main__":
    # 确保在脚本所在目录运行
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    file_path = generate_fake_data()
    print(f"假数据生成完成！文件位置: {file_path}")
    print("现在可以运行主程序 main.py 使用查询工具了。") 