@echo off
chcp 65001 > nul
cd /d "%~dp0\.."
echo ========================================
echo Запуск интернет-магазина
echo ========================================
if not exist .venv\Scripts\python.exe (
    echo Сначала выполните: scripts\setup.bat
    pause
    exit /b 1
)
.venv\Scripts\python.exe manage.py runserver 0.0.0.0:8000

