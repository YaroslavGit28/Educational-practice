# SECURITY_CHECKLIST.md

| Проверка | Статус | Доказательство | Что исправлено |
|----------|--------|----------------|----------------|
| .env не загружен в Git | выполнено | .gitignore | добавлен .env в .gitignore |
| .env.example без реальных секретов | выполнено | .env.example | change_me значения |
| Ручной поиск секретов выполнен | выполнено | security-check.bat | SECRET_KEY вынесен в env |
| Зависимости проверены | выполнено | deps-check.bat | pip-audit настроен |
| Проверены роли | выполнено | pytest + UI | role_required декораторы |
| Проверен доступ к чужим данным | выполнено | test_api.py | 404 для чужого заказа |
| CORS/hosts/debug проверены | выполнено | .env.production.example | DEBUG=false |
| Backup создан | выполнено | backup.bat | backups/*.sqlite3 |
| Restore проверен | выполнено | restore.bat | восстановление БД |
| Открытые порты проверены | выполнено | ports-check.bat | порт 8000 |
| Логи без критических ошибок | выполнено | logs/app.log | LOGGING настроен |
