@echo off
chcp 65001 >nul
echo ========================================
echo   博客系统 - Docker 一键启动
echo ========================================
echo.

REM 检查Docker是否安装
where docker >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [错误] Docker未安装，请先安装Docker Desktop
    pause
    exit /b 1
)

REM 检查docker-compose
where docker-compose >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [错误] Docker Compose未安装
    pause
    exit /b 1
)

REM 检查.env文件
if not exist ".env" (
    echo [提示] 未找到.env文件，从.env.example复制...
    copy .env.example .env
    echo.
    echo [重要] 请编辑.env文件配置环境变量
    echo 按任意键继续...
    pause >nul
)

echo [1/3] 构建镜像...
docker-compose build

echo.
echo [2/3] 启动服务...
docker-compose up -d

echo.
echo [3/3] 等待服务就绪...
timeout /t 10 /nobreak >nul

echo.
echo ========================================
echo   服务启动完成！
echo ========================================
echo.
echo   前端: http://localhost:5173
echo   后端API: http://localhost:8000
echo   API文档: http://localhost:8000/api/docs/
echo   PostgreSQL: localhost:5432
echo   Redis: localhost:6379
echo.
echo   常用命令:
echo     docker-compose ps          - 查看服务状态
echo     docker-compose logs -f     - 查看日志
echo     docker-compose down        - 停止服务
echo.
echo ========================================

pause
