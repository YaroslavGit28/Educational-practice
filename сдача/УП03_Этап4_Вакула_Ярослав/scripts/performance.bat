@echo off
chcp 65001 > nul
cd /d "%~dp0\.."
echo ========================================
echo Проверка производительности
echo ========================================
if not exist reports mkdir reports
curl -s -o nul -w "Health endpoint: %%{time_total}s HTTP %%{http_code}\n" http://127.0.0.1:8000/api/health/ > reports\performance_summary.txt
curl -s -o nul -w "Главная страница: %%{time_total}s HTTP %%{http_code}\n" http://127.0.0.1:8000/ >> reports\performance_summary.txt
type reports\performance_summary.txt
pause
