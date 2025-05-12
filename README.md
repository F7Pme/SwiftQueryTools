# 跨境汇款查询工具

跨境汇款查询工具是一个帮助用户根据SWIFT编码查询相关银行角色、报文类型和直参行信息的应用。本项目采用前后端分离架构，使用Python和HTML/CSS/JS实现。

## 项目结构

- `FrontEnd/`: 存放前端文件(HTML/CSS/JS)
- `BackEnd/`: 存放后端Python代码
- `FakeData/`: 存放生成的Excel数据
- `Tools/`: 工具脚本，包含假数据生成器
- `main.py`: 主程序入口

## 安装依赖

```bash
pip install -r requirements.txt
```

## 使用方法

1. 首次使用，需要先生成测试数据：

```bash
cd Tools
python GenerateFakeData.py
```

2. 运行主程序：

```bash
python main.py
```

3. 程序会自动在默认浏览器中打开应用，然后您可以输入SWIFT代码进行查询

## 国产Linux适配说明

本项目设计时已考虑国产Linux系统(统信UOS V20/麒麟V10)适配需求：

- 使用跨平台的Python库
- 采用平台无关的路径处理
- 前端使用标准Web技术

## 开发说明

- 后端基于Flask框架提供Web服务和API
- 前端使用原生HTML/CSS/JavaScript实现
- 数据使用pandas处理Excel文件 