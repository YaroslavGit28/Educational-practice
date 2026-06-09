.PHONY: setup run check format test api-test quality-check performance logs-check docker-build docker-up docker-down logs clean deploy restart check-deploy build release-check

VENV = .venv
PYTHON = $(VENV)/Scripts/python
PIP = $(VENV)/Scripts/pip

setup:
	@echo "=== Установка зависимостей ==="
	$(PYTHON) -m pip install --upgrade pip
	$(PIP) install -r requirements-dev.txt
	$(PYTHON) manage.py migrate
	$(PYTHON) manage.py load_demo_data

run:
	@echo "=== Запуск сервера ==="
	$(PYTHON) manage.py runserver 0.0.0.0:8000

check:
	@echo "=== Проверка Django ==="
	$(PYTHON) manage.py check
	@echo "=== Тесты ==="
	$(PYTHON) manage.py test tests --verbosity=1
	@echo "=== Compile ==="
	$(PYTHON) -m compileall apps magazin tests -q

format:
	@echo "=== Форматирование кода (требует: pip install black ruff) ==="
	-$(VENV)/Scripts/black apps magazin tests
	-$(VENV)/Scripts/ruff check apps magazin tests --fix

test:
	$(VENV)/Scripts/pytest -v

api-test:
	@echo "=== API health check ==="
	curl -s http://127.0.0.1:8000/api/health/
	@echo.
	@echo "=== API 404 test ==="
	curl -s -o /dev/null -w "HTTP %{http_code}\n" http://127.0.0.1:8000/orders/99999/

quality-check: check api-test logs-check
	@echo "Quality check completed"

performance:
	@echo "=== Performance: health endpoint timing ==="
	curl -s -o /dev/null -w "Time: %{time_total}s\n" http://127.0.0.1:8000/api/health/

logs-check:
	@echo "=== Последние 50 строк логов ==="
	@powershell -Command "if (Test-Path logs/app.log) { Get-Content logs/app.log -Tail 50 } else { echo 'Лог-файл пока пуст' }"

docker-build:
	docker compose build

docker-up:
	docker compose up --build

docker-down:
	docker compose down

logs:
	docker compose logs -f

deploy:
	docker compose -f docker-compose.prod.yml up --build -d

restart:
	docker compose -f docker-compose.prod.yml down
	docker compose -f docker-compose.prod.yml up --build -d

check-deploy:
	docker compose -f docker-compose.prod.yml ps
	docker compose -f docker-compose.prod.yml logs --tail=80

build:
	@echo "=== Сборка release-архива ==="
	powershell -ExecutionPolicy Bypass -File scripts/create-release.ps1

release-check: check build
	@echo "Project is ready for release"

clean:
	@echo "Очистка кэша Python"
	@powershell -Command "Get-ChildItem -Recurse -Directory -Filter __pycache__ | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue"
