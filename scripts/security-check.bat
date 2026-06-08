@echo off
chcp 65001 > nul
cd /d "%~dp0\.."
echo === Проверка подозрительных слов в проекте ===
findstr /s /i /n "password secret token api_key apikey jwt smtp database_url" apps\*.py magazin\*.py 2>nul | findstr /v /i "change_me example demo clean_password forms.ValidationError"
echo.
echo === Проверка .gitignore ===
findstr /i ".env backups logs db.sqlite3" .gitignore
echo.
echo === Git status ===
git status --short 2>nul || echo Git не инициализирован
pause
