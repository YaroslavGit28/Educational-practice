@echo off
chcp 65001 > nul
cd /d "%~dp0\.."
if "%~1"=="" (
    echo Использование: scripts\apply-stage.bat 1
    echo Этапы: 1-6
    pause
    exit /b 1
)
powershell -ExecutionPolicy Bypass -File scripts\apply-stage.ps1 -Stage %1
pause
