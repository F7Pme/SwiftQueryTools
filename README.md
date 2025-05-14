# 跨境汇款查询工具

跨境汇款查询工具是一个帮助用户根据SWIFT编码查询相关银行角色、报文类型和直参行信息的应用。本项目采用前后端分离架构，使用Python和HTML/CSS/JS实现，支持Windows和Linux平台运行。

## 功能介绍

- 通过上传Excel文件导入SWIFT编码数据
- 支持文件拖拽上传功能
- 模糊查询匹配SWIFT编码
- 实时显示匹配建议
- 查询结果展示银行角色、报文类型、直参行等信息

## 项目结构

- `FrontEnd/`: 存放前端文件(HTML/CSS/JS)
- `BackEnd/`: 存放后端Python代码
- `Data/`: 存放上传的数据文件（临时）
- `Tools/`: 工具脚本，包含假数据生成器
- `main.py`: 主程序入口

## 系统要求

- Python 3.7+
- 支持的操作系统：
  - Windows 10/11
  - Linux（包括统信UOS V20、麒麟V10等国产Linux）

## 安装步骤

### Windows环境

1. 安装Python 3.7+（建议使用Python 3.9）
2. 下载或克隆本项目
3. 安装依赖：
```bash
pip install -r requirements.txt
```

### Linux环境（含国产Linux）

1. 确保系统已安装Python 3.7+：
```bash
python3 --version
```

2. 安装Python开发包和pip（如尚未安装）：
```bash
# Debian/Ubuntu/UOS
sudo apt update
sudo apt install python3-pip python3-dev

# CentOS/RHEL/Kylin
sudo yum install python3-pip python3-devel
```

3. 下载或克隆本项目：
```bash
git clone [项目地址] # 如果可用
# 或解压下载的ZIP文件
```

4. 安装项目依赖（建议使用虚拟环境）：
```bash
# 创建虚拟环境（可选）
python3 -m venv venv
source venv/bin/activate

# 安装依赖
pip3 install -r requirements.txt
```

## 使用方法

1. 启动应用：
```bash
# Windows
python main.py

# Linux
python3 main.py
```

2. 应用将自动在默认浏览器中打开，如未打开可手动访问：`http://127.0.0.1:5000`

3. 使用流程：
   - 上传Excel数据文件（支持.xlsx和.xls格式）
   - 在搜索框中输入SWIFT编码查询
   - 可以点击显示的建议快速选择
   - 查看查询结果
   - 如需更换数据文件，点击"重新上传文件"按钮

## Excel文件格式要求

上传的Excel文件必须包含以下列：
- `SWIFTCODE`：银行的SWIFT代码 
- `银行角色`：如"直接参与者"、"间接参与者"
- `直参行SWIFTCODE`：对应的直接参与者SWIFT代码
- `报文类型`：如"CIPS报文"、"MT103"等

如需生成测试数据进行体验，可以运行：
```bash
# Windows
python Tools/GenerateFakeData.py

# Linux
python3 Tools/GenerateFakeData.py
```

## 常见问题解决

1. **无法启动服务**
   - 检查端口5000是否被占用，可修改main.py中的端口号
   - 确保已安装所有依赖

2. **浏览器未自动打开**
   - 手动访问：http://127.0.0.1:5000
   - 在Linux环境中，确保系统已配置默认浏览器

3. **文件上传失败**
   - 确保Excel文件格式正确
   - 检查文件大小是否超过16MB限制
   - 检查是否有写入权限

4. **国产Linux兼容性问题**
   - 如果遇到中文显示问题，确保系统已安装中文字体
   - 在部分环境中可能需要安装额外的依赖：`sudo apt install python3-tk`（UOS）或`sudo yum install python3-tkinter`（麒麟）

## 技术支持

如有任何问题，请联系技术支持或提交Issue。 