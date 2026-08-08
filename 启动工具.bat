@echo off
chcp 936 >nul
title AI成果展
cd /d %~dp0

rem 检查服务是否已在运行
netstat -ano | findstr ":5010" | findstr "LISTENING" >nul 2>&1
if %errorlevel%==0 (
    echo 服务已在运行: http://127.0.0.1:5010
    start http://127.0.0.1:5010
    pause
    exit /b 0
)

echo 正在启动 AI成果展...
start "" pythonw app.py 2>>error.log
timeout /t 2 >nul
echo 服务已启动: http://127.0.0.1:5010
start http://127.0.0.1:5010
pause
