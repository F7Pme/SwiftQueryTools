#!/bin/bash

# 设置颜色输出
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # 无颜色

echo -e "${GREEN}====== 跨境汇款查询工具安装启动脚本 ======${NC}"
echo -e "正在检查必要组件..."

# 获取脚本所在目录的绝对路径
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
cd "$SCRIPT_DIR"

# 检查Python
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}未检测到Python3！安装失败。${NC}"
    echo -e "请先安装Python3: sudo apt update && sudo apt install python3 python3-pip"
    exit 1
fi

# 检查pip
if ! command -v pip3 &> /dev/null; then
    echo -e "${YELLOW}未检测到pip3，尝试安装...${NC}"
    sudo apt update
    sudo apt install -y python3-pip
    if [ $? -ne 0 ]; then
        echo -e "${RED}安装pip3失败，请手动安装后再试！${NC}"
        exit 1
    fi
fi

echo -e "${GREEN}检测到Python $(python3 --version)${NC}"

# 创建虚拟环境（如果不存在）
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}正在创建Python虚拟环境...${NC}"
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo -e "${YELLOW}虚拟环境创建失败，尝试安装venv模块...${NC}"
        sudo apt install -y python3-venv
        python3 -m venv venv
        if [ $? -ne 0 ]; then
            echo -e "${RED}虚拟环境创建失败，将使用系统Python环境...${NC}"
            USE_VENV=0
        else
            USE_VENV=1
        fi
    else
        USE_VENV=1
    fi
else
    USE_VENV=1
    echo -e "${GREEN}检测到已有虚拟环境${NC}"
fi

# 激活虚拟环境
if [ $USE_VENV -eq 1 ]; then
    echo -e "${YELLOW}激活虚拟环境...${NC}"
    source venv/bin/activate
fi

# 安装依赖
echo -e "${YELLOW}安装依赖包...${NC}"
pip3 install -r requirements.txt

if [ $? -ne 0 ]; then
    echo -e "${RED}依赖安装失败！${NC}"
    echo -e "您可以尝试手动执行: pip3 install -r requirements.txt"
    exit 1
fi

echo -e "${GREEN}依赖安装完成！${NC}"

# 检查Data目录
if [ ! -d "Data" ]; then
    mkdir -p Data
    echo -e "${YELLOW}已创建Data目录${NC}"
fi

# 运行程序
echo -e "${GREEN}启动应用程序...${NC}"
echo -e "${YELLOW}应用启动后将在浏览器中打开，或手动访问: http://127.0.0.1:5000${NC}"
echo -e "${YELLOW}按Ctrl+C可终止程序${NC}"

# 运行程序
python3 main.py

# 如果Python进程结束，进行清理
if [ $USE_VENV -eq 1 ]; then
    deactivate
fi

echo -e "${GREEN}程序已退出${NC}" 