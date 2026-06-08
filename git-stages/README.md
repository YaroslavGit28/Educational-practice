# Поэтапная загрузка в Git (УП.03)

Папки `stage-01` … `stage-06` содержат **изменения каждого этапа отдельно**, чтобы коммиты выглядели как работа в разные дни.

## Подготовка (один раз)

```bat
cd internet_magazin
git init
git branch -M main
```

Создайте **первый коммит** — состояние после УП.02 (базовый код без доработок УП.03):

```bat
git add apps magazin manage.py requirements.txt static templates
git commit -m "УП.02: базовая реализация интернет-магазина" --date="2026-06-01T10:00:00"
```

> Если у вас уже полный проект — можно начать с пустого репозитория и применять этапы по порядку.

## Загрузка по этапам

Для каждого этапа **1 → 6**:

```bat
powershell -ExecutionPolicy Bypass -File scripts\apply-stage.ps1 -Stage 1
git add -A
git commit -F git-stages/stage-01/COMMIT.txt --date="2026-06-02T15:30:00"
```

Замените номер этапа и дату из `COMMIT.txt`.

### Таблица этапов

| Этап | Папка | Дата commit | Сообщение (кратко) |
|------|-------|-------------|-------------------|
| 1 | stage-01 | 2026-06-02 | Входной аудит, запуск, миграции, шаблоны |
| 2 | stage-02 | 2026-06-05 | BAT, Makefile, Docker |
| 3 | stage-03 | 2026-06-09 | Развертывание, DEPLOYMENT, release |
| 4 | stage-04 | 2026-06-12 | Тесты и качество |
| 5 | stage-05 | 2026-06-16 | Безопасность, backup |
| 6 | stage-06 | 2026-06-20 | CI/CD, релиз v0.1.1 |

## Пересобрать папки этапов

Если меняли код в проекте:

```bat
powershell -ExecutionPolicy Bypass -File scripts\build-git-stages.ps1
```

## Push на GitHub

```bat
git remote add origin https://github.com/USER/internet_magazin.git
git push -u origin main
```

## Ветка для этапа 6 (инцидент)

После этапа 5 создайте ветку для fix:

```bat
git checkout -b support/fix-login-redirect
powershell -ExecutionPolicy Bypass -File scripts\apply-stage.ps1 -Stage 6
git add -A
git commit -F git-stages/stage-06/COMMIT.txt --date="2026-06-22T11:00:00"
git push -u origin support/fix-login-redirect
```

Создайте Pull Request → merge в main.
