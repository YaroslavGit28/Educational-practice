@echo off
chcp 65001 > nul
cd /d "%~dp0\.."
echo ========================================
echo Перезапуск сервиса
echo ========================================
docker compose -f docker-compose.prod.yml down
docker compose -f docker-compose.prod.yml up --build -d
docker compose -f docker-compose.prod.yml ps
pause
