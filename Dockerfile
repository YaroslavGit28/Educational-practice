FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc libjpeg-dev zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt requirements-dev.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p logs media staticfiles backups

EXPOSE 8000

ENTRYPOINT ["python", "/app/scripts/docker_entrypoint.py"]
CMD ["manage.py", "runserver", "0.0.0.0:8000"]
