# Video Analytics Telegram Bot

Telegram-бот для аналитики по видео на основе запросов на естественном языке.

## Архитектура

- PostgreSQL — хранение данных
- Telegram Bot (aiogram)
- LLM (Ollama, модель llama3.1) - преобразование текста в SQL
- Один запрос → один SQL → одно число

## Структура данных

- videos - итоговая статистика по видео
- video_snapshots - почасовые изменения (delta)

## Запуск проекта (Docker)

1. Создать `.env` на основе `.env.example`
2. Запустить сервисы:

```docker-compose up -d```

3. Загрузить данные:

```docker exec -it analytics_bot python load_data.py data/videos.json```

4. Бот доступен в Telegram

## Принцип работы

1. Пользователь задаёт вопрос на русском языке
2. LLM генерирует SQL-запрос на основе описания схемы
3. SQL выполняется в PostgreSQL
4. Бот возвращает одно числовое значение

## LLM
Используется локально развернутая модель llama3.1 через Ollama.
Схема данных и правила интерпретации описаны в llm_prompt.txt.