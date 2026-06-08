# RECOMMENDATIONS.md

## Дальнейшие улучшения

1. **HTTPS** — настроить SSL-сертификат (Let's Encrypt + Nginx)
2. **PostgreSQL** — заменить SQLite для production
3. **CI security** — добавить pip-audit в GitHub Actions
4. **Мониторинг** — Sentry или аналог для отслеживания ошибок
5. **Автобэкап** — cron/Task Scheduler для `backup.bat`
6. **Rate limiting** — защита от brute-force на login
7. **2FA** — для администраторов
8. **PaaS deploy** — Render/Railway для публичного demo
