# Сервис доставки посылок

Сервис для регистрации и расчета стоимости международных посылок.

## Технологии

- FastAPI + Pydantic
- RabbitMQ
- Redis
- MySQL
- Docker + docker-compose

## API

- `POST /boxes` - регистрация посылки
- `GET /boxes/types` - список типов посылок
- `GET /boxes` - список посылок пользователя
- `GET /boxes/{id}` - информация о посылке

## Запуск

1. Клонировать репозиторий
2. Создать `.env` файл
3. Запустить через docker-compose:

```bash
docker-compose up --build
```

Сервис будет доступен на http://localhost:8000

## Структура проекта

```
src/
├── delivery_service/
│   ├── domain/     # Бизнес-логика
│   ├── application/    # Сценарии использования
│   ├── infrastructure/  # Внешние сервисы
│   ├── presentation/   # API
│   └── entrypoints/    # Точки входа
├── main.py
└── worker.py
```
