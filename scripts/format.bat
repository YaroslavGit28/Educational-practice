@echo off
chcp 65001 > nul
cd /d "%~dp0\.."
echo ========================================
echo Форматирование кода
echo ========================================
call .venv\Scripts\activate.bat
black apps magazin tests
ruff check apps magazin tests --fix
echo Форматирование завершено.
pause

