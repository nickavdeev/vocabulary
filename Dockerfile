# Multi-stage build для минимизации размера финального образа
# Этап 1: Builder
FROM python:3.11 AS builder

# Установка UV для управления зависимостями
RUN pip install uv

# Установка рабочей директории
WORKDIR /app

# Копирование файла проекта
COPY pyproject.toml ./
COPY uv.lock ./

# Установка зависимостей с помощью UV
RUN uv sync --frozen

# Этап 2: Финальный образ
FROM python:3.11-slim

# Установка рабочей директории
WORKDIR /app

# Копирование установленных зависимостей из builder stage
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages

# Копирование исходного кода приложения
COPY . .

# Команда для запуска бота
CMD ["python", "src/bot/main.py"]