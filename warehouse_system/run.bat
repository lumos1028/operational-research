@echo off
REM 多机器人仓储系统启动脚本（Windows）

echo ==========================================
echo 多机器人仓储系统启动
echo ==========================================
echo.

REM 检查Python版本
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 错误: 未找到Python
    pause
    exit /b 1
)

echo ✅ Python已安装
echo.

REM 进入backend目录
cd backend

REM 检查虚拟环境
if not exist "venv" (
    echo 📦 创建虚拟环境...
    python -m venv venv
)

REM 激活虚拟环境
echo 🔧 激活虚拟环境...
call venv\Scripts\activate.bat

REM 安装依赖
echo 📥 安装依赖...
pip install -r requirements.txt

echo.
echo ✅ 依赖安装完成
echo.

REM 启动Flask服务器
echo 🚀 启动后端服务器...
echo 服务器地址: http://localhost:5000
echo.
python app.py

REM 运行完成
deactivate
pause
