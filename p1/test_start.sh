#!/usr/bin/env bash

cp env.example app/.env
docker pull postgres
docker run -d --name test  -p 5432:5432  -e POSTGRES_USER=postgres  -e POSTGRES_PASSWORD=postgres  -e POSTGRES_DB=postgres postgres -N 2000
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python -m pytest app/
deactivate
docker stop test
docker rm test
