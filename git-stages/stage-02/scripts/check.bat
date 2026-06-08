@echo off
chcp 65001 > nul
cd /d "%~dp0\.."
echo ========================================
echo Проверка качества проекта
echo ========================================
set PY=.venv\Scripts\python.exe
if not exist %PY% (
    echo Сначала выполните: scripts\setup.bat
    pause
    exit /b 1
)
%PY% manage.py check
if errorlevel 1 exit /b 1
%PY% manage.py test tests --verbosity=1
if errorlevel 1 exit /b 1
%PY% -m compileall apps magazin tests -q
if errorlevel 1 exit /b 1
echo.
echo Все проверки пройдены.
pause
