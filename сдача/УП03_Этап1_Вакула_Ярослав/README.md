# Интернет-магазин канцтоваров

Django-приложение для учебной практики УП.03 (сопровождение и обслуживание ПО).

## Стек

- Python 3.12
- Django 4.2.7
- SQLite
- Bootstrap 5
- Docker / Docker Compose
- pytest, ruff, black

## Быстрый запуск (Windows)

```bat
scripts\setup.bat
scripts\run.bat
```

Откройте: http://127.0.0.1:8000/

## Быстрый запуск (Makefile)

```bash
make setup
make run
```

## Docker

```bat
copy .env.example .env
scripts\docker-up.bat
```

Production/demo:

```bat
scripts\deploy.bat
```

## Проверки

```bat
scripts\check.bat
scripts\test.bat
scripts\quality-check.bat
```

## Демо-аккаунты

| Email | Пароль | Роль |
|-------|--------|------|
| admin@shop.ru | demo1234 | Администратор |
| customer@shop.ru | demo1234 | Покупатель |

## Документация

- [INSTALL.md](INSTALL.md) — установка
- [DEPLOYMENT.md](DEPLOYMENT.md) — развертывание
- [DEMO_GUIDE.md](DEMO_GUIDE.md) — демонстрация
- [SECURITY.md](SECURITY.md) — безопасность
- [CHANGELOG.md](CHANGELOG.md) — история изменений

## Репозиторий

См. `repo_link.txt`

