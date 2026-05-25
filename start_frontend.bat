@echo off
chcp 65001 >nul
echo ========================================
echo   博客前端 - 快速启动脚本
echo ========================================
echo.

cd blog-frontend

REM 检查node_modules
if not exist "node_modules" (
    echo [1/2] 安装依赖...
    call npm install
) else (
    echo [1/2] 依赖已存在
)

echo [2/2] 启动开发服务器...
echo.
echo ========================================
echo   前端服务已启动
echo   访问地址: http://localhost:5173
echo   按 Ctrl+C 停止服务
echo ========================================
echo.

call npm run dev
