@echo off
chcp 65001 >nul
echo 🚀 启动 DownloadHub...

where python >nul 2>nul
if %errorlevel% neq 0 (
    echo ❌ 未找到 Python，请先安装 Python 3.8+
    pause
    exit /b 1
)

if not exist "venv" (
    echo 📦 创建虚拟环境...
    python -m venv venv
)

echo 🔧 激活虚拟环境...
call venv\Scripts\activate.bat

echo 📥 安装依赖...
pip install -q -r requirements.txt

echo ✅ 启动服务...
python run.py

pause
