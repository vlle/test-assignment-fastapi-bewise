for i in $(seq 1 100);
do
    curl -X 'POST' \
              'http://localhost:8000/questions' \
              -H 'accept: application/json' \
              -H 'Content-Type: application/json' \
              -d '{
      "question_num": 100
    }'
done


