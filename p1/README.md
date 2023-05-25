## Задание 1

### Сборка
 - Запустите ``./server_start.sh ``
 - Если необходимо запустить сервер в свернутом режиме: ``docker-compose up --build -d ``

### Примеры запроса к POST API сервиса
1) OpenAPI 3.1 yaml документация доступна в одноименном файле
2) Пример запроса curl:
```
curl -X 'POST' \
      'http://localhost:8000/questions' \
      -H 'accept: application/json' \
      -H 'Content-Type: application/json' \
      -d '{
  "question_num": 2
}'
```

### Тесты
- Есть опция запустить тесты. Для этого необходимо развернуть Docker с PostgreSQL на отдельном контейнере вне докер-композа.
- Скрипт для запуска тестов: ``./test_start.sh``
