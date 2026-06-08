@echo off
chcp 65001 > nul
cd /d "%~dp0\.."
echo ========================================
echo Восстановление из резервной копии
echo ========================================
echo Доступные backup-файлы:
dir /b backups\*.sqlite3 2>nul
echo.
set /p BACKUP_FILE=Введите имя файла backup (например backup_20260608.sqlite3): 
if exist backups\%BACKUP_FILE% (
    copy /Y backups\%BACKUP_FILE% db.sqlite3
    echo База восстановлена из backups\%BACKUP_FILE%
    echo Запустите scripts\run.bat для проверки.
) else (
    echo Файл backups\%BACKUP_FILE% не найден.
)
pause
