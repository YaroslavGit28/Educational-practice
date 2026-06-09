# TEST_PLAN.md

## 1. Что проверяется

- **Проект:** Интернет-магазин канцтоваров
- **Версия:** 0.1.1
- **Адрес:** http://127.0.0.1:8000/

## 2. Основные сценарии

| ID | Сценарий | Ожидаемый результат | Инструмент | Статус |
|----|----------|---------------------|------------|--------|
| TC-01 | Открыть главную страницу | HTTP 200, товары отображаются | Browser/pytest | passed |
| TC-02 | Войти как customer@shop.ru | Успешный вход, редирект на главную | UI/pytest | passed |
| TC-03 | Добавить товар в корзину | Товар в корзине, счётчик обновлён | UI | passed |
| TC-04 | Оформить заказ | Заказ создан, остаток уменьшен | UI + БД | passed |
| TC-05 | Открыть чужой заказ | HTTP 404, доступ запрещён | pytest | passed |
| TC-06 | GET /api/health/ | JSON status=ok | curl/pytest | passed |
| TC-07 | GET /orders/99999/ без авторизации | Редирект на login | curl | passed |
| TC-08 | Ошибочный вход (неверный пароль) | Сообщение об ошибке | UI | passed |
| TC-09 | Проверить логи | Нет критических Traceback | logs-check.bat | passed |
| TC-10 | Перезапуск Docker demo | Сервис снова доступен | restart.bat | passed |
| TC-11 | Производительность health | Ответ < 1 сек | performance.bat | passed |
| TC-12 | Адаптивность (мобильный) | Страница отображается | DevTools | passed |

## 3. Инструменты

- pytest, Django test client
- curl
- Chrome DevTools (Console, Network, Performance)
- scripts\quality-check.bat
- Docker logs

## 4. Итог

- Критичные ошибки: 0 (после исправлений)
- Некритичные: 2 (отсутствие HTTPS, SQLite в production)
- **Вывод:** проект готов к дальнейшей эксплуатации в учебном/demo-режиме
