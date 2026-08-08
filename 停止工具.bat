@echo off
chcp 936 >nul
title Greenthink - Stop Service
cd /d %~dp0

echo 正在停止 Greenthink 服务...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":5010" ^| findstr "LISTENING"') do taskkill /f /pid %%a >nul 2>&1

echo 服务已停止（端口 5010 已释放）
pause
