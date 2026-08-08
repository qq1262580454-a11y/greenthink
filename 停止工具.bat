@echo off
chcp 936 >nul
title AI成果展 - 停止服务
cd /d %~dp0

echo 正在停止 AI成果展 服务...

rem 按端口 5010 精确结束监听进程（不误杀其他 app.py 服务）
for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":5010" ^| findstr "LISTENING"') do taskkill /f /pid %%a >nul 2>&1

echo 服务已停止（端口 5010 已释放）
pause
