#!/bin/bash

echo "🚀 启动 DownloadHub..."

if ! command -v python3 &> /dev/null; then
    echo "❌ 未找到 Python 3，请先安装 Python 3.8+"
    exit 1
fi

if [ ! -d "venv" ]; then
    echo "📦 创建虚拟环境..."
    python3 -m venv venv
fi

echo "🔧 激活虚拟环境..."
source venv/bin/activate

echo "📥 安装依赖..."
pip install -q -r requirements.txt

echo "✅ 启动服务..."
python run.py
