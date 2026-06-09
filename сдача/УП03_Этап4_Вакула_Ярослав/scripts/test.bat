@echo off
chcp 65001 > nul
cd /d "%~dp0\.."
echo ========================================
echo Запуск тестов
echo ========================================
call .venv\Scripts\activate.bat
if not exist reports mkdir reports
python manage.py test tests --verbosity=2 > reports\pytest_report.txt 2>&1
type reports\pytest_report.txt
pause
