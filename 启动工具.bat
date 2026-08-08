@echo off
chcp 936 >nul
title Greenthink
cd /d %~dp0

rem 从注册表读取管理员密码（不入代码、不入 git），未设置则用默认
for /f "tokens=2*" %%a in ('reg query "HKCU\Environment" /v GREENTHINK_ADMIN_PASSWORD 2^>nul') do set GREENTHINK_ADMIN_PASSWORD=%%b

rem 检查服务是否已在运行
netstat -ano | findstr ":5010" | findstr "LISTENING" >nul 2>&1
if %errorlevel%==0 (
    echo 服务已在运行: http://127.0.0.1:5010
    start http://127.0.0.1:5010
    pause
    exit /b 0
)

echo 正在启动 Greenthink...
start "" pythonw app.py 2>>error.log
timeout /t 2 >nul
echo 服务已启动: http://127.0.0.1:5010
start http://127.0.0.1:5010
pause
