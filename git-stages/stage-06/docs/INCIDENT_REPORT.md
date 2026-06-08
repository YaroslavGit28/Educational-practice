# INCIDENT_REPORT.md

## 1. Инцидент

Некорректный редирект после авторизации при использовании параметра `next`.

## 2. Где обнаружено

Локальный запуск, страница `/users/login/?next=/cart/`

## 3. Как воспроизвести

1. Открыть корзину без авторизации
2. Нажать «Войти для оформления»
3. Ввести корректные email/пароль
4. Наблюдать ошибку redirect (при `next=catalog:index`)

## 4. Диагностика

- Проверен `apps/users/views.py` — `redirect('catalog:index')` передавался как строка в `next`
- Логи Django: ошибка NoReverseMatch / неверный redirect

## 5. Причина

`request.GET.get('next', 'catalog:index')` использовал имя URL вместо пути.

## 6. Исправление

```python
next_url = request.GET.get('next')
if next_url:
    return redirect(next_url)
return redirect('catalog:index')
```

## 7. Проверка

- `pytest tests/smoke/` — passed
- Ручная проверка входа с `?next=/cart/` — passed
- `scripts\check.bat` — passed

## 8. Итог

Проблема исправлена в v0.1.1
