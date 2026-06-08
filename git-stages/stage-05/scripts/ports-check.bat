@echo off
chcp 65001 > nul
cd /d "%~dp0\.."
echo === Docker-контейнеры и порты ===
docker compose ps 2>nul
docker compose -f docker-compose.prod.yml ps 2>nul
echo.
echo === Порты Windows (LISTENING) ===
netstat -ano | findstr LISTENING | findstr ":8000 :5432 :80 "
pause
