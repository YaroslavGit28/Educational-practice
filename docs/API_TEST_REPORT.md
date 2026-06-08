# API_TEST_REPORT.md

## Успешные запросы

| Метод | URL | Код | Результат |
|-------|-----|-----|-----------|
| GET | /api/health/ | 200 | `{"status":"ok","service":"internet_magazin","version":"0.1.1"}` |
| GET | / | 200 | HTML главной страницы |
| GET | /catalog/ | 200 | HTML каталога |
| GET | /users/login/ | 200 | HTML формы входа |

## Ошибочные сценарии

| Метод | URL | Код | Результат |
|-------|-----|-----|-----------|
| GET | /orders/1/ (без auth) | 302 | Редирект на /users/login/ |
| GET | /orders/99999/ (с auth) | 404 | Заказ не найден |
| GET | /orders/{чужой_id}/ (с auth) | 404 | Доступ запрещён |

## Команды проверки

```bat
scripts\api-test.bat
curl http://127.0.0.1:8000/api/health/
```
