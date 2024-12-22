# Используем официальный образ Python
FROM python:3.9-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы приложения в контейнер
COPY app/ .

# Устанавливаем зависимости (если есть requirements.txt)
COPY requirements.txt .
RUN pip3 install --upgrade pip -r requirements.txt

EXPOSE 5000