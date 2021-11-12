# Репозиторий для сбора данных

## Требования дял запуска

1. Docker 19.04 или выше.
2. [docker-compose с поддержкой схемы 3.7 или выше](https://github.com/docker/compose)

## Как запустить

Скопировать `.env.example` в `.env`. Заполнить нужными значениями.

Скачать файл с сессией. Добавить в директорию `sessions`. Указать название сессии (имя файла без расширения). Расширение должно быть: `.session`

Выполнить:
```
docker compose up pull
docker compose up
```

Пример с доступом к СУБД только для целей демонстрации.

СУБД доступна по порту `DB_PORT` на localhost.

Интерфейс для RabbitMQ по [http://localhost:15672/](http://localhost:15672/). Пор зависит от `RABBITMQ_MONITORING_PORT`.

**Используется синтаксис команд [docker-compose V2](https://github.com/docker/compose)**