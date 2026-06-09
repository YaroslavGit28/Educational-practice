@echo off
chcp 65001 > nul
cd /d "%~dp0\.."
echo ========================================
echo Production/Demo развертывание
echo ========================================
if not exist .env.production (
    if exist .env.demo.example (
        copy .env.demo.example .env.production
    ) else (
        copy .env.production.example .env.production
    )
)
docker compose -f docker-compose.prod.yml up --build -d
docker compose -f docker-compose.prod.yml ps
echo.
echo Приложение: http://127.0.0.1:8000/
pause
