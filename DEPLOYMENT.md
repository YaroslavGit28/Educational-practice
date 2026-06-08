# DEPLOYMENT.md

## 1. Где развернут проект

**Вариант:** C — локальный demo-стенд через Docker (production-compose)

**Адрес:** http://127.0.0.1:8000/

## 2. Требования

- Docker Desktop 24+
- Python 3.12 (для локального запуска без Docker)
- Порт 8000 свободен
- SQLite (встроенная БД)

## 3. Переменные окружения

Скопируйте пример:

```bat
copy .env.production.example .env.production
```

Основные переменные: `SECRET_KEY`, `DEBUG=false`, `ALLOWED_HOSTS`, `APP_PORT`.

## 4. Команды развертывания

```bat
scripts\deploy.bat
scripts\check_deploy.bat
```

Или вручную:

```bat
docker compose -f docker-compose.prod.yml up --build -d
```

## 5. Проверка

- Health: http://127.0.0.1:8000/api/health/
- Главная: http://127.0.0.1:8000/
- Логи: `scripts\logs.bat` или `docker compose -f docker-compose.prod.yml logs --tail=80`

## 6. Перезапуск

```bat
scripts\restart.bat
```

## 7. Остановка

```bat
docker compose -f docker-compose.prod.yml down
```

## 8. Release-архив

```bat
scripts\build_release.bat
```

Архив: `release/project_release.zip`
