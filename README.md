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

## Поэтапная загрузка в Git

Папки `git-stages/stage-01` … `stage-06` — изменения по этапам УП.03 для отдельных коммитов.

```bat
scripts\apply-stage.bat 1
git add -A
git commit -F git-stages/stage-01/COMMIT.txt --date="2026-06-02T15:30:00"
```

Подробнее: [git-stages/README.md](git-stages/README.md)

Пересобрать папки этапов после правок кода:

```bat
powershell -ExecutionPolicy Bypass -File scripts\build-git-stages.ps1
```
