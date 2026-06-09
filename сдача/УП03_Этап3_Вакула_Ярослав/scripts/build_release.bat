@echo off
chcp 65001 > nul
cd /d "%~dp0\.."
echo ========================================
echo Сборка release-архива
echo ========================================
powershell -ExecutionPolicy Bypass -File scripts\create-release.ps1
pause
