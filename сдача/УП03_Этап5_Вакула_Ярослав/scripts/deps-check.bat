@echo off
chcp 65001 > nul
cd /d "%~dp0\.."
echo ========================================
echo Проверка зависимостей
echo ========================================
call .venv\Scripts\activate.bat
pip-audit
echo.
echo --- Устаревшие пакеты ---
pip list --outdated
pause
