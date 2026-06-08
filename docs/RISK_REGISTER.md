# RISK_REGISTER.md

| Риск | Признак/доказательство | Вероятность | Влияние | Что сделать |
|------|------------------------|-------------|---------|-------------|
| Проект недоступен после перезапуска | restart.bat проверен | Низкая | Высокое | restart policy в docker-compose.prod.yml |
| Ошибки API приводят к 500 | pytest проверяет 404 для чужих заказов | Средняя | Высокое | get_object_or_404, тесты |
| Утечка .env в Git | .gitignore проверен | Низкая | Высокое | .env.example, security-check.bat |
| Доступ к чужим данным | test_order_detail_foreign_access_denied | Средняя | Высокое | Фильтр user=request.user |
| Потеря данных | backup.bat + restore.bat | Средняя | Высокое | Регулярный backup SQLite |
| Уязвимые зависимости | pip-audit в deps-check.bat | Средняя | Среднее | Обновление пакетов |
| Медленная загрузка | performance.bat < 1s | Низкая | Среднее | Кэширование, оптимизация запросов |
| DEBUG=true в production | .env.production.example DEBUG=false | Средняя | Высокое | Проверка env при deploy |
| Открытый лишний порт | ports-check.bat | Низкая | Среднее | Только 8000 в compose |
| Логи не помогают | LOGGING в settings.py | Средняя | Среднее | logs/app.log, logs-check.bat |
