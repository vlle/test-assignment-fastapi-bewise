## Задание 2

### Сборка
 - Запустите ``./server_start.sh ``
 - Если необходимо запустить сервер в свернутом режиме: ``docker-compose up --build -d ``

### Примеры запроса к POST API сервиса
1) OpenAPI 3.1 yaml документация доступна в одноименном файле
2) Пример запроса curl POST USER:
```
curl -X 'POST' \
      'http://localhost:8000/user' \
      -H 'accept: application/json' \
      -H 'Content-Type: application/json' \
      -d '{
  "nick": "ivan"
}'
```
3) Пример запроса curl POST AUDIO:
```
curl -i -X POST -F "file=@audio-samples/sample1.wav" -F "id=2" -F "uuid=bb21de8e-ce22-485f-8312-49d56f28f949" localhost:8000/audio
```

3) Пример запроса curl GET AUDIO:
```
curl -i -X GET 'localhost:8000/record?id=2&user=2' --output file.mp3
```

### Тесты
- Есть опция запустить тесты. Для этого необходимо развернуть Docker с PostgreSQL на отдельном контейнере вне докер-композа.
- Скрипт для запуска тестов: ``./test_start.sh``
