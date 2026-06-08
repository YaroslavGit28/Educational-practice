# CHANGELOG.md

## [0.1.1] - 2026-06-08

### Fixed
- Исправлен редирект после входа при параметре `next` (issue: некорректный redirect на именованный URL)
- Исправлен `ModuleNotFoundError` для приложений в папке `apps/`
- Добавлена проверка остатков при оформлении заказа
- Возврат товара на склад при отмене заказа

### Added
- Docker, docker-compose, production-compose
- BAT-скрипты и Makefile для setup/run/check/format
- Health endpoint `/api/health/`
- Автотесты pytest (smoke + API + доступ к чужим данным)
- Модули admin_panel и reports с Excel-экспортом
- CI workflow GitHub Actions
- Документация: INSTALL, DEPLOYMENT, DEMO_GUIDE, SECURITY

### Verified
- `scripts\check.bat` — passed
- `pytest` — passed
- GitHub Actions CI — configured

## [0.1.0] - 2026-06-01

### Added
- Базовый проект интернет-магазина (УП.02)
- Модули: users, catalog, cart, orders, processing
