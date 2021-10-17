# Репозиторий для сбора данных

## Требования дял запуска

1. Docker 19.04 или выше.
2. [docker-compose с поддержкой схемы 3.7 или выше](https://github.com/docker/compose)

## Как запустить

В файле `.env` прописаны все переменные окружения.

Достаточно выполнить:
```
docker-compose up
```

СУБД доступна по порту `DB_PORT` на localhost.

Интерфейс для RabbitMQ по [http://localhost:15672/](http://localhost:15672/). Пор зависит от `RABBITMQ_MONITORING_PORT`/