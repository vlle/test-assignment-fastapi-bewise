for i in $(seq 1 10000);
do
curl -i --parallel --parallel-immediate --parallel-max 10 -X 'POST' \
          'http://127.0.0.1:8000/user' \
          -H 'accept: application/json' \
          -H 'Content-Type: application/json' \
          -d '{
  "nick": "ivanivanivaniv"
}'
done

