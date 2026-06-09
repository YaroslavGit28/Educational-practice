@echo off
chcp 65001 > nul
cd /d "%~dp0\.."
echo ========================================
echo API-тестирование
echo ========================================
if not exist reports mkdir reports
echo HTTP/API checks > reports\api_test_report.txt
echo. >> reports\api_test_report.txt
echo GET / >> reports\api_test_report.txt
curl -s -o nul -w "HTTP %%{http_code}\n" http://127.0.0.1:8000/ >> reports\api_test_report.txt
echo GET /api/health/ >> reports\api_test_report.txt
curl -s http://127.0.0.1:8000/api/health/ >> reports\api_test_report.txt
echo. >> reports\api_test_report.txt
echo GET /catalog/ >> reports\api_test_report.txt
curl -s -o nul -w "HTTP %%{http_code}\n" http://127.0.0.1:8000/catalog/ >> reports\api_test_report.txt
echo GET /orders/99999/ (ожидается 302) >> reports\api_test_report.txt
curl -s -o nul -w "HTTP %%{http_code}\n" http://127.0.0.1:8000/orders/99999/ >> reports\api_test_report.txt
echo GET /missing-page/ (ожидается 404) >> reports\api_test_report.txt
curl -s -o nul -w "HTTP %%{http_code}\n" http://127.0.0.1:8000/missing-page/ >> reports\api_test_report.txt
copy /Y reports\api_test_report.txt reports\api_test_result.txt > nul
type reports\api_test_report.txt
pause
