# SECURITY.md

## Базовые меры безопасности

1. **Секреты** — `.env` в `.gitignore`, в репозитории только `.env.example`
2. **DEBUG** — в production/demo отключён (`DEBUG=false`)
3. **Доступ к данным** — заказы доступны только владельцу (`user=request.user`)
4. **Роли** — панели менеджера/кладовщика/админа защищены декораторами
5. **Пароли** — хеширование через Django `set_password`
6. **CSRF** — включён middleware
7. **Backup** — `scripts\backup.bat` для SQLite и media

## Проверка безопасности

```bat
scripts\security-check.bat
scripts\deps-check.bat
scripts\backup.bat
```

## Рекомендации для production

- Использовать HTTPS
- Заменить `SECRET_KEY`
- Настроить PostgreSQL вместо SQLite
- Включить регулярный backup
- Настроить мониторинг логов
