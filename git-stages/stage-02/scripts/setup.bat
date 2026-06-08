@echo off
chcp 65001 > nul
cd /d "%~dp0\.."

set PY=.venv\Scripts\python.exe
set PIP=.venv\Scripts\pip.exe

echo ========================================
echo Установка зависимостей проекта
echo ========================================

if not exist .venv (
    echo Создание виртуального окружения .venv ...
    python -m venv .venv
    if errorlevel 1 (
        echo ОШИБКА: не удалось создать .venv. Установите Python 3.12.
        pause
        exit /b 1
    )
)

if not exist %PY% (
    echo ОШИБКА: %PY% не найден.
    pause
    exit /b 1
)

echo Используется: %PY%
%PY% --version

echo.
echo Установка основных зависимостей (requirements.txt) ...
%PY% -m pip install --default-timeout=120 -r requirements.txt
if errorlevel 1 (
    echo.
    echo ВНИМАНИЕ: pip не смог скачать пакеты с pypi.org.
    echo Если Django уже установлен в .venv — продолжаем без обновления.
    %PY% -c "import django" 2>nul
    if errorlevel 1 (
        echo ОШИБКА: Django не установлен. Проверьте интернет или VPN.
        pause
        exit /b 1
    )
    echo Django найден в .venv — пропускаем установку.
)

echo.
echo Опционально: dev-зависимости (pytest, ruff) ...
%PY% -m pip install --default-timeout=120 -r requirements-dev.txt 2>nul
if errorlevel 1 echo Dev-пакеты не установлены — это не критично для запуска.

if not exist .env (
    if exist .env.example copy /Y .env.example .env > nul
    echo Создан файл .env из .env.example
)

if not exist logs mkdir logs
if not exist backups mkdir backups

echo.
echo Миграции базы данных ...
%PY% manage.py migrate
if errorlevel 1 (
    echo ОШИБКА при migrate.
    pause
    exit /b 1
)

echo.
echo Загрузка демо-данных ...
%PY% manage.py load_demo_data

echo.
echo ========================================
echo Установка завершена успешно.
echo Запуск: scripts\run.bat
echo Сайт:   http://127.0.0.1:8000/
echo ========================================
pause
