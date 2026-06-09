@echo off
chcp 65001 > nul
cd /d "%~dp0\.."
echo ========================================
echo Запуск тестов
echo ========================================
call .venv\Scripts\activate.bat
if not exist reports mkdir reports
python manage.py test tests --verbosity=2 > reports\smoke_test_report.txt 2>&1
copy /Y reports\smoke_test_report.txt reports\pytest_report.txt > nul
type reports\smoke_test_report.txt
pause
