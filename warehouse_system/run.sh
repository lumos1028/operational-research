#!/bin/bash

# 多机器人仓储系统启动脚本

echo "=========================================="
echo "多机器人仓储系统启动"
echo "=========================================="
echo ""

# 检查Python版本
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误: 未找到Python3"
    exit 1
fi

echo "✅ Python版本: $(python3 --version)"
echo ""

# 进入backend目录
cd backend

# 检查虚拟环境
if [ ! -d "venv" ]; then
    echo "📦 创建虚拟环境..."
    python3 -m venv venv
fi

# 激活虚拟环境
echo "🔧 激活虚拟环境..."
source venv/bin/activate

# 安装依赖
echo "📥 安装依赖..."
pip install -r requirements.txt -q

echo ""
echo "✅ 依赖安装完成"
echo ""

# 启动Flask服务器
echo "🚀 启动后端服务器..."
echo "服务器地址: http://localhost:5000"
echo ""
python app.py

# 运行完成
deactivate
