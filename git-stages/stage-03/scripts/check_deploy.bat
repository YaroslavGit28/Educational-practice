@echo off
chcp 65001 > nul
cd /d "%~dp0\.."
echo ========================================
echo Проверка развертывания
echo ========================================
docker compose -f docker-compose.prod.yml ps
echo.
echo --- Логи ---
docker compose -f docker-compose.prod.yml logs --tail=80
echo.
echo --- Health check ---
curl -s http://127.0.0.1:8000/api/health/
echo.
pause
