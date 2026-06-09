@echo off
chcp 65001 > nul
cd /d "%~dp0\.."
echo ========================================
echo Логи приложения
echo ========================================
if exist logs\app.log (
    powershell -Command "Get-Content logs\app.log -Tail 80"
) else (
    echo Лог-файл logs\app.log пока не создан.
)
if exist docker-compose.yml (
    echo.
    echo --- Docker logs ---
    docker compose logs --tail=50 2>nul
)
pause

