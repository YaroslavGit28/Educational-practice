@echo off
chcp 65001 > nul
cd /d "%~dp0\.."
echo ========================================
echo Финальная проверка перед релизом
echo ========================================
call scripts\check.bat
call scripts\build_release.bat
echo Release check completed.
pause
