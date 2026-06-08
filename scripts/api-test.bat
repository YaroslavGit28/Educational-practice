@echo off
chcp 65001 > nul
cd /d "%~dp0\.."
echo ========================================
echo API-тестирование
echo ========================================
if not exist reports mkdir reports
echo GET /api/health/ > reports\api_test_result.txt
curl -s http://127.0.0.1:8000/api/health/ >> reports\api_test_result.txt
echo. >> reports\api_test_result.txt
echo GET /orders/99999/ (ожидается 302/404) >> reports\api_test_result.txt
curl -s -o nul -w "HTTP %%{http_code}" http://127.0.0.1:8000/orders/99999/ >> reports\api_test_result.txt
echo. >> reports\api_test_result.txt
type reports\api_test_result.txt
pause
