# BACKUP_RESTORE_REPORT.md

## Тип хранилища

SQLite (`db.sqlite3`) + папка `media/`

## Backup

**Команда:** `scripts\backup.bat`

**Результат:** копия БД в `backups/backup_YYYYMMDD.sqlite3`, медиа в `backups/media_YYYYMMDD/`

## Restore

**Команда:** `scripts\restore.bat`

**Процедура:**
1. Выбрать файл backup
2. Скопировать в `db.sqlite3`
3. Запустить `scripts\run.bat`
4. Проверить данные (товары, пользователи, заказы)

## Проверка

После restore приложение запускается, демо-пользователи и товары доступны.
