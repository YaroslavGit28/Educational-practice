@echo off
chcp 65001 > nul
cd /d "%~dp0\.."
echo ========================================
echo Резервное копирование SQLite БД
echo ========================================
if not exist backups mkdir backups
for /f "tokens=1-4 delims=/.: " %%a in ("%date% %time%") do set TS=%%c%%b%%a_%%d
if exist db.sqlite3 (
    copy /Y db.sqlite3 backups\backup_%TS%.sqlite3
    echo Backup создан: backups\backup_%TS%.sqlite3
) else (
    echo База данных db.sqlite3 не найдена.
)
if exist media (
    xcopy /E /I /Y media backups\media_%TS% > nul
    echo Медиа скопированы: backups\media_%TS%
)
pause
