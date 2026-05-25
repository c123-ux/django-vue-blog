@echo off
chcp 65001 >nul
echo ========================================
echo   博客系统 - 快速启动脚本
echo ========================================
echo.

REM 检查虚拟环境
if not exist ".venv\Scripts\activate.bat" (
    echo [错误] 虚拟环境不存在，请先运行: python -m venv .venv
    pause
    exit /b 1
)

echo [1/4] 激活虚拟环境...
call .venv\Scripts\activate.bat

echo [2/4] 安装依赖...
pip install -r requirements.txt -q

echo [3/4] 数据库迁移...
python manage.py migrate --noinput

echo [4/4] 启动开发服务器...
echo.
echo ========================================
echo   后端服务已启动
echo   访问地址: http://localhost:8000
echo   API文档: http://localhost:8000/api/docs/
echo   按 Ctrl+C 停止服务
echo ========================================
echo.

python manage.py runserver
