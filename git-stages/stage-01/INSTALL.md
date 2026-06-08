# Инструкция установки

## Требования

- Windows 10/11 или Linux
- Python 3.12+
- Git (опционально)
- Docker Desktop (для контейнерного запуска)

## Установка на Windows

1. Скачайте проект или клонируйте репозиторий
2. Откройте терминал в папке проекта
3. Выполните:

```bat
scripts\setup.bat
```

4. Создайте `.env` из примера:

```bat
copy .env.example .env
```

5. Запустите:

```bat
scripts\run.bat
```

6. Откройте http://127.0.0.1:8000/

## Установка через Docker

```bat
copy .env.example .env
scripts\docker-up.bat
```

## Проверка установки

```bat
scripts\check.bat
curl http://127.0.0.1:8000/api/health/
```

Ожидаемый ответ: `{"status": "ok", ...}`

## Устранение проблем

| Проблема | Решение |
|----------|---------|
| ModuleNotFoundError | Запустите `scripts\setup.bat` |
| База пуста | `python manage.py load_demo_data` |
| Порт занят | Измените `APP_PORT` в `.env` |
