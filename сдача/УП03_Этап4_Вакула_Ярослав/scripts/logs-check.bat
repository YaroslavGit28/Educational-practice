@echo off
chcp 65001 > nul
cd /d "%~dp0\.."
echo ========================================
echo Проверка логов
echo ========================================
if not exist reports mkdir reports
if exist logs\app.log (
    powershell -Command "Get-Content logs\app.log -Tail 100" > reports\logs_tail.txt
    type reports\logs_tail.txt
) else (
    echo Лог-файл не найден > reports\logs_tail.txt
)
pause
