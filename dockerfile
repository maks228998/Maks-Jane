# Используем официальный образ Python в качестве базового
FROM python:3.9-slim

# Устанавливаем необходимые зависимости для psycopg2
RUN apt-get update && apt-get install -y \
    libpq-dev \
    build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем рабочую директорию в контейнере
WORKDIR /app

# Копируем файл с зависимостями в контейнер
COPY requirements.txt .

# Устанавливаем необходимые пакеты из requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Копируем содержимое текущей директории в контейнер в /app
COPY . .

# Устанавливаем клиент PostgreSQL
RUN apt-get update && apt-get install -y postgresql-client

# Открываем порт, на котором работает приложение
EXPOSE 5000

# Команда для запуска приложения
CMD ["python", "main.py"]