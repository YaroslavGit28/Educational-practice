# SUPPORT_REPORT — Этап 6

## 1. Ссылка на репозиторий

См. `repo_link.txt`.

Ветка исправления инцидента: `support/fix-login-redirect` (рекомендуется для PR).

---

## 2. Выбранная проблема

**Инцидент:** некорректный редирект после авторизации при использовании параметра `next`.

При входе с URL `/users/login/?next=catalog:index` возникала ошибка redirect, так как в `next` передавалось имя маршрута вместо пути.

---

## 3. Воспроизведение

1. Открыть корзину без авторизации
2. Нажать «Войти для оформления»
3. Ввести корректные email/пароль
4. Наблюдать ошибку при `next=catalog:index`

---

## 4. Диагностика

| Параметр | Значение |
|----------|----------|
| Файл | `apps/users/views.py` |
| Причина | `redirect('catalog:index')` передавался как строка в `next` |
| Логи | NoReverseMatch / неверный redirect |
| Документ | `docs/INCIDENT_REPORT.md` |

---

## 5. Изменения

| Файл | Изменение |
|------|-----------|
| `apps/users/views.py` | Редирект только на URL из `next`, иначе на `catalog:index` |
| `.github/workflows/ci.yml` | CI: check + migrate + test |
| `CHANGELOG.md` | Версия 0.1.1 |
| `RELEASE_NOTES.md` | Описание релиза |
| `docs/github_issue_template.md` | Шаблон issue |
| `scripts/release-check.bat` | Проверка перед релизом |

---

## 6. Проверка

```bat
scripts\check.bat
scripts\test.bat
```

Результат: 8/8 тестов OK, ручная проверка `?next=/cart/` — passed.

---

## 7. Релиз

| Параметр | Значение |
|----------|----------|
| Версия | **0.1.1** |
| Архив | `release/project_release.zip` |
| Тег | `v0.1.1` (после push на GitHub) |

---

## 8. GitHub workflow

1. Создать Issue по `docs/github_issue_template.md`
2. Ветка `support/fix-login-redirect`
3. Push + Pull Request с описанием и ссылкой на issue
4. CI запускается автоматически (`.github/workflows/ci.yml`)
5. Merge в `main`, тег `v0.1.1`

---

## 9. Скриншоты

| Файл | Что должно быть видно |
|------|----------------------|
| 01_github_issue.png | Созданный Issue |
| 02_branch_created.png | Ветка support/fix-login-redirect |
| 03_code_fix.png | Изменение в views.py |
| 04_local_test.png | Успешный `scripts\test.bat` |
| 05_pull_request.png | Открытый PR |
| 06_ci_success.png | GitHub Actions CI passed |
| 07_merge_or_release.png | Merge / Release |
| 08_changelog.png | CHANGELOG.md v0.1.1 |
| 09_release_zip.png | release/project_release.zip |
| 10_final_app.png | Вход с `?next=/cart/` работает |

---

## 10. Вывод

Инцидент с редиректом после входа устранён. Настроен CI/CD pipeline, подготовлен релиз v0.1.1. Проект готов к сдаче всех 6 этапов УП.03.
