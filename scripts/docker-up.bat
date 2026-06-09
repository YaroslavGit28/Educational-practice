@echo off
chcp 65001 > nul
cd /d "%~dp0\.."
echo ========================================
echo Запуск Docker Compose
echo ========================================
if not exist .env copy .env.example .env
docker compose up --build -d
docker compose exec -T app python manage.py migrate --noinput
docker compose exec -T app python manage.py load_demo_data
docker compose logs -f app

