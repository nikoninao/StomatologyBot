# 🦷 Stomatology Bot

Telegram-бот для записи клиентов к стоматологу. Написан на Python с использованием aiogram 3 и SQLite.

![telegram-cloud-photo-size-2-5292198199386903405-y](https://github.com/user-attachments/assets/f8aed7d8-962c-4ce2-9e53-634db058cc8c)

## Стек

- Python 3.11+
- aiogram 3
- SQLite3
- pydantic-settings
- apscheduler

## Возможности

- Запись к врачу через inline-кнопки
- Выбор дня и времени приёма
- Сохранение записей в базу данных
- Просмотр и отмена своих записей
- Напоминание за час до приёма
- Защита от спама (throttling middleware)
- Админ-Панель (в будущем доработаю)

## Установка

```bash
git clone https://github.com/username/dental-bot.git
cd StomatologyBot
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Настройка

Создай файл `.env` на основе `.env.example`:

```env
BOT_TOKEN=your_token_here
ADMIN_IDS=123456789
DEBUG=False
RATE_LIMIT=10
```

Токен получи у [@BotFather](https://t.me/BotFather).

## Запуск

```bash
python main.py
```

## Структура проекта

```
├── main.py
├── config.py
├── database.py
├── handlers/
│   ├── __init__.py
│   ├── start.py
│   └── help.py
├── middlewares/
│   ├── __init__.py
│   └── throttling.py
├── models/
│   └── __init__.py
├── data/
└── README.md
```

## База данных

SQLite, две таблицы:

- `users` — зарегистрированные пользователи
- `bookings` — записи на приём (день, время, статус напоминания)

## requirements.txt

```
aiogram>=3.0.0
pydantic-settings>=2.0.0
apscheduler>=3.10.0
```

## Лицензия

Лицензий нету
