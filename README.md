# Video Analytics Telegram Bot

Telegram-бот для аналитики по видео. Бот принимает вопросы на русском языке, преобразует их в SQL и возвращает числовой ответ.

---

## Требования

- Docker
- Docker Compose
- Telegram Bot Token

---

## Быстрый запуск (рекомендуется)

### 1. Клонировать репозиторий

```bash
git clone https://github.com/AyoTecca/video-analytics-telegram-bot.git
cd video-analytics-telegram-bot
```

### 2. Настроить переменные окружения

Создайте файл `.env` на основе примера:

```bash
cp .env.example .env
# или на Windows PowerShell:
# copy .env.example .env
```

Укажите в `.env` значение токена бота:

- `TELEGRAM_BOT_TOKEN` (или `TELEGRAM_TOKEN`, если вы используете это имя в проекте)

При необходимости измените остальные значения (Postgres, Ollama и т.д.).

### 3. Запустить сервисы

```bash
docker-compose up -d --build
```

Будут запущены:

- PostgreSQL
- Ollama (LLM)
- Telegram-бот

### 4. Применить миграции БД

```bash
docker exec -it analytics_db psql -U ${POSTGRES_USER} -d ${POSTGRES_DB} -f /app/migrations.sql
```


### 5. Загрузить данные

```bash
docker exec -it analytics_bot python load_data.py data/videos.json
```

### 6. Проверить, что бот работает

Откройте Telegram и напишите боту, например:

```
Сколько всего видео есть в системе?
```

Ответ должен быть одним числом.

---

## Архитектура

- PostgreSQL — хранение статистики
- Telegram bot (`aiogram`) — приём и отправка сообщений
- LLM (Ollama) — преобразование текста → SQL

Принцип: один запрос → один числовой ответ. Контекст диалога не хранится.

## LLM и правила генерации SQL

Описание схемы данных и правил генерации SQL находится в файле `llm_prompt.txt`.

LLM получает:

- описание таблиц
- правила выбора метрик
- ограничения (только SQL, без вспомогательного текста)

---

## Структура проекта

- `bot.py` — Telegram-бот
- `load_data.py` — загрузка JSON в БД
- `migrations.sql` — схема PostgreSQL
- `llm/`, `llm_prompt.txt` — логика и подсказки для LLM
- `docker-compose.yml`, `Dockerfile` — Docker-конфигурация

---

